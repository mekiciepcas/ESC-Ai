# PB-08 P50B 12S4P cell-only sag screen

Date: 2026-09-20  
Status: **REFERENCE / PARAMETRIC SCREEN — NOT PACK FREEZE / NOT PHYSICAL VERIFICATION**

## Purpose

Reduce S1R.3B uncertainty using only already-controlled repository evidence. This note does not select the production cell or prove the 36.0 V loaded-floor requirement.

## Controlled parents

From `PB08_P50B_12S4P_CELL_LEVEL_MASS_ENERGY_BOUND.md` and the Molicel P50B datasheet evidence recorded there:

- reference topology: 12S4P, 48 cells;
- typical cell DC impedance at 50% SOC: 12.8 mOhm;
- ideal equal-sharing 4P group cell-only resistance: 3.2 mOhm;
- 12-series cell-only arithmetic resistance: **38.4 mOhm** at that stated typical condition.

From PB-08:

- upper continuous propulsion study point: 3000 W;
- full-rated-power loaded-floor requirement: 36.0 V;
- propulsion-only continuous pack-current lower bound: 83.33 A.

## Deterministic arithmetic

For this screen only, use `R_cell_only_typ = 0.0384 ohm`.

At the 83.33 A propulsion-only current lower bound:

- `DeltaV = I * R = 83.33 * 0.0384 = 3.20 V`;
- `P_loss = I^2 * R = 83.33^2 * 0.0384 = 266.6 W`;
- ideal equal-sharing cell current = `83.33 / 4 = 20.83 A/cell`.

If 43.2 V nominal open-circuit voltage were used only as a mathematical reference at the same resistance condition, terminal voltage would be `43.2 - 3.20 = 40.0 V`. This is **not** a predicted flight voltage because 43.2 V is the PB-08 nominal system convention, not the P50B open-circuit voltage at 50% SOC.

The same resistance implies that an open-circuit pack voltage of at least `36.0 + 3.20 = 39.20 V` would be required to remain at 36.0 V under 83.33 A **before** adding interconnect, fuse, BMS/disconnect, connector, harness or temperature/aging resistance. This 39.20 V value is a conditional algebraic threshold, not a frozen cutoff.

## Sensitivity

Using the same 38.4 mOhm cell-only typical reference:

| Pack current | Cell current (ideal 4P) | Cell-only sag | Cell-only I^2R loss |
|---:|---:|---:|---:|
| 60 A | 15.00 A | 2.304 V | 138.2 W |
| 70 A | 17.50 A | 2.688 V | 188.2 W |
| 83.33 A | 20.83 A | 3.200 V | 266.6 W |
| 100 A | 25.00 A | 3.840 V | 384.0 W |

## Evidence boundary

This calculation shall **not** be promoted to pack resistance, pack thermal loss, usable energy, endurance, cutoff voltage or qualification. The 12.8 mOhm datum is typical and condition-specific. Real installed resistance and sag require controlled evidence for SOC, temperature, SOH, cell dispersion/current sharing, interconnect/welds, fuse, BMS/disconnect/precharge path, connectors, harness and measurement method.

No claim is made that P50B 12S4P passes the 36.0 V floor at 3 kW. The screen instead shows that cell internal resistance alone is material enough that sag closure cannot be skipped.

## Disposition

- Keep P50B 12S4P `REFERENCE_ONLY`.
- Keep exact pack current, usable energy, cutoff and pack mass OPEN.
- Use this screen to define the next evidence need: obtain/allocate the complete pack current-path resistance and a controlled P50B OCV/resistance envelope versus SOC/temperature/SOH before asserting loaded-floor compliance.
