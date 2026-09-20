# PB-08 B1 gate-drive auxiliary-power parametric screen

Date: 2026-09-20
Status: **DESK / PARAMETRIC REQUALIFICATION PREWORK — NOT U1 LOAD FREEZE**
Authority: PB-08 common electrical platform plus immutable B1 evidence.

## Purpose

Reduce the largest identified onboard auxiliary-load unknown without inventing a U1 operating point. This note converts the legacy B1 MOSFET gate-charge inventory into a parametric gate-drive power equation. It is a screening bound only: exact U1 MOSFET, parallel count, gate voltage, PWM frequency, switching pattern and driver losses remain OPEN.

## Repository-backed B1 inputs

- B1 power stage uses `CSD19536KTT`, **2 parallel MOSFETs per switch position**.
- A three-phase two-level inverter has six switch positions, therefore the B1 population is **12 power MOSFET gates**.
- Repository primary-source reference parameter for `CSD19536KTT`: **Qg typical = 118 nC**.
- The active PB-08 product does **not** freeze this MOSFET or the B1 parallel count; both are requalification candidates only.

## First-order equation

For a conservative PWM-cycle charging screen in which each physical MOSFET gate receives one full gate-charge event per PWM period:

`P_gate,ideal = N_gate * Qg * V_gate * f_pwm`

where:
- `N_gate = 12` only for the legacy B1 2-parallel/switch population;
- `Qg = 118 nC typical` only for the legacy CSD19536KTT reference;
- `V_gate` remains a parameter;
- `f_pwm` remains a parameter.

This expression estimates energy delivered into MOSFET gates. It does not include DRV8353 quiescent/current-pump loss, bootstrap loss beyond the gate-charge term, dead-time/state-dependent effects, external gate-network dissipation allocation, downstream rail-converter loss, or any other +12 V load.

## Parametric arithmetic

Using only the legacy B1 `N_gate` and typical `Qg` as a screening case:

| Gate voltage | PWM | Ideal gate-charge power |
|---:|---:|---:|
| 10 V | 20 kHz | 0.2832 W |
| 10 V | 30 kHz | 0.4248 W |
| 12 V | 20 kHz | 0.3398 W |
| 12 V | 30 kHz | 0.5098 W |

At 12 V, the corresponding ideal average current represented by the gate-charge term is about **28.3 mA at 20 kHz** and **42.5 mA at 30 kHz**.

These are **not U1 requirements** and are not validated B1 measurements. They are arithmetic sensitivity points from a legacy candidate's typical Qg. Qg tolerance/operating-point dependence is not closed here.

## Implication for the PB-08 auxiliary ledger

The prior traction-pack auxiliary ledger correctly kept gate drive OPEN. This screen now establishes a controlled method and order-of-magnitude candidate contribution, but it still cannot be promoted into `P_aux,pack` because:

1. exact U1 MOSFET and parallel count are OPEN;
2. PWM frequency is OPEN pending exact motor inductance/ripple/loss evidence;
3. actual gate-drive amplitude/configuration is not frozen;
4. DRV8353 and converter losses are not closed;
5. `Qg=118 nC` is a typical datasheet anchor, not a worst-case production bound.

When the exact power-stage candidate and PWM are selected, replace this screen with a worst-case gate-drive budget using the selected part's controlled charge data and include driver/converter losses exactly once under the TR-070 anti-double-counting policy.

## Decision

**No G1 value is promoted.** The B1 gate-drive auxiliary-load unknown is reduced from an unstructured OPEN item to a controlled parametric dependency. `P_aux,pack`, numeric `M_cont`, exact MOSFET count and PWM remain OPEN.

No physical, thermal, EMI, flight or production qualification is claimed.