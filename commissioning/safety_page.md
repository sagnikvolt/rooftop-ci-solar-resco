# Safety on a rooftop solar job

This is a plain-language page written for the project, not a replacement for the site's safety plan or the law.

## The three big hazards on this roof

1. **Falls.** A metal-sheet roof at 7° is slippery, has an open edge, and has **translucent skylight strips**. A skylight sheet may not carry a person. The layout keeps 0.5 m clear on each side of every skylight (ASSUMED value), and crews should cover or fence skylights with proper screens before work starts, use edge protection and wear harnesses on anchor lines.
2. **DC electricity.** A string of 17 modules gives up to about 932 V DC on a cold morning (design calculation) and cannot be switched off while there is light. Work on strings with the inverter DC switch off, cables disconnected at the connectors, and the string treated as live.
3. **Fire.** DC arcs do not extinguish by themselves. Use correct connectors, torque, UV-rated cable, and keep the inverter room tidy, signed, with extinguishers and sand buckets.

## Rules for the crew

- Lock out, tag out and test dead before touching any AC or DC conductor.
- PPE: helmets, harnesses, insulated gloves, non-slip footwear (from the safety article below).
- Secure ladders and scaffolding for roof access; the safety article calls for "secure use of ladders" and scaffolding on tin sheds.
- No work on the roof in rain, high wind or when the sheeting is wet; it is slippery.
- Clean modules in the early morning or evening, when they are cooler and produce less.
- Keep first-aid kit, fire extinguishers and sand buckets on site, and record on-site activities.
- Earth the plant per IS 3043 and fit lightning protection where the site assessment calls for it.

## Where this comes from

- General safety article (ladders, PPE, extinguishers, training, IS 3043, NBC compliance): https://www.saurenergy.com/solar-energy-blog/how-to-ensure-safety-at-rooftop-solar-power-plants (read 2026-11-05).
- 932 V string voltage and 0.5 m skylight keepout: this repository (`design/strings.py`, `survey/roof_data.json`).
- Items without a source above are ordinary working practice. A site-specific safety plan and the contractor's competent persons decide the details.
