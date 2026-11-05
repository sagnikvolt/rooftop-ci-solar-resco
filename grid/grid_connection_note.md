# Grid connection and regulation note

Main source: WBSEDCL, "Procedures" document for rooftop solar (2025), https://www.wbsedcl.in/irj/go/km/docs/internet/new_website/pdf/Solar/Guideline.pdf (read 2026-11-05). This is the utility's own document, so it is stronger than the news articles used earlier. It follows the WBERC 2025 rooftop regulations. The gazette text itself is still unread (see `VERIFICATION.md`).

## 1. Where the plant connects

- Supply above 170 kW (200 kVA) contract demand connects **at 11 kV or above**.
- An HT consumer **may connect its plant at its own LT bus bar**, but the **net meter must sit on the HT side of its transformer**.
- Our client is assumed to have an 11 kV supply with its own transformer (contract demand 350 kVA), so the plant ties into the client's LT bus and the net meter is on the 11 kV side. This is what the single-line diagram (`drawings/sld.png`) shows.

## 2. Size limits and one warning

| Rule (WBSEDCL document) | Value |
|---|---|
| Net metering | 1 kW up to 500 kW or the contract demand, whichever is lower |
| Net billing and gross metering | 1 kW up to the contract demand |
| Total on one feeder or distribution transformer | Must not exceed 100 % of its capacity |

**Open question that affects our size.** The document pairs "170 kW" with "200 kVA", which implies a power factor of about 0.85. If the cap is the contract demand converted to kW at 0.85, then:

- 350 kVA x 0.85 = **297.5 kW**.
- Our plant is 307.4 kWp DC (220 kVA AC). If the cap applies to **DC kWp**, we are 9.9 kWp over.
- If the cap applies to **AC inverter capacity** (220 kVA), we are well inside it.
- The document does not say which. `design/sizing.py` currently uses 350 x 0.95 = 332 kW, the more generous reading.
- If the strict reading is confirmed, the fix is **28 strings = 268.9 kWp** (strings must come in groups of four: 2 inverters x 2 slopes). All results would then need re-running.

Also, the contract demand of 350 kVA is itself an ASSUMED client value.

## 3. Metering

- One **net meter** at the HT side, plus one **generation meter** for net metering/billing (two for gross metering).
- WBSEDCL tests, installs and maintains the metering. The cost is in the quotation to the applicant.
- Loss factor at HV is 1; at LT and MV it is 0.971 under certain connection diagrams. Our HT-side net meter avoids the LT loss factor.

## 4. Settlement options and the feed-in tariff

| Mode | How it settles |
|---|---|
| Net metering | Exports offset imports unit for unit. Unused credit carries forward and resets to zero each financial year |
| Net billing | Exports valued at the feed-in tariff and offset against imports at the retail tariff. Credit carries forward, resets each year |
| Gross metering | All generation valued at the feed-in tariff; all consumption at the retail tariff. Net amount owed to the prosumer is paid at year end |

**FY 2025-26 feed-in tariff:** EHV Rs 3.73/kWh, **HV Rs 3.89/kWh**, LT and MV Rs 4.37/kWh. For an 11 kV HT consumer the HV figure is the relevant one. The FY 2026-27 value was not found (Open).

An 11 kV industrial consumer on Rate E(B) pays about Rs 7.06/kWh energy charge plus a Rs 384/kVA/month demand charge (see `VERIFICATION.md`; MVCA extra). Self-used solar therefore saves nearly twice what an export earns (Rs 3.89), which is why a plant sized to the daytime load makes sense.

## 5. RESCO

The document says a consumer may install the system itself or through a service provider such as a **RESCO or Utility Led Aggregation (ULA)**. It says nothing about ownership, financing or contract terms. This confirms RESCO is allowed in principle, but the commercial terms are between the RESCO and the client.

## 6. Process, fees and timelines (per the document)

- Application fee: HV/EHV **Rs 5,000** (LT/MV Rs 1,000).
- Forms: S1 application; S2, S3, S4 agreements (net metering, net billing, gross metering); S5 installation certificate; S6 self-certification where applicable.
- Steps and time limits: inspection within 15 days of application; go-ahead and quotation within 20 days; pay the quotation within 90 days; submit S5/S6 within 180 days of go-ahead; connectivity inspection within 10 days of the forms; agreement, meter installation, commissioning and synchronisation within 15 days.
- The document says a Chief Electrical Inspector clearance (or self-certification on S6) is needed for supply below 11 kV. Our 11 kV client may need CEIG clearance for the HT part; check.

## 7. Technical requirements

- Anti-islanding, synchronisation and harmonic filtering are built into the inverter and are the prosumer's responsibility.
- An OEM fitness certificate from an NABL-accredited lab is submitted with Form S5.
- Isolating devices must be accessible to WBSEDCL.
- **Periodic fitness testing: every 2 years for systems above 170 kW** (3 years up to 170 kW). Our 307 kWp plant falls in the 2-year group.
- Harmonics beyond limits can lead to disconnection.

## 8. What stays open

1. Gazette text of the WBERC 2025 regulations (capacity unit, RESCO terms).
2. FY 2026-27 tariff order and feed-in tariff.
3. Which licensee supplies the real site (assumed WBSEDCL).
4. Whether CEIG clearance applies at 11 kV.
