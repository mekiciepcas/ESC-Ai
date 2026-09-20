# PB-08 P50B 12S4P endurance / energy-margin screen

Date: 2026-09-20  
Status: **TRADE / ENERGY-BOUND PREWORK — NOT PACK FREEZE OR ENDURANCE QUALIFICATION**

## Purpose

Use only already-controlled PB-08 mission and cell-level energy inputs to quantify how the reference P50B 12S4P topology relates to the 10-minute / 20% gross-reserve sizing rule. This is a deterministic arithmetic screen, not a flight-endurance prediction and not a production pack selection.

## Controlled parent inputs

From `mission_requirements.json`:
- upper continuous aggregate propulsion study point = **3000 W**,
- target hover / first-order energy sizing duration = **10 min**,
- gross-pack reserve sizing policy = **20%**,
- PB-08 3 kW variant gross rated energy target = **>=750 Wh**.

From `PB08_P50B_12S4P_CELL_LEVEL_MASS_ENERGY_BOUND.md`:
- P50B 12S4P reference topology = 48 cells,
- minimum datasheet cell-level energy roll-up = **840 Wh**,
- typical cell-level energy roll-up = **864 Wh**,
- complete pack implementation remains OPEN.

## Deterministic energy arithmetic

The repository already carries the first-order 3 kW / 10 min / 20% reserve sizing result:

`E_gross,required = 3000 W * (10/60 h) / (1 - 0.20) = 625 Wh`

PB-08 deliberately freezes a more conservative product target of **>=750 Wh gross rated energy**. Relative to that frozen target, the reference 12S4P cell inventory provides:

- minimum-datasheet cell-energy margin: `840 - 750 = 90 Wh` = **12.0% above the 750 Wh target**,
- typical cell-energy margin: `864 - 750 = 114 Wh` = **15.2% above the 750 Wh target**.

Relative to the pure first-order 625 Wh mission-sizing arithmetic, the cell inventory provides:

- minimum-datasheet cell-energy headroom: `840 - 625 = 215 Wh` = **34.4%**,
- typical cell-energy headroom: `864 - 625 = 239 Wh` = **38.2%**.

These percentages are energy-accounting headroom only. They are not usable-energy guarantees.

## Reserve-accounted idealized duration screen

If the same 20% reserve policy is applied directly to the cell-level energy inventory, the arithmetic energy available before reserve is:

- minimum-datasheet case: `840 * 0.80 = 672 Wh`,
- typical case: `864 * 0.80 = 691.2 Wh`.

At exactly 3000 W propulsion demand, ignoring every auxiliary and conversion loss:

- minimum-datasheet idealized duration = `672 / 3000 * 60 = 13.44 min`,
- typical idealized duration = `691.2 / 3000 * 60 = 13.824 min`.

**These 13.44 / 13.824 minute figures are mathematical upper screens under explicitly idealized assumptions, not predicted flight endurance.** Real usable duration can only decrease when traction-pack auxiliary demand, ESC/motor conversion losses, voltage/sag cutoff behavior, temperature/SOC/SOH effects, reserve implementation, cell imbalance, BMS/protection limits and non-hover mission segments are included.

## Closure consequence

This screen establishes that the existing reference 12S4P cell inventory is not energy-deficient against the frozen >=750 Wh gross-rated target at the cell-data level. It does **not** prove that a completed P50B 12S4P pack meets the PB-08 mission because the following remain OPEN:

- exact production cell and P-count selection,
- complete installed pack mass and hardware,
- usable-energy definition at the controlled cutoff / loaded-floor policy,
- pack sag over SOC / temperature / SOH,
- simultaneous traction-pack auxiliary demand and conversion losses,
- actual vehicle hover power after MTOW / rotor architecture closure,
- BMS / fuse / disconnect / precharge constraints,
- physical endurance validation.

Therefore no G1 row or backlog task is promoted by this note. The correct next battery closure is still complete installed-pack hardware/mass plus sag/current-path evidence; the critical system path remains S1R.2 mass / rotor architecture closure.

## Evidence boundary

No physical-test, thermal, EMI, production-readiness or flight-qualification claim is made. P50B 12S4P remains `REFERENCE_ONLY` until an explicit product decision and complete pack evidence exist.
