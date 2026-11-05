"""Usable roof area after setbacks and obstacles.

How this works (worked example for the assumed roof in roof_data.json):
  Each slope is a rectangle: ridge_length x slope_length = 60 x 20 = 1,200 m2.
  Keep out of the way of panels:
    - a strip along the eave (lower edge), the ridge, and both gable ends
    - each translucent skylight strip, plus a safety clearance on both sides
  Remaining area per slope:
    along the ridge : 60 - 2 x 1.0 (gable setbacks)              = 58.0 m
    up the slope    : 20 - 1.0 (eave) - 0.5 (ridge)             = 18.5 m
    gross usable    : 58.0 x 18.5                                = 1,073 m2
    skylights       : 2 strips x (1.2 + 2 x 0.5) m wide x 18.5 m =    81.4 m2
    usable per slope: 1,073 - 81.4                               =  991.6 m2
  Two slopes: 1,983.2 m2.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def usable_area(roof):
    along = roof["ridge_length_m"] - 2 * roof["edge_setback_gable_m"]
    up = roof["slope_length_m"] - roof["edge_setback_eave_m"] - roof["ridge_setback_m"]
    gross = along * up
    keepout_width = roof["translucent_strip_width_m"] + 2 * roof["translucent_keepout_each_side_m"]
    skylights = roof["translucent_strips_per_slope"] * keepout_width * up
    return {"gross": gross, "skylights": skylights, "usable": gross - skylights}


def main():
    with open(os.path.join(HERE, "roof_data.json")) as f:
        roof = json.load(f)
    per_slope = usable_area(roof)
    total_roof = roof["ridge_length_m"] * roof["slope_length_m"] * len(roof["slopes"])
    total_usable = per_slope["usable"] * len(roof["slopes"])
    print(f"Roof area (both slopes): {total_roof:,.1f} m2")
    print(f"Per slope: gross usable {per_slope['gross']:,.1f} m2, skylight keep-out {per_slope['skylights']:,.1f} m2, usable {per_slope['usable']:,.1f} m2")
    print(f"Total usable: {total_usable:,.1f} m2 ({100 * total_usable / total_roof:.0f}% of roof)")


if __name__ == "__main__":
    main()
