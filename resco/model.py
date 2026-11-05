"""RESCO financial model for the rooftop plant (standard library only).

How this works, step by step:
  1. PV output by hour. PVsyst gave the energy for each (month, hour of day), summed over
     the month (pvsyst/egrid_month_hour_kwh.csv). Dividing by the days in the month gives
     an "average day" for every month. Every day of the month gets that same profile.
     (Real days vary with cloud; an average day slightly overstates self-use. Noted.)
  2. Load by hour: survey/hourly_load.csv (8,760 hours, assumed factory).
  3. Each hour: self-used energy = min(PV, load). Surplus PV is exported.
  4. Money. Self-used energy is billed by the RESCO at the RESCO tariff = grid energy
     charge x (1 - discount). The client saves the difference. Exported energy is valued at
     the HV feed-in tariff (net-billing reading). Demand-charge savings are set to ZERO
     (solar cannot be relied on to cut contract demand), which is conservative.
  5. Cash flows for 25 years. Output falls each year (degradation). Tariffs rise by an
     escalation rate. The RESCO pays capex in year 0 and O&M every year.
  6. Results: RESCO project IRR (no loan, no tax: simple), simple payback, NPV, and what the
     client saves.
Every input that is not sourced is marked ASSUMED in INPUTS and in ASSUMPTIONS.md.
"""
import calendar
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")

# --- inputs: (value, source). Sources are in VERIFICATION.md or ASSUMPTIONS.md -------------
INPUTS = {
    "plant_kwp": 307.4,                 # design/sizing.py
    "grid_energy_tariff": 7.06,         # Rs/kWh, WBSEDCL Rate E(B), 11 kV industry, normal: 707/706/705 P/kWh summer/monsoon/winter, taken flat at the monsoon value (season months not defined for industry; ASSUMED). MVCA extra, not included. VERIFICATION.md
    "feed_in_tariff": 3.89,             # Rs/kWh, HV, FY2025-26 (WBSEDCL document, VERIFICATION.md)
    "capex_per_wp": 38.0,               # Rs/Wp, installer pages, May and Oct 2026 (VERIFICATION.md); range 38 to 50
    "om_pct_of_capex": 1.0,             # % of capex per year, ASSUMED (no source found)
    "resco_discount": 0.20,             # fraction off the grid energy charge, ASSUMED: low end of the 20 to 50 % seen in a general guide
    "escalation": 0.02,                 # per year on both tariffs, ASSUMED
    "first_year_degradation": 0.01,     # Waaree datasheet: 99.0 % at end of year 1
    "annual_degradation": 0.004,        # (99.0 - 87.4) / 29 years, from the 30-year linear warranty (inferred, a guarantee not an expectation)
    "years": 25,                        # contract length, general guide says 10 to 25
    "discount_rate": 0.10,              # for NPV, ASSUMED
}

# Rate E(BT), 11 kV industry on the optional TOD scheme, Rs/kWh at the monsoon column (VERIFICATION.md).
# Only used for the optional TOD sensitivity case, never for the base case.
TOD_RATE = {"06-17": 6.94, "17-23": 8.36, "23-06": 5.17}
# Demand charge, Rs per kVA per month, both E(B) and E(BT). Deliberately NOT counted as a saving.
DEMAND_CHARGE_RS_PER_KVA_MONTH = 384


def tod_rate_for_hour(h):
    """Rate E(BT) energy charge for the clock hour starting at h (0..23)."""
    if 6 <= h < 17:
        return TOD_RATE["06-17"]
    if 17 <= h < 23:
        return TOD_RATE["17-23"]
    return TOD_RATE["23-06"]


def read_pv_month_hour(path=None):
    """Return pv[month 1..12][hour 0..23] = kWh in an average day of that month."""
    path = path or os.path.join(ROOT, "pvsyst", "egrid_month_hour_kwh.csv")
    pv = {}
    with open(path, encoding="utf-8-sig") as f:
        rows = list(csv.reader(f, delimiter=";"))
    names = [calendar.month_name[m] for m in range(1, 13)]
    for r in rows:
        if r and r[0] in names:
            m = names.index(r[0]) + 1
            days = calendar.monthrange(2026, m)[1]
            pv[m] = [max(0.0, float(x)) / days for x in r[1:25]]    # negative night values -> 0
    return pv


def read_load(path=None):
    path = path or os.path.join(ROOT, "survey", "hourly_load.csv")
    out = []
    with open(path) as f:
        for r in csv.DictReader(f):
            out.append((int(r["month"]), int(r["hour_of_day"]), float(r["load_kw"])))
    return out


def year1_energy(plant_kwp, pv=None, load=None, design_kwp=307.4):
    """Annual PV, self-used and exported energy (kWh) for a plant size, scaling PVsyst's output linearly."""
    pv = pv or read_pv_month_hour()
    load = load or read_load()
    scale = plant_kwp / design_kwp
    total = self_used = 0.0
    tod_value = 0.0                        # Rs of grid energy charge avoided at Rate E(BT)
    for month, hour, load_kw in load:
        gen = pv[month][hour] * scale      # kWh in this hour = average kW for one hour
        total += gen
        used = min(gen, load_kw)
        self_used += used
        tod_value += used * tod_rate_for_hour(hour)
    return {"pv_kwh": total, "self_kwh": self_used, "export_kwh": total - self_used,
            "self_fraction": self_used / total if total else 0.0,
            "tod_avg_rate": tod_value / self_used if self_used else 0.0}


def irr(cashflows, lo=-0.99, hi=1.0):
    """Internal rate of return by bisection: the rate where NPV = 0."""
    def npv(r):
        return sum(cf / (1 + r) ** t for t, cf in enumerate(cashflows))
    if npv(lo) * npv(hi) > 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        if npv(lo) * npv(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def run(**override):
    p = dict(INPUTS)
    p.update(override)
    e = year1_energy(p["plant_kwp"])
    if p.get("tod"):
        # optional case: the client is on Rate E(BT); the solar energy offsets the hour-by-hour TOD rate
        p["grid_energy_tariff"] = e["tod_avg_rate"]
    capex = p["plant_kwp"] * 1000 * p["capex_per_wp"]
    resco_tariff0 = p["grid_energy_tariff"] * (1 - p["resco_discount"])
    cash = [-capex]
    client_saving = []
    payback = None
    cum = -capex
    for yr in range(1, p["years"] + 1):
        derate = (1 - p["first_year_degradation"]) * (1 - p["annual_degradation"]) ** (yr - 1)
        esc = (1 + p["escalation"]) ** (yr - 1)
        self_kwh = e["self_kwh"] * derate
        exp_kwh = e["export_kwh"] * derate
        revenue = self_kwh * resco_tariff0 * esc + exp_kwh * p["feed_in_tariff"] * esc
        om = capex * p["om_pct_of_capex"] / 100 * esc
        cf = revenue - om
        cash.append(cf)
        client_saving.append(self_kwh * (p["grid_energy_tariff"] - resco_tariff0) * esc)
        prev, cum = cum, cum + cf
        if payback is None and cum >= 0:
            payback = (yr - 1) + (-prev / cf)
    npv = sum(cf / (1 + p["discount_rate"]) ** t for t, cf in enumerate(cash))
    return {
        "inputs": p, "energy_year1": e, "capex_rs": capex, "resco_tariff_year1": resco_tariff0,
        "project_irr": irr(cash), "payback_years": payback, "npv_rs": npv,
        "client_saving_year1_rs": client_saving[0], "client_saving_total_rs": sum(client_saving),
        "cashflows": cash,
    }


def sensitivity_table(discounts=(0.20, 0.30, 0.40), capexes=(38, 44, 50)):
    rows = []
    for d in discounts:
        for c in capexes:
            r = run(resco_discount=d, capex_per_wp=c)
            rows.append({"discount": d, "capex": c, "irr": r["project_irr"], "payback": r["payback_years"],
                         "saving1": r["client_saving_year1_rs"], "tariff": r["resco_tariff_year1"]})
    return rows


def self_consumption_curve(step=10, lo=50, hi=500):
    """Table for the website calculator: energy flows for plant sizes from lo to hi kWp."""
    pv, load = read_pv_month_hour(), read_load()
    rows = []
    for kwp in range(lo, hi + 1, step):
        e = year1_energy(kwp, pv, load)
        rows.append({"kwp": kwp, **{k: round(v, 1) if k != "self_fraction" else round(v, 4) for k, v in e.items()}})
    return rows


if __name__ == "__main__":
    r = run()
    e = r["energy_year1"]
    print(f"Year-1 PV {e['pv_kwh']:,.0f} kWh, self-used {e['self_kwh']:,.0f} ({e['self_fraction']:.1%}), exported {e['export_kwh']:,.0f}")
    print(f"Capex Rs {r['capex_rs']:,.0f}; RESCO tariff Rs {r['resco_tariff_year1']:.2f}/kWh")
    print(f"Project IRR {r['project_irr']:.1%}; payback {r['payback_years']:.1f} yr; NPV Rs {r['npv_rs']:,.0f}")
    t = run(tod=True)
    print(f"TOD case (Rate E(BT)): avg avoided rate Rs {t['inputs']['grid_energy_tariff']:.2f}/kWh, IRR {t['project_irr']:.1%}, payback {t['payback_years']:.1f} yr, client saves Rs {t['client_saving_year1_rs']:,.0f} in year 1")
    print(f"Client saves Rs {r['client_saving_year1_rs']:,.0f} in year 1, Rs {r['client_saving_total_rs']:,.0f} over {r['inputs']['years']} years")
    with open(os.path.join(HERE, "self_consumption_curve.json"), "w") as f:
        json.dump({"note": "Year-1 energy for plant sizes, from PVsyst output scaled linearly and the assumed hourly load. See resco/model.py.",
                   "rows": self_consumption_curve()}, f, indent=1)
    print("wrote resco/self_consumption_curve.json")
