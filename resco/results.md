# RESCO model results (base case and sensitivity)

Run `python3 resco/model.py` to reproduce. Inputs and their sources are in the `INPUTS` table at the top of `resco/model.py`; every unsourced input is marked ASSUMED there and in `ASSUMPTIONS.md`.

## Base case

| Item | Value |
|---|---|
| Plant | 307.4 kWp, PVsyst year-1 output 409,153 kWh (the model rebuilds 409,200 kWh from the hourly table) |
| Self-used on site | 377,485 kWh (92.2 %) |
| Exported | 31,715 kWh (7.8 %), mostly Sundays and holidays |
| Capex | Rs 38 per Wp = Rs 1.17 crore |
| Grid energy charge | Rs 3.84 per kWh (WBSEDCL HV industrial, FY2025-26) |
| RESCO tariff, year 1 | 20 % below grid = Rs 3.07 per kWh |
| O&M | 1 % of capex per year (ASSUMED) |
| Escalation | 2 % per year on both tariffs (ASSUMED) |
| Degradation | 1 % in year 1, then 0.4 % per year (Waaree warranty) |
| Contract | 25 years, no loan, no tax |

| Result | Value |
|---|---|
| RESCO project IRR | 10.1 % |
| RESCO simple payback | 9.5 years |
| RESCO NPV at 10 % | Rs 1.2 lakh (almost zero: a 10 % project) |
| Client saving, year 1 | Rs 2.87 lakh |
| Client saving over 25 years | Rs 87 lakh |

## Sensitivity: RESCO IRR and client saving

| RESCO discount | Capex Rs/Wp | RESCO IRR | Payback (yr) | Client saves, yr 1 (Rs) |
|---|---|---|---|---|
| 20% | 38 | 10.1% | 9.5 | 287,010 |
| 20% | 44 | 8.2% | 11.0 | 287,010 |
| 20% | 50 | 6.7% | 12.6 | 287,010 |
| 30% | 38 | 8.6% | 10.7 | 430,515 |
| 30% | 44 | 6.8% | 12.5 | 430,515 |
| 30% | 50 | 5.3% | 14.3 | 430,515 |
| 40% | 38 | 6.9% | 12.3 | 574,020 |
| 40% | 44 | 5.2% | 14.4 | 574,020 |
| 40% | 50 | 3.9% | 16.5 | 574,020 |

## How to read this

- **The self-use is high (92 %)** because the plant is sized to the weekday daytime load. That part is robust.
- **The money is thin because the grid energy charge is low.** At Rs 3.84 per kWh, a 20 % discount leaves only Rs 3.07 per kWh. Installer pages that quote 3 to 4 year paybacks assume a Rs 8 to 12 per kWh tariff. That is about double this HV industrial energy charge. Those figures do not describe this client.
- **Solar saves the energy charge only here.** The bill also has a demand charge of roughly Rs 705 per kVA per month (VERIFICATION.md). Solar cannot be relied on to lower it, so it is set to zero. Fuel surcharge, duty and other per-unit items are not counted either. Counting any per-unit extras the grid bill carries would raise the savings. This is deliberately conservative.
- **RESCO versus client-owned.** If the client bought the plant, it would save about Rs 15.7 lakh per year on year-1 numbers (self-use at Rs 3.84 plus exports at Rs 3.89) against a Rs 1.17 crore capex, which is roughly 7.4 years simple payback before O&M, and 8 to 9 years after O&M. A RESCO at 20 % discount trades that payback for zero upfront cost.
- **The break-even is a tariff question.** A RESCO needs a discount small enough to earn its return and large enough to tempt the client. At Rs 3.84 per kWh that window is narrow. This is the main finding to discuss in an interview.

## Limits

1. PV output uses PVsyst's average day per month, which slightly overstates self-use compared with real cloudy days.
2. No soiling, shading or unavailability in PVsyst (see pvsyst/results.md), so output is optimistic.
3. Capex comes from two installer marketing pages, not a quote or a benchmark order.
4. No tax, depreciation benefits, loan, inverter replacement or insurance. Adding them would change IRR.
5. FY2025-26 tariffs are used for 25 years with 2 % escalation (ASSUMED). The FY2026-27 order was not found.
6. The load is an assumed factory, not a measured one.
