#!/usr/bin/env python3
"""Fail-closed checker for PB08 installed-axis/structure mass evidence.

This tool validates evidence completeness and arithmetic only. It does not
perform a physical measurement, freeze Quad/Hexa, or establish flight readiness.
"""
import argparse, json, math, statistics, sys
from pathlib import Path

REQUIRED_REPEATS = 3
SCREEN_GAIN_KG = 2.025

def finite_pos(x):
    return isinstance(x, (int, float)) and math.isfinite(x) and x > 0

def fail(errors, msg):
    errors.append(msg)

def check_repeats(errors, label, values, reported):
    if not isinstance(values, list) or len(values) < REQUIRED_REPEATS or not all(finite_pos(v) for v in values):
        fail(errors, f"{label}: require >= {REQUIRED_REPEATS} positive finite repeat measurements")
        return
    if not finite_pos(reported):
        fail(errors, f"{label}: reported mass missing/invalid")
        return
    mean = statistics.fmean(values)
    tol = max(0.1, abs(mean) * 1e-6)
    if abs(reported - mean) > tol:
        fail(errors, f"{label}: reported mass {reported} g != repeat mean {mean:.6f} g")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("record", type=Path)
    args = ap.parse_args()
    d = json.loads(args.record.read_text(encoding="utf-8"))
    e = []
    if d.get("physical_measurement") is not True: fail(e, "physical_measurement must be true for a populated result")
    art=d.get("article",{}); inst=d.get("instrumentation",{}); b=d.get("installed_axis_boundary",{}); am=d.get("installed_axis_mass",{}); sb=d.get("structure_boundary",{}); sm=d.get("structure_mass",{}); rv=d.get("review",{})
    for k in ("vehicle_configuration_revision","propulsion_axis_revision","frame_revision","measurement_date","operator"):
        if not art.get(k): fail(e, f"article.{k} required")
    for k in ("scale_make_model","scale_serial","calibration_reference"):
        if not inst.get(k): fail(e, f"instrumentation.{k} required")
    if not finite_pos(inst.get("resolution_g")): fail(e,"instrumentation.resolution_g must be positive")
    if inst.get("calibration_valid_on_measurement_date") is not True: fail(e,"valid calibration required")
    for k in ("motor_included","propeller_included","esc_included","esc_baseplate_enclosure_included","axis_harness_connectors_included","mounting_hardware_included"):
        if b.get(k) is not True: fail(e, f"installed-axis boundary incomplete: {k} must be explicitly true")
    if b.get("arm_structure_included") is not False: fail(e,"arm_structure_included must be false to avoid double counting structure delta")
    check_repeats(e,"installed_axis",am.get("repeat_measurements_g"),am.get("reported_mass_g"))
    if not finite_pos(am.get("uncertainty_g")) or not am.get("raw_data_ref"): fail(e,"installed-axis uncertainty and raw_data_ref required")
    for k in ("quad_common_structure_revision","hexa_common_structure_revision"):
        if not sb.get(k): fail(e,f"structure_boundary.{k} required")
    if sb.get("same_payload_battery_mission_equipment_basis") is not True: fail(e,"Quad/Hexa structure comparison must use same payload/battery/mission-equipment basis")
    if sb.get("axis_hardware_excluded_from_structure_delta") is not True: fail(e,"axis hardware must be excluded from structure delta")
    check_repeats(e,"quad_structure",sm.get("quad_repeat_measurements_g"),sm.get("quad_reported_mass_g"))
    check_repeats(e,"hexa_structure",sm.get("hexa_repeat_measurements_g"),sm.get("hexa_reported_mass_g"))
    q,h,delta=sm.get("quad_reported_mass_g"),sm.get("hexa_reported_mass_g"),sm.get("hexa_minus_quad_delta_g")
    if finite_pos(q) and finite_pos(h):
        expected=h-q
        if not isinstance(delta,(int,float)) or not math.isfinite(delta) or abs(delta-expected)>max(0.1,abs(expected)*1e-6): fail(e,"hexa_minus_quad_structure_delta arithmetic inconsistent")
    if not finite_pos(sm.get("uncertainty_g")) or not sm.get("raw_data_ref"): fail(e,"structure uncertainty and raw_data_ref required")
    for k in ("boundary_reviewed","raw_data_reviewed","calibration_reviewed"):
        if rv.get(k) is not True: fail(e,f"review.{k} must be true")
    if not rv.get("reviewer") or not rv.get("review_date"): fail(e,"reviewer and review_date required")
    decision=None
    if not e and finite_pos(am.get("reported_mass_g")) and isinstance(delta,(int,float)) and math.isfinite(delta):
        penalty_kg=2*am["reported_mass_g"]/1000 + delta/1000
        decision={"hexa_incremental_mass_penalty_kg":round(penalty_kg,6),"screen_gain_kg":SCREEN_GAIN_KG,"mass_screen_margin_kg":round(SCREEN_GAIN_KG-penalty_kg,6),"mass_screen_only":"HEXA_FAVORED" if penalty_kg<SCREEN_GAIN_KG else ("QUAD_FAVORED" if penalty_kg>SCREEN_GAIN_KG else "TIE")}
    out={"schema_check":"PASS" if not e else "FAIL","errors":e,"derived_mass_trade_screen":decision,"physical_qualification":False,"rotor_architecture_frozen":False,"note":"PASS validates record completeness/arithmetic only; degraded-mode policy and remaining G0/G1 evidence are still required."}
    print(json.dumps(out,indent=2))
    return 0 if not e else 2

if __name__ == "__main__": sys.exit(main())
