# Copyright 2026 The Project Contributors
# SPDX-License-Identifier: MIT
"""Lightweight SVG chart generator — standard-library only, no matplotlib/pygal.

Each function returns a complete ``<svg …>…</svg>`` string suitable for writing to a ``.svg`` file or
embedding inline.  All charts use ``viewBox`` for responsive sizing.
"""

from __future__ import annotations

import html

DEFAULT_COLORS = ["#4CAF50", "#2196F3", "#FF9800", "#E91E63", "#9C27B0", "#00BCD4"]

_FONT = "system-ui, -apple-system, sans-serif"


# ---------------------------------------------------------------------------
# Sparkline
# ---------------------------------------------------------------------------


def sparkline_svg(
    values: list[float],
    width: int = 80,
    height: int = 16,
    color: str = "#4CAF50",
) -> str:
    """Tiny inline sparkline — a polyline with no axes or labels."""
    if not values:
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}"></svg>'

    lo, hi = min(values), max(values)
    span = hi - lo if hi != lo else 1.0
    n = len(values)
    step = width / max(n - 1, 1)
    pad = 1  # 1 px vertical pad so the line doesn't clip at the edges

    points = " ".join(
        f"{i * step:.1f},{pad + (height - 2 * pad) * (1 - (v - lo) / span):.1f}" for i, v in enumerate(values)
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}">'
        f'<polyline fill="none" stroke="{color}" stroke-width="1.5" points="{points}"/>'
        f"</svg>"
    )


# ---------------------------------------------------------------------------
# Bar chart
# ---------------------------------------------------------------------------


def bar_chart_svg(
    labels: list[str],
    values: list[float],
    title: str,
    width: int = 600,
    height: int = 300,
    colors: list[str] | None = None,
) -> str:
    """Simple vertical bar chart with axis labels."""
    colors = colors or DEFAULT_COLORS
    if not values:
        return _empty_svg(title, width, height)

    margin = {"top": 40, "right": 20, "bottom": 60, "left": 60}
    plot_w = width - margin["left"] - margin["right"]
    plot_h = height - margin["top"] - margin["bottom"]
    max_val = max(values) or 1.0
    bar_w = plot_w / max(len(values), 1) * 0.7
    gap = plot_w / max(len(values), 1) * 0.3

    parts: list[str] = [_svg_open(title, width, height)]

    # Title
    parts.append(
        f'<text x="{width / 2}" y="24" text-anchor="middle" '
        f'font-family="{_FONT}" font-size="14" font-weight="600" fill="#333">'
        f"{html.escape(title)}</text>"
    )

    # Bars
    for i, (lbl, val) in enumerate(zip(labels, values, strict=False)):
        bh = (val / max_val) * plot_h
        x = margin["left"] + i * (bar_w + gap) + gap / 2
        y = margin["top"] + plot_h - bh
        c = colors[i % len(colors)]
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{bh:.1f}" fill="{c}"/>')
        # Value label above bar
        parts.append(
            f'<text x="{x + bar_w / 2:.1f}" y="{y - 4:.1f}" text-anchor="middle" '
            f'font-family="{_FONT}" font-size="10" fill="#555">{_fmt(val)}</text>'
        )
        # X-axis label
        parts.append(
            f'<text x="{x + bar_w / 2:.1f}" y="{height - margin["bottom"] + 16:.1f}" '
            f'text-anchor="middle" font-family="{_FONT}" font-size="10" fill="#666">'
            f"{html.escape(str(lbl))}</text>"
        )

    # X-axis line
    parts.append(
        f'<line x1="{margin["left"]}" y1="{margin["top"] + plot_h}" '
        f'x2="{width - margin["right"]}" y2="{margin["top"] + plot_h}" '
        f'stroke="#ccc" stroke-width="1"/>'
    )

    parts.append("</svg>")
    return "".join(parts)


# ---------------------------------------------------------------------------
# Line chart (multi-series)
# ---------------------------------------------------------------------------


def line_chart_svg(
    series: dict[str, list[tuple[str, float]]],
    title: str,
    width: int = 600,
    height: int = 300,
) -> str:
    """Multi-series line chart.  *series* maps a series name to ``[(label, value), …]``."""
    if not series or all(not pts for pts in series.values()):
        return _empty_svg(title, width, height)

    margin = {"top": 40, "right": 120, "bottom": 60, "left": 60}
    plot_w = width - margin["left"] - margin["right"]
    plot_h = height - margin["top"] - margin["bottom"]

    all_vals = [v for pts in series.values() for _, v in pts]
    lo, hi = min(all_vals), max(all_vals)
    span = hi - lo if hi != lo else 1.0

    # Collect unique x-labels in order of first appearance.
    x_labels: list[str] = []
    seen: set[str] = set()
    for pts in series.values():
        for lbl, _ in pts:
            if lbl not in seen:
                x_labels.append(lbl)
                seen.add(lbl)

    x_step = plot_w / max(len(x_labels) - 1, 1)
    x_idx = {lbl: i for i, lbl in enumerate(x_labels)}

    parts: list[str] = [_svg_open(title, width, height)]

    # Title
    parts.append(
        f'<text x="{width / 2}" y="24" text-anchor="middle" '
        f'font-family="{_FONT}" font-size="14" font-weight="600" fill="#333">'
        f"{html.escape(title)}</text>"
    )

    # Grid lines (3 horizontal)
    for frac in (0, 0.5, 1.0):
        gy = margin["top"] + plot_h * (1 - frac)
        gv = lo + span * frac
        parts.append(
            f'<line x1="{margin["left"]}" y1="{gy:.1f}" '
            f'x2="{margin["left"] + plot_w}" y2="{gy:.1f}" stroke="#eee" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{margin["left"] - 6}" y="{gy + 4:.1f}" text-anchor="end" '
            f'font-family="{_FONT}" font-size="9" fill="#999">{_fmt(gv)}</text>'
        )

    # Series
    for si, (name, pts) in enumerate(series.items()):
        c = DEFAULT_COLORS[si % len(DEFAULT_COLORS)]
        coords = []
        for lbl, val in pts:
            xi = margin["left"] + x_idx[lbl] * x_step
            yi = margin["top"] + plot_h * (1 - (val - lo) / span)
            coords.append(f"{xi:.1f},{yi:.1f}")
        if coords:
            parts.append(f'<polyline fill="none" stroke="{c}" stroke-width="2" points="{" ".join(coords)}"/>')
            # Dots
            for coord in coords:
                cx, cy = coord.split(",")
                parts.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="{c}"/>')
        # Legend entry
        ly = margin["top"] + 10 + si * 18
        lx = width - margin["right"] + 10
        parts.append(f'<rect x="{lx}" y="{ly - 6}" width="10" height="10" fill="{c}"/>')
        parts.append(
            f'<text x="{lx + 14}" y="{ly + 3}" font-family="{_FONT}" font-size="10" fill="#333">'
            f"{html.escape(name)}</text>"
        )

    # X-axis labels (show at most 10 to avoid overlap)
    step = max(1, len(x_labels) // 10)
    for i, lbl in enumerate(x_labels):
        if i % step != 0:
            continue
        lx = margin["left"] + i * x_step
        parts.append(
            f'<text x="{lx:.1f}" y="{height - margin["bottom"] + 16:.1f}" '
            f'text-anchor="middle" font-family="{_FONT}" font-size="9" fill="#666">'
            f"{html.escape(lbl)}</text>"
        )

    parts.append("</svg>")
    return "".join(parts)


# ---------------------------------------------------------------------------
# Stacked bar chart
# ---------------------------------------------------------------------------


def stacked_bar_svg(
    labels: list[str],
    series: dict[str, list[float]],
    title: str,
    width: int = 600,
    height: int = 300,
) -> str:
    """Stacked vertical bar chart.  *series* maps series name → list of values (one per label)."""
    if not labels or not series:
        return _empty_svg(title, width, height)

    margin = {"top": 40, "right": 120, "bottom": 60, "left": 60}
    plot_w = width - margin["left"] - margin["right"]
    plot_h = height - margin["top"] - margin["bottom"]

    # Compute totals per bar for scaling.
    totals = [sum(vals[i] for vals in series.values()) for i in range(len(labels))]
    max_total = max(totals) if totals else 1.0
    if max_total == 0:
        max_total = 1.0

    bar_w = plot_w / max(len(labels), 1) * 0.7
    gap = plot_w / max(len(labels), 1) * 0.3

    parts: list[str] = [_svg_open(title, width, height)]

    # Title
    parts.append(
        f'<text x="{width / 2}" y="24" text-anchor="middle" '
        f'font-family="{_FONT}" font-size="14" font-weight="600" fill="#333">'
        f"{html.escape(title)}</text>"
    )

    # Bars — bottom-up stacking
    for i, lbl in enumerate(labels):
        x = margin["left"] + i * (bar_w + gap) + gap / 2
        cum_h = 0.0
        for si, vals in enumerate(series.values()):
            val = vals[i] if i < len(vals) else 0.0
            bh = (val / max_total) * plot_h
            y = margin["top"] + plot_h - cum_h - bh
            c = DEFAULT_COLORS[si % len(DEFAULT_COLORS)]
            parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{bh:.1f}" fill="{c}"/>')
            cum_h += bh
        # X-axis label
        parts.append(
            f'<text x="{x + bar_w / 2:.1f}" y="{height - margin["bottom"] + 16:.1f}" '
            f'text-anchor="middle" font-family="{_FONT}" font-size="10" fill="#666">'
            f"{html.escape(str(lbl))}</text>"
        )

    # Legend
    for si, sname in enumerate(series):
        c = DEFAULT_COLORS[si % len(DEFAULT_COLORS)]
        ly = margin["top"] + 10 + si * 18
        lx = width - margin["right"] + 10
        parts.append(f'<rect x="{lx}" y="{ly - 6}" width="10" height="10" fill="{c}"/>')
        parts.append(
            f'<text x="{lx + 14}" y="{ly + 3}" font-family="{_FONT}" font-size="10" fill="#333">'
            f"{html.escape(sname)}</text>"
        )

    # X-axis line
    parts.append(
        f'<line x1="{margin["left"]}" y1="{margin["top"] + plot_h}" '
        f'x2="{width - margin["right"]}" y2="{margin["top"] + plot_h}" '
        f'stroke="#ccc" stroke-width="1"/>'
    )

    parts.append("</svg>")
    return "".join(parts)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _svg_open(title: str, width: int, height: int) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" role="img" '
        f'aria-label="{html.escape(title)}">'
    )


def _empty_svg(title: str, width: int, height: int) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}">'
        f'<text x="{width / 2}" y="{height / 2}" text-anchor="middle" '
        f'font-family="{_FONT}" font-size="12" fill="#999">No data</text>'
        f"</svg>"
    )


def _fmt(v: float) -> str:
    """Format a number concisely: drop trailing zeros, keep ≤4 significant digits."""
    if v == int(v):
        return str(int(v))
    return f"{v:.4g}"
