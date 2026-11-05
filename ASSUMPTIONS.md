# Assumptions log

Format: parameter | value | source | reason. Add a row for every design or financial assumption. Nothing is presented as fact unless it has a source.

| Parameter | Value | Source | Reason |
|---|---|---|---|
| Site | Anonymised warehouse in Hooghly district (Singur-Dankuni industrial belt); no real company or address | Design choice | The study is independent, not a real client project |
| Roof type | Metal sheet (trapezoidal profile) on steel purlins, gable shape | ASSUMED | Most common warehouse and factory shed type in the belt |
| Roof size | 60 m along the ridge x 20 m up each slope; two slopes = 2,400 m2 | ASSUMED | Typical single-bay shed; chosen to fit a 300 to 500 kWp plant |
| Roof orientation | Ridge runs north-south; slopes face east (azimuth 90 deg) and west (270 deg) | ASSUMED | East-west roofs are common and suit flush-mount on both slopes |
| Roof tilt | 7 deg | ASSUMED | Typical low-pitch shed roof; to be measured on a real survey |
| Setbacks | 1.0 m at eave and both gable ends, 0.5 m at ridge | ASSUMED | Working and maintenance clearance; Phase 2 must check fire-access and walkway rules and cite the source |
| Obstacles | Two translucent skylight strips per slope, 1.2 m wide, running up the slope, with 0.5 m clearance each side | ASSUMED | Skylight strips are standard in sheds and are not walkable, so panels keep clear |
| Usable area | 991.6 m2 per slope, 1,983.2 m2 total (83 % of roof) | Computed by survey/usable_area.py | From the assumptions above |
| Client type | Light manufacturing or packaging unit, two shifts | ASSUMED | Daytime-heavy load that suits rooftop solar |
| Shift pattern | 06:00 to 22:00, Monday to Saturday; Sunday base load only (20 % of working load); night base load 15 % | ASSUMED | Typical two-shift small factory |
| Supply | HV industrial, 11 kV, WBSEDCL area (rate E(B)), contract demand 350 kVA, power factor 0.95 | ASSUMED | WBSEDCL HV rate found in VERIFICATION.md; confirm which licensee supplies the exact site |
| Monthly consumption | 120,000 kWh average (1,440,000 kWh per year), 10 % higher May to Sep, 5 % lower Nov to Feb | ASSUMED | Gives an average load of 164 kW and a peak of 293.5 kW, below the 332 kW contract demand |
| Daytime share | 63.3 % of annual energy falls between 06:00 and 17:00; 46.2 % between 08:00 and 16:00 | Computed by survey/hourly_load.py | Result of the shift pattern above |
| Record low temperature | 3.4 degC | Project 1 (Kolkata data), see that repo | Reused; the Singur belt is close; to be checked against site data |
| Hot cell temperature | 75 degC | ASSUMED | Flush-mounted modules on a metal roof run hot with little air flow behind |
| Voc safety margin | 5 % below the voltage limit | Same as Project 1 | Keeps strings clear of the inverter and MC4 limits on the coldest morning |
| Modules in series | 17 (931.8 V cold, 629.4 V hot) | Computed by design/strings.py | 18 would be only 1.3 % under the 1,000 V MC4 limit |
| Strings per MPPT | 2, with both strings on the same roof slope | Design choice | 2 x Imp = 25.94 A, just under the 26 A limit; Project 1 had an MPPT current problem, checked here. Short bursts above 26 A at high irradiance cause a little clipping, to be seen in PVsyst |
| Module gap | 0.02 m between modules | ASSUMED | Typical clamp gap |
| Module layout | Portrait, long side up the slope, flush with the roof | ASSUMED | Standard for metal sheet roofs with rails |
| Peak AC output | 0.80 kW per kWp for an east-west flush roof | ASSUMED | Used only to set the load limit; to be replaced by PVsyst results |
| Number of inverters | 2 x Sungrow SG110CX (220 kVA) | Design choice | Fits 307 kWp; DC/AC 1.40 is high but east-west output peaks lower; PVsyst will show the clipping loss |
| Regulatory limit | 332 kW (the lower of 500 kW and 350 kVA x 0.95) | VERIFICATION.md (partly verified) | Applied as kWp, the safer reading, because the unit is not stated |
| PVsyst weather site | Kolkata, Meteonorm 8.1 (1991-2012), synthetic | PVsyst database | Nearest PVsyst site to Hooghly district; no measured data for the roof |
| PVsyst inverter model | SG110CX-P2 (110 kWac, 180-1000 V, 12 MPPT) | PVsyst database | The plain SG110CX is not in the database; same power rating. Multi-MPPT off, one inverter per slope |
| PVsyst losses | PVsyst defaults for wiring, mismatch, quality, thermal (Uc 20 W/m²K) | PVsyst defaults | No site data. Soiling, shading and unavailability are left at zero, so yield is optimistic; see pvsyst/results.md |
| Bifacial gain | Not modelled | Design choice | Flush metal roof, almost no rear gain; safe side |
| Wind speed for Hooghly | 50 m/s, same as Kolkata | VERIFICATION.md (partly verified) | Hooghly is next to Kolkata and not listed separately |
| Wind k factors, Cpe, Cpi | Not chosen; k = 1 used only to illustrate 1.5 kN/m² | ASSUMED | Code tables not fetched; real roof needs an engineer's check |
| AC breaker sizes | 200 A per inverter, 400 A main | ASSUMED (125 % of continuous current, next standard frame) | design/ac_side.py; to be confirmed by a protection study |
| Grid connection | Plant ties into the client's LT bus; net meter on the HT side | VERIFICATION.md (WBSEDCL document) | Rule for an HT consumer connecting at its LT bus |
| Cap reading | Cap applied as 350 kVA x 0.95 = 332 kWp | ASSUMED (generous reading) | The WBSEDCL document pairs 170 kW with 200 kVA (about 0.85), which would give 297.5 kW; see grid/grid_connection_note.md |
| O&M cost | 1 % of capex per year, escalating with the tariff | ASSUMED | No O&M figure found in any source fetched |
| Tariff escalation | 2 % per year on grid and RESCO tariffs | ASSUMED | Keeps the discount constant; no forecast sourced |
| Base RESCO discount | 20 % off the grid energy charge | ASSUMED | Low end of the 20 to 50 % seen in a general guide; shown with sensitivities |
| Discount rate for NPV | 10 % | ASSUMED | Typical order of magnitude; shown only as a yardstick |
| Demand charge savings | Zero | Design choice | Solar cannot be relied on to cut contract demand; conservative |
| Export value | HV feed-in tariff Rs 3.89 per kWh (net billing reading) | VERIFICATION.md | Net metering would credit against imports instead; exports are only 8 % of output |
| Tax, loan, inverter replacement | Not modelled | Design choice | Keeps the model simple enough to explain; listed as limits in resco/results.md |
