# Copyright 2026 The Project Contributors
# SPDX-License-Identifier: MIT
"""Hand-built SVG charts for the Smoke Health dashboard — standard-library only.

Every chart is authored on a 760-wide canvas (matching the ``<img width="760">`` in the markdown) using
GitHub's own Primer palette, so the committed SVGs read correctly inside a GitHub README. Charts carry no
scripts or embedded fonts (GitHub strips both from ``<img>``-loaded SVG); theming is done by emitting a
*light* and a *dark* variant of every chart and selecting between them with a ``<picture>`` block.

Each public ``*_svg`` function takes already-aggregated data plus a :class:`Theme` and returns a complete
``<svg …>…</svg>`` string. The geometry mirrors the design reference so the same data reproduces the
reference pixels; with live data the same code lays out structurally-identical charts.
"""

from __future__ import annotations

import html
from dataclasses import dataclass

# System fonts only — GitHub sanitizes @font-face / web fonts out of <img>-loaded SVG.
_SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif"
_MONO = "ui-monospace,SFMono-Regular,Menlo,monospace"


@dataclass(frozen=True)
class Theme:
    """The handful of surface/text tokens that flip between GitHub's light and dark color schemes.

    Outcome colors (pass green, fail red, warn amber) and the categorical provider hues are *not* here:
    the reference uses the same saturated values on both backgrounds, so they live as module constants.
    """

    name: str
    text: str  # strong body text
    muted: str  # labels, axis ticks
    grid: str  # hairlines, dividers, gridlines
    track: str  # unfilled bar track
    inset: str  # canvas-inset fill (e.g. the hollow avg diamond)


THEMES: dict[str, Theme] = {
    "light": Theme(
        "light", text="#1f2328", muted="#656d76", grid="#d8dee4", track="#eaeef2", inset="#f6f8fa"
    ),
    "dark": Theme("dark", text="#e6edf3", muted="#8b949e", grid="#30363d", track="#21262d", inset="#161b22"),
}

# Outcome semantics — identical across themes (these are the summary accents and failure-split fills).
_PASS = "#2DA44E"
_FAIL = "#E5534B"
_WARN = "#D4A72C"

# Failure-category fills.
_CAT_COLORS = {"classification": "#E5534B", "deterministic": "#E0A53B", "infra": "#A371F7"}
# Token pipeline stages.
_READINESS = "#7C8BA5"
_EXTRACTION = "#6E6BE8"

# Categorical provider hues for the multi-series charts (latency / cost / efficiency). Distinct,
# none pure green/red (reserved for outcome), legible on both #ffffff and #0d1117.
PROVIDER_COLORS: dict[str, str] = {
    "anthropic": "#E8835A",
    "deepseek": "#6366F1",
    "gemini": "#2DA98C",
    "llama": "#A371F7",
    "mistral": "#F0A23B",
    "openai": "#1F9CF0",
}
_FALLBACK_PROVIDER = "#8b949e"


def provider_color(provider: str) -> str:
    return PROVIDER_COLORS.get(provider, _FALLBACK_PROVIDER)


# Pass-rate → bar fill, interpolated green→amber→red. Anchors are read off the reference scorecard
# (gemini #2da44e at 100%, deepseek #e06943 at 87%), so the interpolation reproduces it closely.
_SCORE_STOPS: list[tuple[float, tuple[int, int, int]]] = [
    (0.00, (0xE5, 0x53, 0x4B)),
    (0.90, (0xE0, 0x69, 0x43)),
    (0.94, (0xC0, 0xA7, 0x30)),
    (0.97, (0x67, 0xA5, 0x42)),
    (1.00, (0x2D, 0xA4, 0x4E)),
]


def score_color(fraction: float) -> str:
    """Interpolate the scorecard bar color for a pass-rate fraction in [0, 1]."""
    f = max(0.0, min(1.0, fraction))
    lo = _SCORE_STOPS[0]
    if f <= lo[0]:
        return _rgb(lo[1])
    for (a0, c0), (a1, c1) in zip(_SCORE_STOPS, _SCORE_STOPS[1:], strict=False):
        if f <= a1:
            k = (f - a0) / (a1 - a0)
            return _rgb(tuple(round(c0[i] + (c1[i] - c0[i]) * k) for i in range(3)))
    return _rgb(_SCORE_STOPS[-1][1])


# ---------------------------------------------------------------------------
# Low-level SVG element helpers
# ---------------------------------------------------------------------------


def _rgb(c: tuple[int, ...]) -> str:
    return f"#{c[0]:02x}{c[1]:02x}{c[2]:02x}"


def _esc(s: object) -> str:
    return html.escape(str(s), quote=False)


def _num(v: float) -> str:
    """Compact coordinate string: integers stay integers, else two decimals (trailing zeros trimmed)."""
    if v == int(v):
        return str(int(v))
    return f"{v:.2f}".rstrip("0").rstrip(".")


def _svg_open(width: int, height: int, label: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" role="img" aria-label="{html.escape(label)}" '
        f'font-family="{_SANS}">'
    )


def _text(x, y, size, content, *, fill, weight=400, anchor="start", mono=False, ls=None) -> str:
    attrs = (
        f'<text x="{_num(x)}" y="{_num(y)}" font-size="{size}" font-weight="{weight}" '
        f'text-anchor="{anchor}" fill="{fill}"'
    )
    if mono:
        attrs += f' font-family="{_MONO}"'
    if ls is not None:
        attrs += f' letter-spacing="{ls}"'
    return f"{attrs}>{content}</text>"


def _rect(x, y, w, h, fill, *, rx=None) -> str:
    r = f' rx="{rx}"' if rx is not None else ""
    return f'<rect x="{_num(x)}" y="{_num(y)}" width="{_num(w)}" height="{_num(h)}"{r} fill="{fill}"></rect>'


def _line(x1, y1, x2, y2, stroke, *, width=1, dash=None, cap=None, opacity=None) -> str:
    extra = ""
    if dash is not None:
        extra += f' stroke-dasharray="{dash}"'
    if cap is not None:
        extra += f' stroke-linecap="{cap}"'
    if opacity is not None:
        extra += f' opacity="{opacity}"'
    return (
        f'<line x1="{_num(x1)}" y1="{_num(y1)}" x2="{_num(x2)}" y2="{_num(y2)}" '
        f'stroke="{stroke}" stroke-width="{width}"{extra}></line>'
    )


def tokens_label(total_tokens: float) -> str:
    """Format a token total like the reference scorecard table: millions to two decimals (``7.25M``)."""
    return f"{total_tokens / 1e6:.2f}M"


# ---------------------------------------------------------------------------
# 1. Summary banner
# ---------------------------------------------------------------------------


def summary_banner_svg(providers: int, avg_pass: float, total_fails: int, flaky: int, theme: Theme) -> str:
    """Four stat cells (providers · avg pass · total failures · flaky tests) separated by hairlines."""
    cells = [
        (str(providers), "PROVIDERS", theme.text),
        (f"{avg_pass:.1f}%", "AVG PASS RATE", _PASS),
        (str(total_fails), "TOTAL FAILURES", _FAIL),
        (str(flaky), "FLAKY TESTS", _WARN),
    ]
    xs = [24, 214, 404, 594]
    dividers = [190, 380, 570]
    p = [_svg_open(760, 124, "Smoke health summary")]
    for i, (number, label, color) in enumerate(cells):
        x = xs[i]
        if i > 0:
            dx = dividers[i - 1]
            p.append(_line(dx, 24, dx, 104, theme.grid))
        p.append(_rect(x, 40, 22, 3, color, rx=1.5))
        p.append(_text(x, 82, 34, _esc(number), fill=color, weight=700))
        p.append(_text(x, 104, 11, label, fill=theme.muted, ls=0.6))
    p.append("</svg>")
    return "".join(p)


# ---------------------------------------------------------------------------
# 2. Provider scorecard (horizontal pass-rate bars)
# ---------------------------------------------------------------------------


def scorecard_svg(rows: list[dict], theme: Theme) -> str:
    """One horizontal bar per provider, sorted by pass rate desc. *rows*: {provider, pass_pct, fails}.

    The x-axis is magnified to 90–100% via the dashed gridlines while bars run a true 0–100% track, so
    a 100% bar lands exactly on the 100% gridline and the spread between providers reads clearly.
    """
    track_x, track_w = 132, 468
    first_y, row_h, bar_h = 31, 38, 12
    n = len(rows)
    grid_bottom = first_y + (n - 1) * row_h + bar_h + 7
    p = [_svg_open(760, grid_bottom + 16, "Pass rate by provider")]

    def gx(pct: float) -> float:  # 90→553.2, 100→600 (4.68 px per percent)
        return track_x + track_w + (pct - 100.0) * (track_w / 100.0)

    for pct in (90, 95, 100):
        x = gx(pct)
        p.append(_line(x, 14, x, grid_bottom, theme.grid, dash="2 4"))
        p.append(_text(x, 10, 9, f"{pct}%", fill=theme.muted, anchor="middle"))

    for i, r in enumerate(rows):
        y = first_y + i * row_h
        pct = float(r["pass_pct"] or 0)
        fails = int(r["fails"] or 0)
        p.append(_text(8, y + 10, 13, _esc(r["provider"]), fill=theme.text, weight=600))
        p.append(_rect(track_x, y, track_w, bar_h, theme.track, rx=6))
        p.append(_rect(track_x, y, track_w * pct / 100.0, bar_h, score_color(pct / 100.0), rx=6))
        p.append(_text(614, y + 10, 12.5, f"{pct:.1f}%", fill=theme.text, weight=700, mono=True))
        if fails == 0:
            p.append(_text(692, y + 10, 11, "clean", fill=_PASS))
        else:
            p.append(_text(692, y + 10, 11, f"{fails} fails", fill=theme.muted))
    p.append("</svg>")
    return "".join(p)


# ---------------------------------------------------------------------------
# 3 & 5. Trend line charts (latency, cost) — shared engine
# ---------------------------------------------------------------------------


def trend_chart_svg(x_labels, series, theme, *, label, fmt_y) -> str:
    """Multi-series line chart over a shared run axis.

    *x_labels* is one date label per run (oldest→newest); *series* maps provider → values aligned to
    those runs (``None`` where a provider didn't run). *fmt_y* formats an axis value (seconds, dollars).
    """
    pad_l, plot_r, top, bottom = 56, 642, 22, 306
    n = len(x_labels)
    vals = [v for pts in series.values() for v in pts if v is not None]
    axis_max = (max(vals) * 1.12) if vals else 1.0
    if axis_max <= 0:
        axis_max = 1.0

    def x_of(i: int) -> float:
        return pad_l + (plot_r - pad_l) * (i / (n - 1) if n > 1 else 0.5)

    def y_of(v: float) -> float:
        return bottom - (v / axis_max) * (bottom - top)

    p = [_svg_open(760, 348, label)]
    for frac in (0.0, 0.25, 0.5, 0.75, 1.0):
        gy = bottom - frac * (bottom - top)
        p.append(_line(pad_l, gy, plot_r, gy, theme.grid))
        p.append(
            _text(pad_l - 10, gy + 4, 9.5, fmt_y(axis_max * frac), fill=theme.muted, anchor="end", mono=True)
        )

    stride = max(1, (n + 11) // 12)  # thin labels out if there are many runs
    for i, lbl in enumerate(x_labels):
        if i % stride and i != n - 1:
            continue
        p.append(_text(x_of(i), 324, 9.5, _esc(lbl), fill=theme.muted, anchor="middle", mono=True))

    for name in sorted(series):  # alphabetical so the legend order is stable
        c = provider_color(name)
        pts = [(x_of(i), y_of(v)) for i, v in enumerate(series[name]) if v is not None]
        if not pts:
            continue
        coords = " ".join(f"{_num(x)},{_num(y)}" for x, y in pts)
        p.append(
            f'<polyline fill="none" stroke="{c}" stroke-width="2.4" stroke-linejoin="round" '
            f'stroke-linecap="round" points="{coords}"></polyline>'
        )
        for x, y in pts:
            p.append(f'<circle cx="{_num(x)}" cy="{_num(y)}" r="2.6" fill="{c}"></circle>')

    for k, name in enumerate(sorted(series)):
        ly = 27 + k * 20
        c = provider_color(name)
        p.append(_line(656, ly, 672, ly, c, width=3, cap="round"))
        p.append(_text(678, ly + 3, 11, _esc(name), fill=theme.text))
    p.append("</svg>")
    return "".join(p)


# ---------------------------------------------------------------------------
# 4. Token split (readiness vs extraction), width ∝ total tokens
# ---------------------------------------------------------------------------


def token_split_svg(rows: list[dict], theme: Theme) -> str:
    """Horizontal split bar per provider. *rows*: {provider, readiness, extraction}, sorted by total desc.

    Bar length encodes total tokens (so volume is comparable across providers); the readiness/extraction
    split is the colored segments, with the extraction share labelled inside its segment.
    """
    first_y, row_h, bar_h = 51, 34, 16
    bar_x, max_w = 110, 514
    n = len(rows)
    max_total = max((r["readiness"] + r["extraction"]) for r in rows) or 1

    p = [_svg_open(760, first_y + (n - 1) * row_h + bar_h + 17, "Token split readiness vs extraction")]
    p.append(_rect(110, 18, 11, 11, _READINESS, rx=2.5))
    p.append(_text(127, 28, 11, "Readiness (assessment)", fill=theme.muted))
    p.append(_rect(300, 18, 11, 11, _EXTRACTION, rx=2.5))
    p.append(_text(317, 28, 11, "Extraction (contract)", fill=theme.muted))

    for i, r in enumerate(rows):
        y = first_y + i * row_h
        ready, extr = r["readiness"], r["extraction"]
        total = ready + extr
        rw = max_w * ready / max_total
        ew = max_w * extr / max_total
        p.append(_text(8, y + 12, 12.5, _esc(r["provider"]), fill=theme.text, weight=600))
        p.append(_rect(bar_x, y, rw, bar_h, _READINESS, rx=3))
        p.append(_rect(bar_x + rw, y, ew, bar_h, _EXTRACTION, rx=3))
        if ew >= 22 and total:
            share = round(100 * extr / total)
            p.append(
                _text(
                    bar_x + rw + ew / 2, y + 12, 10.5, f"{share}%", fill="#fff", weight=600, anchor="middle"
                )
            )
        p.append(_text(636, y + 12, 11.5, f"{total / 1e6:.1f}M", fill=theme.text, weight=600, mono=True))
    p.append("</svg>")
    return "".join(p)


# ---------------------------------------------------------------------------
# 6. Failure categories (stacked per provider)
# ---------------------------------------------------------------------------


def failure_split_svg(rows: list[dict], theme: Theme) -> str:
    """Stacked failure bar per provider. *rows*: {provider, counts: {cat: n}, total}, sorted by total desc.

    Providers with zero failures render a green "clean run record" marker instead of a bar.
    """
    first_y, row_h, bar_h = 51, 34, 16
    bar_x, plot_w = 110, 450
    n = len(rows)
    max_total = max((r["total"] for r in rows), default=0) or 1
    scale = plot_w / max_total

    p = [_svg_open(760, first_y + (n - 1) * row_h + bar_h + 17, "Failure categories by provider")]
    for cat, lx in {"classification": 110, "deterministic": 246.4, "infra": 376.2}.items():
        p.append(_rect(lx, 18, 11, 11, _CAT_COLORS[cat], rx=2.5))
        p.append(_text(lx + 17, 28, 11, cat, fill=theme.muted))

    for i, r in enumerate(rows):
        y = first_y + i * row_h
        total = int(r["total"])
        p.append(_text(8, y + 12, 12.5, _esc(r["provider"]), fill=theme.text, weight=600))
        if total == 0:
            p.append(_rect(110, y, 18, bar_h, _PASS, rx=4))
            p.append(_text(136, y + 12, 11.5, "0 — clean run record", fill=_PASS, weight=600))
            continue
        cur = bar_x
        for cat in ("classification", "deterministic", "infra"):
            count = int(r["counts"].get(cat, 0))
            if not count:
                continue
            seg_w = count * scale
            p.append(_rect(cur, y, seg_w, bar_h, _CAT_COLORS[cat], rx=3))
            p.append(_text(cur + seg_w / 2, y + 12, 10.5, count, fill="#fff", weight=700, anchor="middle"))
            cur += seg_w + 2
        p.append(_text(cur + 8, y + 12, 11, f"{total} fails", fill=theme.muted))
    p.append("</svg>")
    return "".join(p)


# ---------------------------------------------------------------------------
# 7. LLM efficiency (min→p95 range per provider)
# ---------------------------------------------------------------------------


def llm_efficiency_svg(rows: list[dict], theme: Theme) -> str:
    """One row per provider, sorted by avg desc. *rows*: {provider, min, avg, median, p95, max}.

    Each row draws a faint min→p95 range bar with a median dot, an avg diamond and a p95 tick; an
    off-axis max (a retry/tool-loop storm) is annotated with a ``max N`` label.
    """
    pad_l, plot_r = 110, 642
    first_c, row_h = 65, 34
    n = len(rows)
    grid_bottom = first_c + (n - 1) * row_h + 9
    label_y = grid_bottom + 30

    max_p95 = max((float(r["p95"] or 0) for r in rows), default=0)
    span = max_p95 if max_p95 > 0 else 1.0
    scale = (572 - pad_l) / span  # widest p95 lands at ~x=572, leaving a gutter for the max label

    def x_of(v: float) -> float:
        return pad_l + scale * v

    p = [_svg_open(760, label_y + 12, "LLM calls per test by provider")]
    p.append(f'<circle cx="116" cy="24" r="4" fill="{theme.text}"></circle>')
    p.append(_text(126, 28, 11, "median", fill=theme.muted))
    p.append(
        f'<path d="M206 20 l5 5 -5 5 -5 -5 z" fill="none" stroke="{theme.text}" stroke-width="1.6"></path>'
    )
    p.append(_text(216, 28, 11, "avg", fill=theme.muted))
    p.append(_line(286, 19, 286, 29, theme.text, width=2))
    p.append(_text(294, 28, 11, "p95", fill=theme.muted))
    p.append(_text(360, 28, 11, "bar = min → p95", fill=theme.muted))

    grid_max = int(max_p95 // 10 * 10)
    for v in range(0, grid_max + 1, 10):
        gx = x_of(v)
        p.append(_line(gx, 42, gx, grid_bottom, theme.grid))
        p.append(_text(gx, label_y, 9.5, v, fill=theme.muted, anchor="middle", mono=True))

    for i, r in enumerate(rows):
        cy = first_c + i * row_h
        c = provider_color(r["provider"])
        vmin, vavg, vmed, vp95, vmax = (float(r[k] or 0) for k in ("min", "avg", "median", "p95", "max"))
        p.append(_text(8, cy + 4, 12.5, _esc(r["provider"]), fill=theme.text, weight=600))
        p.append(_line(x_of(vmin), cy, x_of(vp95), cy, c, width=5, cap="round", opacity=0.32))
        p.append(_line(x_of(vp95), cy - 6, x_of(vp95), cy + 6, c, width=2))
        diamond = f"M{_num(x_of(vavg))} {cy - 6} l6 6 -6 6 -6 -6 z"
        p.append(f'<path d="{diamond}" fill="{theme.inset}" stroke="{c}" stroke-width="1.8"></path>')
        p.append(f'<circle cx="{_num(x_of(vmed))}" cy="{cy}" r="4.5" fill="{c}"></circle>')
        if x_of(vmax) > plot_r - 46:  # max runs off the plotted range — call it out
            p.append(_text(610, cy + 4, 10.5, f"max {int(vmax)}", fill=theme.muted, mono=True))
    p.append("</svg>")
    return "".join(p)
