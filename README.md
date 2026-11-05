# Rooftop C&I Solar and RESCO Model (West Bengal)

**Goal:** design a 300 to 500 kWp rooftop solar plant for a factory or warehouse roof in the Hooghly/Howrah industrial belt, and model it as a RESCO project (the developer owns and runs the plant, the client pays per kWh).

**Status:** in progress (Phase 1 done: assumed roof, client and hourly load profile; Phase 2, design, is next).

> Design decisions, inputs and checks are mine; AI tools assisted with scripting and documentation.

## About the site
The roof and the client are **assumed and anonymised**: "a warehouse roof in Hooghly district". It is a design study, not a real client project. No site survey has been done.

## Planned contents
| Folder | What will be here |
|---|---|
| `survey/` | site survey checklist, roof data, client load profile, commissioning and safety checklists |
| `design/` | plant sizing, string design, layout logic, wind-load note, grid connection |
| `pvsyst/` | my PVsyst exports and screenshots |
| `finance/` | RESCO financial model (Python), inputs and outputs |
| `drawings/` | layout and single-line diagram (DXF/PNG/PDF) |
| `site/` | one-page showcase website with a RESCO tariff calculator |
| `report/` | PDF report |
| `tests/` | tests for sizing, strings and the financial model |

Every assumption is logged in [`ASSUMPTIONS.md`](ASSUMPTIONS.md). Every external fact (tariff, regulation, price, standard) is listed with its source and access date in [`VERIFICATION.md`](VERIFICATION.md). If I could not find a source, it is marked `ASSUMED`.

## Related work
- [5 MWp ground-mount solar plant design](https://github.com/sagnikvolt/solar-pv-plant-5mwp-wb) (PVsyst, Python, AutoCAD)
- [SunSense](https://sunsense.sagniknath.in), rooftop solar planner for Indian homes

## Limitations
Preliminary design only. No structural certification, no site survey, no real client data. Screenshots and charts in this repository come from real software runs; there are no AI-generated images.
