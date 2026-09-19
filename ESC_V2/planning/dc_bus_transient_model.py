"""First-order ESC DC-bus transient requirement model.

Design-use only. This deliberately does NOT predict a product transient without
measured harness/loop inductance, current step and clamp behaviour.
"""
from dataclasses import dataclass
from math import sqrt

@dataclass(frozen=True)
class BusCase:
    battery_max_v: float
    loop_inductance_h: float
    current_step_a: float
    current_fall_time_s: float
    bus_capacitance_f: float | None = None
    clamp_voltage_v: float | None = None


def inductive_energy_j(L_h: float, current_a: float) -> float:
    return 0.5 * L_h * current_a**2


def unclamped_l_di_dt_v(L_h: float, current_step_a: float, fall_time_s: float) -> float:
    if fall_time_s <= 0:
        raise ValueError("fall_time_s must be > 0")
    return L_h * current_step_a / fall_time_s


def ideal_cap_energy_rise_v(v0: float, energy_j: float, capacitance_f: float) -> float:
    """Ideal upper-bound capacitor energy absorption, ignoring ESR/ESL/load/clamp."""
    if capacitance_f <= 0:
        raise ValueError("capacitance_f must be > 0")
    return sqrt(v0**2 + 2.0 * energy_j / capacitance_f)


def evaluate(case: BusCase) -> dict:
    e = inductive_energy_j(case.loop_inductance_h, case.current_step_a)
    dv_ldi = unclamped_l_di_dt_v(case.loop_inductance_h, case.current_step_a, case.current_fall_time_s)
    out = {
        "battery_max_v": case.battery_max_v,
        "inductive_energy_j": e,
        "first_order_Ldi_dt_v": dv_ldi,
        "battery_plus_Ldi_dt_v": case.battery_max_v + dv_ldi,
        "evidence_warning": "PARAMETRIC_ONLY_NOT_A_PRODUCT_TRANSIENT_PREDICTION"
    }
    if case.bus_capacitance_f is not None:
        out["ideal_cap_energy_absorption_final_v"] = ideal_cap_energy_rise_v(
            case.battery_max_v, e, case.bus_capacitance_f
        )
    if case.clamp_voltage_v is not None:
        out["clamp_above_battery_v"] = case.clamp_voltage_v - case.battery_max_v
        out["clamp_static_headroom_positive"] = case.clamp_voltage_v > case.battery_max_v
    return out


if __name__ == "__main__":
    # Illustrative sensitivity grid only; NOT measured harness values.
    battery_max = 18 * 4.2
    for L_uH in (0.5, 1.0, 2.0, 5.0):
        for I_a in (100, 150, 200, 250):
            c = BusCase(battery_max, L_uH * 1e-6, I_a, 2e-6)
            r = evaluate(c)
            print(f"L={L_uH:>3.1f}uH I={I_a:>3}A E={r['inductive_energy_j']:.4f}J "
                  f"Ldi/dt={r['first_order_Ldi_dt_v']:.1f}V raw={r['battery_plus_Ldi_dt_v']:.1f}V")
