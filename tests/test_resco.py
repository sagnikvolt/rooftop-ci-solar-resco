import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "resco"))
import model  # noqa: E402


class ResultTests(unittest.TestCase):
    def test_irr_hand_check(self):
        # pay 100 now, get 110 next year -> 10 % return
        assert abs(model.irr([-100, 110]) - 0.10) < 1e-6

    def test_pv_matches_pvsyst_total(self):
        e = model.year1_energy(307.4)
        assert abs(e["pv_kwh"] - 409153) / 409153 < 0.002      # PVsyst report: 409,153 kWh/yr

    def test_energy_balance_and_limits(self):
        e = model.year1_energy(307.4)
        assert abs(e["pv_kwh"] - e["self_kwh"] - e["export_kwh"]) < 1e-6
        assert 0 < e["self_kwh"] <= e["pv_kwh"]

    def test_bigger_plant_exports_more_share(self):
        small = model.year1_energy(100)["self_fraction"]
        big = model.year1_energy(500)["self_fraction"]
        assert big < small

    def test_discount_moves_returns_the_right_way(self):
        low = model.run(resco_discount=0.10)
        high = model.run(resco_discount=0.40)
        assert low["project_irr"] > high["project_irr"]                         # RESCO earns less at a bigger discount
        assert low["client_saving_year1_rs"] < high["client_saving_year1_rs"]   # client saves more

    def test_capex_check_by_hand(self):
        r = model.run()
        assert abs(r["capex_rs"] - 307.4 * 1000 * 38) < 1

    def test_grid_tariff_is_energy_charge_not_demand_charge(self):
        # WBSEDCL Rate E(B): 707/706/705 P/kWh energy, 384 Rs/kVA/month demand (VERIFICATION.md, corrected 5 Nov 2026)
        assert 7.05 <= model.INPUTS["grid_energy_tariff"] <= 7.07
        assert model.DEMAND_CHARGE_RS_PER_KVA_MONTH == 384
        assert model.INPUTS["grid_energy_tariff"] > model.INPUTS["feed_in_tariff"]     # self-use must be worth more than export

    def test_tod_case_is_close_to_base_and_uses_daytime_rate(self):
        base, tod = model.run(), model.run(tod=True)
        avoided = tod["inputs"]["grid_energy_tariff"]
        assert 6.9 < avoided < 7.0                       # almost all solar falls in the 06-17 h band at Rs 6.94
        assert abs(base["project_irr"] - tod["project_irr"]) < 0.01

    def test_base_case_numbers(self):
        r = model.run()
        assert abs(r["resco_tariff_year1"] - 5.648) < 0.001
        assert 0.19 < r["project_irr"] < 0.20
        assert 5.0 < r["payback_years"] < 5.6
