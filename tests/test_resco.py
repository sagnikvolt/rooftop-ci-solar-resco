import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "resco"))
import model  # noqa: E402


def test_irr_hand_check():
    # pay 100 now, get 110 next year -> 10 % return
    assert abs(model.irr([-100, 110]) - 0.10) < 1e-6


def test_pv_matches_pvsyst_total():
    e = model.year1_energy(307.4)
    assert abs(e["pv_kwh"] - 409153) / 409153 < 0.002      # PVsyst report: 409,153 kWh/yr


def test_energy_balance_and_limits():
    e = model.year1_energy(307.4)
    assert abs(e["pv_kwh"] - e["self_kwh"] - e["export_kwh"]) < 1e-6
    assert 0 < e["self_kwh"] <= e["pv_kwh"]


def test_bigger_plant_exports_more_share():
    small = model.year1_energy(100)["self_fraction"]
    big = model.year1_energy(500)["self_fraction"]
    assert big < small


def test_discount_moves_returns_the_right_way():
    low = model.run(resco_discount=0.10)
    high = model.run(resco_discount=0.40)
    assert low["project_irr"] > high["project_irr"]                         # RESCO earns less at a bigger discount
    assert low["client_saving_year1_rs"] < high["client_saving_year1_rs"]   # client saves more


def test_capex_check_by_hand():
    r = model.run()
    assert abs(r["capex_rs"] - 307.4 * 1000 * 38) < 1
