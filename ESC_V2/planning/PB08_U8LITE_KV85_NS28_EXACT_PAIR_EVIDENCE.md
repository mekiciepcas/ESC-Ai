# PB-08 U8 Lite KV85 + NS28x9.2 exact-pair evidence

Date: 2026-09-20  
Status: **PRIMARY-SOURCE TRADE EVIDENCE / NOT A MOTOR, PROP, ROTOR OR BOM FREEZE**

## Purpose

Replace the previous same-class HEP-L propeller mass anchor with a manufacturer-explicit compatible propeller for the T-Motor U8 Lite KV85 12S candidate, while keeping all custom ESC/mechanical installed masses OPEN.

## Primary evidence

T-Motor's current U8 Lite product page explicitly states for **U8 Lite KV85**:
- rated voltage: **12S**,
- motor mass including cable: **243 g**,
- slot/pole configuration: **36N42P**,
- interphase resistance: **225 +/- 5 mOhm**,
- recommended propeller class: **28-29 inch**.

The same manufacturer page's product description explicitly pairs **U8 Lite KV85 at 12S with T-MOTOR NS28x9.2 carbon propeller** and states a 7.1 kg maximum-thrust claim for that combination. This is manufacturer sizing evidence, not physical verification of this project.

Source, accessed 2026-09-20:
https://store.tmotor.com/cn/product/u8-lite-kv85-u-efficiency.html

T-Motor's current NS28x9.2 product page states:
- model: **28x9.2**,
- integrated two-blade propeller,
- mass: **59 g**,
- diameter: **28 inch**,
- pitch: **9.2 inch**,
- recommended thrust/RPM: **5-9.5 kg / 2900-3940 rpm**,
- recommended maximum thrust/RPM: **19 kg / 5490 rpm**.

Source, accessed 2026-09-20:
https://store.tmotor.com/product/ns28x9_2-prop-uav-carbon-fiber.html

## Exact-pair partial mass ledger

Because the motor manufacturer itself names NS28x9.2 for the KV85/12S combination, the prior compatibility caveat attached to the HEP-L 29-inch mass-class anchor is removed for this specific motor+prop pair.

| Item | Mass | Evidence |
|---|---:|---|
| T-Motor U8 Lite KV85 incl. cable | 0.243 kg | primary manufacturer |
| T-Motor NS28x9.2 integrated propeller | 0.059 kg | primary manufacturer; explicitly paired on motor page |
| **Exact-pair partial subtotal** | **0.302 kg** | motor + prop only |

This remains a **partial** installed-axis mass. It does not include custom ESC, cooling/baseplate, enclosure, local DC/phase harness/connectors, or mounting hardware.

## PB-08 mass-bound consequence

PB-08 optimistic Hexa-vs-Quad per-axis break-even before extra Hexa structure/common-system mass is 1.0125 kg/axis.

With the exact-pair partial subtotal:

`m_remaining = 1.0125 - 0.302 = 0.7105 kg/axis`.

Therefore custom ESC + cooling/baseplate + enclosure + local harness/connectors + mounting hardware must collectively remain below **710.5 g/axis** merely to preserve a mathematically possible Hexa mass advantage at the deliberately optimistic zero-extra-structure/common boundary.

Sensitivity only, not product assumptions:

| Total Hexa structural/common penalty D | Axis mass limit | Remaining after exact-pair 0.302 kg subtotal |
|---:|---:|---:|
| 0.0 kg | 1.0125 kg | 0.7105 kg |
| 0.5 kg | 0.7625 kg | 0.4605 kg |
| 1.0 kg | 0.5125 kg | 0.2105 kg |

## What this closes and what it does not

Closed as evidence:
- exact manufacturer-explicit motor/prop compatibility anchor for U8 Lite KV85 + NS28x9.2 at 12S,
- exact published motor mass and propeller mass,
- exact-pair motor+prop partial mass subtotal of 0.302 kg.

Still OPEN:
- whether this pair is selected for PB-08,
- exact PB-08 hover/max operating point and efficiency,
- custom ESC installed mass,
- cooling/enclosure/harness/connector/mounting mass,
- Quad/Hexa structural/common mass delta,
- degraded-mode policy,
- rotor architecture and MTOW/payload freeze.

No physical test, flight qualification, thermal validation or production-readiness claim is made.
