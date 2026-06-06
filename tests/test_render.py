# Copyright 2026 The Project Contributors
# SPDX-License-Identifier: MIT
import json
from pathlib import Path

from smoke_history.render_dashboard import main, render

DATA = Path(__file__).parent / "testdata"


def test_renders_scorecard_rows():
    md = render(DATA)
    assert "## Provider scorecard" in md
    assert "| anthropic |" in md
    assert "| llama |" in md


def test_flags_cross_provider_flaky_test():
    md = render(DATA)
    row = next((line for line in md.splitlines() if "extractsBoundaryEvent" in line), "")
    assert row, "expected a flaky-table row for extractsBoundaryEvent"
    # it fails on both gemini and llama in the fixtures (cross-provider)
    assert "gemini" in row and "llama" in row


def test_empty_dir_renders_placeholder(tmp_path):
    assert "No completed runs" in render(tmp_path)


def test_only_partial_rows_renders_placeholder(tmp_path):
    # files exist, but every row is runComplete=false -> the view is empty -> placeholder, not blank tables
    (tmp_path / "run.jsonl").write_text(
        json.dumps({"provider": "x", "testMethod": "m", "outcome": "pass", "runComplete": False}) + "\n",
        encoding="utf-8",
    )
    assert "No completed runs" in render(tmp_path)


def test_cli_output_ends_with_exactly_one_newline(capsys, monkeypatch):
    # The dashboard is written via `python -m smoke_history.render_dashboard data > SMOKE_HEALTH.md`; the file
    # must end with exactly one newline or end-of-file-fixer rejects it. Run main() in-process, check stdout.
    monkeypatch.setattr("sys.argv", ["render_dashboard", str(DATA)])
    main()
    out = capsys.readouterr().out
    assert out.endswith("\n") and not out.endswith("\n\n")
