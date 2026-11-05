"""Hourly load profile (8,760 hours) for the ASSUMED client.

How this works:
  1. Start from a shape for one working day (night base load, a day-shift and
     evening-shift plateau, a small lunch dip).
  2. Multiply by a day-of-week factor (Sunday is mostly off) and a month factor
     (a little more load in the hot months for cooling).
  3. Add a small repeatable random wobble (fixed seed, so the file is the same every run).
  4. Scale everything so the year adds up to exactly ANNUAL_KWH.

Worked example (check by hand): ANNUAL_KWH = 12 x 120,000 = 1,440,000 kWh,
so the average load is 1,440,000 / 8,760 = 164.4 kW.

All numbers below are ASSUMED, see ASSUMPTIONS.md. Run:  python survey/hourly_load.py
"""
import csv
import datetime
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))

MONTHLY_KWH = 120_000                 # ASSUMED average monthly consumption
ANNUAL_KWH = 12 * MONTHLY_KWH
CONTRACT_DEMAND_KVA = 350             # ASSUMED
POWER_FACTOR = 0.95                   # ASSUMED
YEAR = 2026                           # only used to get day-of-week and month; 8,760 h year
NOISE = 0.03                          # +/- 3 % hour-to-hour wobble
SEED = 42

# Shape for a working day, relative to the shift plateau (1.0). Index = hour of day.
DAY_SHAPE = (
    [0.15] * 6                        # 00:00-05:59 night base load (lights, compressors, security)
    + [0.9]                           # 06:00 shift start ramp-up
    + [1.0] * 6                       # 07:00-12:59
    + [0.8]                           # 13:00 lunch dip
    + [1.0] * 8                       # 14:00-21:59 (second shift)
    + [0.15] * 2                      # 22:00-23:59
)
assert len(DAY_SHAPE) == 24

# Monday = 0 ... Sunday = 6. Sunday: base load only.
WEEKDAY_FACTOR = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.2]

# Jan..Dec. Hot, humid months need more cooling.
MONTH_FACTOR = [0.95, 0.95, 1.0, 1.05, 1.1, 1.1, 1.05, 1.05, 1.05, 1.0, 0.95, 0.95]


def build_profile():
    rng = random.Random(SEED)
    start = datetime.datetime(YEAR, 1, 1)
    rows = []
    raw = []
    for h in range(8760):
        t = start + datetime.timedelta(hours=h)
        shape = DAY_SHAPE[t.hour] * WEEKDAY_FACTOR[t.weekday()] * MONTH_FACTOR[t.month - 1]
        shape *= 1 + rng.uniform(-NOISE, NOISE)
        raw.append(shape)
        rows.append((h, t.month, t.weekday(), t.hour))
    scale = ANNUAL_KWH / sum(raw)     # kWh per shape unit; each hour is 1 h so kW = kWh
    return [(h, m, wd, hr, shape * scale) for (h, m, wd, hr), shape in zip(rows, raw)]


def summary(profile):
    kw = [r[4] for r in profile]
    day = sum(r[4] for r in profile if 6 <= r[3] < 17)       # WBSEDCL normal-period window 06:00-17:00
    solar_hours = sum(r[4] for r in profile if 8 <= r[3] < 16)
    return {
        "annual_kwh": sum(kw),
        "average_kw": sum(kw) / len(kw),
        "peak_kw": max(kw),
        "min_kw": min(kw),
        "share_0600_1700": day / sum(kw),
        "share_0800_1600": solar_hours / sum(kw),
        "contract_demand_kw": CONTRACT_DEMAND_KVA * POWER_FACTOR,
    }


def main():
    profile = build_profile()
    out = os.path.join(HERE, "hourly_load.csv")
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["hour_of_year", "month", "weekday_mon0", "hour_of_day", "load_kw"])
        for h, m, wd, hr, kw in profile:
            w.writerow([h, m, wd, hr, f"{kw:.2f}"])
    s = summary(profile)
    print(f"Wrote {out}")
    print(f"Annual energy      : {s['annual_kwh']:,.0f} kWh")
    print(f"Average load       : {s['average_kw']:.1f} kW")
    print(f"Peak / min load    : {s['peak_kw']:.1f} kW / {s['min_kw']:.1f} kW")
    print(f"Contract demand    : {s['contract_demand_kw']:.0f} kW ({CONTRACT_DEMAND_KVA} kVA x PF {POWER_FACTOR})")
    print(f"Energy 06:00-17:00 : {100 * s['share_0600_1700']:.1f} % of annual")
    print(f"Energy 08:00-16:00 : {100 * s['share_0800_1600']:.1f} % of annual (core solar hours)")


if __name__ == "__main__":
    main()
