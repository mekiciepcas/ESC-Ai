#!/usr/bin/env python3
"""Parametric ESC DC-link precharge/disconnect screening model.

No project values are assumed. Supply explicit numeric arguments. Results are analysis
screens only and do not select a resistor, contactor, fuse, clamp, or capacitor.
"""
import argparse, math, json


def model(vbus, c_f, r_ohm, target_fraction, disconnect_current=None, stray_l_h=None, clamp_v=None):
    if not (0 < target_fraction < 1):
        raise ValueError("target_fraction must be between 0 and 1")
    if min(vbus, c_f, r_ohm) <= 0:
        raise ValueError("vbus, c_f and r_ohm must be > 0")
    tau = r_ohm * c_f
    t_target = -tau * math.log(1.0 - target_fraction)
    i0 = vbus / r_ohm
    p0 = vbus * vbus / r_ohm
    e_cap_final = 0.5 * c_f * vbus * vbus
    # For an ideal RC charge from a stiff source, resistor energy equals final capacitor energy.
    e_r_ideal_full_charge = e_cap_final
    out = {
        "inputs": {"vbus_V": vbus, "capacitance_F": c_f, "precharge_R_ohm": r_ohm,
                   "target_fraction": target_fraction},
        "precharge": {"tau_s": tau, "time_to_target_s": t_target,
                      "initial_current_A": i0, "initial_resistor_power_W": p0,
                      "final_cap_energy_J": e_cap_final,
                      "ideal_resistor_energy_full_charge_J": e_r_ideal_full_charge},
        "disconnect": {"status": "OPEN_INPUTS"}
    }
    if disconnect_current is not None and stray_l_h is not None:
        e_l = 0.5 * stray_l_h * disconnect_current * disconnect_current
        d = {"current_A": disconnect_current, "stray_L_H": stray_l_h,
             "inductive_energy_J": e_l}
        if clamp_v is not None:
            if clamp_v <= vbus:
                d["clamp_screen"] = "INVALID: clamp_v must exceed vbus for this simple screen"
            else:
                d["ideal_constant_current_absorption_time_s"] = e_l / ((clamp_v-vbus)*disconnect_current) if disconnect_current else 0
                d["note"] = "Idealized energy/time screen only; real current decays and parasitics/topology dominate."
        out["disconnect"] = d
    return out


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--vbus", type=float, required=True)
    p.add_argument("--cap-uF", type=float, required=True)
    p.add_argument("--r-ohm", type=float, required=True)
    p.add_argument("--target", type=float, default=0.90)
    p.add_argument("--disconnect-current", type=float)
    p.add_argument("--stray-uH", type=float)
    p.add_argument("--clamp-v", type=float)
    a=p.parse_args()
    print(json.dumps(model(a.vbus,a.cap_uF*1e-6,a.r_ohm,a.target,a.disconnect_current,
                           None if a.stray_uH is None else a.stray_uH*1e-6,a.clamp_v),indent=2))

if __name__ == "__main__":
    main()
