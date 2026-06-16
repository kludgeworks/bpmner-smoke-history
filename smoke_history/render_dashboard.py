# Copyright 2026 The Project Contributors
# SPDX-License-Identifier: MIT
"""Render the "Smoke Health" dashboard from accumulated per-run result files.

Reads a directory tree of newline-delimited JSON (`*.jsonl`), one `SmokeRunResult` per line, runs the
analytics with DuckDB (queries in `queries/`), and prints the dashboard markdown. The dashboard is the
repo homepage: CI renders it to `README.md` and commits it alongside the theme-paired SVG charts.

    uv run python -m smoke_history.render_dashboard <data-dir> --assets-dir assets/smoke-health > README.md
"""

from __future__ import annotations

import argparse
import html
import sys
from collections.abc import Callable
from pathlib import Path

import duckdb

from smoke_history import charts
from smoke_history.charts import THEMES

_QUERIES = Path(__file__).resolve().parent.parent / "queries"
_FLAKY_TOP = 6  # rows in the headline flaky table; the rest collapse into a <details>.
_PLACEHOLDER = "# 🔬 Smoke Health\n\n_No completed runs recorded yet._\n"

# Eighth-block characters for the proportional table bars, 1/8 … 8/8 (index 0 is the empty placeholder).
_BLOCKS = " ▏▎▍▌▋▊▉█"


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
    """Like _rows but returns [] if the query references columns absent from the loaded data.

    A missing column is expected (the schema evolves run-to-run), but a typo'd column or table name
    raises the same BinderException — so log to stderr, otherwise a broken query just silently drops
    its whole section with no trace in the CI log.
    """
    try:
        return _rows(con, query)
    except duckdb.BinderException as e:
        sys.stderr.write(f"  query '{query}' skipped — column/table not found: {e}\n")
        return []


def _cell(value: object) -> str:
    """Markdown-table-safe: escape pipes and flatten newlines so a stray value can't corrupt the table."""
    return str(value).replace("|", "\\|").replace("\n", " ").replace("\r", " ")


def unicode_bar(fraction: float, cells: int) -> str:
    """A proportional bar of `cells` width built from eighth-blocks, padded with `░` to a fixed width."""
    fraction = max(0.0, min(1.0, fraction))
    eighths = round(fraction * cells * 8)
    full, rem = divmod(eighths, 8)
    bar = "█" * full + (_BLOCKS[rem] if rem else "")
    bar += "░" * (cells - len(bar))
    return bar


def _model_family(served_models: object) -> str:
    """Flatten the per-row (comma-joined) servedModel strings into a sorted, de-duplicated family list."""
    models = {m.strip() for s in (served_models or []) for m in str(s).split(",") if m.strip()}
    return ", ".join(sorted(models))


# ---------------------------------------------------------------------------
# Chart asset writing + <picture> helpers
# ---------------------------------------------------------------------------


def _write_pair(assets_dir: Path, name: str, make: Callable[[charts.Theme], str]) -> None:
    """Write the light + dark SVG variants of a chart.

    Every chart is emitted twice so the <picture> block can serve the right one per the reader's color
    scheme; the trailing newline keeps the end-of-file-fixer happy on every regeneration.
    """
    assets_dir.mkdir(parents=True, exist_ok=True)
    for theme_name, theme in THEMES.items():
        (assets_dir / f"{name}-{theme_name}.svg").write_text(make(theme) + "\n", encoding="utf-8")


def _picture(base: str, name: str, alt: str) -> list[str]:
    """A GitHub <picture> block pairing the dark/light SVG variants with a data-derived alt."""
    return [
        "<picture>",
        f'  <source media="(prefers-color-scheme: dark)" srcset="{base}/{name}-dark.svg">',
        f'  <img alt="{html.escape(alt)}" src="{base}/{name}-light.svg" width="760">',
        "</picture>",
    ]


def _pct_label(pct: float) -> str:
    """Format a pass rate for prose: 100.0 → "100", 98.5 → "98.5"."""
    return f"{float(pct):g}"


# ---------------------------------------------------------------------------
# Section builders — each returns the section's markdown lines (no surrounding blanks).
# ---------------------------------------------------------------------------


def _scorecard_section(scorecard: list[dict], assets: Path | None, base: str | None) -> list[str]:
    rows = sorted(scorecard, key=lambda r: (-(r["pass_pct"] or 0), r["provider"]))
    out = ["## Provider scorecard", ""]

    if assets is not None and base is not None:
        _write_pair(assets, "scorecard", lambda t: charts.scorecard_svg(rows, t))
        alt = "Pass rate by provider — " + ", ".join(
            f"{r['provider']} {_pct_label(r['pass_pct'] or 0)}%" for r in rows
        )
        out += _picture(base, "scorecard", alt)
        out += [""]

    out += [
        "<details>",
        "<summary><b>Full table</b> — pass-rate bars, fails, cost & tokens per run</summary>",
        "",
        "| Provider | Pass rate | Fails | $/run | Tokens | Model family |",
        "|---|:--|--:|--:|--:|---|",
    ]
    na_providers: list[str] = []
    for r in rows:
        pct = float(r["pass_pct"] or 0)
        bar = unicode_bar(pct / 100.0, 14)
        if r["cost_caveat"]:
            cost = "n/a"
            na_providers.append(r["provider"])
        else:
            cost = f"${r['cost_per_run'] or 0:.4f}"
        tokens = charts.tokens_label(r["tokens"] or 0)
        family = _model_family(r.get("served_models"))
        out.append(
            f"| `{_cell(r['provider'])}` | `{bar}` {pct:.1f}% | {int(r['fails'] or 0)} | {cost} | "
            f"{tokens} | `{_cell(family)}` |"
        )
    if na_providers:
        joined = ", ".join(f"`{p}`" for p in na_providers)
        out += ["", f"_\\* {joined} cost is `n/a` — provider has no configured pricing._"]
    out += ["", "</details>"]
    return out


def _trend_section(
    con: duckdb.DuckDBPyConnection,
    assets: Path,
    base: str,
    *,
    query: str,
    value_of: Callable[[dict], float | None],
    name: str,
    heading: str,
    intro: list[str],
    fmt_y: Callable[[float], str],
    alt_metric: str,
    exclude: frozenset[str] = frozenset(),
) -> list[str]:
    """Shared builder for the two trend line charts (latency, cost). Returns [] if there's too little data."""
    rows = _try_rows(con, query)
    points: dict[str, dict[str, float]] = {}  # provider -> {runId: value}
    run_ts: dict[str, str] = {}
    for r in rows:
        if r["provider"] in exclude:
            continue
        v = value_of(r)
        if v is None:
            continue
        run_ts.setdefault(str(r["runId"]), str(r["run_ts"]))
        points.setdefault(r["provider"], {})[str(r["runId"])] = v

    runs = sorted(run_ts, key=lambda rid: (run_ts[rid], rid))  # runId breaks any run_ts tie deterministically
    if len(runs) < 2 or not points:
        return []

    x_labels = [f"{run_ts[rid][5:7]}/{run_ts[rid][8:10]}" for rid in runs]
    series = {prov: [vals.get(rid) for rid in runs] for prov, vals in points.items()}

    # Highest/lowest by per-provider mean, for the alt text.
    means = {p: sum(v for v in vals.values()) / len(vals) for p, vals in points.items()}
    hi = max(means, key=lambda p: means[p])
    lo = min(means, key=lambda p: means[p])
    alt = f"{alt_metric} by provider over runs — {hi} highest, {lo} lowest"

    _write_pair(assets, name, lambda t: charts.trend_chart_svg(x_labels, series, t, label=alt, fmt_y=fmt_y))
    return [heading, "", *intro, "", *_picture(base, name, alt)]


def _token_section(con: duckdb.DuckDBPyConnection, assets: Path, base: str) -> list[str]:
    rows = _try_rows(con, "stage_split")
    if not rows:
        return []

    def stage_tokens(provider: str, stage: str) -> int:
        r = next((x for x in rows if x["provider"] == provider and x["stage"] == stage), None)
        return (r["total_prompt_tokens"] or 0) + (r["total_completion_tokens"] or 0) if r else 0

    providers = sorted({r["provider"] for r in rows})
    data = [
        {
            "provider": p,
            "readiness": stage_tokens(p, "ProcessInputAssessment"),
            "extraction": stage_tokens(p, "ValidatedProcessContract"),
        }
        for p in providers
    ]
    data = [d for d in data if d["readiness"] + d["extraction"] > 0]
    if not data:
        return []
    data.sort(key=lambda d: -(d["readiness"] + d["extraction"]))

    extraction_dominant = sum(1 for d in data if d["extraction"] > d["readiness"])
    alt = (
        f"Token split by provider — extraction dominates for {extraction_dominant} of {len(data)} "
        "providers (readiness vs extraction tokens)"
    )
    _write_pair(assets, "token-split", lambda t: charts.token_split_svg(data, t))
    return [
        "## Token split — readiness vs extraction",
        "",
        "_Tokens spent in the cheap readiness gatekeeper (`ProcessInputAssessment`) vs the expensive "
        "extraction stage (`ValidatedProcessContract`), per provider._",
        "",
        *_picture(base, "token-split", alt),
    ]


def _failure_section(
    con: duckdb.DuckDBPyConnection, providers: list[str], assets: Path | None, base: str | None
) -> list[str]:
    rows = _try_rows(con, "failure_categories")
    if not rows and assets is None:
        return []

    out = [
        "## Failure categories",
        "",
        "> [!TIP]",
        "> `deterministic` = harness/config failure (e.g. context load) · `classification` = the model "
        'produced a wrong answer · `infra` = timeout/transport. This separates _"the harness broke"_ '
        'from _"the model struggled."_',
    ]

    if assets is not None and base is not None:
        per_provider = {p: {"provider": p, "counts": {}, "total": 0} for p in providers}
        for r in rows:
            entry = per_provider.setdefault(
                r["provider"], {"provider": r["provider"], "counts": {}, "total": 0}
            )
            entry["counts"][r["failureCategory"]] = int(r["failures"])
            entry["total"] += int(r["failures"])
        data = sorted(per_provider.values(), key=lambda d: (-d["total"], d["provider"]))
        worst = data[0] if data and data[0]["total"] else None
        alt = (
            f"Failure categories by provider — {worst['provider']} has the most failures ({worst['total']})"
            if worst
            else "Failure categories by provider — all providers clean"
        )
        _write_pair(assets, "failure-split", lambda t: charts.failure_split_svg(data, t))
        out += ["", *_picture(base, "failure-split", alt)]

    if rows:
        out += [
            "",
            "<details>",
            "<summary><b>Failure detail</b> — counts, share & sample signatures</summary>",
            "",
            "| Provider | Category | Failures | % of fails | Sample signature |",
            "|---|---|--:|--:|---|",
        ]
        for r in rows:
            # Truncate the raw signature *before* escaping — slicing escaped text could split a "\|" and
            # leave a trailing backslash that escapes the table's delimiter pipe.
            sig = r["sample_signature"] or ""
            if len(sig) > 80:
                sig = sig[:79] + "…"
            out.append(
                f"| `{_cell(r['provider'])}` | {_cell(r['failureCategory'])} | {int(r['failures'])} | "
                f"{r['pct_of_provider_failures'] or 0} | `{_cell(sig)}` |"
            )
        out += ["", "</details>"]
    return out


def _flaky_section(flaky: list[dict]) -> list[str]:
    if not flaky:
        return []
    out = [
        "## Flaky tests",
        "",
        "> [!WARNING]",
        "> Fails **across providers** ⇒ the test or prompt is suspect. Fails on **one provider** ⇒ a "
        "model limit.",
        "",
        "| Test | Fail rate | Providers failed | Samples |",
        "|---|:--|---|--:|",
    ]

    def row(r: dict) -> str:
        pct = float(r["fail_pct"] or 0)
        bar = unicode_bar(min(1.0, pct / 100.0 * 2.0), 12)  # ×2 so single-digit fail rates stay visible
        failed = f"{r['providers_failed']} — {_cell(r['failed_on'])}"
        return f"| `{_cell(r['testMethod'])}` | `{bar}` {pct:.1f}% | {failed} | {r['samples']} |"

    head, rest = flaky[:_FLAKY_TOP], flaky[_FLAKY_TOP:]
    out += [row(r) for r in head]
    if rest:
        ceiling = float(rest[0]["fail_pct"] or 0)  # rows are fail-rate desc, so the first hidden is the cap
        out += [
            "",
            "<details>",
            f"<summary>{len(rest)} more flaky tests (≤ {ceiling:.1f}% fail rate)</summary>",
            "",
            "| Test | Fail rate | Providers failed | Samples |",
            "|---|:--|---|--:|",
            *[row(r) for r in rest],
            "",
            "</details>",
        ]
    return out


def _llm_efficiency_section(con: duckdb.DuckDBPyConnection, assets: Path, base: str) -> list[str]:
    rows = _try_rows(con, "llm_call_distribution")
    if not rows:
        return []
    data = [
        {
            "provider": r["provider"],
            "min": r["min_calls"],
            "avg": r["avg_calls"],
            "median": r["median_calls"],
            "p95": r["p95_calls"],
            "max": r["max_calls"],
        }
        for r in rows
    ]
    data.sort(key=lambda d: (-(d["avg"] or 0), d["provider"]))

    outlier = max(data, key=lambda d: d["p95"] or 0)
    others = [d for d in data if d is not outlier]
    prov = outlier["provider"]
    med, p95, mx = (int(outlier[k] or 0) for k in ("median", "p95", "max"))
    if others:
        # The "outlier vs. the rest" framing only holds with ≥2 providers; name the modal median of the rest.
        medians = [int(d["median"] or 0) for d in others]
        common_median = max(set(medians), key=medians.count)
        callout = (
            f"> `{prov}` is the outlier — median {med} calls/test but a P95 of {p95} and a max of "
            f"**{mx}**, suggesting retry or tool-loop storms. Every other provider sits at a median "
            f"of {common_median}."
        )
        alt = f"LLM calls per test by provider — {prov} spread is far wider than the rest"
    else:
        callout = (
            f"> `{prov}` ran a median of {med} LLM calls/test (P95 {p95}, max **{mx}**). More calls per "
            "test point to retry or tool-loop storms."
        )
        alt = f"LLM calls per test — {prov}: median {med}, P95 {p95}, max {mx}"
    _write_pair(assets, "llm-efficiency", lambda t: charts.llm_efficiency_svg(data, t))
    return ["## LLM efficiency", "", "> [!IMPORTANT]", callout, "", *_picture(base, "llm-efficiency", alt)]


# ---------------------------------------------------------------------------
# Top-level assembly
# ---------------------------------------------------------------------------


def render(data_dir: Path | str, assets_dir: Path | str | None = None) -> str:
    con = duckdb.connect(":memory:")
    # Placeholder when there are no *completed* rows — not merely no files: a directory of only
    # runComplete=false rows passes the file check but the view is empty.
    if not _load(con, Path(data_dir)) or con.execute("SELECT count(*) FROM results").fetchone()[0] == 0:
        return _PLACEHOLDER

    assets = Path(assets_dir) if assets_dir is not None else None
    base = assets.as_posix() if assets is not None else None

    scorecard = _rows(con, "scorecard")
    flaky = _rows(con, "flaky")
    providers = sorted({r["provider"] for r in scorecard})
    # Providers with no configured pricing — excluded from the per-test cost chart and named in its note.
    unpriced = sorted(r["provider"] for r in scorecard if r["cost_caveat"])

    parts: list[list[str]] = [["# 🔬 Smoke Health"]]

    # Summary banner + report-only note.
    if assets is not None and base is not None and scorecard:
        avg_pass = sum(r["pass_pct"] or 0 for r in scorecard) / len(scorecard)
        total_fails = sum(int(r["fails"] or 0) for r in scorecard)
        _write_pair(
            assets,
            "summary",
            lambda t: charts.summary_banner_svg(len(scorecard), avg_pass, total_fails, len(flaky), t),
        )
        alt = (
            f"{len(scorecard)} providers · {avg_pass:.1f}% average pass rate · "
            f"{total_fails} total failures · {len(flaky)} flaky tests"
        )
        parts.append(_picture(base, "summary", alt))
    parts.append(
        [
            "> [!NOTE]",
            "> **Report-only · all recorded runs.** _Provider_ = the model family under test. Pass/fail "
            "reflects the authoritative post-retry outcome joined from `test.xml`.",
        ]
    )

    parts.append(_scorecard_section(scorecard, assets, base))

    if assets is not None and base is not None:
        parts.append(
            _trend_section(
                con,
                assets,
                base,
                query="latency_timeseries",
                value_of=lambda r: (r["avg_llm_time_ms"] / 1000) if r["avg_llm_time_ms"] else None,
                name="latency-trend",
                heading="## Latency",
                intro=["_Average LLM response time per provider over runs (seconds, wall-clock)._"],
                fmt_y=lambda v: f"{v:.1f}s",
                alt_metric="Average LLM latency",
            )
        )
        parts.append(
            _trend_section(
                con,
                assets,
                base,
                query="cost_timeseries",
                value_of=_cost_per_test,
                name="cost-trend",
                heading="## Cost per test",
                intro=[
                    "> [!CAUTION]",
                    "> Cost is normalised **per test** — shard sizes vary run-to-run, so raw per-run "
                    f"totals aren't comparable.{_excluded_note(unpriced)}",
                ],
                fmt_y=lambda v: f"${v:.3f}",
                alt_metric="Cost per test",
                exclude=frozenset(unpriced),
            )
        )
        parts.append(_token_section(con, assets, base))

    parts.append(_failure_section(con, providers, assets, base))
    parts.append(_flaky_section(flaky))

    if assets is not None and base is not None:
        parts.append(_llm_efficiency_section(con, assets, base))

    parts.append(
        [
            "---",
            "",
            "<sub>📖 How this repo works — ingest, querying & setup → [`ABOUT.md`](ABOUT.md) · Regenerated "
            "every run by `render_dashboard.py`. Machine-managed — do not edit by hand.</sub>",
        ]
    )

    blocks = ["\n".join(part) for part in parts if part]
    return "\n\n".join(blocks) + "\n"


def _excluded_note(unpriced: list[str]) -> str:
    """Trailing clause for the cost caveat naming providers dropped for lack of configured pricing."""
    if not unpriced:
        return ""
    joined = ", ".join(f"`{p}`" for p in unpriced)
    verb = "is" if len(unpriced) == 1 else "are"
    return f" {joined} {verb} excluded (no configured pricing)."


def _cost_per_test(r: dict) -> float | None:
    """Cost normalised per test, or None when the run is unpriced / has no tests.

    Providers run rotating shards (4–8 tests/run), so raw per-run totals conflate per-test cost with
    shard size; normalising to cost-per-test makes runs comparable. Unpriced providers are dropped.
    """
    if not r["cost_known"] or r["total_cost"] is None:
        return None
    tests = r["tests_in_run"] or 0
    if not tests:
        return None
    return r["total_cost"] / tests


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
