#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = ["xmlformatter"]
# ///
#
# Copyright 2026 The Project Contributors
# SPDX-License-Identifier: MIT
#
#MISE description="Check or fix XML formatting (xmlformatter)."
#USAGE flag "-c --check" help="Fail if any file is not formatted."
#USAGE flag "-f --fix" help="Rewrite files in place."
#USAGE arg "<files>" var=#true help="XML files to check/fix."
from __future__ import annotations

import os
import sys
from pathlib import Path

import xmlformatter

_FORMATTER = xmlformatter.Formatter(indent=2, indent_char=" ", encoding_output="utf-8", preserve=["literal"])


def main() -> int:
    fix = os.environ.get("usage_fix") == "true"
    files = os.environ.get("usage_files", "").split()  # usage passes variadic args space-separated
    unformatted: list[str] = []
    for name in files:
        path = Path(name)
        formatted = _FORMATTER.format_file(str(path))  # bytes
        if not formatted.endswith(b"\n"):
            formatted += b"\n"  # match the repo's end-of-file-newline convention
        if formatted == path.read_bytes():
            continue
        if fix:
            path.write_bytes(formatted)
        else:
            unformatted.append(name)
    if unformatted:
        sys.stderr.write("XML not formatted (run with --fix):\n")
        sys.stderr.write("".join(f"  {f}\n" for f in unformatted))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
