# PVsyst results: base case

PVsyst 7.4.7, project `RooftopCI_Hooghly_307kWp`, run on 5 Nov 2026.
Full report: [`pvsyst_report_base_307kWp.pdf`](pvsyst_report_base_307kWp.pdf) (8 pages).

## What was simulated

| Item | Value |
|---|---|
| Site / weather | Kolkata, Meteonorm 8.1 (1991-2012), synthetic hourly. Kolkata is the nearest PVsyst site to Hooghly district; the real site is about 30 km away |
| Orientation | 2 fixed planes: 7° tilt facing east (azimuth -90°) and 7° facing west (+90°) |
| Module | Waaree BiN-08-565, 565 Wp (custom parameters in PVsyst) |
| Inverter | Sungrow SG110CX-P2, 110 kWac (nearest model in the PVsyst database to the SG110CX) |
| Layout | 17 modules per string, 16 strings per slope, one inverter per slope |
| Size | 544 modules = 307 kWp DC, 220 kWac, DC/AC ratio 1.40 |
| Shading | None defined (no 3D scene) |

## Results

| Result | Value |
|---|---|
| Energy injected to grid | 409,153 kWh per year |
| Specific production | 1,331 kWh per kWp per year |
| Performance ratio | 84.9 % |
| Global horizontal irradiation | 1,574 kWh/m² |
| Irradiation on the 7° planes | 1,568 kWh/m² |

Monthly range of PR: 0.827 (May) to 0.876 (January).

## Loss chain (from the PVsyst loss diagram)

| Step | Loss |
|---|---|
| Angle of incidence (IAM) | -2.76 % |
| Irradiance level | -0.90 % |
| Temperature | -7.52 % |
| Module quality | +0.50 % |
| Mismatch | -2.00 % |
| DC wiring (ohmic) | -0.88 % |
| Inverter efficiency | -2.13 % |
| Inverter over nominal power (clipping) | -0.32 % |

## How to read these numbers

- **Clipping is small.** DC/AC of 1.40 costs only 0.32 % of energy, because east and west planes peak at different times and a 7° tilt keeps the peak low. A third inverter is not needed.
- **Temperature is the largest loss** at 7.5 %, as expected for Kolkata with flush-mounted modules (heat transfer is poor, so PVsyst uses Uc = 20 W/m²K).
- **Tilt costs energy.** PVsyst's quick optimisation put the loss against the best orientation at about 5.9 % for east-west 7°. That is the price of a flush roof mount with no tilting structure.

## What this run does NOT include (read before quoting the numbers)

These are PVsyst defaults, not site measurements, so the yield is on the optimistic side:

1. **No soiling loss.** Dust on a roof near Hooghly in the dry season is real; a soiling loss still has to be chosen and sourced.
2. **No shading and no unavailability.** The roof has two skylight strips and a ridge but no tall neighbours by assumption.
3. **Bifacial gain not modelled.** The module is bifacial, but a flush metal-sheet roof gives almost no rear-side gain, so the run treats it as monofacial. This is the safe side.
4. **Synthetic weather.** Meteonorm monthly values turned into hourly data, not measured years.
5. **Inverter model.** The SG110CX-P2 (180-1000 V, 12 MPPT) is used instead of the SG110CX (200-1000 V, 9 MPPT) in `design/equipment.py`. Power is the same; the MPPT count differs. Multi-MPPT mode was switched off, so PVsyst treats each slope's 16 strings as one input and ignores per-MPPT current effects.
6. **PVsyst licence.** The licence showed "0 days remaining" at the time of the run. The simulation ran normally; re-run on a valid licence before treating the PDF as final.

## Cross-checks

- PVsyst's own string check reports Voc 958 V at -10 °C for 17 modules, under the 1,000 V limit. Our hand calculation gave 931.8 V at 3.4 °C. The difference is the colder reference temperature PVsyst uses.
- DC/AC ratio 1.40 matches `design/sizing.py`.
- 544 modules and 307.4 kWp match the design.
