#!/usr/bin/env python3
"""PB-08 installed non-cell pack-resistance evidence verifier.

Fails closed: an unpopulated template or incomplete/mismatched evidence never produces
PASS. This script performs arithmetic/consistency checks only; it is not physical
qualification evidence.
"""
import argparse, json, math, sys
from pathlib import Path

REQ_SCHEMA = "PB08-PACK-R-MEAS-01"

def finite_pos(x):
    return isinstance(x, (int, float)) and math.isfinite(x) and x > 0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("result", type=Path)
    args = ap.parse_args()
    d = json.loads(args.result.read_text(encoding="utf-8"))
    errors, warnings = [], []
    if d.get("schema_revision") != REQ_SCHEMA:
        errors.append("unsupported schema_revision")
    a, c, i, b, m, ac, r = (d.get(k, {}) for k in ["article_under_test","test_condition","instrumentation","measurement_boundaries","measurement","acceptance_context","review"])
    required_identity = ["pack_id","pack_revision","cell_mpn","series_count","parallel_count","configuration_evidence_ref"]
    for k in required_identity:
        if a.get(k) in (None, "", []): errors.append(f"missing article_under_test.{k}")
    for k in ["pack_temperature_c","soc_percent","soh_or_cycle_state"]:
        if c.get(k) in (None, ""): errors.append(f"missing test_condition.{k}")
    if i.get("four_wire_kelvin_method_confirmed") is not True: errors.append("four-wire/Kelvin method not confirmed")
    if not i.get("calibration_refs"): errors.append("missing instrumentation.calibration_refs")
    if not b.get("source_voltage_points") or not b.get("load_voltage_points"): errors.append("measurement boundaries incomplete")
    il, ih, vl, vh = (m.get(k) for k in ["current_low_a","current_high_a","voltage_drop_low_v","voltage_drop_high_v"])
    if not all(isinstance(x,(int,float)) and math.isfinite(x) for x in [il,ih,vl,vh]):
        errors.append("four finite low/high current and voltage-drop values required")
    else:
        di, dv = ih-il, vh-vl
        if di <= 0: errors.append("delta current must be > 0")
        else:
            calc_r = 1000.0*dv/di
            if calc_r <= 0: errors.append("derived non-cell resistance must be > 0")
            reported = m.get("derived_noncell_resistance_mohm")
            if not finite_pos(reported): errors.append("missing/invalid derived_noncell_resistance_mohm")
            elif not math.isclose(reported, calc_r, rel_tol=1e-3, abs_tol=1e-4): errors.append(f"reported resistance inconsistent; calculated {calc_r:.6g} mOhm")
    if not m.get("raw_data_ref"): errors.append("missing measurement.raw_data_ref")
    if not isinstance(m.get("repeat_count"), int) or m.get("repeat_count",0) < 2: errors.append("repeat_count must be >= 2")
    if len(m.get("repeat_results_mohm",[])) != m.get("repeat_count"): errors.append("repeat_results_mohm length must equal repeat_count")
    if not finite_pos(m.get("uncertainty_mohm")): warnings.append("positive uncertainty_mohm not supplied")
    current, ocv, cell_rdc, cell_pack_r, noncell = ac.get("applicable_pack_current_a"), ac.get("condition_matched_pack_ocv_v"), ac.get("condition_matched_cell_rdc_mohm"), ac.get("derived_cell_only_pack_resistance_mohm"), m.get("derived_noncell_resistance_mohm")
    if all(finite_pos(x) for x in [current,ocv,cell_rdc,cell_pack_r,noncell]) and finite_pos(a.get("series_count")) and finite_pos(a.get("parallel_count")):
        expected_cell_pack = cell_rdc*a["series_count"]/a["parallel_count"]
        if not math.isclose(cell_pack_r, expected_cell_pack, rel_tol=1e-3, abs_tol=1e-4): errors.append(f"cell-only pack resistance inconsistent; calculated {expected_cell_pack:.6g} mOhm")
        loaded = ocv-current*(cell_pack_r+noncell)/1000.0
        reported_loaded = ac.get("predicted_loaded_bus_v")
        if not isinstance(reported_loaded,(int,float)) or not math.isclose(reported_loaded, loaded, rel_tol=1e-3, abs_tol=1e-3): errors.append(f"predicted_loaded_bus_v missing/inconsistent; calculated {loaded:.6g} V")
        expected_result = "PASS" if loaded >= ac.get("pb08_loaded_floor_v",36.0) else "FAIL"
        if ac.get("loaded_floor_result") != expected_result: errors.append(f"loaded_floor_result must be {expected_result} for supplied arithmetic")
    else:
        errors.append("acceptance context incomplete; cannot evaluate 36 V loaded floor")
    if r.get("evidence_level") in (None,"","UNPOPULATED_TEMPLATE") or r.get("disposition") in (None,"","OPEN"): errors.append("review/evidence disposition not closed")
    out={"status":"PASS" if not errors else "FAIL_CLOSED","errors":errors,"warnings":warnings,"physical_qualification":False}
    print(json.dumps(out,indent=2))
    return 0 if not errors else 2
if __name__ == "__main__": sys.exit(main())
