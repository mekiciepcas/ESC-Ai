#!/usr/bin/env python3
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def req(cond, msg):
    if not cond:
        raise SystemExit(f"FAIL: {msg}")

model = load("PHASE_CURRENT_MODEL_PB02.json")
pb = load("PRODUCT_BASELINE_PB-03.json")
g1 = load("G1_REQUIREMENTS_MATRIX.json")
mission = load("mission_requirements.json")
progress = load("REQUIREMENTS_PROGRESS.json")

# Recompute the two torque-constant bounds from the published proxy back-EMF constants.
omega_krpm = 1000.0 * 2.0 * math.pi / 60.0
ke_peak = model["proxy_electrical_constants"]["back_emf_vpk_per_krpm"] / omega_krpm
ke_rms = model["proxy_electrical_constants"]["back_emf_vrms_per_krpm"] / omega_krpm
kt_from_peak = math.sqrt(3.0 / 2.0) * ke_peak
kt_from_rms = math.sqrt(3.0) * ke_rms
req(abs(kt_from_peak - model["torque_constant_model"]["kt_rms_from_vpk_nm_per_a"]) < 5e-6, "Kt from Vpk mismatch")
req(abs(kt_from_rms - model["torque_constant_model"]["kt_rms_from_vrms_nm_per_a"]) < 5e-6, "Kt from Vrms mismatch")

# Recompute the two sizing parents used for the frozen requirements.
rated_torque = model["manufacturer_curve_points"]["rated_27kg"]["torque_nm"]
max_torque = model["manufacturer_curve_points"]["published_curve_max"]["torque_nm"]
conservative_kt = min(kt_from_peak, kt_from_rms)
rated_upper = rated_torque / conservative_kt
max_upper = max_torque / conservative_kt
req(rated_upper * 1.15 <= 125.0, "125 A continuous requirement no longer covers rated model +15%")
req(max_upper * 1.10 <= 265.0, "265 A overload requirement no longer covers curve max model +10%")
req(265.0 * math.sqrt(2.0) <= 375.0, "375 A instantaneous peak does not cover 265 Arms sine peak")
req(400.0 > 375.0, "sense range does not exceed design peak")

# PB-03 additive decisions.
by_id = {d["id"]: d for d in pb["new_frozen_decisions"]}
req(by_id["PB-022"]["value"] == 125, "PB-022 mismatch")
req(by_id["PB-023"]["value"]["rms_a_min"] == 265, "PB-023 RMS mismatch")
req(by_id["PB-023"]["value"]["instantaneous_peak_a_min"] == 375, "PB-023 peak mismatch")
req(by_id["PB-024"]["value"] == {"negative_a": -400, "positive_a": 400}, "PB-024 sense range mismatch")

# G1 rows and mission authority must agree.
rows = {r["id"]: r for r in g1["rows"]}
for rid in ("G1-03", "G1-04", "G1-08"):
    req(rows[rid]["status"] == "PASS", f"{rid} is not PASS")
req(g1["product_baseline_authority"] == "PRODUCT_BASELINE_PB-03.json", "G1 authority is not PB-03")
req(g1["summary"] == {"required_rows": 46, "pass": 25, "open": 21}, "G1 summary mismatch")

esc = mission["requirements"]["esc"]
req(esc["phase_rms_current_a"] == 125, "mission continuous phase current mismatch")
req(esc["phase_overload_rms_current_a"] == 265, "mission overload RMS mismatch")
req(esc["phase_peak_current_a"] == 375, "mission phase peak mismatch")
req(esc["phase_current_sense_range_a"] == [-400, 400], "mission sense range mismatch")

req(progress["g1_system_freeze"]["pass_rows"] == 25, "progress pass rows mismatch")
req(progress["g1_system_freeze"]["open_rows"] == 21, "progress open rows mismatch")
req(abs(progress["g1_system_freeze"]["percent"] - 54.3) < 1e-9, "progress percent mismatch")

print("PASS")
print(f"Kt_rms_bound_Nm_per_Arms={min(kt_from_peak, kt_from_rms):.6f}..{max(kt_from_peak, kt_from_rms):.6f}")
print(f"rated_model_upper_Arms={rated_upper:.2f}")
print(f"curve_max_model_upper_Arms={max_upper:.2f}")
print("frozen_continuous_phase_Arms=125")
print("frozen_overload_phase_Arms_3s=265")
print("frozen_instantaneous_phase_peak_A=375")
print("frozen_phase_sense_range_A=+/-400")
