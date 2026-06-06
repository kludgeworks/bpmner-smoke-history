# Copyright 2026 The Project Contributors
# SPDX-License-Identifier: MIT
from pathlib import Path

from smoke_history.render_dashboard import render

DATA = Path(__file__).parent / "testdata"


def test_renders_scorecard_rows():
    md = render(DATA)
    assert "## Provider scorecard" in md
    assert "| anthropic |" in md
    assert "| llama |" in md


def test_flags_cross_provider_flaky_test():
    md = render(DATA)
    # extractsBoundaryEvent fails on 2 providers (gemini + llama) in the fixtures
    assert "extractsBoundaryEvent" in md
    assert " 2 (" in md


def test_empty_dir_renders_placeholder(tmp_path):
    assert "No completed runs" in render(tmp_path)
