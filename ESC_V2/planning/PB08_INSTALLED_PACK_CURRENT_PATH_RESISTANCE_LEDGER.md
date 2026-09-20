# PB-08 installed pack current-path resistance closure ledger

Date: 2026-09-20
Status: **OPEN / CLOSURE CONTRACT ONLY — NO INSTALLED-PACK COMPLIANCE CLAIM**
Scope: S1R.3B / UAV-005

## Purpose

Convert the conditional non-cell resistance allowance into a controlled installed-pack evidence ledger without inventing component resistance. This file does **not** select a fuse, BMS/disconnect, connector, busbar, harness, cell interconnect or pack topology. Unknown values remain OPEN.

## Controlled parents

- PB-08 full-rated loaded-bus floor: **36.0 V**.
- Propulsion-only continuous pack-current lower bound: **83.33 A** (`3000 W / 36.0 V`).
- Reference topology only: P50B 12S4P.
- Condition-specific cell-only reference used by the preceding screen: **38.4 mOhm** (typical 50%-SOC datum under ideal 4P sharing).
- `P_aux,pack`, simultaneous installed current, exact pack, OCV/SOC-temperature-SOH envelope and actual non-cell resistance remain OPEN.

## Governing equations

For any controlled operating condition `k`:

`R_noncell,max,k = (V_OCV,k - V_loaded_floor) / I_pack,k - R_cell,k`

Installed-path compliance at that same condition requires:

`R_noncell,installed,k = R_cell_interconnect + R_busbar + R_fuse + R_BMS_or_disconnect + R_connector + R_harness + R_other`

and

`R_noncell,installed,k <= R_noncell,max,k`.

Voltage drop and dissipation for each installed element `i` are:

`DeltaV_i = I_pack,k * R_i,k`

`P_i = I_pack,k^2 * R_i,k`.

All resistance values must be evaluated at an evidenced relevant temperature/current condition; room-temperature nominal resistance alone is not sufficient for final thermal/loaded-floor compliance.

## Installed-path evidence ledger

| Path element | Exact MPN / geometry | Resistance basis | R at relevant condition | Temperature / condition | Evidence | Status |
|---|---|---|---:|---|---|---|
| Cell-to-cell / parallel-group interconnect | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN |
| Series busbar / pack conductor | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN |
| Main fuse | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN |
| BMS power path or contactor/disconnect | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN |
| Pack output connector pair | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN |
| Vehicle traction harness to ESC distribution | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN |
| Distribution junction / additional bolted joints | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN |
| Other series element | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN |
| **TOTAL NON-CELL** | — | sum of evidenced rows only | **OPEN** | joint worst-case condition required | — | **OPEN** |

## Evidence acceptance rules

A row may become numeric only from one of the following:

1. exact selected-part primary-source resistance/drop data with the applicable current and temperature condition identified;
2. geometry/material calculation with controlled dimensions, material resistivity and temperature correction;
3. controlled four-wire measurement of the installed element/path with current, temperature and uncertainty recorded.

Do not infer actual installed resistance from current rating, fuse ampere rating, connector marketing current, cable AWG alone, or B1/A2 legacy values.

## Closure test

The 36.0 V loaded-floor claim remains OPEN until one joint operating point contains all of:

- evidenced `V_OCV,k` and `R_cell,k` at the same SOC/temperature/SOH condition;
- evidenced simultaneous `I_pack,k`, including propulsion and traction-pack auxiliary demand;
- exact installed non-cell path and resistance sum at relevant temperature;
- fuse/BMS/disconnect/connector/harness thermal limits at that current/duration;
- demonstrated positive voltage margin after measurement/model uncertainty.

The preceding 39.20 V conditional threshold has **0 mOhm** algebraic non-cell allowance at 83.33 A with the 38.4 mOhm cell-only reference. Therefore it cannot establish installed-pack compliance because every real installed path has positive series resistance.

## Next evidence actions

1. Populate exact pack current-path architecture only after component/geometry selections are controlled.
2. Obtain a controlled P50B OCV/Rdc envelope versus SOC, temperature and SOH before choosing the limiting allowance row.
3. Replace 83.33 A with the final simultaneous continuous pack current only when `P_aux,pack` and residual uncertainty policy close.
4. Calculate element voltage drop and I²R heating, then verify thermal ratings and the 36.0 V floor jointly.

Evidence level: **ENGINEERING CLOSURE CONTRACT / NO PHYSICAL VERIFICATION**.
