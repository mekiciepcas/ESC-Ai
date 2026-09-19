#!/usr/bin/env python3
"""Parametric HV-sense dynamic/ADC-settling screening model.

No product values are embedded. All electrical inputs are required.
This is a first-order screening model, not a SPICE or bench substitute.
"""
import argparse
import json
import math


def _positive(value, name):
    if value <= 0:
        raise ValueError(f"{name} must be > 0")
    return value


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--r-top-ohm", type=float, required=True)
    p.add_argument("--r-bottom-ohm", type=float, required=True)
    p.add_argument("--c-divider-f", type=float, required=True)
    p.add_argument("--opamp-gbw-hz", type=float, required=True)
    p.add_argument("--opamp-noise-gain", type=float, required=True)
    p.add_argument("--opamp-slew-v-per-s", type=float, required=True)
    p.add_argument("--adc-series-ohm", type=float, required=True)
    p.add_argument("--adc-cap-f", type=float, required=True)
    p.add_argument("--adc-sample-time-s", type=float, required=True)
    p.add_argument("--adc-bits", type=int, required=True)
    p.add_argument("--vref-v", type=float, required=True)
    p.add_argument("--vbus-step-v", type=float, required=True)
    p.add_argument(
        "--settling-lsb-fraction",
        type=float,
        required=True,
        help="Allowed residual error as a fraction of one ADC LSB, e.g. 0.5",
    )
    a = p.parse_args()

    for name in (
        "r_top_ohm",
        "r_bottom_ohm",
        "c_divider_f",
        "opamp_gbw_hz",
        "opamp_noise_gain",
        "opamp_slew_v_per_s",
        "adc_series_ohm",
        "adc_cap_f",
        "adc_sample_time_s",
        "vref_v",
        "vbus_step_v",
        "settling_lsb_fraction",
    ):
        _positive(getattr(a, name), name)
    if a.adc_bits <= 0:
        raise ValueError("adc_bits must be > 0")

    ratio = a.r_bottom_ohm / (a.r_top_ohm + a.r_bottom_ohm)
    r_thevenin = (a.r_top_ohm * a.r_bottom_ohm) / (a.r_top_ohm + a.r_bottom_ohm)
    tau_div = r_thevenin * a.c_divider_f
    fc_div = 1.0 / (2.0 * math.pi * tau_div)

    v_step_adc = a.vbus_step_v * ratio
    lsb = a.vref_v / (2**a.adc_bits)
    allowed_error_v = a.settling_lsb_fraction * lsb
    relative_allowed = min(
        0.999999999,
        allowed_error_v / max(abs(v_step_adc), 1e-30),
    )

    # First-order closed-loop approximation. Screening only.
    f_closed_loop = a.opamp_gbw_hz / a.opamp_noise_gain
    tau_opamp = 1.0 / (2.0 * math.pi * f_closed_loop)
    t_opamp_linear = -tau_opamp * math.log(relative_allowed)
    t_opamp_slew = abs(v_step_adc) / a.opamp_slew_v_per_s
    t_opamp_estimated = max(t_opamp_linear, t_opamp_slew)

    tau_adc = a.adc_series_ohm * a.adc_cap_f
    residual_adc = math.exp(-a.adc_sample_time_s / tau_adc)
    adc_error_v = abs(v_step_adc) * residual_adc
    adc_error_lsb = adc_error_v / lsb
    adc_pass = adc_error_v <= allowed_error_v

    t_div_settle = -tau_div * math.log(relative_allowed)

    result = {
        "status": "SCREENING_ONLY",
        "divider": {
            "ratio": ratio,
            "thevenin_ohm": r_thevenin,
            "tau_s": tau_div,
            "fc_hz": fc_div,
            "estimated_settle_to_target_s": t_div_settle,
        },
        "opamp": {
            "estimated_closed_loop_bandwidth_hz": f_closed_loop,
            "first_order_tau_s": tau_opamp,
            "linear_settle_to_target_s": t_opamp_linear,
            "slew_time_for_step_s": t_opamp_slew,
            "estimated_settle_s": t_opamp_estimated,
        },
        "adc_acquisition": {
            "tau_s": tau_adc,
            "sample_time_s": a.adc_sample_time_s,
            "residual_fraction": residual_adc,
            "estimated_error_v": adc_error_v,
            "estimated_error_lsb": adc_error_lsb,
            "pass_requested_target": adc_pass,
        },
        "target": {
            "vbus_step_v": a.vbus_step_v,
            "adc_step_v": v_step_adc,
            "adc_lsb_v": lsb,
            "allowed_error_v": allowed_error_v,
            "allowed_error_lsb": a.settling_lsb_fraction,
        },
        "limitations": [
            "No op-amp output impedance, phase margin, parasitics, ADC kickback, clamp capacitance, PCB capacitance or switching-node dv/dt model.",
            "Op-amp is approximated as a single-pole closed-loop system plus slew limit.",
            "ADC acquisition is approximated by a single R*C charge path.",
            "Use manufacturer SPICE/bench validation before schematic freeze.",
        ],
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
