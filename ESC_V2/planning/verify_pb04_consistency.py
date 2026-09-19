#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "ESC_V2" / "planning"


def load(name: str):
    return json.loads((P / name).read_text(encoding="utf-8"))


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(f"FAIL: {msg}")


pb = load("PRODUCT_BASELINE_PB-04.json")
mission = load("mission_requirements.json")
g1 = load("G1_REQUIREMENTS_MATRIX.json")
progress = load("REQUIREMENTS_PROGRESS.json")
master = load("REQUIREMENTS_MASTER.json")

require(pb["revision"] == "PB-04", "product baseline revision")

req = mission["requirements"]
require(req["flight_profile"]["target_total_flight_time_min"] == 10, "10 min total mission target")
require(req["flight_profile"]["target_hover_time_min"] == 10, "10 min hover-equivalent sizing target")
require(abs(req["flight_profile"]["reserve_energy_fraction"] - 0.20) < 1e-12, "20% energy sizing reserve")
require(req["propulsion"]["controller_electrical_rpm_capability_min"] == 90000, "90 keRPM controller capability")

v_outer = req["battery"]["outer_full_charge_system_ceiling_v"]
kv = req["propulsion"]["motor_kv_rpm_per_v"]
pole_pairs = req["propulsion"]["reference_motor_pole_pairs"]
erpm_screen = v_outer * kv * pole_pairs
require(erpm_screen == 75600, "80 V / 45 KV / 21 pole-pair eRPM screen")
require(req["propulsion"]["controller_electrical_rpm_capability_min"] > erpm_screen, "controller capability must exceed frozen-envelope no-load screen")
require(req["propulsion"]["controller_electrical_rpm_capability_min"] / erpm_screen >= 1.15, "at least 15% controller eRPM headroom")

require(req["esc"]["pwm_frequency_hz"] is None, "PWM must remain OPEN before motor inductance evidence")
require(req["esc"]["pwm_preferred_analysis_window_hz"] == [24000, 32000], "preferred PWM analysis window")

summary = g1["summary"]
require(summary == {"required_rows": 46, "pass": 28, "open": 18}, "G1 summary must be 28/46")
require(progress["g1_system_freeze"]["pass_rows"] == 28, "progress G1 pass count")
require(progress["g1_system_freeze"]["required_rows"] == 46, "progress G1 required count")
require(abs(progress["g1_system_freeze"]["percent"] - 60.9) < 1e-12, "progress G1 percentage")
require(master["progress"]["g1_pass_rows"] == 28, "master G1 pass count")
require(abs(master["progress"]["g1_system_freeze_value_closure_percent"] - 60.9) < 1e-12, "master G1 percentage")
require(master["child_requirement_authorities"]["product_baseline"] == "PRODUCT_BASELINE_PB-04.json", "PB04 master authority")

print("PASS")
print(f"erpm_screen={int(erpm_screen)}")
print(f"controller_capability={req['propulsion']['controller_electrical_rpm_capability_min']}")
print(f"erpm_headroom_percent={(req['propulsion']['controller_electrical_rpm_capability_min'] / erpm_screen - 1) * 100:.1f}")
print("mission_target_min=10")
print("energy_sizing_reserve_percent=20")
print("pwm_frozen=false")
print("pwm_preferred_window_hz=24000..32000")
print("g1_pass=28/46")
