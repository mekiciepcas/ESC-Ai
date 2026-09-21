# PB-08 B1 gate-drive traction-pack current sensitivity

Date: 2026-09-21  
Branch: `uav-rebaseline`  
Status: **LEGACY B1 REQUALIFICATION SENSITIVITY / NOT U1 AUXILIARY BUDGET**

## Purpose

Translate the already-controlled TR-071 ideal gate-charge power screen into traction-pack-referred current sensitivity at the frozen PB-08 36.0 V loaded floor. This is arithmetic prework only. It does not select the U1 MOSFET, switch count, gate voltage, PWM frequency, gate driver, auxiliary converter, or conversion efficiency.

## Controlled parent evidence

TR-071 records legacy B1 with 12 physical CSD19536KTT gates and controlled typical `Qg = 118 nC`, using:

`P_gate,ideal = N_gate * Qg * V_gate * f_pwm`

The controlled sensitivity endpoints are:

- 10 V gate amplitude, 20 kHz PWM: `P_gate,ideal = 0.2832 W`
- 12 V gate amplitude, 30 kHz PWM: `P_gate,ideal = 0.5098 W`

These are legacy B1 screening points, not PB-08/U1 requirements.

## Pack-current translation

At the frozen PB-08 loaded-floor voltage `V_pack = 36.0 V`, an ideal lossless conversion path gives only a mathematical lower bound:

`I_pack,ideal = P_gate,ideal / 36.0 V`

| Legacy B1 sensitivity point | Ideal gate-charge power | Ideal-lossless pack-current lower bound |
|---|---:|---:|
| 10 V / 20 kHz | 0.2832 W | 7.867 mA |
| 12 V / 30 kHz | 0.5098 W | 14.161 mA |

The endpoint span is therefore 6.294 mA at 36.0 V. This is not an uncertainty interval and not a U1 current allocation; it is only the arithmetic consequence of the two TR-071 sensitivity endpoints.

For any real implementation with conversion-path efficiency `eta_path < 1`, the pack-referred current for the same ideal gate-charge energy is:

`I_pack = P_gate,ideal / (36.0 V * eta_path)`

Because PB-08/U1 `eta_path` is OPEN, no real pack-current value is asserted.

## Engineering disposition

This calculation shows that the legacy B1 dynamic gate-charge term is small relative to the existing 83.33 A propulsion-only pack-current lower bound, but it **cannot be omitted** from the final auxiliary ledger and it cannot be used to close `P_aux,pack`. The final U1 term must be recomputed after exact MOSFET MPN/count, gate amplitude, PWM, driver topology and conversion efficiency are frozen.

No quiescent driver current, bootstrap loss, switching-node coupling loss, auxiliary-converter quiescent current, fan/MCU/CAN/sensor demand, or vehicle avionics demand is included here.

## Closure rule

Promote a gate-drive contribution into the PB-08 traction-pack auxiliary budget only when all of the following are controlled for U1: exact MOSFET and gate count; applicable Qg basis; gate amplitude; PWM frequency; driver topology and quiescent/dynamic demand; auxiliary conversion path and worst-case efficiency across the applicable bus/environment envelope.

Until then, `P_aux,pack` and exact continuous pack current remain OPEN. This artifact does not advance G1, qualify B1, allocate `U1-SCH-R001`, or constitute physical verification.
