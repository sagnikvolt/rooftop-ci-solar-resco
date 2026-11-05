// Same arithmetic as resco/model.py, so the calculator on the page matches the Python model.
// Energy flows come from the table in data.js (PVsyst output against the assumed load);
// everything after that (tariffs, degradation, cash flows, IRR) is computed here.
(function (root) {
  function interp(curve, kwp) {
    var lo = curve[0], hi = curve[curve.length - 1];
    if (kwp <= lo.kwp) return scale(lo, kwp / lo.kwp);
    if (kwp >= hi.kwp) return scale(hi, kwp / hi.kwp);
    for (var i = 0; i < curve.length - 1; i++) {
      var a = curve[i], b = curve[i + 1];
      if (kwp >= a.kwp && kwp <= b.kwp) {
        var t = (kwp - a.kwp) / (b.kwp - a.kwp);
        return { pv_kwh: a.pv_kwh + t * (b.pv_kwh - a.pv_kwh),
                 self_kwh: a.self_kwh + t * (b.self_kwh - a.self_kwh),
                 export_kwh: a.export_kwh + t * (b.export_kwh - a.export_kwh) };
      }
    }
  }
  function scale(r, f) { return { pv_kwh: r.pv_kwh * f, self_kwh: r.self_kwh * f, export_kwh: r.export_kwh * f }; }

  function irr(cf) {
    function npv(r) { var s = 0; for (var t = 0; t < cf.length; t++) s += cf[t] / Math.pow(1 + r, t); return s; }
    var lo = -0.99, hi = 1.0;
    if (npv(lo) * npv(hi) > 0) return null;
    for (var k = 0; k < 200; k++) {
      var mid = (lo + hi) / 2;
      if (npv(lo) * npv(mid) <= 0) hi = mid; else lo = mid;
    }
    return (lo + hi) / 2;
  }

  function run(p, curve) {
    var e = interp(curve, p.plant_kwp);
    var capex = p.plant_kwp * 1000 * p.capex_per_wp;
    var rescoTariff0 = p.grid_energy_tariff * (1 - p.resco_discount);
    var cash = [-capex], saving = [], cum = -capex, payback = null, cumulative = [-capex];
    for (var yr = 1; yr <= p.years; yr++) {
      var derate = (1 - p.first_year_degradation) * Math.pow(1 - p.annual_degradation, yr - 1);
      var esc = Math.pow(1 + p.escalation, yr - 1);
      var selfKwh = e.self_kwh * derate, expKwh = e.export_kwh * derate;
      var revenue = selfKwh * rescoTariff0 * esc + expKwh * p.feed_in_tariff * esc;
      var om = capex * p.om_pct_of_capex / 100 * esc;
      var cf = revenue - om;
      cash.push(cf);
      saving.push(selfKwh * (p.grid_energy_tariff - rescoTariff0) * esc);
      var prev = cum; cum += cf; cumulative.push(cum);
      if (payback === null && cum >= 0) payback = (yr - 1) + (-prev / cf);
    }
    var npvSum = 0;
    for (var t = 0; t < cash.length; t++) npvSum += cash[t] / Math.pow(1 + p.discount_rate, t);
    return { energy: e, capex: capex, rescoTariff0: rescoTariff0, irr: irr(cash), payback: payback, npv: npvSum,
             saving1: saving[0], savingTotal: saving.reduce(function (a, b) { return a + b; }, 0),
             cumulative: cumulative };
  }

  var api = { run: run, irr: irr, interp: interp };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.RescoModel = api;
})(typeof window !== "undefined" ? window : this);
