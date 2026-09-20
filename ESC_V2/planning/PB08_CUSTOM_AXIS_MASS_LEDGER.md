# PB-08 custom installed-axis mass ledger

Date: 2026-09-20  
Status: **TRADE EVIDENCE / NOT A ROTOR OR BOM FREEZE**  
Authority: PB-08 common-platform mass trade. Unknown installed masses remain `OPEN`.

## Purpose

Close as much of S1R.2 installed-axis mass as evidence permits. Controlling equation: `Delta_residual = 2.025 - 2*m_axis - delta_structure - delta_common` kg. At the deliberately optimistic `delta_structure = delta_common = 0` boundary, break-even is 1.0125 kg/axis.

## Primary-source exact-pair propulsion anchor

T-Motor publishes U8 Lite KV85 as 12S, 243 g including cable, 36N42P and 225 +/- 5 mOhm interphase resistance. The manufacturer's current U8 Lite product description explicitly pairs **U8 Lite KV85 at 12S with NS28x9.2** carbon propeller. T-Motor's NS28x9.2 page publishes **59 g** mass for the integrated two-blade propeller.

Sources accessed 2026-09-20:
- https://store.tmotor.com/cn/product/u8-lite-kv85-u-efficiency.html
- https://store.tmotor.com/product/ns28x9_2-prop-uav-carbon-fiber.html

Detailed evidence boundary: `PB08_U8LITE_KV85_NS28_EXACT_PAIR_EVIDENCE.md`.

## Evidence-backed partial axis ledger

| Axis item | Mass | Evidence status |
|---|---:|---|
| U8 Lite KV85 motor incl. cable | 0.243 kg | PRIMARY MANUFACTURER |
| NS28x9.2 integrated propeller | 0.059 kg | PRIMARY MANUFACTURER; explicitly paired with KV85/12S |
| Custom ESC PCB + components | OPEN | no controlled mass evidence |
| ESC baseplate / heat spreader | OPEN | no controlled mass evidence |
| ESC enclosure / environmental sealing | OPEN | no controlled mass evidence |
| Local DC harness + connector | OPEN | no controlled mass evidence |
| Motor phase connector / termination delta | OPEN | no controlled mass evidence |
| Axis mounting hardware | OPEN | no controlled mass evidence |
| **Known exact-pair partial subtotal** | **0.302 kg** | not a complete installed axis |

## Hard mass-budget consequence

`m_remaining_to_axis_break_even = 1.0125 - 0.302 = 0.7105 kg/axis`.

Thus custom ESC + cooling/enclosure + local harness/connectors + axis mounting hardware must collectively remain below **710.5 g/axis** merely to preserve a mathematically possible Hexa mass advantage before Hexa-specific structural/common-system penalty.

For `D = delta_structure + delta_common`, `m_axis_limit = (2.025 - D)/2` and remaining non-motor/prop allowance is `(2.025 - D)/2 - 0.302` kg.

Sensitivity only, not product assumptions:

| D | Maximum total axis mass | Remaining after 0.302 kg |
|---:|---:|---:|
| 0.0 kg | 1.0125 kg | 0.7105 kg |
| 0.5 kg | 0.7625 kg | 0.4605 kg |
| 1.0 kg | 0.5125 kg | 0.2105 kg |

This does not prove Quad or Hexa superior.

## Repository-evidence audit for custom ESC mass

Current B1 BOM/planning records contain no controlled PCB, populated-board, baseplate, enclosure, connector/harness or mounting-hardware mass suitable for PB-08 installed-axis calculation. Those terms remain OPEN rather than inferred from dimensions or generic density.

## Closure criteria

A complete `m_axis` may enter the architecture decision only when exact motor mass, exact propeller plus adapter/mounting mass, custom ESC populated mass, cooling/baseplate/enclosure mass, local harness/connectors/terminations mass, mounting hardware mass, and exact motor/prop operating-point compatibility are controlled. Motor and propeller masses/compatibility now have primary evidence for U8 Lite KV85 + NS28x9.2; mounting/adapter hardware and all custom ESC/mechanical terms remain OPEN. Rotor architecture remains OPEN.
