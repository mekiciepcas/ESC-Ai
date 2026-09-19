#!/usr/bin/env python3
"""Condition-normalized MOSFET loss screening calculator.

All operating-point and device parameters are caller-supplied.
No ESC rating, voltage class, PWM frequency, current or temperature is assumed.
"""
import argparse
import json


def _positive(value, name):
    if value <= 0:
        raise ValueError(f"{name} must be > 0")
    return value


def _at_least_one(value, name):
    if value < 1:
        raise ValueError(f"{name} must be >= 1")
    return value


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--device-name", required=True)
    p.add_argument("--vbus-v", type=float, required=True)
    p.add_argument(
        "--switch-rms-current-a",
        type=float,
        required=True,
        help="Effective RMS current through one logical switch over the analysis interval.",
    )
    p.add_argument(
        "--commutation-current-a",
        type=float,
        required=True,
        help="Current at a switching transition for one logical switch.",
    )
    p.add_argument(
        "--effective-switching-rate-hz",
        type=float,
        required=True,
        help="Effective switching events per second per logical switch used by this screening model.",
    )
    p.add_argument("--rds-hot-ohm", type=float, required=True)
    p.add_argument("--tr-s", type=float, required=True)
    p.add_argument("--tf-s", type=float, required=True)
    p.add_argument("--coss-f", type=float, required=True)
    p.add_argument("--qrr-c", type=float, required=True)
    p.add_argument("--parallel-devices-per-switch", type=int, required=True)
    p.add_argument(
        "--current-sharing-factor",
        type=float,
        required=True,
        help=">=1 multiplier on ideal conduction loss for sharing/tolerance uncertainty.",
    )
    p.add_argument(
        "--logical-switch-count",
        type=int,
        required=True,
        help="Usually 6 for a three-phase two-level VSI, but caller must specify.",
    )
    p.add_argument("--include-qrr", action="store_true")
    p.add_argument("--include-coss", action="store_true")
    a = p.parse_args()

    for name in (
        "vbus_v",
        "switch_rms_current_a",
        "commutation_current_a",
        "effective_switching_rate_hz",
        "rds_hot_ohm",
        "tr_s",
        "tf_s",
        "coss_f",
        "qrr_c",
        "current_sharing_factor",
    ):
        _positive(getattr(a, name), name)
    _at_least_one(a.parallel_devices_per_switch, "parallel_devices_per_switch")
    _at_least_one(a.logical_switch_count, "logical_switch_count")
    if a.current_sharing_factor < 1.0:
        raise ValueError("current_sharing_factor must be >= 1")

    n_parallel = a.parallel_devices_per_switch
    n_switches = a.logical_switch_count

    # Ideal sharing gives R_eq = Rds/N. The sharing factor penalizes that idealization.
    p_cond_per_logical = (
        a.switch_rms_current_a**2
        * (a.rds_hot_ohm / n_parallel)
        * a.current_sharing_factor
    )

    # Linear V-I overlap approximation. This is only a common-condition screening term.
    e_overlap = 0.5 * a.vbus_v * a.commutation_current_a * (a.tr_s + a.tf_s)
    p_overlap_per_logical = e_overlap * a.effective_switching_rate_hz

    # First-order parallel-device scaling. Real Eoss/Qrr are nonlinear and condition dependent.
    p_coss_per_logical = (
        0.5
        * (n_parallel * a.coss_f)
        * a.vbus_v**2
        * a.effective_switching_rate_hz
        if a.include_coss
        else 0.0
    )
    p_qrr_per_logical = (
        (n_parallel * a.qrr_c)
        * a.vbus_v
        * a.effective_switching_rate_hz
        if a.include_qrr
        else 0.0
    )

    per_logical = (
        p_cond_per_logical
        + p_overlap_per_logical
        + p_coss_per_logical
        + p_qrr_per_logical
    )
    total = per_logical * n_switches
    per_device_average = total / (n_switches * n_parallel)

    result = {
        "status": "SCREENING_ONLY",
        "device": a.device_name,
        "inputs": vars(a),
        "loss_w": {
            "conduction_per_logical_switch": p_cond_per_logical,
            "switching_overlap_per_logical_switch": p_overlap_per_logical,
            "coss_per_logical_switch": p_coss_per_logical,
            "qrr_per_logical_switch": p_qrr_per_logical,
            "total_per_logical_switch": per_logical,
            "total_all_logical_switches": total,
            "average_per_physical_device": per_device_average,
        },
        "limitations": [
            "Linear V-I overlap is a screening approximation; use measured/manufacturer Eon/Eoff where available.",
            "Coss is treated as constant at the caller-supplied point; real Eoss is nonlinear versus VDS.",
            "Qrr is comparable only when representative of the same current, voltage, di/dt and temperature.",
            "No dead-time body-diode loss, gate-drive loss, avalanche, stray-inductance overshoot, modulation-specific event count, SOA or transient thermal impedance is included.",
            "Current-sharing factor is not a substitute for layout and thermal validation.",
            "Do not use this output as an ESC continuous-current or production-qualification claim.",
        ],
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
