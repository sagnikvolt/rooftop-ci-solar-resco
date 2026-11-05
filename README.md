# Rooftop C&I Solar and RESCO Model (West Bengal)

A 307 kWp rooftop plant designed for an **assumed warehouse roof in Hooghly district**, with a RESCO model (the developer owns and runs the plant; the client pays per kWh).

**Status:** Complete as a design study (Nov 2026). Live: https://rooftop.sagniknath.in

> Design decisions, inputs and checks are mine; AI tools assisted with scripting and documentation.

## Key results

| Item | Result |
|---|---|
| Plant | 307.4 kWp, 544 modules (565 Wp), 2 inverters of 110 kVA, 17 modules per string |
| Yield (PVsyst 7.4.7, P50) | 409,153 kWh per year, performance ratio 84.9 % (soiling and shading not yet modelled) |
| Used on site | 92 % (377,485 kWh); the rest is exported at the HV feed-in rate of Rs 3.89/kWh |
| Grid energy charge | about Rs 7.06 per kWh (WBSEDCL Rate E(B), 11 kV industry, FY2025-26; MVCA extra, not included) |
| RESCO tariff, year 1 | Rs 5.65 per kWh (20 % below grid) |
| RESCO project IRR / payback | 19.4 % / 5.3 years (capex Rs 38 per Wp = Rs 1.17 crore, no tax, no loan) |
| Client saving | Rs 5.3 lakh in year 1, Rs 1.6 crore over 25 years, no capex |
| 20 to 30 % discount at Rs 38 to 50 per Wp | IRR 12 to 19 % (see [`resco/results.md`](resco/results.md)) |
| Biggest risks | capex (installer pages, not a quote), real yield, how the capacity cap is read |

The roof and the client are **assumed and anonymised**. It is a design study, not a real client project; no site survey has been done.

## Folders

| Folder | What is in it |
|---|---|
| `survey/` | roof data, usable area, assumed client load profile, survey checklist |
| `design/` | sizing, string design, AC side, wind-load note |
| `pvsyst/` | PVsyst exports, results and screenshots |
| `grid/` | grid connection and regulation note |
| `resco/` | RESCO financial model (Python), results and sensitivity |
| `commissioning/` | commissioning checklist and safety note |
| `drawings/` | roof layout and single-line diagram |
| `site/` | showcase website with a RESCO calculator (deployed from this folder) |
| `report/` | PDF report and the script that builds it |
| `tests/` | tests for sizing, strings, the financial model and the website calculator |

Every assumption is logged in [`ASSUMPTIONS.md`](ASSUMPTIONS.md). Every external fact (tariff, regulation, price, standard) is listed with its source and access date in [`VERIFICATION.md`](VERIFICATION.md). If I could not find a source, it is marked `ASSUMED`. Progress by phase is in [`PLAN.md`](PLAN.md).

## Run it

```
python3 resco/model.py                 # base case and TOD case
python3 resco/write_results.py         # rewrites resco/results.md
python3 resco/export_site_data.py      # rewrites site/data.js
python3 report/make_report.py          # rebuilds the PDF (needs reportlab, matplotlib)
python3 report/make_og_image.py        # rebuilds the link-preview image, favicon and copies the PDF and SLD into site/assets
pip install -r requirements-dev.txt && python3 -m pytest    # tests (the calculator test also needs node)
```

## Related work
- [5 MWp ground-mount solar plant design](https://github.com/sagnikvolt/solar-pv-plant-5mwp-wb) (PVsyst, Python, AutoCAD)
- [SunSense](https://sunsense.sagniknath.in), rooftop solar planner for Indian homes

## Limitations
Preliminary design only. No structural certification, no site survey, no real client data. Screenshots and charts in this repository come from real software runs; there are no AI-generated images.

*Correction, 5 Nov 2026: the first version read the WBSEDCL tariff columns the wrong way round (energy charge Rs 3.84). The energy charge is about Rs 7.06 per kWh; 384 is the demand charge in Rs/kVA/month. See `VERIFICATION.md`.*
