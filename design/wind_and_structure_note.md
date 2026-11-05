# Wind and structure note (screening level, not a structural design)

Purpose: show how wind is checked for a flush-mounted array on a metal-sheet roof, with every number traced to a source or marked ASSUMED. A structural engineer must check the actual roof before anything is built.

## 1. Basic wind speed

- IS 875 (Part 3):2015 gives a basic wind speed **Vb = 50 m/s for Kolkata (wind zone V)**. Source: https://infralens.in/handbook/wind-speed (secondary source, read 2026-11-05).
- Hooghly district is not listed separately on that page. Hooghly is next to Kolkata, so this note **assumes the same 50 m/s**. Check the IS 875 (Part 3) wind map or the code table before using it.

## 2. From basic wind speed to pressure (the formula, step by step)

IS 875 (Part 3) uses these steps:

1. Design wind speed: **Vz = Vb x k1 x k2 x k3 x k4**
   - k1 = risk factor (life of the building)
   - k2 = height and terrain factor
   - k3 = topography factor
   - k4 = importance factor (cyclone-prone areas)
2. Design wind pressure: **pz = 0.6 x Vz²** (pascals, with Vz in m/s)
3. Force on a surface: **F = (Cpe - Cpi) x pz x A**, where Cpe and Cpi are pressure coefficients and A is the area.

**Not done here:** the k factors and the pressure coefficients (Cpe, Cpi) come from tables in the code, which were not fetched this session. They are marked ASSUMED / open in `ASSUMPTIONS.md` rather than guessed.

### Illustration only (all k factors set to 1.0)

pz = 0.6 x 50² = 0.6 x 2,500 = **1,500 Pa = 1.5 kN/m²**.

This is a reference pressure, not a design value. The real design pressure on a roof edge or corner can be several times higher than the mid-roof value, and k factors can push it up or down.

## 3. Why wind matters most for this roof

- Modules lie **flush** on the roof at 7°, so there is little "sail" area. The main risk is **uplift** (suction), which tries to pull clamps out of the sheeting and purlins.
- The pull-out strength of the clamp-to-sheet fixing and the purlin strength are what govern. These depend on the roof and the clamp product, and are unknown here.
- Edge and ridge zones see the highest suction. This is one reason the layout keeps setbacks (1.0 m at eaves and gable ends, 0.5 m at the ridge).

## 4. Dead load of the array

From the module datasheet (see `VERIFICATION.md`): 32.5 kg and 2.278 m x 1.134 m = 2.583 m².

Dead load = 32.5 x 9.81 / 2.583 = **123 N/m² = 0.12 kN/m²** (modules only; rails and clamps add a little).

This is small compared with the 1.5 kN/m² reference wind pressure above, which is why the check on a light roof is about **fixings and purlins**, not about the weight of the modules.

## 5. What a real roof check needs (survey checklist items)

1. Roof sheet type, thickness and the spacing of purlins.
2. Roof age and corrosion state; is it fit for 25 years?
3. Clamp type (standing-seam clamp or through-fix) and its tested pull-out value from the supplier.
4. Structural engineer's sign-off on purlin and rafter capacity for the added load.
5. Local wind speed from the code table or wind map, and the k factors for the site.

## 6. Fire access and setbacks

The layout uses 1.0 m at eaves and gable ends and 0.5 m at the ridge. These are **design choices (ASSUMED)** for access and wind, not values taken from a regulation. No Indian regulation giving a required rooftop setback was found this session. Fire-safety practice found: warning signs and extinguishers in the inverter room, and compliance with the National Building Code and BIS standards (https://www.saurenergy.com/solar-energy-blog/how-to-ensure-safety-at-rooftop-solar-power-plants, a general article). Confirm local fire-authority requirements before design freeze.
