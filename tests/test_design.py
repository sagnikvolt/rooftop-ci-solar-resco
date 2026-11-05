import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "design"))
import sizing  # noqa: E402
import strings  # noqa: E402


class StringTests(unittest.TestCase):
    def test_voc_cold_hand_check(self):
        # 51.90 x (1 + 0.0026 x 21.6) = 51.90 x 1.05616 = 54.8147
        self.assertAlmostEqual(strings.voc_cold(), 54.8147, places=3)

    def test_vmp_hot_hand_check(self):
        # 43.56 x (1 - 0.0030 x 50) = 37.026
        self.assertAlmostEqual(strings.vmp_hot(), 37.026, places=3)

    def test_max_modules_is_17(self):
        # 18 modules gives 986.7 V, only 1.3 % under the 1,000 V MC4 limit, so 17
        self.assertEqual(strings.max_modules_per_string(), 17)

    def test_17_ok_18_rejected(self):
        self.assertTrue(strings.check(17)["voc_ok"])
        self.assertFalse(strings.check(18)["voc_ok"])

    def test_mppt_current(self):
        c = strings.check(17, strings_per_mppt=2)
        self.assertAlmostEqual(c["mppt_operating_current_a"], 25.94, places=2)
        self.assertTrue(c["mppt_operating_ok"])
        self.assertTrue(c["mppt_isc_ok"])
        self.assertFalse(strings.check(17, strings_per_mppt=3)["mppt_operating_ok"])


class SizingTests(unittest.TestCase):
    def test_final_design(self):
        d = sizing.design()
        self.assertEqual(d["n_modules"], 544)
        self.assertAlmostEqual(d["dc_kwp"], 544 * 0.565, places=6)
        self.assertEqual(d["strings_per_inverter"], 16)

    def test_design_inside_all_limits(self):
        d = sizing.design()
        self.assertLessEqual(d["dc_kwp"], d["roof_limit_kwp"])
        self.assertLessEqual(d["dc_kwp"], d["regulatory_limit_kw"])
        self.assertLessEqual(d["dc_kwp"], d["load_limit_kwp"])

    def test_roof_count_hand_check(self):
        # 58 m along ridge - 3 x ... : bay (58 - 2 x 2.2)/3 = 17.87 m -> 15 modules of 1.154 m;
        # 3 bays x 15 = 45 per row; 18.5 m / 2.298 m = 8 rows; 45 x 8 x 2 = 720
        n, per_row, rows = sizing.roof_module_count()
        self.assertEqual((n, per_row, rows), (720, 45, 8))

    def test_equal_east_west_split(self):
        d = sizing.design()
        self.assertEqual(d["n_strings"] % 4, 0)


if __name__ == "__main__":
    unittest.main()


def test_ac_current_matches_datasheet():
    import ac_side
    # datasheet max AC current for SG110CX is 158.8 A; 110 kVA / (sqrt3 x 400 V) = 158.77 A
    assert abs(ac_side.ac_current_a(110) - 158.8) < 0.1


def test_breaker_sizes():
    import ac_side
    r = ac_side.ac_side(2)
    assert r["breaker_per_inverter_a"] == 200      # 158.8 x 1.25 = 198.5 A -> 200 A
    assert r["breaker_main_a"] == 400              # 317.5 x 1.25 = 397 A -> 400 A


def test_commissioning_expected_voc():
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "commissioning"))
    import expected_values
    # 17 x 51.90 = 882.3 V at 25 degC; at 45 degC: 882.3 x (1 - 0.0026 x 20) = 836.4 V
    assert abs(expected_values.expected(25)["voc_v"] - 882.3) < 0.01
    assert abs(expected_values.expected(45)["voc_v"] - 836.42) < 0.05
