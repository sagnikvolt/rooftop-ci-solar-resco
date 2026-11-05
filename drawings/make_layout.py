"""Roof layout drawing: writes layout.dxf (for CAD) and layout.png (for the site).

How this works:
  - The geometry comes from survey/roof_data.json and design/sizing.py, the same numbers
    used everywhere else, so the drawing cannot drift from the design.
  - Each slope is drawn as a 60 m x 20 m rectangle (ridge on the middle line, east slope
    below it, west slope above it). The ridge really runs north-south; the drawing is
    rotated so it reads left to right.
  - Modules are placed row by row starting at the ridge, bay by bay (a bay is the
    stretch of roof between skylight strips), until the design count for that slope is
    reached (272 = 16 strings x 17 modules). Strings are numbered in that placement
    order, so the string grouping is INDICATIVE: the real wiring route is decided on site.
  - The slope is drawn at its true length along the slope (20 m). The 7 degree tilt
    makes the plan length only 0.7 % shorter, which is ignored here.
"""
import json
import os
import sys

import ezdxf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "design"))
from equipment import MODULE          # noqa: E402
import sizing                         # noqa: E402

ROOF = json.load(open(os.path.join(HERE, "..", "survey", "roof_data.json")))
D = sizing.design()

RIDGE = ROOF["ridge_length_m"]
SLOPE = ROOF["slope_length_m"]
GABLE = ROOF["edge_setback_gable_m"]
EAVE = ROOF["edge_setback_eave_m"]
RIDGE_SB = ROOF["ridge_setback_m"]
MW, ML = MODULE["width_m"], MODULE["length_m"]     # portrait: width along ridge, length up slope
GAP = sizing.MODULE_GAP_M
MODS_PER_SLOPE = D["n_modules"] // 2
PER_STRING = D["modules_per_string"]


def bays():
    """x ranges (along the ridge) of the three bays and the skylight strips between them."""
    keep = ROOF["translucent_keepout_each_side_m"]
    sw = ROOF["translucent_strip_width_m"]
    n = ROOF["translucent_strips_per_slope"]
    usable = RIDGE - 2 * GABLE
    bay_w = (usable - n * (sw + 2 * keep)) / (n + 1)
    out, strips, x = [], [], GABLE
    for i in range(n + 1):
        out.append((x, x + bay_w))
        x += bay_w
        if i < n:
            strips.append((x + keep, x + keep + sw))
            x += sw + 2 * keep
    return out, strips


def place_modules():
    """Return a list of (x, y_from_ridge, string_no) for ONE slope. y is measured away from the ridge."""
    bay_list, _ = bays()
    rows = D["rows_per_slope"]
    mods = []
    for r in range(rows):
        y0 = RIDGE_SB + r * (ML + GAP)
        for (bx0, bx1) in bay_list:
            k = int((bx1 - bx0) // (MW + GAP))
            for c in range(k):
                mods.append((bx0 + c * (MW + GAP), y0))
    mods = mods[:MODS_PER_SLOPE]
    return [(x, y, i // PER_STRING + 1) for i, (x, y) in enumerate(mods)], len(mods)


def draw_png(path):
    mods, n = place_modules()
    bay_list, strips = bays()
    cmap = plt.get_cmap("hsv")
    fig, ax = plt.subplots(figsize=(15, 6.5))
    for name, sign in (("East slope (azimuth 90°)", -1), ("West slope (azimuth 270°)", 1)):
        # slope outline
        ax.add_patch(Rectangle((0, 0 if sign > 0 else -SLOPE), RIDGE, SLOPE, fill=False, ec="black", lw=1.5))
        # setback zone (hatched border)
        ax.add_patch(Rectangle((GABLE, (RIDGE_SB if sign > 0 else -(SLOPE - EAVE))),
                               RIDGE - 2 * GABLE, SLOPE - EAVE - RIDGE_SB,
                               fill=False, ec="grey", lw=0.8, ls="--"))
        for (sx0, sx1) in strips:                       # skylight strips and their keepout
            ax.add_patch(Rectangle((sx0, 0 if sign > 0 else -SLOPE), sx1 - sx0, SLOPE,
                                   fc="#9ad0ec", ec="#2a7ab0", lw=0.6, zorder=2))
        for x, y, s in mods:
            ytop = y if sign > 0 else -(y + ML)
            ax.add_patch(Rectangle((x, ytop), MW, ML, fc=cmap(((s - 1) * 5 % 16) / 16.0 * 0.9), ec="black", lw=0.15, zorder=3))
        ax.text(RIDGE / 2, (SLOPE + 1.2) if sign > 0 else -(SLOPE + 2.2), name, ha="center", fontsize=11, weight="bold")
    ax.axhline(0, color="black", lw=2)
    ax.text(RIDGE + 0.5, 0, "Ridge", va="center", fontsize=9)
    ax.text(RIDGE + 0.5, SLOPE - 1, "Eave", va="center", fontsize=9)
    ax.text(RIDGE + 0.5, -SLOPE + 1, "Eave", va="center", fontsize=9)
    ax.set_xlim(-2, RIDGE + 5)
    ax.set_ylim(-SLOPE - 4, SLOPE + 4)
    ax.set_aspect("equal")
    ax.set_xlabel("Along the ridge (m). Ridge runs north-south; drawing rotated to read left to right")
    ax.set_ylabel("Distance from ridge along the slope (m)")
    fig.suptitle(f"Roof layout: {D['n_modules']} modules, {D['dc_kwp']:.1f} kWp "
                 f"({MODS_PER_SLOPE} per slope = {D['n_strings']//2} strings x {PER_STRING}). "
                 "Colours = strings (indicative grouping).\nBlue = skylight strips with keepout. Dashed = setback line. "
                 "Empty roof = 88 spare positions per slope (kept free for access and future expansion).",
                 fontsize=10)
    fig.tight_layout()
    fig.savefig(path, dpi=130, bbox_inches="tight")
    plt.close(fig)


def draw_dxf(path):
    mods, n = place_modules()
    bay_list, strips = bays()
    doc = ezdxf.new("R2010")
    doc.units = ezdxf.units.M
    for name, color in (("ROOF", 7), ("SETBACK", 8), ("SKYLIGHT", 5), ("MODULES", 3), ("TEXT", 7)):
        doc.layers.add(name, color=color)
    msp = doc.modelspace()
    for slope, sign in (("EAST SLOPE", -1), ("WEST SLOPE", 1)):
        y0 = 0 if sign > 0 else -SLOPE
        msp.add_lwpolyline([(0, y0), (RIDGE, y0), (RIDGE, y0 + SLOPE), (0, y0 + SLOPE)],
                           close=True, dxfattribs={"layer": "ROOF"})
        sy0 = RIDGE_SB if sign > 0 else -(SLOPE - EAVE)
        msp.add_lwpolyline([(GABLE, sy0), (RIDGE - GABLE, sy0),
                            (RIDGE - GABLE, sy0 + SLOPE - EAVE - RIDGE_SB), (GABLE, sy0 + SLOPE - EAVE - RIDGE_SB)],
                           close=True, dxfattribs={"layer": "SETBACK", "linetype": "CONTINUOUS"})
        for sx0, sx1 in strips:
            msp.add_lwpolyline([(sx0, y0), (sx1, y0), (sx1, y0 + SLOPE), (sx0, y0 + SLOPE)],
                               close=True, dxfattribs={"layer": "SKYLIGHT"})
        for x, y, s in mods:
            yt = y if sign > 0 else -(y + ML)
            msp.add_lwpolyline([(x, yt), (x + MW, yt), (x + MW, yt + ML), (x, yt + ML)],
                               close=True, dxfattribs={"layer": "MODULES"})
        msp.add_text(slope, height=1.0, dxfattribs={"layer": "TEXT"}).set_placement(
            (RIDGE / 2 - 5, SLOPE + 1.5 if sign > 0 else -SLOPE - 2.5))
    msp.add_line((0, 0), (RIDGE, 0), dxfattribs={"layer": "ROOF", "lineweight": 50})
    doc.saveas(path)


if __name__ == "__main__":
    mods, n = place_modules()
    print(f"modules placed per slope: {n} (design: {MODS_PER_SLOPE}); roof capacity per slope: "
          f"{D['roof_modules'] // 2}; spare positions: {D['roof_modules'] // 2 - n}")
    draw_png(os.path.join(HERE, "layout.png"))
    draw_dxf(os.path.join(HERE, "layout.dxf"))
    print("wrote drawings/layout.png and drawings/layout.dxf")
