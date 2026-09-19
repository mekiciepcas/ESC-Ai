#!/usr/bin/env python3
"""Parametric HV-divider + buffer + ADC static error model.

No product defaults are embedded. Every electrical input is required so the tool
cannot silently promote a screening assumption into the UAV baseline.

Model scope:
- nominal divider transfer;
- worst-case divider ratio from resistor tolerances;
- op-amp input offset referred to HV input;
- op-amp input-bias-current error using divider Thevenin resistance;
- ideal ADC LSB and half-LSB quantization referred to HV input.

Not modeled here: resistor tempco correlation, ADC INL/DNL/gain/offset, VREF error,
RC settling, op-amp finite gain/bandwidth, leakage, dv/dt coupling, common-mode
transients, clamp leakage, PCB contamination, or calibration. Those require the
final G1/G2 architecture and exact MPNs.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, asdict
import json


@dataclass
class Result:
    vhv_v: float
    rtop_ohm: float
    rbot_ohm: float
    divider_ratio_nom: float
    sense_nom_v: float
    hv_full_scale_from_vref_v: float
    ratio_min: float
    ratio_max: float
    sense_min_from_res_tol_v: float
    sense_max_from_res_tol_v: float
    hv_error_res_tol_min_v: float
    hv_error_res_tol_max_v: float
    r_thevenin_ohm: float
    opamp_vos_referred_hv_v: float
    opamp_ib_referred_hv_v: float
    adc_lsb_v: float
    adc_half_lsb_referred_hv_v: float


def positive(value: str) -> float:
    x = float(value)
    if x <= 0:
        raise argparse.ArgumentTypeError("value must be > 0")
    return x


def nonnegative(value: str) -> float:
    x = float(value)
    if x < 0:
        raise argparse.ArgumentTypeError("value must be >= 0")
    return x


def compute(args: argparse.Namespace) -> Result:
    rtop = args.rtop_ohm
    rbot = args.rbot_ohm
    ratio = rbot / (rtop + rbot)
    sense = args.vhv_v * ratio

    t_top = args.rtop_tol_pct / 100.0
    t_bot = args.rbot_tol_pct / 100.0

    # Divider ratio is minimized by high Rtop / low Rbot and maximized by
    # low Rtop / high Rbot.
    rtop_hi = rtop * (1.0 + t_top)
    rtop_lo = rtop * (1.0 - t_top)
    rbot_hi = rbot * (1.0 + t_bot)
    rbot_lo = rbot * (1.0 - t_bot)

    ratio_min = rbot_lo / (rtop_hi + rbot_lo)
    ratio_max = rbot_hi / (rtop_lo + rbot_hi)

    sense_min = args.vhv_v * ratio_min
    sense_max = args.vhv_v * ratio_max

    # Re-refer sense-node error back to HV using the nominal divider ratio.
    hv_err_res_min = (sense_min - sense) / ratio
    hv_err_res_max = (sense_max - sense) / ratio

    rth = (rtop * rbot) / (rtop + rbot)
    vos_v = args.opamp_vos_uv * 1e-6
    ib_a = args.opamp_ib_na * 1e-9

    hv_vos = vos_v / ratio
    hv_ib = (ib_a * rth) / ratio

    adc_lsb = args.adc_vref_v / (2 ** args.adc_bits)
    hv_half_lsb = (0.5 * adc_lsb) / ratio

    return Result(
        vhv_v=args.vhv_v,
        rtop_ohm=rtop,
        rbot_ohm=rbot,
        divider_ratio_nom=ratio,
        sense_nom_v=sense,
        hv_full_scale_from_vref_v=args.adc_vref_v / ratio,
        ratio_min=ratio_min,
        ratio_max=ratio_max,
        sense_min_from_res_tol_v=sense_min,
        sense_max_from_res_tol_v=sense_max,
        hv_error_res_tol_min_v=hv_err_res_min,
        hv_error_res_tol_max_v=hv_err_res_max,
        r_thevenin_ohm=rth,
        opamp_vos_referred_hv_v=hv_vos,
        opamp_ib_referred_hv_v=hv_ib,
        adc_lsb_v=adc_lsb,
        adc_half_lsb_referred_hv_v=hv_half_lsb,
    )


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--vhv-v", type=positive, required=True)
    p.add_argument("--rtop-ohm", type=positive, required=True,
                   help="Total series upper-divider resistance")
    p.add_argument("--rbot-ohm", type=positive, required=True)
    p.add_argument("--rtop-tol-pct", type=nonnegative, required=True)
    p.add_argument("--rbot-tol-pct", type=nonnegative, required=True)
    p.add_argument("--opamp-vos-uv", type=nonnegative, required=True,
                   help="Magnitude used for worst-case static error screening")
    p.add_argument("--opamp-ib-na", type=nonnegative, required=True,
                   help="Magnitude used for worst-case bias-current screening")
    p.add_argument("--adc-vref-v", type=positive, required=True)
    p.add_argument("--adc-bits", type=int, required=True)
    args = p.parse_args()
    if args.adc_bits <= 0:
        p.error("--adc-bits must be > 0")

    print(json.dumps(asdict(compute(args)), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
