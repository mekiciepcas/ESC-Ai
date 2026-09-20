# PB-08 P50B 12S4P cell-mass floor screen

Date: 2026-09-20
Status: REFERENCE-TOPOLOGY MASS PREWORK / NO PACK FREEZE

## Purpose
Bound one previously open part of S1R.3B using current manufacturer primary evidence, without inventing pack hardware mass. The P50B 12S4P topology remains reference-only and is not a production pack selection.

## Primary evidence
Molicel INR-21700-P50B Product Data Sheet v1.1 states maximum cell weight = 71 g, typical capacity = 18.0 Wh, minimum capacity = 17.5 Wh. Manufacturer product page also lists 71 g maximum cell weight. Source URLs:
- https://www.molicel.com/product/inr-21700-p50b/
- https://www.molicel.com/wp-content/uploads/4.TR%E7%B0%A1%E6%98%93%E8%A6%8F%E6%A0%BC_INR21700P50B_1.1_Product-Data-Sheet-of-INR-21700-P50B-80122.pdf

## Controlled derivation
Reference topology cell count: `12S * 4P = 48 cells`.

Using the manufacturer maximum cell mass:
- maximum cell inventory mass for the reference topology = `48 * 71 g = 3408 g = 3.408 kg`.
- minimum-datasheet cell energy inventory = `48 * 17.5 Wh = 840 Wh`.
- typical cell energy inventory = `48 * 18.0 Wh = 864 Wh`.

For arithmetic screening only, energy divided by the maximum cell-inventory mass gives:
- `840 Wh / 3.408 kg = 246.48 Wh/kg` using minimum energy and maximum cell mass.
- `864 Wh / 3.408 kg = 253.52 Wh/kg` using typical energy and maximum cell mass.

These are **cell-inventory** ratios, not installed-pack specific energy. Installed pack mass must be greater than the cell inventory once interconnects, insulation, compression/retention, enclosure, BMS, fuse, disconnect/precharge, connectors, harness, thermal hardware and mounting are included.

## Mass ledger boundary
| Element | Controlled mass | Status / required evidence |
|---|---:|---|
| 48 x P50B cells | <=3.408 kg from 71 g/cell max | PRIMARY-SOURCE BOUND; exact lot mass not measured |
| cell interconnects / busbars | OPEN | exact geometry/material or measured assembly |
| insulation / barriers / holders | OPEN | exact design/BOM or measured assembly |
| enclosure / structural retention | OPEN | exact CAD/material or measured assembly |
| BMS electronics | OPEN | exact selected assembly |
| fuse | OPEN | exact selected part |
| disconnect / contactor / solid-state switch | OPEN | exact selected implementation |
| precharge hardware | OPEN | exact selected implementation |
| connectors / service disconnect | OPEN | exact selected parts |
| traction harness | OPEN | exact length/gauge/terminations or measured assembly |
| thermal hardware | OPEN | exact design |
| vehicle mounting hardware | OPEN | exact design |
| **installed pack total** | **OPEN** | sum of controlled installed elements / physical weighing |

## Promotion rule
The 3.408 kg value may be used only as a manufacturer-max **cell inventory bound** for the reference-only 12S4P screen. It shall not be entered as battery mass in `mission_requirements.json` and shall not close S1R.2, UAV-001, UAV-002 or UAV-005. Installed battery mass requires the complete pack hardware ledger or controlled physical measurement.

## Engineering implication
The reference topology already consumes up to 3.408 kg before any pack overhead. Therefore architecture/mass trades that use only bare-cell mass are optimistic. This narrows the missing evidence: the remaining battery-mass unknown is pack overhead plus exact as-built cell lot mass, not the cell-count arithmetic itself.

## Claims explicitly not made
No exact production pack selection; no installed pack mass; no usable-energy claim; no thermal/current-sharing proof; no 36 V loaded-floor compliance; no flight endurance or qualification claim.
