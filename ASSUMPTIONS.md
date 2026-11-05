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
