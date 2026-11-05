"""Equipment data used in the design. Values are from manufacturer datasheets
(see VERIFICATION.md). Change them here and every calculation follows."""

MODULE = {
    "name": "Waaree ELITE BiN-08-565",
    "pmax_w": 565.0,
    "voc_v": 51.90,
    "vmp_v": 43.56,
    "isc_a": 13.75,
    "imp_a": 12.97,
    "temp_coeff_pmax_pct": -0.30,   # %/degC
    "temp_coeff_voc_pct": -0.26,    # %/degC
    "temp_coeff_isc_pct": 0.046,    # %/degC
    "length_m": 2.278,
    "width_m": 1.134,
    "weight_kg": 32.5,
    "max_system_voltage_v": 1500.0,
    "max_series_fuse_a": 30.0,
}

INVERTER = {
    "name": "Sungrow SG110CX",
    "ac_kva_45c": 110.0,
    "max_dc_voltage_v": 1100.0,
    "mppt_min_v": 200.0,
    "mppt_max_v": 1000.0,
    "start_v": 250.0,
    "n_mppt": 9,
    "strings_per_mppt": 2,
    "max_input_current_per_mppt_a": 26.0,
    "max_isc_per_mppt_a": 40.0,
    "mc4_voltage_limit_v": 1000.0,   # datasheet footnote: supplied MC4 connectors not for systems that can exceed 1000 V
}
