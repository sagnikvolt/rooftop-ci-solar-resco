# Commissioning checklist (307 kWp rooftop plant)

How to use: print this, tick each line, write the measured value beside it, sign and date. Expected values come from the design (`commissioning/expected_values.py`). Acceptance ranges marked * are common practice quoted by a general guide, not a clause of the standard ("Acceptance ranges are set by project specs and local rules"); confirm them with the engineer of record. Source for the test list: https://www.anernstore.com/blogs/diy-solar-guides/iec-62446-1-commissioning-test-records (read 2026-11-05). IEC 62446-1 itself was not available to read.

## A. Paperwork before energising

- [ ] Approved single-line diagram and layout drawing (this repo: `drawings/sld.png`, `drawings/layout.png`)
- [ ] WBSEDCL go-ahead and quotation paid (WBSEDCL procedures document)
- [ ] OEM fitness certificate for the inverters, tested at an NABL-accredited centre, with Form S5
- [ ] Form S6 self-certification, or Chief Electrical Inspector clearance (check whether it applies at 11 kV)
- [ ] Net-meter and generation-meter installed by the utility on the HT side
- [ ] Module and inverter datasheets and serial numbers recorded

## B. Visual inspection (power OFF)

- [ ] Module count and strings match the drawing: 544 modules, 32 strings of 17
- [ ] No cracked glass, no damaged frames, no shading objects
- [ ] Clamps torqued to the supplier's value; torque recorded
- [ ] Cables supported, UV-rated, no sharp bends, no contact with roof edges
- [ ] MC4 connectors fully clicked in, from the same make on both ends of each joint
- [ ] Frames and structure bonded to earth; earthing per IS 3043
- [ ] Skylight strips clear and marked; setbacks respected
- [ ] Warning signs fitted at inverters, panels and the roof access point
- [ ] Fire extinguishers and sand buckets at the inverter area

## C. String tests (DC, before closing the inverter DC switch)

Expected values for 17 modules in series:

| Check | Expected | Accept |
|---|---|---|
| Polarity of every string | Correct sign at inverter input | No reversals |
| Voc at 25 °C cell temp | 882.3 V | about ±5 % * (838 to 926 V) |
| Voc at 45 °C cell temp | 836.4 V | about ±5 % * (795 to 878 V) |
| Strings of the same slope | Within a few volts of each other | A low string means a missing or bad module |
| Isc per string | up to 13.75 A at full sun (STC); scale with irradiance | about ±10 % * of expected at the measured irradiance |
| Insulation resistance, string to earth | at least 1 MΩ for systems above 120 V * | record test voltage and conditions |

Safety note: a 17-module string reaches about 932 V when cold (design calculation). Treat every string as live whenever there is light.

## D. Inverter and AC side

- [ ] AC breakers 200 A per inverter and 400 A main fitted as per the drawing (sizes are ASSUMED; confirm by protection study)
- [ ] AC voltage 400 V three-phase and frequency 50 Hz measured at the point of interconnection
- [ ] Phase sequence correct
- [ ] Inverter start-up, grid-fail shutdown and reconnection observed; anti-islanding behaviour recorded
- [ ] Grid-code settings loaded as WBSEDCL requires
- [ ] Harmonics (THD) measured and within utility limits
- [ ] Generation meter reading matches the inverter display within tolerance

## E. First-day performance record

- [ ] Irradiance and module temperature at noon recorded
- [ ] Inverter power at noon against expected: a clean sunny noon should give roughly the 220 kWac limit only if DC/AC clipping applies (design DC/AC 1.40; PVsyst shows clipping loss 0.32 % per year)
- [ ] Photo record of nameplates, wiring and labelling
- [ ] Handover: drawings, test records, warranty papers, O&M contact

## F. After handover

- Fitness testing of the plant every **2 years** (above 170 kW; WBSEDCL document).
- A system idle for more than 6 months needs fresh certification (WBSEDCL document).
- Clean modules in the early morning or evening; log activities (safety article below).
