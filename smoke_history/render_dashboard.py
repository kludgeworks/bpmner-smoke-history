# Copyright 2026 The Project Contributors
# SPDX-License-Identifier: MIT
"""Render the "Smoke Health" dashboard from accumulated per-run result files.

Reads a directory tree of newline-delimited JSON (`*.jsonl`), one `SmokeRunResult` per line, runs the
analytics with DuckDB (queries in `queries/`), and prints the dashboard markdown.

    uv run python -m smoke_history.render_dashboard <data-dir>
"""

from __future__ import annotations

import argparse
from pathlib import Path

import duckdb

from smoke_history.charts import line_chart_svg, stacked_bar_svg

_QUERIES = Path(__file__).resolve().parent.parent / "queries"
_FLAKY_LIMIT = 25
_PLACEHOLDER = "# 🔬 Smoke Health\n\n_No completed runs recorded yet._\n"


def _load(con: duckdb.DuckDBPyConnection, data_dir: Path) -> bool:
    """Load every `*.jsonl` under data_dir into a `results` view. Returns False if there are no files."""
    files = sorted(Path(data_dir).rglob("*.jsonl"))
    if not files:
        return False
    # read_json_auto can't take a prepared parameter for its file list, so inline the (escaped) paths.
    # These are local filesystem paths, not user input.
    file_list = ", ".join("'" + str(f).replace("'", "''") + "'" for f in files)
    con.execute(
        f"""
        CREATE OR REPLACE VIEW results AS
        SELECT * FROM read_json_auto([{file_list}], format='newline_delimited',
                                     union_by_name=true, ignore_errors=true)
        WHERE runComplete  -- partial/cancelled runs are kept on disk but excluded from the dashboard
        """
    )
    return True


def _rows(con: duckdb.DuckDBPyConnection, query: str) -> list[dict]:
    cur = con.execute((_QUERIES / f"{query}.sql").read_text(encoding="utf-8"))
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r, strict=False)) for r in cur.fetchall()]


def _try_rows(con: duckdb.DuckDBPyConnection, query: str) -> list[dict]:
    """Like _rows but returns [] if the query references columns absent from the loaded data."""
    try:
        return _rows(con, query)
    except duckdb.BinderException:
        return []


def _cell(value: object) -> str:
    """Markdown-table-safe: escape pipes and flatten newlines so a stray value can't corrupt the table."""
    return str(value).replace("|", "\\|").replace("\n", " ").replace("\r", " ")


def _run_count(con: duckdb.DuckDBPyConnection) -> int:
    return con.execute("SELECT count(DISTINCT runId) FROM results").fetchone()[0]


def _render_scorecard(con: duckdb.DuckDBPyConnection) -> list[str]:
    out = [
        "## Provider scorecard",
        "",
        "| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for r in _rows(con, "scorecard"):
        cost = "n/a*" if r["cost_caveat"] else f"${r['cost_per_run'] or 0:.4f}"
        out.append(
            f"| {_cell(r['provider'])} | `{_cell(r['model'] or '?')}` | {r['runs']} | {r['pass_pct']} | "
            f"{r['fails']} | {cost} | {r['tokens'] or 0} |"
        )
    out += ["", "_\\* cost unknown — provider has no configured pricing._"]
    return out


def _render_flaky(con: duckdb.DuckDBPyConnection) -> list[str]:
    out = [
        "## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)",
        "",
        "| Test | Fail % | Providers failed | Samples |",
        "|---|---:|---|---:|",
    ]
    flaky = _rows(con, "flaky")
    if not flaky:
        out.append("| _none_ | | | |")
    for r in flaky[:_FLAKY_LIMIT]:
        out.append(
            f"| `{_cell(r['testMethod'])}` | {r['fail_pct']} | "
            f"{r['providers_failed']} ({_cell(r['failed_on'])}) | {r['samples']} |"
        )
    if len(flaky) > _FLAKY_LIMIT:
        out += ["", f"_…and {len(flaky) - _FLAKY_LIMIT} more flaky tests._"]
    return out


def _render_stage_split(con: duckdb.DuckDBPyConnection) -> list[str]:
    rows = _try_rows(con, "stage_split")
    # Filter out rows where all metrics are None (e.g. deepseek which never reaches the LLM stage).
    rows = [r for r in rows if any(r[k] is not None for k in ("total_prompt_tokens", "total_llm_calls"))]
    if not rows:
        return []
    out = [
        "## Stage breakdown",
        "",
        "_Per-pipeline-stage model and token usage (readiness vs extraction)._",
        "",
        "| Provider | Stage | Model | Prompt tokens | Completion tokens | LLM calls | Samples |",
        "|---|---|---|---:|---:|---:|---:|",
    ]
    for r in rows:
        stage = _cell(r["stage"]).replace("goal-", "")
        out.append(
            f"| {_cell(r['provider'])} | {stage} | `{_cell(r['model'] or '?')}` | "
            f"{r['total_prompt_tokens'] or 0} | {r['total_completion_tokens'] or 0} | "
            f"{r['total_llm_calls'] or 0} | {r['samples']} |"
        )
    return out


def _render_llm_efficiency(con: duckdb.DuckDBPyConnection) -> list[str]:
    rows = _try_rows(con, "llm_call_distribution")
    if not rows:
        return []
    out = [
        "## LLM efficiency",
        "",
        "_Distribution of LLM API calls per test — more calls may indicate retries or tool loops._",
        "",
        "| Provider | Min | Avg | Median | P95 | Max | σ | Samples |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in rows:
        median = int(r["median_calls"]) if r["median_calls"] is not None else "?"
        p95 = int(r["p95_calls"]) if r["p95_calls"] is not None else "?"
        out.append(
            f"| {_cell(r['provider'])} | {r['min_calls']} | {r['avg_calls']} | "
            f"{median} | {p95} | {r['max_calls']} | {r['stddev_calls'] or 0} | {r['samples']} |"
        )
    return out


def _render_latency(con: duckdb.DuckDBPyConnection, assets_dir: Path | None) -> list[str]:
    """Generate an avg-latency-over-runs line chart per provider (seconds).

    A per-(run, provider) table grows unbounded as runs accumulate; a time-series chart stays a fixed
    size and surfaces the trend, which is what matters for latency.
    """
    if assets_dir is None:
        return []
    rows = _try_rows(con, "latency_timeseries")
    # Only runs with real latency data (pre-instrumentation runs report 0).
    rows = [r for r in rows if r["avg_llm_time_ms"]]
    if len({r["runId"] for r in rows}) < 2:
        return []

    # Build series: provider -> [(run_label, avg_seconds), ...]; rows are already ordered by run_ts.
    by_provider: dict[str, list[tuple[str, float]]] = {}
    for r in rows:
        label = str(r["runId"])[-8:]
        by_provider.setdefault(r["provider"], []).append((label, r["avg_llm_time_ms"] / 1000))

    svg = line_chart_svg(by_provider, "Avg LLM latency by provider over runs (s)")
    assets_dir.mkdir(parents=True, exist_ok=True)
    (assets_dir / "latency-trend.svg").write_text(svg + "\n", encoding="utf-8")

    return [
        "## Latency",
        "",
        "_Average LLM response time per provider over runs (seconds, wall-clock)._",
        "",
        "![Avg LLM latency by provider over runs](assets/smoke-health/latency-trend.svg)",
    ]


def _render_failure_categories(con: duckdb.DuckDBPyConnection) -> list[str]:
    rows = _try_rows(con, "failure_categories")
    rows = [r for r in rows if r["failureCategory"] is not None]
    if not rows:
        return []
    out = [
        "## Failure categories",
        "",
        "_`deterministic` = harness/config failure (e.g. context load); `classification` = the model "
        "produced a wrong answer. Separates 'the harness broke' from 'the model struggled'._",
        "",
        "| Provider | Category | Failures | % of provider fails | Sample signature |",
        "|---|---|---:|---:|---|",
    ]
    for r in rows:
        sig = _cell(r["sample_signature"] or "")
        if len(sig) > 80:
            sig = sig[:77] + "…"
        out.append(
            f"| {_cell(r['provider'])} | {_cell(r['failureCategory'])} | {r['failures']} | "
            f"{r['pct_of_provider_failures'] or 0} | {sig} |"
        )
    return out


def _render_cost_chart(con: duckdb.DuckDBPyConnection, assets_dir: Path | None) -> list[str]:
    """Generate a cost-trend SVG if 2+ runs exist and an assets dir is provided."""
    if assets_dir is None:
        return []
    rows = _try_rows(con, "cost_timeseries")
    runs = sorted({r["runId"] for r in rows})
    if len(runs) < 2:
        return []

    # Build series: provider -> [(run_label, cost_per_test), ...]
    # Providers run rotating shards, so the test count per run varies (4–8). Charting raw per-run
    # totals would conflate per-test cost with shard size, so normalise to cost-per-test.
    by_provider: dict[str, list[tuple[str, float]]] = {}
    for r in rows:
        if not r["cost_known"]:
            continue
        tests = r["tests_in_run"] or 0
        if not tests:
            continue
        label = str(r["runId"])[-8:]
        by_provider.setdefault(r["provider"], []).append((label, r["total_cost"] / tests))

    if not by_provider:
        return []

    svg = line_chart_svg(by_provider, "Cost per test by provider over runs ($)")
    assets_dir.mkdir(parents=True, exist_ok=True)
    # Trailing newline so the committed asset satisfies the end-of-file-fixer on every regeneration.
    (assets_dir / "cost-trend.svg").write_text(svg + "\n", encoding="utf-8")

    return [
        "## Cost trends",
        "",
        "_Cost **per test** — shard sizes vary run-to-run, so raw per-run totals aren't comparable._",
        "",
        "![Cost per test by provider over runs](assets/smoke-health/cost-trend.svg)",
    ]


def _render_token_chart(con: duckdb.DuckDBPyConnection, assets_dir: Path | None) -> list[str]:
    """Generate a readiness-vs-extraction token chart per provider.

    The pipeline has two stages: a cheap readiness gatekeeper (ProcessInputAssessment) and an
    expensive extraction step (ValidatedProcessContract). How tokens split between them is a leading
    indicator of prompt-engineering drift that raw prompt/completion totals mask.
    """
    if assets_dir is None:
        return []
    rows = _try_rows(con, "stage_split")
    if not rows:
        return []

    providers = sorted({r["provider"] for r in rows})

    def _stage_tokens(provider: str, stage: str) -> int:
        r = next((x for x in rows if x["provider"] == provider and x["stage"] == stage), None)
        return (r["total_prompt_tokens"] or 0) + (r["total_completion_tokens"] or 0) if r else 0

    readiness = [_stage_tokens(p, "ProcessInputAssessment") for p in providers]
    extraction = [_stage_tokens(p, "ValidatedProcessContract") for p in providers]
    if not any(readiness) and not any(extraction):
        return []

    svg = stacked_bar_svg(
        providers,
        {"Readiness (assessment)": readiness, "Extraction (contract)": extraction},
        "Token split: readiness vs extraction",
    )
    assets_dir.mkdir(parents=True, exist_ok=True)
    (assets_dir / "token-split.svg").write_text(svg + "\n", encoding="utf-8")

    return [
        "## Token split (readiness vs extraction)",
        "",
        "_Tokens spent in the cheap readiness gatekeeper vs the expensive extraction stage, per provider._",
        "",
        "![Token split by provider](assets/smoke-health/token-split.svg)",
    ]


def render(data_dir: Path | str, assets_dir: Path | str | None = None) -> str:
    con = duckdb.connect(":memory:")
    # Placeholder when there are no *completed* rows — not merely no files: a directory of only
    # runComplete=false rows passes the file check but the view is empty.
    if not _load(con, Path(data_dir)) or con.execute("SELECT count(*) FROM results").fetchone()[0] == 0:
        return _PLACEHOLDER

    assets = Path(assets_dir) if assets_dir is not None else None

    out = [
        "# 🔬 Smoke Health",
        "",
        "_Report-only · all recorded runs · provider = model family under test._",
        "",
    ]
    out += _render_scorecard(con)
    out += [""]
    out += _render_flaky(con)

    # New sections — each returns [] if the data doesn't warrant a section.
    for section_fn in (
        lambda: _render_failure_categories(con),
        lambda: _render_stage_split(con),
        lambda: _render_llm_efficiency(con),
        lambda: _render_latency(con, assets),
        lambda: _render_cost_chart(con, assets),
        lambda: _render_token_chart(con, assets),
    ):
        section = section_fn()
        if section:
            out += [""]
            out += section

    out.append("")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("data_dir", help="directory tree of *.jsonl result files")
    ap.add_argument(
        "--assets-dir",
        default=None,
        help="directory for generated SVG chart assets (default: no charts)",
    )
    # render() already terminates with a single newline; write it verbatim so the file ends with exactly one.
    # A bare print() would append a second, producing a trailing blank line that end-of-file-fixer rejects.
    args = ap.parse_args()
    print(render(args.data_dir, args.assets_dir), end="")


if __name__ == "__main__":
    main()
