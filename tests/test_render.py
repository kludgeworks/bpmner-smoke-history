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


def _write_rows(data: Path, rows: list[dict]) -> None:
    data.mkdir()
    (data / "run.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")


def _row(md: str, name: str) -> str:
    return next(line for line in md.splitlines() if name in line)


def test_no_signal_quota_rows_do_not_poison_priced_costs(tmp_path):
    data = tmp_path / "data"
    rows = [
        {
            "ts": "2026-06-05T10:00:00Z",
            "runId": "1",
            "provider": "openai",
            "servedModel": "gpt-4.1",
            "testMethod": "ok1",
            "outcome": "pass",
            "costUsd": 0.01,
            "costKnown": "priced",
            "promptTokens": 10,
            "completionTokens": 2,
            "llmCallCount": 1,
            "runComplete": True,
        },
        {
            "ts": "2026-06-05T10:00:01Z",
            "runId": "1",
            "provider": "openai",
            "servedModel": "gpt-4.1",
            "testMethod": "quotaNoise",
            "outcome": "fail",
            "failureSignal": "no_signal",
            "failureSignature": "quota exhausted before request",
            "costUsd": None,
            "costKnown": "unknown",
            "promptTokens": 0,
            "completionTokens": 0,
            "llmCallCount": 0,
            "runComplete": True,
        },
        {
            "ts": "2026-06-06T10:00:00Z",
            "runId": "2",
            "provider": "openai",
            "servedModel": "gpt-4.1",
            "testMethod": "ok2",
            "outcome": "pass",
            "costUsd": 0.02,
            "costKnown": "priced",
            "promptTokens": 20,
            "completionTokens": 4,
            "llmCallCount": 1,
            "runComplete": True,
        },
    ]
    _write_rows(data, rows)

    assets = tmp_path / "assets"
    md = render(data, assets_dir=assets)

    assert "| `openai` |" in md
    assert "| `openai` | `██████████████` 100.0% | 0 | $0.0150 |" in md
    assert "quotaNoise" not in md
    assert "cost-trend-light.svg" in md
    assert (assets / "cost-trend-light.svg").exists()


def test_no_signal_rows_do_not_inflate_flaky_or_failure_categories(tmp_path):
    data = tmp_path / "data"
    common = {
        "ts": "2026-06-05T10:00:00Z",
        "runId": "1",
        "servedModel": "model",
        "costUsd": 0.01,
        "costKnown": "priced",
        "promptTokens": 10,
        "completionTokens": 2,
        "runComplete": True,
    }
    rows = [
        common
        | {
            "provider": "anthropic",
            "testMethod": "quotaOnly",
            "outcome": "fail",
            "failureSignal": "no_signal",
            "failureSignature": "billing quota",
            "llmCallCount": 0,
        },
        common
        | {
            "provider": "gemini",
            "testMethod": "quotaOnly",
            "outcome": "fail",
            "failureSignal": "no_signal",
            "failureSignature": "billing quota",
            "llmCallCount": 0,
        },
        common
        | {
            "provider": "llama",
            "testMethod": "signalTest",
            "outcome": "fail",
            "failureCategory": "classification",
            "failureSignature": "signalTest::wrong",
            "llmCallCount": 2,
        },
        common
        | {
            "provider": "openai",
            "testMethod": "signalTest",
            "outcome": "pass",
            "failureSignature": None,
            "llmCallCount": 1,
        },
    ]
    _write_rows(data, rows)

    md = render(data)

    assert "quotaOnly" not in md
    signal_row = _row(md, "`signalTest`")
    assert "1 — llama" in signal_row
    assert signal_row.endswith("| 2 |")
    assert "| `llama` | classification | 1 | 100.0 | `signalTest::wrong` |" in md
    assert "| `anthropic` | infra |" not in md
    assert "| `gemini` | infra |" not in md


def test_genuinely_unpriced_signal_provider_remains_caveated(tmp_path):
    data = tmp_path / "data"
    _write_rows(
        data,
        [
            {
                "ts": "2026-06-05T10:00:00Z",
                "runId": "1",
                "provider": "unpriced",
                "servedModel": "local",
                "testMethod": "realSignal",
                "outcome": "fail",
                "failureCategory": "infra",
                "failureSignature": "realSignal::timeout",
                "costUsd": 0.0,
                "costKnown": "unknown",
                "promptTokens": 10,
                "completionTokens": 2,
                "llmCallCount": 1,
                "runComplete": True,
            }
        ],
    )

    md = render(data)

    assert "| `unpriced` | `░░░░░░░░░░░░░░` 0.0% | 1 | n/a |" in md
    assert "`unpriced` cost is `n/a`" in md


def test_legacy_quota_fallback_requires_zero_calls(tmp_path):
    data = tmp_path / "data"
    base = {
        "ts": "2026-06-05T10:00:00Z",
        "runId": "1",
        "servedModel": "model",
        "outcome": "fail",
        "failureCategory": "infra",
        "costUsd": 0.0,
        "costKnown": "unknown",
        "promptTokens": 0,
        "completionTokens": 0,
        "runComplete": True,
    }
    _write_rows(
        data,
        [
            base
            | {
                "provider": "legacy",
                "testMethod": "quotaZero",
                "failureSignature": "quota exhausted",
                "llmCallCount": 0,
            },
            base
            | {
                "provider": "legacy",
                "testMethod": "partialQuota",
                "failureSignature": "quota after one call",
                "llmCallCount": 1,
            },
        ],
    )

    md = render(data)

    assert "quotaZero" not in md
    assert "partialQuota" in md


def test_legacy_unknown_cost_without_quota_clue_remains_signal(tmp_path):
    data = tmp_path / "data"
    _write_rows(
        data,
        [
            {
                "ts": "2026-06-05T10:00:00Z",
                "runId": "1",
                "provider": "legacy",
                "servedModel": "model",
                "testMethod": "harnessSetup",
                "outcome": "fail",
                "failureCategory": "infra",
                "failureSignature": "harness setup failed",
                "costUsd": 0.0,
                "costKnown": "unknown",
                "promptTokens": 0,
                "completionTokens": 0,
                "llmCallCount": 0,
                "runComplete": True,
            }
        ],
    )

    md = render(data)

    assert "| `legacy` | `░░░░░░░░░░░░░░` 0.0% | 1 | n/a |" in md
    assert "| `legacy` | infra | 1 | 100.0 | `harness setup failed` |" in md
    assert "| `harnessSetup` |" in md


def test_unicode_bar_is_fixed_width_and_proportional():
    # 14-cell scorecard scale: full bar at 100%, exact eighth-block remainder, padded with ░.
    assert unicode_bar(1.0, 14) == "█" * 14
    assert unicode_bar(0.0, 14) == "░" * 14
    assert len(unicode_bar(0.734, 14)) == 14
    assert unicode_bar(0.5, 8) == "████░░░░"
    # 12-cell flaky scale (callers pre-double the fraction); a quarter-bar uses the 2/8 block.
    assert unicode_bar(0.25, 12) == "███░░░░░░░░░"
    assert unicode_bar(0.44 * 2, 12) == "██████████▌░"
