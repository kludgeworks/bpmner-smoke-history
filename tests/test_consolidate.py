# Copyright 2026 The Project Contributors
# SPDX-License-Identifier: MIT
from pathlib import Path

from smoke_history.consolidate import _norm, consolidate

DATA = Path(__file__).parent / "testdata-consolidate"


def test_consolidates_every_provider():
    rows = consolidate(DATA, "test-run")
    assert len(rows) == 6  # anthropic (3) + llama (3)
    assert all(r["runId"] == "test-run" for r in rows)


def test_reconciles_flake_to_final_verdict():
    by = {(r["provider"], _norm(r["testMethod"])): r for r in consolidate(DATA, "r")}
    boundary = by[("llama", "extractsBoundaryEvent")]
    # the in-JVM recorder saw this fail, but the final test.xml passed on retry
    assert boundary["outcome"] == "pass"
    assert boundary["attempts"] == 2  # one prior attempt + the final run


def test_clean_run_has_single_attempt():
    by = {(r["provider"], _norm(r["testMethod"])): r for r in consolidate(DATA, "r")}
    assert by[("anthropic", "extractsServiceTask")]["attempts"] == 1


def test_missing_results_file_is_skipped(tmp_path):
    (tmp_path / "smoke-ghost").mkdir()  # a provider dir with no smoke-results.jsonl
    assert consolidate(tmp_path, "r") == []
