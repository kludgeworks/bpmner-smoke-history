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
    flake = by[("llama", "extractsBoundaryEvent")]
    assert flake["outcome"] == "pass"
    assert flake["firstAttemptOutcome"] == "fail"
    assert flake["finalOutcome"] == "pass"
    assert flake["recoveredOnRetry"] is True


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
    assert rows[0]["firstAttemptOutcome"] == "fail"
    assert rows[0]["finalOutcome"] == "fail"
    assert rows[0]["recoveredOnRetry"] is False


def test_row_without_outcome_does_not_crash(tmp_path):
    # A recorder row missing "outcome" entirely, with no test.xml to reconcile, must not KeyError.
    _provider(tmp_path, json.dumps({"testClass": "T", "testMethod": "m()"}))
    rows = consolidate(tmp_path, "r")
    assert len(rows) == 1
    assert rows[0]["firstAttemptOutcome"] == "unknown"
    assert rows[0]["finalOutcome"] == "unknown"
    assert rows[0]["recoveredOnRetry"] is False


def test_malformed_line_is_skipped(tmp_path):
    _provider(
        tmp_path,
        json.dumps({"testClass": "T", "testMethod": "m()", "outcome": "pass"}),
        "{not valid json",
    )
    rows = consolidate(tmp_path, "r")
    assert len(rows) == 1  # the bad line is skipped, the good one kept


def test_retry_recovery_fields(tmp_path):
    """A test that the recorder saw fail but test.xml says passed gets all retry fields set."""
    p = tmp_path / "smoke-retry"
    p.mkdir()
    (p / "smoke-results.jsonl").write_text(
        json.dumps({"testClass": "RetrySmokeTest", "testMethod": "flakyMethod()", "outcome": "fail"})
        + "\n"
        + json.dumps({"testClass": "RetrySmokeTest", "testMethod": "stableMethod()", "outcome": "pass"})
        + "\n",
        encoding="utf-8",
    )
    (p / "test.xml").write_text(
        '<testsuite tests="2">'
        '  <testcase classname="RetrySmokeTest" name="flakyMethod()"></testcase>'
        '  <testcase classname="RetrySmokeTest" name="stableMethod()"></testcase>'
        "</testsuite>",
        encoding="utf-8",
    )
    rows = consolidate(tmp_path, "r42")
    by_method = {_norm(r["testMethod"]): r for r in rows}

    recovered = by_method["flakyMethod"]
    assert recovered["outcome"] == "pass"  # backward-compatible: final verdict
    assert recovered["firstAttemptOutcome"] == "fail"  # recorder's first-attempt view
    assert recovered["finalOutcome"] == "pass"  # authoritative XML verdict
    assert recovered["recoveredOnRetry"] is True
    assert recovered["runId"] == "r42"

    stable = by_method["stableMethod"]
    assert stable["outcome"] == "pass"
    assert stable["firstAttemptOutcome"] == "pass"
    assert stable["finalOutcome"] == "pass"
    assert stable["recoveredOnRetry"] is False
