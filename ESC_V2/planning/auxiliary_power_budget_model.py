#!/usr/bin/env python3
"""Parametric auxiliary-power budget calculator for ESC U1 prework.

No product operating-point defaults are embedded. Every numeric input must be supplied
by the caller and should be tagged with evidence outside this script.

This is a first-order SCREENING tool, not physical validation or converter design.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def positive(name: str, value: float, allow_zero: bool = False) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    if allow_zero:
        if value < 0:
            raise ValueError(f"{name} must be >= 0")
    elif value <= 0:
        raise ValueError(f"{name} must be > 0")
    return value


def load_power(load: dict, rail_v: float) -> tuple[float, float]:
    """Return (current_A, power_W). Exactly one of current_a or power_w is required."""
    has_i = load.get("current_a") is not None
    has_p = load.get("power_w") is not None
    if has_i == has_p:
        raise ValueError(
            f"load {load.get('name', '<unnamed>')} must provide exactly one of current_a or power_w"
        )
    if has_i:
        i = positive(f"{load.get('name')}.current_a", load["current_a"], allow_zero=True)
        return i, i * rail_v
    p = positive(f"{load.get('name')}.power_w", load["power_w"], allow_zero=True)
    return p / rail_v, p


def gate_drive_power(gd: dict) -> float:
    """First-order P = Qg * Vdrive * switching_events_per_second.

    Caller must define the total number of full gate-charge events represented by
    devices_per_event * events_per_device_per_pwm_cycle. This avoids assuming a
    particular SVPWM switching pattern or parallel-FET count.
    """
    qg_c = positive("gate_drive.qg_c", gd["qg_c"])
    v_drive = positive("gate_drive.v_drive", gd["v_drive"])
    pwm_hz = positive("gate_drive.pwm_hz", gd["pwm_hz"])
    devices = positive("gate_drive.devices_per_event", gd["devices_per_event"])
    events = positive(
        "gate_drive.events_per_device_per_pwm_cycle",
        gd["events_per_device_per_pwm_cycle"],
    )
    return qg_c * v_drive * pwm_hz * devices * events


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json", type=Path)
    args = parser.parse_args()

    data = json.loads(args.input_json.read_text(encoding="utf-8"))
    rails = data.get("rails")
    if not isinstance(rails, dict) or not rails:
        raise ValueError("input must contain non-empty 'rails' object")

    result = {
        "status": "SCREENING_ONLY",
        "warning": "No result is a U1 requirement or validated hardware measurement.",
        "rails": {},
    }

    for rail_name, rail in rails.items():
        rail_v = positive(f"{rail_name}.voltage_v", rail["voltage_v"])
        loads = rail.get("loads", [])
        if not isinstance(loads, list):
            raise ValueError(f"{rail_name}.loads must be a list")

        load_rows = []
        total_i = 0.0
        total_p = 0.0
        for load in loads:
            i, p = load_power(load, rail_v)
            total_i += i
            total_p += p
            load_rows.append({"name": load.get("name"), "current_a": i, "power_w": p})

        margin_fraction = positive(
            f"{rail_name}.design_margin_fraction",
            rail["design_margin_fraction"],
            allow_zero=True,
        )
        result["rails"][rail_name] = {
            "voltage_v": rail_v,
            "loads": load_rows,
            "summed_current_a": total_i,
            "summed_power_w": total_p,
            "design_margin_fraction": margin_fraction,
            "budget_current_with_margin_a": total_i * (1.0 + margin_fraction),
            "budget_power_with_margin_w": total_p * (1.0 + margin_fraction),
        }

    if data.get("gate_drive") is not None:
        gd = data["gate_drive"]
        p_gate = gate_drive_power(gd)
        source_rail = gd["source_rail"]
        if source_rail not in result["rails"]:
            raise ValueError("gate_drive.source_rail must match a defined rail")
        rail_v = result["rails"][source_rail]["voltage_v"]
        result["gate_drive_screening"] = {
            "source_rail": source_rail,
            "first_order_gate_charge_power_w": p_gate,
            "equivalent_average_source_current_a_at_100pct_driver_efficiency": p_gate / rail_v,
            "limitation": (
                "This term excludes driver quiescent current, bootstrap/charge-pump loss, "
                "Miller/recovery effects and real switching-pattern variation. Apply measured "
                "driver efficiency/loss separately before converter sizing."
            ),
        }

    converters = data.get("converters", [])
    if not isinstance(converters, list):
        raise ValueError("converters must be a list")
    converter_rows = []
    for conv in converters:
        output_rail = conv["output_rail"]
        if output_rail not in result["rails"]:
            raise ValueError(f"unknown converter output rail {output_rail}")
        efficiency = positive(f"{conv.get('name')}.efficiency", conv["efficiency"])
        if efficiency > 1.0:
            raise ValueError("converter efficiency must be <= 1")
        p_out = result["rails"][output_rail]["budget_power_with_margin_w"]
        p_in = p_out / efficiency
        converter_rows.append({
            "name": conv.get("name"),
            "output_rail": output_rail,
            "efficiency": efficiency,
            "required_input_power_w_for_output_budget": p_in,
            "note": "Caller must add source-rail local loads and converter quiescent/startup behavior separately.",
        })
    result["converter_screening"] = converter_rows

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
