# Copyright 2026 The Project Contributors
# SPDX-License-Identifier: MIT
import json
from pathlib import Path

from smoke_history.consolidate import _norm, consolidate

DATA = Path(__file__).parent / "testdata-consolidate"


def test_consolidates_every_provider():
    rows = consolidate(DATA, "test-run")
    assert len(rows) == 6  # anthropic (3) + llama (3)
    assert all(r["runId"] == "test-run" for r in rows)


def test_reconciles_flake_to_final_verdict():
    by = {(r["provider"], _norm(r["testMethod"])): r for r in consolidate(DATA, "r")}
    # the recorder saw this fail, but the final test.xml passed on retry -> authoritative pass
    assert by[("llama", "extractsBoundaryEvent")]["outcome"] == "pass"


def test_missing_results_file_is_skipped(tmp_path):
    (tmp_path / "smoke-ghost").mkdir()  # a provider dir with no smoke-results.jsonl
    assert consolidate(tmp_path, "r") == []


def _provider(tmp_path, *lines: str) -> Path:
    p = tmp_path / "smoke-x"
    p.mkdir()
    (p / "smoke-results.jsonl").write_text("".join(line + "\n" for line in lines), encoding="utf-8")
    return p


def test_missing_test_xml_keeps_recorder_outcome(tmp_path):
    # rows but no test.xml -> cannot reconcile; keep the recorder's (pre-retry) outcome, don't drop
    _provider(tmp_path, json.dumps({"testClass": "T", "testMethod": "m()", "outcome": "fail"}))
    rows = consolidate(tmp_path, "r")
    assert len(rows) == 1
    assert rows[0]["outcome"] == "fail"  # unchanged — no XML to override it


def test_malformed_line_is_skipped(tmp_path):
    _provider(
        tmp_path,
        json.dumps({"testClass": "T", "testMethod": "m()", "outcome": "pass"}),
        "{not valid json",
    )
    rows = consolidate(tmp_path, "r")
    assert len(rows) == 1  # the bad line is skipped, the good one kept
