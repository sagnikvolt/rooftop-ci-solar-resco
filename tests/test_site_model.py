"""Checks that the calculator on the website (site/model.js) gives the same answers as resco/model.py."""
import json
import os
import shutil
import subprocess
import sys
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "resco"))
import model  # noqa: E402

JS = """
global.window = {};
require(process.argv[1] + '/site/data.js');
const M = require(process.argv[1] + '/site/model.js');
const D = window.DATA;
const out = [];
for (const o of [{}, {resco_discount: 0.4, capex_per_wp: 50}, {plant_kwp: 150, years: 15}]) {
  const r = M.run(Object.assign({}, D.inputs, o), D.curve);
  out.push({irr: r.irr, payback: r.payback, saving1: r.saving1});
}
console.log(JSON.stringify(out));
"""


class SiteModelTests(unittest.TestCase):
    @unittest.skipIf(shutil.which("node") is None, "node not installed")
    def test_js_matches_python(self):
        res = subprocess.run(["node", "-e", JS, os.path.abspath(ROOT)], capture_output=True, text=True, check=True)
        js = json.loads(res.stdout)
        cases = [{}, {"resco_discount": 0.4, "capex_per_wp": 50}, {"plant_kwp": 150, "years": 15}]
        for j, c in zip(js, cases):
            p = model.run(**c)
            assert abs(j["irr"] - p["project_irr"]) < 0.002           # curve interpolation allows a tiny gap
            assert abs(j["saving1"] - p["client_saving_year1_rs"]) / p["client_saving_year1_rs"] < 0.003
