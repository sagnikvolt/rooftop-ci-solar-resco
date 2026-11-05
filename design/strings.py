"""String design: how many modules in series, and how many strings per MPPT.

How this works (worked example, numbers from equipment.py):
  Cold morning: voltage is highest. Voc at 3.4 degC =
      51.90 x (1 + 0.0026 x (25 - 3.4)) = 54.81 V per module
  The string must stay under the inverter limit (1,100 V) and under the 1,000 V
  limit of the supplied MC4 connectors, with a safety margin.
      17 modules -> 931.8 V   (6.8 % under 1,000 V)
      18 modules -> 986.6 V   (only 1.3 % under 1,000 V, rejected)
  Hot afternoon: voltage is lowest. Vmp at cell temperature 75 degC =
      43.56 x (1 - 0.0030 x (75 - 25)) = 37.03 V per module
      17 modules -> 629.5 V   (inside the 200 to 1,000 V MPPT window)
  Current: two strings share one MPPT, so
      2 x Imp = 25.94 A (limit 26 A) and 2 x Isc = 27.50 A (limit 40 A).
"""
from equipment import INVERTER, MODULE

T_COLD_C = 3.4      # record low, taken from Project 1 (Kolkata); ASSUMED to apply near Singur
T_CELL_HOT_C = 75.0  # ASSUMED hot cell temperature for flush-mounted modules on a metal roof
VOC_MARGIN = 0.05   # keep 5 % under the voltage limit (same margin as Project 1)


def voc_cold(t_cold=T_COLD_C):
    m = MODULE
    return m["voc_v"] * (1 + m["temp_coeff_voc_pct"] / 100 * (t_cold - 25))


def vmp_hot(t_cell=T_CELL_HOT_C):
    m = MODULE
    return m["vmp_v"] * (1 + m["temp_coeff_pmax_pct"] / 100 * (t_cell - 25))


def max_modules_per_string():
    limit = min(INVERTER["max_dc_voltage_v"], INVERTER["mc4_voltage_limit_v"]) * (1 - VOC_MARGIN)
    return int(limit // voc_cold())


def min_modules_per_string():
    n = 1
    while n * vmp_hot() < INVERTER["mppt_min_v"]:
        n += 1
    return n


def check(n_series, strings_per_mppt=2):
    voc = n_series * voc_cold()
    vmp = n_series * vmp_hot()
    i_op = strings_per_mppt * MODULE["imp_a"]
    i_sc = strings_per_mppt * MODULE["isc_a"]
    return {
        "n_series": n_series,
        "voc_cold_v": voc,
        "vmp_hot_v": vmp,
        "margin_to_1000v_pct": 100 * (1 - voc / INVERTER["mc4_voltage_limit_v"]),
        "voc_ok": voc <= INVERTER["max_dc_voltage_v"] * (1 - VOC_MARGIN) and voc <= INVERTER["mc4_voltage_limit_v"] * (1 - VOC_MARGIN),
        "vmp_ok": INVERTER["mppt_min_v"] <= vmp <= INVERTER["mppt_max_v"],
        "mppt_operating_current_a": i_op,
        "mppt_operating_ok": i_op <= INVERTER["max_input_current_per_mppt_a"],
        "mppt_isc_a": i_sc,
        "mppt_isc_ok": i_sc <= INVERTER["max_isc_per_mppt_a"],
    }


if __name__ == "__main__":
    print(f"Voc at {T_COLD_C} degC : {voc_cold():.2f} V per module")
    print(f"Vmp at {T_CELL_HOT_C} degC : {vmp_hot():.2f} V per module")
    print(f"Modules in series: min {min_modules_per_string()}, max {max_modules_per_string()}")
    for n in (17, 18):
        print(check(n))
