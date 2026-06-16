# Copyright 2026 The Project Contributors
# SPDX-License-Identifier: MIT
import json
from pathlib import Path

from smoke_history.render_dashboard import main, render, unicode_bar

DATA = Path(__file__).parent / "testdata"


def test_renders_scorecard_rows():
    md = render(DATA)
    assert "## Provider scorecard" in md
    # Providers are rendered as code spans in the full table now.
    assert "| `anthropic` |" in md
    assert "| `llama` |" in md


def test_emits_summary_note_and_footnote():
    md = render(DATA)
    assert md.startswith("# 🔬 Smoke Health")
    assert "> [!NOTE]" in md
    # The homepage owns the whole file, so the pointer to the moved docs must be generated, not hand-added.
    assert "[`ABOUT.md`](ABOUT.md)" in md
    assert "Machine-managed — do not edit by hand." in md


def _flaky_row(md: str) -> str:
    # The flaky table cell wraps the whole test name in backticks ("`name`"); the failure-detail table
    # only ever shows it as a signature prefix ("`name::…"), so the closing backtick disambiguates.
    return next(line for line in md.splitlines() if "`extractsBoundaryEvent`" in line)


def test_flags_cross_provider_flaky_test():
    row = _flaky_row(render(DATA))
    # it fails on both gemini and llama in the fixtures (cross-provider)
    assert "gemini" in row and "llama" in row


def test_flaky_rate_uses_unicode_bar():
    row = _flaky_row(render(DATA))
    assert "░" in row or "█" in row, "flaky fail-rate column should render a unicode bar"


def test_empty_dir_renders_placeholder(tmp_path):
    assert "No completed runs" in render(tmp_path)


def test_only_partial_rows_renders_placeholder(tmp_path):
    # files exist, but every row is runComplete=false -> the view is empty -> placeholder, not blank tables
    (tmp_path / "run.jsonl").write_text(
        json.dumps({"provider": "x", "testMethod": "m", "outcome": "pass", "runComplete": False}) + "\n",
        encoding="utf-8",
    )
    assert "No completed runs" in render(tmp_path)


def test_token_split_section_needs_assets():
    # The token chart is chart-only, so without an assets dir the section is omitted entirely.
    assert "## Token split" not in render(DATA)


def test_renders_latency_chart_when_nonzero(tmp_path):
    # Latency is a chart (needs an assets dir + 2+ runs with non-zero llmTimeMs).
    md = render(DATA, assets_dir=tmp_path / "assets" / "smoke-health")
    if "## Latency" in md:
        assert "latency-trend-light.svg" in md
        assert "latency-trend-dark.svg" in md


def test_renders_failure_categories():
    md = render(DATA)
    # The fixtures carry failing rows with a failureCategory, so the detail table renders.
    assert "## Failure categories" in md
    assert "Sample signature" in md


def test_picture_blocks_pair_light_and_dark(tmp_path):
    assets = tmp_path / "assets" / "smoke-health"
    md = render(DATA, assets_dir=assets)
    # Every emitted chart is a <picture> pairing a dark <source> with a light <img> fallback.
    assert md.count("<picture>") == md.count("prefers-color-scheme: dark")
    assert (assets / "summary-light.svg").exists()
    assert (assets / "summary-dark.svg").exists()


def test_output_is_deterministic(tmp_path):
    a = render(DATA, assets_dir=tmp_path / "a")
    b = render(DATA, assets_dir=tmp_path / "a")  # same dir on purpose: identical links
    assert a == b
    assert a.endswith("\n") and not a.endswith("\n\n")


def test_cli_output_ends_with_exactly_one_newline(capsys, monkeypatch):
    # The dashboard is written via `python -m smoke_history.render_dashboard data > README.md`; the file
    # must end with exactly one newline or end-of-file-fixer rejects it. Run main() in-process, check stdout.
    monkeypatch.setattr("sys.argv", ["render_dashboard", str(DATA)])
    main()
    out = capsys.readouterr().out
    assert out.endswith("\n") and not out.endswith("\n\n")


def test_llm_efficiency_callout_handles_single_provider(tmp_path):
    # Only one provider has llmCallCount data: the callout must not claim "every other provider".
    data = tmp_path / "data"
    data.mkdir()
    rows = [
        {
            "provider": "openai",
            "testMethod": f"t{i}",
            "outcome": "pass",
            "runComplete": True,
            "runId": "1",
            "ts": f"2026-06-05T10:00:0{i}Z",
            "llmCallCount": 5 + i,
            "servedModel": "gpt-4.1",
            "costUsd": 0.01,
            "costKnown": "priced",
            "promptTokens": 100,
            "completionTokens": 20,
        }
        for i in range(4)
    ]
    (data / "run.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    md = render(data, assets_dir=tmp_path / "assets")
    assert "## LLM efficiency" in md
    assert "Every other provider" not in md
    assert "median of 0" not in md
    assert "`openai` ran a median of" in md


def test_unicode_bar_is_fixed_width_and_proportional():
    # 14-cell scorecard scale: full bar at 100%, exact eighth-block remainder, padded with ░.
    assert unicode_bar(1.0, 14) == "█" * 14
    assert unicode_bar(0.0, 14) == "░" * 14
    assert len(unicode_bar(0.734, 14)) == 14
    assert unicode_bar(0.5, 8) == "████░░░░"
    # 12-cell flaky scale (callers pre-double the fraction); a quarter-bar uses the 2/8 block.
    assert unicode_bar(0.25, 12) == "███░░░░░░░░░"
    assert unicode_bar(0.44 * 2, 12) == "██████████▌░"
