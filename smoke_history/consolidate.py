# Copyright 2026 The Project Contributors
# SPDX-License-Identifier: MIT
"""Consolidate one CI run's per-provider smoke artifacts into a single enriched JSONL file.

Each provider's smoke job uploads an artifact `smoke-<provider>/` containing:
  smoke-results.jsonl            one SmokeRunResult per test (the in-JVM recorder's attempt-1 view)
  test.xml                       Bazel's final JUnit XML (authoritative outcome after retries)
  test_attempts/attempt_*.xml    prior-attempt XMLs, present only when Bazel retried (--flaky_test_attempts)

For each row we override `outcome` with the authoritative final verdict from test.xml (joined by test
method) and fill `attempts` (Bazel retries the whole target, so attempts is per-provider). A row that the
in-JVM recorder saw fail but the final test.xml passed is a flake: outcome=pass, attempts>1. Providers
that uploaded no smoke-results.jsonl are skipped and logged (a hard-killed/OOM job is no-data for the run).

    uv run python -m smoke_history.consolidate <artifacts-dir> <run-id> -o run-<id>.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def _norm(method: str) -> str:
    """Join key: drop a trailing '()' so the recorder's displayName matches the test.xml `name`."""
    return method[:-2] if method.endswith("()") else method


def _junit_outcomes(xml_path: Path) -> dict[str, str]:
    """Map normalized test-method name -> pass|fail|skip from a JUnit XML file (empty if unreadable)."""
    out: dict[str, str] = {}
    try:
        root = ET.parse(xml_path).getroot()
    except (ET.ParseError, OSError):
        return out
    for tc in root.iter("testcase"):
        name = _norm(tc.get("name", ""))
        if tc.find("skipped") is not None:
            out[name] = "skip"
        elif tc.find("failure") is not None or tc.find("error") is not None:
            out[name] = "fail"
        else:
            out[name] = "pass"
    return out


def _attempts(provider_dir: Path) -> int:
    """Bazel retries the whole target, so attempts is per-provider: prior attempt XMLs + the final run."""
    return len(list((provider_dir / "test_attempts").glob("*.xml"))) + 1


def consolidate(artifacts_dir: Path, run_id: str) -> list[dict]:
    rows: list[dict] = []
    provider_dirs = sorted(d for d in Path(artifacts_dir).glob("smoke-*") if d.is_dir())
    for pd in provider_dirs:
        jsonl = pd / "smoke-results.jsonl"
        if not jsonl.exists():
            sys.stderr.write(f"  {pd.name}: no smoke-results.jsonl — excluded (no-data)\n")
            continue
        verdicts = _junit_outcomes(pd / "test.xml")
        attempts = _attempts(pd)
        n = 0
        for line in jsonl.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            final = verdicts.get(_norm(row.get("testMethod", "")))
            if final is not None:
                row["outcome"] = final  # authoritative final verdict, post-retry
            row["attempts"] = attempts
            row["runId"] = run_id
            rows.append(row)
            n += 1
        sys.stderr.write(f"  {pd.name}: {n} rows, attempts={attempts}\n")
    sys.stderr.write(f"consolidated {len(rows)} rows from {len(provider_dirs)} provider artifact(s)\n")
    return rows


def _write(rows: list[dict], out_path: Path) -> None:
    Path(out_path).write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("artifacts_dir", help="dir of downloaded smoke-<provider>/ artifacts")
    ap.add_argument("run_id", help="CI run id (stamped onto every row)")
    ap.add_argument("-o", "--output", required=True, help="output JSONL path")
    args = ap.parse_args()
    _write(consolidate(Path(args.artifacts_dir), args.run_id), Path(args.output))


if __name__ == "__main__":
    main()
