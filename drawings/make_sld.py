"""Single-line diagram (SLD) of the plant: writes sld.png and sld.svg.

How this works: boxes and lines are drawn with matplotlib from the design numbers
(design/sizing.py and design/ac_side.py). Reading the diagram from left to right follows
the energy: modules -> inverter -> AC breaker -> plant AC breaker -> client's LT bus ->
transformer -> HT side, where the net meter sits.
Items marked ASSUMED are sizes not yet checked by a full protection study.
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "design"))
import sizing      # noqa: E402
import ac_side     # noqa: E402

D = sizing.design()
A = ac_side.ac_side(D["n_inverters"])
PER_SLOPE = D["n_strings"] // 2


def box(ax, x, y, w, h, text, fc="#ffffff", fs=8):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02", fc=fc, ec="black", lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs)


def line(ax, x0, y0, x1, y1, lw=1.5, color="black"):
    ax.plot([x0, x1], [y0, y1], color=color, lw=lw, solid_capstyle="butt")


def build():
    fig, ax = plt.subplots(figsize=(16, 8.5))
    ax.set_xlim(0, 32)
    ax.set_ylim(0, 17)
    ax.axis("off")
    rows = [(11.2, "East slope", "Inverter 1"), (3.6, "West slope", "Inverter 2")]
    for y, slope, inv in rows:
        # PV array
        box(ax, 0.5, y, 5.4, 3.2,
            f"{slope} PV array\n{PER_SLOPE} strings x {D['modules_per_string']} modules\n"
            f"= {PER_SLOPE * D['modules_per_string']} x 565 Wp = {PER_SLOPE * D['modules_per_string'] * 0.565:.1f} kWp\n"
            "2 strings per MPPT, no string fuses\n(2 x Isc = 27.5 A < module 30 A fuse rating)",
            fc="#fff4cc", fs=7.5)
        line(ax, 5.9, y + 1.6, 8.0, y + 1.6)
        ax.text(6.95, y + 2.0, "DC PV cable\n(size to be calculated)", ha="center", fontsize=6.5)
        # inverter
        box(ax, 8.0, y + 0.2, 4.4, 2.8,
            f"{inv}\nSungrow SG110CX-P2\n110 kW / 110 kVA\nbuilt-in DC switch, DC SPD,\nanti-islanding", fc="#dff0ff", fs=7.5)
        line(ax, 12.4, y + 1.6, 14.4, y + 1.6)
        # AC breaker per inverter
        box(ax, 14.4, y + 0.9, 2.6, 1.4, f"MCCB {A['breaker_per_inverter_a']:.0f} A\n(ASSUMED:\n1.25 x {A['current_per_inverter_a']:.1f} A)", fs=7)
        line(ax, 17.0, y + 1.6, 18.6, y + 1.6)
        line(ax, 18.6, y + 1.6, 18.6, 8.7)
    # AC combiner bus
    line(ax, 18.6, 8.7, 20.0, 8.7)
    box(ax, 20.0, 7.6, 3.2, 2.2,
        f"Plant AC panel\nMain MCCB {A['breaker_main_a']:.0f} A\n(ASSUMED)\nAC SPD\n"
        "Generation meter", fc="#e6f4e6", fs=7.5)
    line(ax, 23.2, 8.7, 24.6, 8.7)
    box(ax, 24.6, 7.5, 3.2, 2.4, "Client LT bus (415 V)\nexisting main incomer\n+ new plant breaker", fs=7.5)
    line(ax, 26.2, 7.5, 26.2, 5.6)
    box(ax, 24.6, 3.6, 3.2, 2.0, "Client transformer\n11 kV / 415 V\n350 kVA (ASSUMED)", fs=7.5)
    line(ax, 26.2, 3.6, 26.2, 2.6)
    box(ax, 24.6, 0.6, 3.2, 2.0, "NET METER\n(utility, HT side)\nthen 11 kV supply", fc="#ffe0e0", fs=7.5)
    line(ax, 27.8, 1.6, 30.2, 1.6)
    ax.text(30.4, 1.6, "WBSEDCL\n11 kV line", va="center", fontsize=8, weight="bold")
    # earthing and notes
    box(ax, 0.5, 0.4, 14.0, 2.3,
        "Earthing: array frames and inverters bonded to the plant earth (IS 3043); lightning protection per site assessment.\n"
        "Anti-islanding and grid-support functions are in the inverter (WBSEDCL document, 'Responsibility' table).\n"
        "Net meter must be on the HT side of the transformer when an HT consumer connects at its LT bus\n"
        "(WBSEDCL procedures, 'Voltage level of connectivity').", fc="#f5f5f5", fs=7.2)
    fig.suptitle(f"Single-line diagram: {D['dc_kwp']:.1f} kWp rooftop plant, {D['n_inverters']} x 110 kVA inverters, "
                 "connected at the client's LT bus (anonymised site, assumed values)", fontsize=11)
    return fig


if __name__ == "__main__":
    fig = build()
    fig.savefig(os.path.join(HERE, "sld.png"), dpi=130)
    fig.savefig(os.path.join(HERE, "sld.svg"))
    print("wrote drawings/sld.png and drawings/sld.svg")
