# PB-08 continuous-current margin / derating policy

Date: 2026-09-20  
Branch: `uav-rebaseline`  
Status: **CONTROLLED METHOD — NUMERIC MARGIN OPEN**

## Purpose

Define how the PB-08 whole-pack continuous-current margin `M_cont` shall be closed without double-counting worst-case effects already embedded in the propulsion power, loaded-voltage floor, auxiliary-load ledger, or component derating. This document does **not** assign a numeric margin.

The governing current contract remains:

`I_pack,cont,req = ((3000 W + P_aux,pack) / 36.0 V) * (1 + M_cont)`

The repository-proven propulsion-only lower bound remains `3000/36 = 83.33 A`.

## Margin taxonomy

| Effect | Treatment | Rationale |
|---|---|---|
| Aggregate propulsion upper continuous point (3000 W) | Already in numerator; do not add again through `M_cont` | PB-08 freezes 3.0 kW as the upper continuous propulsion design point. |
| Loaded full-rated-power voltage floor (36.0 V) | Already in denominator; do not add a second generic low-voltage factor | The current equation already evaluates at the controlled loaded floor. |
| Evidence-backed simultaneous auxiliary demand | Add explicitly as `P_aux,pack`; do not duplicate in `M_cont` | Auxiliary demand belongs in the power numerator. |
| Converter/path losses for auxiliary loads | Include in each pack-referred auxiliary ledger row | Prevents a second efficiency allowance in `M_cont`. |
| Cell/pack sag below 36.0 V | Not covered by margin; must be prevented/qualified by pack sag verification | 36.0 V is the full-rated-power floor, so operation below it is a separate requirement/derating question. |
| SOC / temperature / SOH current capability | Verify explicitly against cell/pack limits; do not hide in a generic current multiplier | These are physical qualification dimensions, not arithmetic uncertainty. |
| Parallel-cell current sharing | Verify explicitly; not a substitute for whole-pack current margin | Cell imbalance/current-sharing can limit a pack even when terminal current arithmetic passes. |
| Harness / connector / fuse / switch thermal derating | Apply at component qualification against the resulting required current | Component derating must not inflate vehicle load demand. |
| Measurement / model uncertainty in continuous propulsion demand | Eligible for `M_cont` only if not already included in the controlled 3 kW parent | Requires evidence and an explicit allocation. |
| Mission/transient peak current | Excluded from `M_cont`; separate peak/degraded-mode requirement | Continuous and transient sizing are different contracts. |
| Manufacturing tolerance affecting auxiliary demand | Prefer worst-case row values in `P_aux,pack`; residual only may enter `M_cont` | Avoids stacking worst-case component values plus a duplicate blanket tolerance. |

## Closure rule

`M_cont` may be assigned a numeric value only after all of the following are true:

1. `P_aux,pack` contains the simultaneous continuous traction-fed auxiliary loads with conversion losses or explicitly bounded efficiency.
2. The 3 kW propulsion parent is confirmed to be a requirement ceiling rather than a nominal value requiring an additional load-growth allowance.
3. Any remaining model/measurement uncertainty is identified by source and is demonstrably not already represented by the 3 kW / 36 V parents or the auxiliary ledger.
4. The chosen margin is recorded as an allocation with rationale, not copied from a legacy B1 rating or an unrelated aerospace rule of thumb.
5. Pack sag, SOC/temperature/SOH and current-sharing qualification remain separate acceptance checks.

Until these conditions close, `M_cont = OPEN` and `I_pack,cont,req` remains OPEN; only the 83.33 A propulsion-only mathematical lower bound is controlled.

## Verification consequence

When a numeric margin is eventually proposed, the verification record shall show a one-line reconciliation table with: base propulsion power, pack-referred auxiliary power, voltage floor, residual uncertainty allocation, resulting continuous current, and separate component derating checks. A reviewer must be able to identify every percentage or watt exactly once.

## Evidence boundary

No physical test result, pack qualification, thermal result, flight qualification, or production readiness is claimed here. This policy does not select a cell, BMS, fuse, connector, contactor, converter, motor, propeller, MOSFET, or rotor architecture.
