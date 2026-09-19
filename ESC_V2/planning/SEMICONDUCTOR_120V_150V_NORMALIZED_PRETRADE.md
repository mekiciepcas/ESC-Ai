# 120 V vs 150 V MOSFET normalized pretrade

Date: 2026-09-19
Branch: `uav-rebaseline`
Status: `TRADE_ONLY / NOT A G2 SELECTION`

## Purpose
Reduce G2 risk without promoting benchmark values into product requirements. This comparison keeps the current 81 V architecture stress reference as a trade-only voltage and compares same-package current-generation Infineon TOLL devices.

## Primary-source anchors

| Parameter | 120 V anchor | 150 V anchor |
|---|---:|---:|
| Device | IPT017N12NM6 / equivalent automotive IAUTN12S5N017 class | IAUTN15S6N025 |
| VDS max | 120 V | 150 V |
| RDS(on) max @10 V, 25 C | 1.7 mOhm | 2.5 mOhm |
| Qg typ @10 V | ~111-113 nC | 107 nC |
| Qg max | ~141-145 nC | 139 nC |
| RthJC | ~0.38 K/W | 0.42 K/W max |
| Package | TOLL | TOLL |
| Tj max | 175 C | 175 C |

Sources: Infineon IPT017N12NM6 / IAUTN12S5N017 / IAUTN15S6N025 product pages and datasheets. Product pages identify the 120 V 1.7 mOhm class and 150 V 2.5 mOhm class as active/preferred current-generation devices.

## Static voltage margin at the existing trade-only 81 V stress reference

- 120 V class: 39 V absolute static margin; 32.5% of device VDS rating.
- 150 V class: 69 V absolute static margin; 46.0% of device VDS rating.

These are **not** derating approvals. They exclude switching overshoot, regeneration, harness/PCB inductance, battery tolerance and repetitive avalanche.

## Condition-normalized conduction comparison

Because G1 phase current and junction temperature are OPEN, no product-current loss number is generated. Instead, conduction loss is normalized to effective logical-switch RMS current `I_sw,rms` and hot-resistance multiplier `k_hot`:

`Pcond,logical = I_sw,rms^2 * RDS25 * k_hot / Nparallel * kshare`

For equal `k_hot`, equal parallel count and equal sharing factor, the 150 V anchor's conduction term is approximately:

`2.5 / 1.7 = 1.47x`

or about **47% higher** than the 120 V anchor solely from the 25 C maximum RDS(on) headline. This is not the final hot-loss ratio because each device's temperature curve must be applied at the same evidenced junction temperature.

## Gate-charge observation

The headline total gate charges are similar (~111-113 nC for the 120 V anchor versus 107 nC for the 150 V anchor). Therefore the 150 V class is **not automatically disqualified by gate charge**. Exact driver loss and transition speed remain dependent on Qgd, plateau voltage, gate resistance, driver source/sink current and layout.

## Decision implication

At the current evidence level:

1. **Do not freeze 120 V.** It has the lower headline conduction resistance, but 39 V static margin at the 81 V stress reference is not yet a proven repetitive-transient margin.
2. **Do not freeze 150 V.** It provides materially more static voltage margin but carries a headline conduction-resistance penalty versus the selected 120 V anchor.
3. Keep **both 120 V and 150 V active through G1**.
4. The first hard discriminator shall be the frozen `VBUS_max/transient` plus explicit VDS derating/overshoot policy. Only surviving classes proceed to common-condition hot-loss/SOA/thermal comparison.
5. If the eventual verified repetitive/transient ceiling makes the 120 V class marginal, prefer 150 V rather than relying on avalanche as a normal operating mechanism.

## Exact inputs still required for selection

- frozen VBUS min/nom/full-charge/transient,
- repetitive switching overshoot allowance,
- phase RMS and peak current plus overload duration,
- PWM frequency and modulation/event count,
- gate-drive voltage/resistance and allowed dv/dt,
- common hot junction/case/baseplate point,
- motor inductance/current ripple,
- package/baseplate thermal path,
- SOA/repetitive avalanche policy,
- parallel-device count and current-sharing tolerance.

## Productization decision

**Decision PRETRADE-SEM-01:** preserve a 150 V-capable architecture path in U1 studies while 120 V remains an efficiency candidate. Do not design auxiliary sensing/gate-drive/layout assumptions that make a later 150 V choice impossible before G1 transient closure.

This is an architecture-risk decision, not a production MPN or voltage-class freeze.
