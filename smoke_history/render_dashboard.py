# Copyright 2026 The Project Contributors
# SPDX-License-Identifier: MIT
"""Render the "Smoke Health" dashboard from accumulated per-run result files.

Reads a directory tree of newline-delimited JSON (`*.jsonl`), one `SmokeRunResult` per line, runs the
rolling-window analytics with DuckDB (queries in `queries/`), and prints the dashboard markdown.

    uv run python -m smoke_history.render_dashboard <data-dir>
"""

from __future__ import annotations

import argparse
from pathlib import Path

import duckdb

WINDOW_RUNS = 60  # documented rolling window; widen once enough history accrues
_QUERIES = Path(__file__).resolve().parent.parent / "queries"


def _load(con: duckdb.DuckDBPyConnection, data_dir: Path) -> bool:
    """Load every `*.jsonl` under data_dir into a `results` view. Returns False if there's no data."""
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


def render(data_dir: Path | str) -> str:
    con = duckdb.connect(":memory:")
    if not _load(con, Path(data_dir)):
        return "# 🔬 Smoke Health\n\n_No completed runs recorded yet._\n"

    out = [
        "# 🔬 Smoke Health",
        "",
        f"_Rolling window: last {WINDOW_RUNS} runs · report-only · provider = model family under test._",
        "",
        "## Provider scorecard",
        "",
        "| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for r in _rows(con, "scorecard"):
        cost = "n/a*" if r["cost_caveat"] else f"${r['cost_per_run'] or 0:.4f}"
        out.append(
            f"| {r['provider']} | `{r['model'] or '?'}` | {r['runs']} | {r['pass_pct']} | "
            f"{r['fails']} | {cost} | {r['tokens'] or 0} |"
        )
    out += [
        "",
        "_\\* cost unknown — provider has no configured pricing._",
        "",
        "## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)",
        "",
        "| Test | Fail % | Providers failed | Samples |",
        "|---|---:|---|---:|",
    ]
    flaky = _rows(con, "flaky")
    if not flaky:
        out.append("| _none_ | | | |")
    for r in flaky:
        out.append(
            f"| `{r['testMethod']}` | {r['fail_pct']} | "
            f"{r['providers_failed']} ({r['failed_on']}) | {r['samples']} |"
        )
    out.append("")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("data_dir", help="directory tree of *.jsonl result files")
    print(render(ap.parse_args().data_dir))


if __name__ == "__main__":
    main()
