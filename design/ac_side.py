"""AC side currents and breaker sizes, with the arithmetic shown.

How this works:
  A three-phase inverter's AC current is I = S / (sqrt(3) x V), where S is its apparent
  power in VA and V the line-to-line voltage. The breaker must carry that current
  continuously, so it is sized above it by a safety factor.
"""
import math

from equipment import INVERTER

AC_VOLTAGE_V = 400            # SG110CX three-phase line voltage (datasheet, see VERIFICATION.md)
BREAKER_FACTOR = 1.25         # ASSUMED: size breakers at 125 % of continuous current (common practice)
STANDARD_FRAMES_A = [63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630]   # ASSUMED standard MCCB ratings


def ac_current_a(kva, volts=AC_VOLTAGE_V):
    return kva * 1000 / (math.sqrt(3) * volts)


def next_standard(amps):
    for a in STANDARD_FRAMES_A:
        if a >= amps:
            return a
    raise ValueError("above the largest standard frame in the table")


def ac_side(n_inverters=2):
    per_inv = ac_current_a(INVERTER["ac_kva_45c"])
    total = per_inv * n_inverters
    return {
        "current_per_inverter_a": per_inv,
        "breaker_per_inverter_a": next_standard(per_inv * BREAKER_FACTOR),
        "current_total_a": total,
        "breaker_main_a": next_standard(total * BREAKER_FACTOR),
    }


if __name__ == "__main__":
    for k, v in ac_side().items():
        print(f"{k}: {v:.1f}")
