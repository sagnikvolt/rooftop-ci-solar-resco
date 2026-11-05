import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "survey"))
import hourly_load as hl  # noqa: E402


class HourlyLoadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile = hl.build_profile()
        cls.summary = hl.summary(cls.profile)

    def test_has_8760_hours(self):
        self.assertEqual(len(self.profile), 8760)

    def test_annual_energy_matches_assumption(self):
        # hand check: 12 months x 120,000 kWh
        self.assertAlmostEqual(self.summary["annual_kwh"], 1_440_000, places=3)

    def test_average_load_hand_check(self):
        self.assertAlmostEqual(self.summary["average_kw"], 1_440_000 / 8760, places=6)

    def test_peak_below_contract_demand(self):
        self.assertLess(self.summary["peak_kw"], self.summary["contract_demand_kw"])

    def test_sunday_lower_than_weekday(self):
        sun = [r[4] for r in self.profile if r[2] == 6 and 8 <= r[3] < 16]
        mon = [r[4] for r in self.profile if r[2] == 0 and 8 <= r[3] < 16]
        self.assertLess(sum(sun) / len(sun), 0.5 * sum(mon) / len(mon))

    def test_repeatable(self):
        self.assertEqual(self.profile[100][4], hl.build_profile()[100][4])


if __name__ == "__main__":
    unittest.main()
