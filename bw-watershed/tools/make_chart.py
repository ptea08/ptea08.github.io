#!/usr/bin/env python3
"""Regenerate the two-panel results chart inside index.html.

The bar geometry is derived from ROWS rather than hand-written, so the chart
cannot drift out of step with the table beneath it. Edit ROWS and re-run:

    python3 tools/make_chart.py

Replaces the existing <svg class="chart">...</svg> in place. Stdlib only.
"""
import re
from pathlib import Path

# label, panoptic quality, over-segmentation ratio, is-ours
# Same rows, same order, as the results table in index.html.
ROWS = [
    ("MLP-S \u2192 UNet (ours)", 0.310, 1.76, True),
    ("No bootstrap (3 img)",     0.273, 1.66, False),
    ("RF \u2192 UNet",           0.263, 1.51, False),
    ("MLP-D \u2192 UNet",        0.247, 1.69, False),
    ("Mask2Former (ZS)",         0.171, 0.60, False),
    ("CellPose + RF",            0.102, 0.85, False),
    ("EcoTaxa",                  0.056, 1.24, False),
    ("StarDist + RF",            0.030, 4.79, False),
    ("StarDist (native)",        0.003, 2.85, False),
    ("CellPose (native)",        0.000, 0.26, False),
    ("Cellpose-SAM (ZS)",        0.000, 1.61, False),
]

LBL_X, ROW_H, BAR_H, Y0 = 162, 28, 14, 34

# `val` is the right edge of a dedicated value column. Values are not placed at
# the end of their bar: at OSR ~1 that put them on top of the dashed ideal line.
PQ  = dict(x=175, w=200, mx=0.35, val=410, ticks=(0, .1, .2, .3),      fmt="%.3f", tf="%.1f")
OSR = dict(x=450, w=190, mx=5.0,  val=690, ticks=(0, 1, 2, 3, 4, 5),   fmt="%.2f", tf="%d")

HEIGHT = Y0 + len(ROWS) * ROW_H + 15
GRID_TOP, GRID_BOT = Y0 - 2, Y0 + len(ROWS) * ROW_H


def build() -> str:
    out = []
    add = out.append
    add(
        f'<svg class="chart" viewBox="0 0 700 {HEIGHT}" role="img" aria-label="Panoptic '
        f'quality and over-segmentation ratio for every method in the results table. '
        f'Bootstrapped Watershed reaches the highest panoptic quality at 0.310, and '
        f'an over-segmentation ratio of 1.76 against an ideal of 1.">'
    )
    add(f'<text class="hd" x="{PQ["x"]}" y="14">PANOPTIC QUALITY</text>')
    add(f'<text class="hd" x="{OSR["x"]}" y="14">OVER-SEGMENTATION RATIO</text>')

    for panel in (PQ, OSR):
        for v in panel["ticks"]:
            x = panel["x"] + v / panel["mx"] * panel["w"]
            cls = "axis" if v == 0 else ("ideal" if (panel is OSR and v == 1) else "grid")
            add(f'<line class="{cls}" x1="{x:.1f}" y1="{GRID_TOP}" x2="{x:.1f}" y2="{GRID_BOT}"/>')
            add(f'<text class="tick" x="{x:.1f}" y="{GRID_TOP - 4}">{panel["tf"] % v}</text>')

    add(
        f'<text class="tick" x="{OSR["x"] + OSR["w"] / OSR["mx"]:.1f}" y="{GRID_BOT + 12}" '
        f'style="fill:var(--accent)">ideal</text>'
    )

    for i, (label, pq, osr, ours) in enumerate(ROWS):
        y = Y0 + i * ROW_H + (ROW_H - BAR_H) / 2
        baseline = y + BAR_H / 2 + 3.5
        add(f'<text class="lbl{" on" if ours else ""}" x="{LBL_X}" y="{baseline:.1f}">{label}</text>')
        for value, panel in ((pq, PQ), (osr, OSR)):
            width = value / panel["mx"] * panel["w"]
            if width > 0:
                add(
                    f'<rect class="bar{" ours" if ours else ""}" x="{panel["x"]}" '
                    f'y="{y:.1f}" width="{width:.1f}" height="{BAR_H}" rx="2"/>'
                )
            add(
                f'<text class="val{" on" if ours else ""}" x="{panel["val"]}" '
                f'y="{baseline:.1f}">{panel["fmt"] % value}</text>'
            )

    add("</svg>")
    return "\n      ".join(out)


def main() -> None:
    page = Path(__file__).resolve().parent.parent / "index.html"
    source = page.read_text()
    updated, count = re.subn(r'<svg class="chart".*?</svg>', lambda _: build(), source, flags=re.S)
    if count != 1:
        raise SystemExit(f"expected exactly one chart in {page}, found {count}")
    page.write_text(updated)
    print(f"{page.name}: chart regenerated, {len(ROWS)} rows, height {HEIGHT}")


if __name__ == "__main__":
    main()
