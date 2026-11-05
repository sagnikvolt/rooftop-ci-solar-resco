"""Expected string readings for commissioning, computed from the design.

How this works: a string is 17 modules in series. Voltages add, current stays the same.
Measured Voc should be close to 17 x module Voc, corrected for the cell temperature at the
time of the test. We print the STC values and the value at a chosen cell temperature.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "design"))
from equipment import MODULE  # noqa: E402
import strings            # noqa: E402


def expected(cell_temp_c=25.0, n_series=None):
    n = n_series or strings.max_modules_per_string()
    voc = n * MODULE["voc_v"] * (1 + MODULE["temp_coeff_voc_pct"] / 100 * (cell_temp_c - 25))
    return {"n_series": n, "cell_temp_c": cell_temp_c, "voc_v": voc, "isc_a_at_stc": MODULE["isc_a"],
            "voc_tolerance_v": (0.95 * voc, 1.05 * voc)}


if __name__ == "__main__":
    for t in (25, 45):
        e = expected(t)
        lo, hi = e["voc_tolerance_v"]
        print(f"cell {t} C: expected string Voc {e['voc_v']:.1f} V (accept {lo:.0f} to {hi:.0f} V, +-5 %)")
