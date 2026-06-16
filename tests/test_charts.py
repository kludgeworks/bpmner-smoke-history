# Copyright 2026 The Project Contributors
# SPDX-License-Identifier: MIT
from smoke_history import charts
from smoke_history.charts import THEMES, score_color


def _scorecard_rows():
    return [
        {"provider": "gemini", "pass_pct": 100.0, "fails": 0},
        {"provider": "deepseek", "pass_pct": 87.0, "fails": 12},
    ]


def test_every_chart_emits_a_light_and_dark_variant_that_differ():
    light, dark = THEMES["light"], THEMES["dark"]
    rows = _scorecard_rows()
    builders = [
        lambda t: charts.summary_banner_svg(6, 95.2, 36, 14, t),
        lambda t: charts.scorecard_svg(rows, t),
        lambda t: charts.token_split_svg([{"provider": "openai", "readiness": 1, "extraction": 3}], t),
        lambda t: charts.failure_split_svg(
            [{"provider": "openai", "counts": {"classification": 2}, "total": 2}], t
        ),
        lambda t: charts.llm_efficiency_svg(
            [{"provider": "mistral", "min": 5, "avg": 10, "median": 8, "p95": 33, "max": 69}], t
        ),
        lambda t: charts.trend_chart_svg(
            ["06/03", "06/05"], {"gemini": [1.0, 2.0]}, t, label="x", fmt_y=lambda v: f"{v:.1f}s"
        ),
    ]
    for build in builders:
        svg_light, svg_dark = build(light), build(dark)
        assert svg_light.startswith("<svg") and svg_light.rstrip().endswith("</svg>")
        assert svg_light != svg_dark, "light and dark variants must differ (theme tokens applied)"
        # Theme surface tokens must actually appear in the right variant.
        assert light.text in svg_light
        assert dark.text in svg_dark


def test_score_color_interpolates_green_to_red():
    assert score_color(1.0) == "#2da44e"  # reference anchor: gemini at 100%
    # Low pass rates land on the reference red-orange (±1 per channel from rounding).
    r, g, b = (int(score_color(0.87)[i : i + 2], 16) for i in (1, 3, 5))
    assert (r, g, b) == (0xE0, 0x68, 0x43) or (r, g, b) == (0xE0, 0x69, 0x43)
    # Midrange lands in amber territory (red channel still substantial).
    assert int(score_color(0.94)[1:3], 16) > 150


def test_scorecard_full_bar_lands_on_the_100pct_gridline():
    svg = charts.scorecard_svg([{"provider": "gemini", "pass_pct": 100.0, "fails": 0}], THEMES["light"])
    # 100% gridline sits at x=600 and a 100% fill bar reaches the same x (track x=132 + width 468).
    assert 'width="468"' in svg
    assert ">clean<" in svg  # zero-fail providers are tagged clean


def test_provider_color_falls_back_for_unknown_provider():
    assert charts.provider_color("gemini") == "#2DA98C"
    assert charts.provider_color("nonesuch") == "#8b949e"
