#!/usr/bin/env python3
"""Fail-closed verifier for PB-08 P50B condition-matched OCV/Rdc evidence.

This tool validates evidence structure and arithmetic only. It does not create
physical evidence, interpolate missing data, or establish pack qualification.
"""
import json
import math
import sys
from pathlib import Path

TOL_MOHM = 0.02


def present(v):
    return v is not None and v != "" and v != []


def fail(msg, errors):
    errors.append(msg)


def main(path):
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    errors = []
    art = d.get("cell_article", {})
    inst = d.get("instrumentation", {})
    method = d.get("test_method", {})
    review = d.get("review", {})
    points = d.get("points", [])

    for k in ("sample_id", "lot_or_batch_id", "cycle_count", "soh_percent", "soh_basis"):
        if not present(art.get(k)): fail(f"cell_article.{k} missing", errors)
    for k in ("voltage_instrument_id", "current_instrument_id", "temperature_instrument_id", "raw_data_ref"):
        if not present(inst.get(k)): fail(f"instrumentation.{k} missing", errors)
    if not inst.get("calibration_refs"): fail("instrumentation.calibration_refs missing", errors)
    for k in ("soc_preparation_method", "rest_time_before_ocv_s", "temperature_stabilization_criterion", "pulse_duration_s", "rdc_sample_time_after_pulse_start_s"):
        if not present(method.get(k)): fail(f"test_method.{k} missing", errors)
    if not review.get("physical_measurement"): fail("review.physical_measurement is not true", errors)
    if not review.get("condition_matching_confirmed"): fail("condition matching not confirmed", errors)
    if not review.get("raw_data_reviewed"): fail("raw data not reviewed", errors)
    if not review.get("calibration_reviewed"): fail("calibration not reviewed", errors)
    for k in ("reviewer", "review_date"):
        if not present(review.get(k)): fail(f"review.{k} missing", errors)

    valid_points = 0
    for i, p in enumerate(points):
        prefix = f"points[{i}]"
        req = ("point_id","soc_percent","cell_temperature_c","soh_percent","pre_pulse_ocv_v","pulse_current_a","pulse_voltage_v","rdc_mohm_reported","repeat_count","repeat_results_ref","uncertainty_or_tolerance_note")
        missing = [k for k in req if not present(p.get(k))]
        if missing:
            fail(f"{prefix} missing: {', '.join(missing)}", errors)
            continue
        if p["pulse_current_a"] <= 0:
            fail(f"{prefix}.pulse_current_a must be > 0 for DISCHARGE", errors); continue
        if p["pre_pulse_ocv_v"] <= p["pulse_voltage_v"]:
            fail(f"{prefix} has non-positive discharge voltage drop", errors); continue
        rcalc = 1000.0 * (p["pre_pulse_ocv_v"] - p["pulse_voltage_v"]) / p["pulse_current_a"]
        if not math.isclose(rcalc, p["rdc_mohm_reported"], abs_tol=TOL_MOHM, rel_tol=0.002):
            fail(f"{prefix} Rdc mismatch: recalculated={rcalc:.6f} mOhm reported={p['rdc_mohm_reported']} mOhm", errors)
        if present(p.get("rdc_mohm_recalculated")) and not math.isclose(rcalc, p["rdc_mohm_recalculated"], abs_tol=TOL_MOHM, rel_tol=0.002):
            fail(f"{prefix}.rdc_mohm_recalculated inconsistent", errors)
        if p["repeat_count"] < 2:
            fail(f"{prefix}.repeat_count must be >= 2", errors)
        if p.get("valid_for_envelope") is True and not errors:
            valid_points += 1

    if not points: fail("no measurement points", errors)
    if valid_points == 0: fail("no fail-closed valid envelope point", errors)

    out = {
        "verifier": "PB08-P50B-OCV-RDC-VERIFY-01",
        "evidence_record_valid": not errors,
        "valid_envelope_points": valid_points if not errors else 0,
        "physical_qualification": False,
        "pack_loaded_floor_compliance": None,
        "errors": errors,
        "note": "PASS validates record completeness/condition matching/arithmetic only; it is not cell, pack, flight, thermal, or safety qualification."
    }
    print(json.dumps(out, indent=2))
    return 0 if not errors else 2


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "PB08_P50B_OCV_RDC_MEASUREMENT_RESULT.template.json"
    raise SystemExit(main(target))
