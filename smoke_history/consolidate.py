# Copyright 2026 The Project Contributors
# SPDX-License-Identifier: MIT
"""Consolidate one CI run's per-provider smoke artifacts into a single enriched JSONL file.

Each provider's smoke job uploads an artifact `smoke-<provider>/` containing:
  smoke-results.jsonl   one SmokeRunResult per test (the in-JVM recorder's attempt-1 view)
  test.xml              Bazel's final JUnit XML (authoritative outcome after any --flaky_test_attempts)

We override each row's `outcome` with the authoritative final verdict from test.xml — joined by
`(test-class, test-method)` — and stamp the canonical `runId` (the dispatching Actions run id). A row the
recorder saw fail but the final XML passed is thus published as pass (a flake that recovered on retry).

Degradation is explicit, never silent: a provider with no smoke-results.jsonl is skipped (no-data); a
provider with rows but a missing/unreadable test.xml keeps the recorder's pre-retry outcomes and is
logged (we cannot reconcile without the XML); a malformed JSONL line is skipped and logged.

    uv run python -m smoke_history.consolidate <artifacts-dir> <run-id> -o run-<id>.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def _norm(method: str) -> str:
    """Drop a trailing '()' so the recorder's displayName matches the test.xml `name`."""
    return method[:-2] if method.endswith("()") else method


def _simple_class(name: str) -> str:
    """Simple class name: the recorder records simple names, test.xml carries the FQN."""
    return name.rsplit(".", 1)[-1]


def _junit_outcomes(xml_path: Path) -> dict[tuple[str, str], str]:
    """Map (simple-classname, method) -> pass|fail|skip from a JUnit XML file (empty if unreadable)."""
    out: dict[tuple[str, str], str] = {}
    try:
        root = ET.parse(xml_path).getroot()
    except ET.ParseError, OSError:
        return out
    for tc in root.iter("testcase"):
        key = (_simple_class(tc.get("classname", "")), _norm(tc.get("name", "")))
        if tc.find("skipped") is not None:
            out[key] = "skip"
        elif tc.find("failure") is not None or tc.find("error") is not None:
            out[key] = "fail"
        else:
            out[key] = "pass"
    return out


def consolidate(artifacts_dir: Path, run_id: str) -> list[dict]:
    rows: list[dict] = []
    provider_dirs = sorted(d for d in Path(artifacts_dir).glob("smoke-*") if d.is_dir())
    for pd in provider_dirs:
        jsonl = pd / "smoke-results.jsonl"
        if not jsonl.exists():
            sys.stderr.write(f"  {pd.name}: no smoke-results.jsonl — excluded (no-data)\n")
            continue
        verdicts = _junit_outcomes(pd / "test.xml")
        n = 0
        for lineno, line in enumerate(jsonl.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as e:
                sys.stderr.write(f"  {pd.name}: skipping malformed line {lineno}: {e}\n")
                continue
            final = verdicts.get((row.get("testClass", ""), _norm(row.get("testMethod", ""))))
            if final is not None:
                row["outcome"] = final  # authoritative final verdict, post-retry
            row["runId"] = run_id
            rows.append(row)
            n += 1
        if n and not verdicts:
            sys.stderr.write(f"  {pd.name}: test.xml missing/unreadable — kept {n} recorder rows\n")
        else:
            sys.stderr.write(f"  {pd.name}: {n} rows\n")
    sys.stderr.write(f"consolidated {len(rows)} rows from {len(provider_dirs)} provider artifact(s)\n")
    return rows


def _write(rows: list[dict], out_path: Path) -> None:
    Path(out_path).write_text(
        "".join(json.dumps(r, separators=(",", ":")) + "\n" for r in rows), encoding="utf-8"
    )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("artifacts_dir", help="dir of downloaded smoke-<provider>/ artifacts")
    ap.add_argument("run_id", help="Actions run id (stamped onto every row as runId)")
    ap.add_argument("-o", "--output", required=True, help="output JSONL path")
    args = ap.parse_args()
    _write(consolidate(Path(args.artifacts_dir), args.run_id), Path(args.output))


if __name__ == "__main__":
    main()
