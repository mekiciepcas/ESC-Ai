# PB-08 P50B 12S4P conditional non-cell resistance allowance screen

Date: 2026-09-20
Status: **REFERENCE-TOPOLOGY ARITHMETIC SCREEN / NO PACK FREEZE / NO PHYSICAL VERIFICATION**

## Purpose

Bound how much **additional installed series resistance outside the cells** could be tolerated while holding the PB-08 36.0 V full-rated-power loaded-floor requirement at the existing propulsion-only continuous-current lower bound. This is a conditional algebraic screen only; it does not establish actual pack resistance or compliance.

## Controlled parents

- PB-08 full-rated-power loaded floor: `V_loaded,min = 36.0 V`.
- PB-08 upper continuous propulsion study point: `P_prop = 3000 W`.
- Propulsion-only current lower bound at that floor: `I = 3000/36 = 83.33 A`.
- Reference topology only: Molicel P50B 12S4P.
- Existing condition-specific cell-only screen: typical P50B DC impedance `12.8 mOhm/cell @ 50% SOC`; ideal equal 4P sharing gives `R_cells = 38.4 mOhm`.

## Equation

For a chosen pack open-circuit voltage `V_OCV`, the total series-resistance ceiling consistent with 36.0 V at 83.33 A is:

`R_total,max = (V_OCV - 36.0) / 83.33`

The corresponding non-cell allowance is:

`R_noncell,max = R_total,max - 0.0384 ohm`

where `R_noncell` would have to include all installed contributions outside the cell model, including tabs/busbars/interconnects, fuse, BMS/disconnect switching path, connectors and harness.

## Conditional sensitivity

| Assumed OCV for arithmetic only | Total resistance ceiling | Cell-only reference | Remaining non-cell allowance | Interpretation |
|---:|---:|---:|---:|---|
| 39.20 V | 38.4 mOhm | 38.4 mOhm | 0.0 mOhm | Existing cell-only screen already consumes the full algebraic allowance. |
| 40.00 V | 48.0 mOhm | 38.4 mOhm | 9.6 mOhm | Very small conditional installed-path allowance. |
| 41.00 V | 60.0 mOhm | 38.4 mOhm | 21.6 mOhm | Conditional only; 41 V is not a frozen operating OCV. |
| 43.20 V | 86.4 mOhm | 38.4 mOhm | 48.0 mOhm | Uses PB-08 nominal system convention as an arithmetic point, not an asserted 50%-SOC OCV. |
| 50.40 V | 172.8 mOhm | 38.4 mOhm | 134.4 mOhm | Full-charge bus point; not representative of end-of-mission loaded-floor compliance. |

All values are first-order `V = OCV - I*R` arithmetic. The 43.2 V and 50.4 V rows are sensitivity points because PB-08 controls those bus conventions; they are **not** claims that P50B OCV equals those values at the impedance datum condition.

## Engineering consequence

The installed-path resistance budget cannot be frozen from nominal/full-charge voltage. At the condition-specific 39.20 V threshold derived by the preceding cell-only screen, there is **zero** remaining algebraic allowance for fuse/BMS/disconnect/connectors/harness/interconnect resistance. Therefore a real 36.0 V loaded-floor proof requires, at minimum, a controlled joint envelope for:

1. cell OCV versus SOC / temperature / SOH,
2. cell DC resistance versus SOC / temperature / SOH and current/time condition,
3. installed non-cell path resistance versus temperature and aging,
4. actual simultaneous pack current including auxiliary demand,
5. current sharing and cutoff/derating policy.

## Explicit non-claims

- No OCV point in this document is promoted to a PB-08 cell or pack requirement.
- `38.4 mOhm` remains a typical, condition-specific, ideal-sharing **cell-only** reference value.
- No fuse, BMS, disconnect, connector, busbar or harness resistance is invented.
- No loaded-floor compliance, thermal qualification, endurance, flight qualification or production readiness is claimed.
- P50B 12S4P remains reference-only; exact cell/P-count/pack implementation remains OPEN.

## Closure dependency

`controlled OCV/Rdc(SOC,T,SOH) + exact installed current-path components/geometry + simultaneous current -> installed pack sag/loss envelope -> 36 V loaded-floor compliance decision -> G1C`
