# PB-08 custom installed-axis mass ledger

Date: 2026-09-20  
Status: **TRADE EVIDENCE / NOT A ROTOR OR BOM FREEZE**  
Authority: PB-08 common-platform mass trade. Unknown installed masses remain `OPEN`.

## Purpose

Close as much of the S1R.2 installed-axis mass term as evidence permits without inventing custom ESC, cooling, harness or mounting mass. The controlling PB-08 Hexa-vs-Quad residual equation remains:

`Delta_residual = 2.025 - 2*m_axis - delta_structure - delta_common` kg.

Hexa has positive residual-mass advantage only when this value is greater than zero. At the deliberately optimistic boundary `delta_structure = delta_common = 0`, the per-axis break-even remains 1.0125 kg.

## Primary-source propulsion mass anchors

Current T-Motor manufacturer data for U8 Lite KV85 states:
- rated voltage: 12S,
- motor mass including cable: **243 g**,
- recommended propeller class: **28-29 inch**,
- configuration: **36N42P**,
- interphase resistance: **225 +/- 5 mOhm**,
- peak current: **19.1 A for 180 s**,
- max power: **916.8 W for 180 s**.

Source: T-Motor U8 Lite KV85 product page, accessed 2026-09-20: https://store.tmotor.com/product/u8-lite-kv85-u-efficiency.html

Current T-Motor manufacturer data for the HEP-L 29x11 propeller states:
- diameter: **29 inch**,
- average mass: **63 g**,
- normal thrust range: **2.9-5 kg**,
- normal RPM range: **1950-2510 rpm**,
- recommended maximum RPM: **4900 rpm**.

Source: T-Motor HEP-L 29x11 product page, accessed 2026-09-20: https://store.tmotor.com/jp/product/hep-l-29-11-carbon-fiber-multirotor-propeller.html

Important compatibility boundary: the HEP-L page names a U8II Lite KV100 combination, while the motor anchor above is U8 Lite KV85. Therefore **243 g + 63 g is a mass-class ledger anchor only**, not an exact selected motor/propeller pair and not operating-point evidence.

## Evidence-backed partial axis ledger

| Axis item | Mass | Evidence status |
|---|---:|---|
| U8 Lite KV85 motor incl. cable | 0.243 kg | PRIMARY MANUFACTURER |
| 29-inch HEP-L propeller | 0.063 kg | PRIMARY MANUFACTURER; mass-class anchor only |
| Custom ESC PCB + components | OPEN | no controlled mass evidence |
| ESC baseplate / heat spreader | OPEN | no controlled mass evidence |
| ESC enclosure / environmental sealing | OPEN | no controlled mass evidence |
| Local DC harness + connector | OPEN | no controlled mass evidence |
| Motor phase connector / termination delta | OPEN | no controlled mass evidence |
| Axis mounting hardware | OPEN | no controlled mass evidence |
| **Known partial subtotal** | **0.306 kg** | not a complete installed axis |

## Hard mass-budget consequence

Using only the source-backed partial subtotal and the optimistic zero-extra-structure/common boundary:

`m_remaining_to_axis_break_even = 1.0125 - 0.306 = 0.7065 kg/axis`.

Thus the combined mass of the custom ESC, its cooling/enclosure, local harness/connectors and axis mounting hardware must be **less than 706.5 g per axis merely to keep the Hexa mass case mathematically possible before any Hexa-specific structural/common-system penalty is charged**.

More generally, for a measured or allocated Hexa structural/common penalty `D = delta_structure + delta_common`:

`m_axis_limit = (2.025 - D) / 2` kg,

and with the 0.306 kg partial propulsion subtotal:

`m_ESC_cooling_harness_mount_limit = (2.025 - D)/2 - 0.306` kg.

Examples are sensitivity only, not product assumptions:

| Hexa extra structural/common penalty D | Maximum total axis mass | Remaining after 0.306 kg partial subtotal |
|---:|---:|---:|
| 0.0 kg | 1.0125 kg | 0.7065 kg |
| 0.5 kg | 0.7625 kg | 0.4565 kg |
| 1.0 kg | 0.5125 kg | 0.2065 kg |

The table shows why structure and custom-ESC installed mass must be measured/allocated together. It does **not** prove Quad or Hexa is superior.

## Repository-evidence audit for custom ESC mass

The current B1 BOM and planning records contain electrical components and provisional DC-link quantities but no controlled PCB mass, populated-board mass, baseplate mass, enclosure mass, connector/harness mass or mounting-hardware mass suitable for the PB-08 installed-axis calculation. Therefore these terms remain OPEN rather than being inferred from board dimensions, copper density, generic enclosure data or historical hardware.

B1 remains an electrical requalification candidate only; this ledger does not qualify B1 for PB-08.

## Closure criteria for this ledger

A complete `m_axis` may be promoted into the PB-08 architecture decision only when all of the following are controlled for one exact candidate axis:

1. exact motor MPN and measured/manufacturer mass,
2. exact propeller + adapter/mounting mass,
3. custom ESC populated mass,
4. cooling/baseplate/enclosure installed mass,
5. local harness/connectors/terminations mass,
6. axis mounting hardware mass,
7. compatibility of the exact motor/prop operating point with the 12S PB-08 electrical envelope.

Until then `m_axis` remains OPEN and rotor architecture remains OPEN.
