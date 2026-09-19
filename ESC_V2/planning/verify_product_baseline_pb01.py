#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANNING = ROOT / "planning"


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def require(cond, message):
    if not cond:
        raise SystemExit(f"FAIL: {message}")


def row_map(matrix):
    return {row["id"]: row for row in matrix["rows"]}


pb = load(PLANNING / "PRODUCT_BASELINE_PB-01.json")
mission = load(PLANNING / "mission_requirements.json")
design = load(ROOT / "design_basis.json")
g1 = load(PLANNING / "G1_REQUIREMENTS_MATRIX.json")
progress = load(PLANNING / "REQUIREMENTS_PROGRESS.json")

require(pb["revision"] == "PB-01", "unexpected product baseline revision")
require(pb["status"] == "PARTIAL_PRODUCT_BASELINE_FROZEN", "PB-01 must be frozen partial baseline")

frozen = {d["id"]: d for d in pb["frozen_decisions"]}
for required_id in [f"PB-{i:03d}" for i in range(1, 11)]:
    require(required_id in frozen, f"missing {required_id}")

vehicle = mission["requirements"]["vehicle"]
iface = mission["requirements"]["control_and_interface"]
sysreq = design["system_requirement"]

require(vehicle["architecture"] == "X8_COAXIAL_4_ARM_8_INDEPENDENT_PROPULSION_CHANNELS", "mission architecture drift")
require(vehicle["rotor_count"] == 8, "mission rotor count drift")
require(vehicle["coaxial_packaging_baseline"] is True, "coaxial baseline drift")
require(vehicle["single_motor_failure_requirement"] == "CONTROLLED_LANDING_REQUIRED", "failure policy drift")
require(vehicle["continued_hover_at_max_payload_after_single_failure_required"] is False, "continued-hover policy drift")
require(iface["flight_controller_interface"] == "CAN_FD_CAPABLE_CLASSIC_CAN_COMPATIBLE", "FC interface drift")
require(iface["automatic_rearm_after_fault_or_reset"] is False, "re-arm policy drift")

require(sysreq["vehicle_architecture"] == vehicle["architecture"], "design basis vehicle architecture mismatch")
require(sysreq["rotor_count"] == 8, "design basis rotor count mismatch")
require(sysreq["dc_bus_full_charge_max_v"] == 80.0, "80 V bus ceiling drift")
require(sysreq["repetitive_dc_bus_and_switching_transient_ceiling_v"] == 120.0, "120 V transient ceiling drift")
require(sysreq["normal_operation_may_rely_on_mosfet_avalanche"] is False, "avalanche policy drift")
require(sysreq["power_semiconductor_vds_class_min_v"] == 150, "150 V semiconductor class drift")
require(sysreq["legacy_drv8353_allowed_in_u1_primary_baseline"] is False, "DRV8353 exclusion drift")
require(sysreq["flight_controller_interface"] == iface["flight_controller_interface"], "design/mission CAN mismatch")
require(sysreq["arming_policy"]["automatic_rearm_after_fault_or_reset"] is False, "design basis re-arm drift")

rows = row_map(g1)
expected_pass = {
    "G0-01",
    "G0-13",
    "G1A-01",
    "G1A-02",
    "G1C-04",
    "G1C-05",
    "G1-17",
    "G1-18",
}
actual_pass = {rid for rid, row in rows.items() if row["status"] == "PASS"}
require(actual_pass == expected_pass, f"unexpected PASS set: {sorted(actual_pass)}")
require(g1["summary"]["required_rows"] == 46, "G1 required row count drift")
require(g1["summary"]["pass"] == 8, "G1 pass count drift")
require(g1["summary"]["open"] == 38, "G1 open count drift")
require(progress["g1_system_freeze"]["pass_rows"] == 8, "progress pass count mismatch")
require(progress["g1_system_freeze"]["open_rows"] == 38, "progress open count mismatch")
require(abs(progress["g1_system_freeze"]["percent"] - 17.4) < 1e-9, "progress percent mismatch")

# Safety: PB-01 intentionally does not invent operating current/power/PWM/eRPM.
for key in [
    "esc_continuous_power_w",
    "esc_peak_power_w",
    "esc_continuous_phase_current_a",
    "esc_peak_phase_current_a",
    "esc_continuous_dc_current_a",
    "esc_peak_dc_current_a",
    "pwm_frequency_hz",
    "electrical_rpm_max",
]:
    require(sysreq[key] is None, f"{key} must remain open in PB-01")

print("PASS")
print("product_baseline=PB-01")
print("vehicle_architecture=X8_COAXIAL_4_ARM_8_INDEPENDENT_PROPULSION_CHANNELS")
print("rotor_count=8")
print("single_failure=CONTROLLED_LANDING_REQUIRED")
print("dc_bus_full_charge_ceiling_v=80")
print("repetitive_transient_ceiling_v=120")
print("power_semiconductor_vds_min_v=150")
print("flight_controller_interface=CAN_FD_CAPABLE_CLASSIC_CAN_COMPATIBLE")
print("g1_pass=8/46")
print("g1_percent=17.4")
