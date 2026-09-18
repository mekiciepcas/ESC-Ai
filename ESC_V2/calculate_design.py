"""A0 sizing only: not firmware, circuit simulation, or hardware validation."""
import json
import math
from pathlib import Path

root = Path(__file__).resolve().parent
d = json.loads((root / "design_basis.json").read_text(encoding="utf-8"))
b, m, inv, sense = (d[k] for k in ("battery", "motor", "inverter", "measurement_preliminary"))
nominal = b["series"] * b["cell_nominal_v"]
capacity = b["parallel"] * b["cell_capacity_typ_ah"]
motor_input = m["shaft_power_target_w"] / m["efficiency_budget_assumption"]
battery_power = motor_input / inv["efficiency_budget_assumption"]
pack_r = b["series"] / b["parallel"] * b["cell_dc_resistance_estimate_ohm"]
ratio = sense["bus_divider_bottom_ohm"] / (sense["bus_divider_top_ohm"] + sense["bus_divider_bottom_ohm"])
out = {
    "status": "calculated_estimates_not_measured",
    "pack": {"cell_count": b["series"] * b["parallel"], "nominal_v": nominal,
             "full_v": b["series"] * b["cell_charge_v"], "typ_capacity_ah": capacity,
             "typ_energy_wh": nominal * capacity,
             "cell_current_at_system_limit_a": b["system_discharge_limit_a"] / b["parallel"],
             "cell_only_pack_resistance_estimate_ohm": pack_r,
             "cell_only_heat_at_system_limit_w": b["system_discharge_limit_a"] ** 2 * pack_r},
    "power": {"motor_input_w": motor_input, "battery_terminal_power_w": battery_power,
              "inverter_loss_w": battery_power - motor_input,
              "battery_current_by_terminal_voltage_a": {str(v): battery_power / v for v in (39, 44, nominal, 54.6)},
              "nominal_energy_runtime_min_ideal": nominal * capacity / battery_power * 60,
              "shaft_torque_at_reference_speed_nm": m["shaft_power_target_w"] / (2 * math.pi * m["reference_speed_rpm"] / 60)},
    "thermal": {"fet_conduction_loss_estimate_w": 3 * inv["phase_rms_design_target_a"] ** 2 * inv["hot_fet_rds_estimate_ohm"] / inv["parallel_fets_per_switch"],
                "heatsink_to_ambient_max_k_per_w": (inv["baseplate_target_c"] - inv["rated_ambient_target_c"]) / inv["heatsink_loss_budget_w"]},
    "measurement": {"adc_at_max_check_v": sense["bus_check_max_v"] * ratio,
                    "adc_at_full_pack_v": b["series"] * b["cell_charge_v"] * ratio,
                    "ideal_bus_adc_fullscale_v": sense["adc_reference_v"] / ratio,
                    "current_volts_per_amp": sense["low_side_shunt_ohm"] * sense["current_amp_gain"],
                    "amp_outputs_at_range_endpoints_v": [sense["adc_reference_v"] / 2 + sign * inv["current_measurement_range_target_a"] * sense["low_side_shunt_ohm"] * sense["current_amp_gain"] for sign in (-1, 1)]}
}
assert out["measurement"]["adc_at_max_check_v"] < sense["adc_reference_v"]
assert battery_power / b["full_power_min_v"] < b["system_discharge_limit_a"]
assert math.sqrt(2) * inv["phase_rms_design_target_a"] < inv["instantaneous_phase_software_limit_target_a"]
(root / "calculated_budget.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(out, indent=2, ensure_ascii=False))
