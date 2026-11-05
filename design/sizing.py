"""Plant size = the smallest of three limits, then rounded to whole strings and inverters.

How this works:
  1. Roof limit: how many modules physically fit in the usable area.
  2. Regulatory limit: WBERC 2025 rooftop rules cap a system at the lower of 500 kW
     or the consumer's sanctioned load / contract demand (see VERIFICATION.md).
  3. Load limit: size so the plant's peak output roughly matches the average
     working-day daytime load, so most energy is used on site.
  The plant size is the smallest of these, then rounded down to whole strings
  split equally between the east and west slopes and across the inverters.
"""
import csv
import json
import os

from equipment import INVERTER, MODULE
import strings

HERE = os.path.dirname(os.path.abspath(__file__))
SURVEY = os.path.join(HERE, "..", "survey")

MODULE_GAP_M = 0.02                  # ASSUMED gap between modules
SKYLIGHT_SEGMENTS = 3                # two skylight strips split each slope into three bays
PEAK_AC_PER_KWP = 0.80               # ASSUMED peak AC kW per kWp for an east-west flush roof
CONTRACT_DEMAND_KVA = 350            # ASSUMED, same as survey/hourly_load.py
POWER_FACTOR = 0.95
REGULATORY_LIMIT_KW = 500


def roof_module_count():
    with open(os.path.join(SURVEY, "roof_data.json")) as f:
        roof = json.load(f)
    up = roof["slope_length_m"] - roof["edge_setback_eave_m"] - roof["ridge_setback_m"]
    along = roof["ridge_length_m"] - 2 * roof["edge_setback_gable_m"]
    keepout = roof["translucent_strips_per_slope"] * (
        roof["translucent_strip_width_m"] + 2 * roof["translucent_keepout_each_side_m"])
    bay_width = (along - keepout) / SKYLIGHT_SEGMENTS
    per_row = int(bay_width // (MODULE["width_m"] + MODULE_GAP_M)) * SKYLIGHT_SEGMENTS
    rows = int(up // (MODULE["length_m"] + MODULE_GAP_M))   # portrait, long side up the slope
    return per_row * rows * len(roof["slopes"]), per_row, rows


def load_limit_kwp():
    total, n = 0.0, 0
    with open(os.path.join(SURVEY, "hourly_load.csv")) as f:
        for r in csv.DictReader(f):
            if int(r["weekday_mon0"]) <= 5 and 8 <= int(r["hour_of_day"]) < 16:
                total += float(r["load_kw"])
                n += 1
    mean_kw = total / n
    return mean_kw, mean_kw / PEAK_AC_PER_KWP


def design():
    n_roof, per_row, rows = roof_module_count()
    roof_kwp = n_roof * MODULE["pmax_w"] / 1000
    reg_kw = min(REGULATORY_LIMIT_KW, CONTRACT_DEMAND_KVA * POWER_FACTOR)
    mean_load_kw, load_kwp = load_limit_kwp()
    limit_kwp = min(roof_kwp, reg_kw, load_kwp)

    n_series = strings.max_modules_per_string()
    string_kwp = n_series * MODULE["pmax_w"] / 1000
    # whole strings, split equally between the two slopes (so an even number) and across inverters
    n_strings = int(limit_kwp // string_kwp)
    n_inverters = 2
    group = n_inverters * 2          # strings come in groups of (inverters x slopes)
    n_strings = (n_strings // group) * group
    per_inv = n_strings // n_inverters
    dc_kwp = n_strings * string_kwp
    ac_kva = n_inverters * INVERTER["ac_kva_45c"]
    return {
        "roof_modules": n_roof, "modules_per_row": per_row, "rows_per_slope": rows,
        "roof_limit_kwp": roof_kwp,
        "regulatory_limit_kw": reg_kw,
        "mean_workday_daytime_load_kw": mean_load_kw, "load_limit_kwp": load_kwp,
        "limit_kwp": limit_kwp,
        "modules_per_string": n_series, "string_kwp": string_kwp,
        "n_strings": n_strings, "strings_per_inverter": per_inv,
        "n_modules": n_strings * n_series, "dc_kwp": dc_kwp,
        "n_inverters": n_inverters, "ac_kva": ac_kva, "dc_ac_ratio": dc_kwp / ac_kva,
        "strings_per_mppt_slope": per_inv // 2 // 2 if per_inv % 4 == 0 else None,
    }


def main():
    d = design()
    print(f"Roof limit        : {d['roof_modules']} modules ({d['modules_per_row']} per row x {d['rows_per_slope']} rows x 2 slopes) = {d['roof_limit_kwp']:.1f} kWp")
    print(f"Regulatory limit  : {d['regulatory_limit_kw']:.0f} kW (lower of {REGULATORY_LIMIT_KW} kW and {CONTRACT_DEMAND_KVA} kVA x {POWER_FACTOR})")
    print(f"Load limit        : {d['load_limit_kwp']:.1f} kWp (mean working-day 08-16h load {d['mean_workday_daytime_load_kw']:.0f} kW / {PEAK_AC_PER_KWP})")
    print(f"Binding limit     : {d['limit_kwp']:.1f} kWp")
    print(f"String            : {d['modules_per_string']} modules = {d['string_kwp']:.3f} kWp")
    print(f"Plant             : {d['n_strings']} strings x {d['modules_per_string']} = {d['n_modules']} modules = {d['dc_kwp']:.1f} kWp")
    print(f"Inverters         : {d['n_inverters']} x {INVERTER['name']} = {d['ac_kva']:.0f} kVA, {d['strings_per_inverter']} strings each, DC/AC {d['dc_ac_ratio']:.2f}")


if __name__ == "__main__":
    main()
