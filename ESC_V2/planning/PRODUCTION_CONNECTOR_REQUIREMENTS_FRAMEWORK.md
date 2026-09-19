# Production connector requirements framework

Date: 2026-09-19  
Branch: `uav-rebaseline`  
Status: `STRUCTURE_DEFINED_PRODUCT_VALUES_OPEN`

## Purpose

Define what must be proven before any external or board-to-board connector is promoted from B1 PoC hardware to a U1 production-intent connector. This framework implements `MFG-IF-001` without guessing vehicle/harness values.

## Anti-hallucination rule

All numeric electrical, mechanical and environmental values remain `OPEN/TBD` unless they come from frozen parent requirements, exact connector primary-source evidence or physical test. Existing B1 WR-PHD headers and the logical 2x20 board interface are references only.

## Connector classes to be closed

| Interface class | Example function | Current U1 status |
|---|---|---|
| Battery/DC input | pack to ESC power | OPEN |
| Three motor phases | ESC to motor U/V/W | OPEN |
| CAN / vehicle control | CANH/CANL and optional shield/ground | OPEN |
| Hall / rotor position | sensor supply + signals | OPEN |
| Motor temperature | resistive/digital sensor interface | OPEN |
| Fan / auxiliary load | exported power/control | OPEN |
| Service/debug | SWD/JTAG/UART/service | OPEN |
| Power-control board interconnect | control/power partition interface | OPEN |

## Mandatory requirement record for each production connector

Each connector shall have the following fields before G3/G5 release:

### Identity and mating

- U1 interface ID.
- PCB reference designator(s).
- Exact manufacturer.
- Exact orderable PCB-side MPN.
- Exact mating connector/housing MPN.
- Exact terminal/contact MPN.
- Approved wire gauge range.
- Approved seal/backshell/strain-relief parts if applicable.
- Pin-map authority and revision.
- Keying/polarization mechanism.
- Positive latch/locking mechanism.
- Mating orientation and service-access definition.
- DNP/service-only status where relevant.

### Electrical envelope

- Maximum continuous current per contact: `OPEN`.
- Peak/transient current per contact and duration: `OPEN`.
- Maximum working voltage: `OPEN`.
- Dielectric-withstand requirement: `OPEN`.
- Contact resistance limit and temperature-rise criterion: `OPEN`.
- Creepage/clearance contribution where relevant: `OPEN`.
- Shield/drain assignment where relevant: `OPEN`.
- Grounding/reference strategy: `OPEN`.
- Hot-plug requirement: `OPEN`.
- Reverse-polarity/mismating hazard and prevention: `OPEN`.

### Mechanical / environmental envelope

- Operating temperature: `OPEN`.
- Storage temperature: `OPEN`.
- Vibration spectrum/level: `OPEN`.
- Mechanical shock requirement: `OPEN`.
- Retention / pull-force requirement: `OPEN`.
- Connector mating-cycle target: `OPEN`.
- Ingress / sealing target: `OPEN`.
- Dust, water, chemical/spray exposure: `OPEN`.
- UV/outdoor exposure if external: `OPEN`.
- Altitude/pressure implication: `OPEN`.
- Harness bend-radius and strain-relief requirement: `OPEN`.

### Manufacturing / serviceability

- Exact footprint linked to primary drawing.
- PCB keepout/courtyard.
- Assembly process compatibility.
- Inspection access.
- Pin-1/orientation marking.
- Replacement/service policy.
- Supplier lifecycle/availability evidence.
- Alternate part policy and exact compatibility constraints.

## Interface-specific closure notes

### Battery/DC input

Must not be selected before `UAV-005/UAV-006` freeze the voltage/current envelope. Connector current rating alone is not sufficient; contact temperature rise, cable gauge, duty cycle, ambient and fault coordination must be evaluated together.

### Motor phase connectors

Must close continuous/peak phase current, thermal rise, vibration retention and creepage/clearance against final bus voltage. Three identical phase interfaces shall have controlled pin/keying conventions that prevent accidental cross-connection or polarity assumptions not represented in firmware/system integration.

### CAN / control connector

Must close CAN topology, shield/reference policy, termination location, signal return strategy and transient protection before pinout freeze. If the CAN architecture is isolated, the connector grounding/shield strategy shall reflect that architecture explicitly.

### Hall / motor temperature

Cannot be frozen before the selected motor defines sensor electrical type, supply requirement, voltage levels, fault behavior and connector compatibility. B1 WR-PHD headers are not promoted automatically.

### Fan / exported auxiliary power

Connector selection must wait for `PWR-EXT-001` continuous/peak/inrush/short/backfeed contract. A converter's output-current rating is not a connector load requirement.

### Control/power board interconnect

Logical same-net equivalence is insufficient. Production closure shall prove mating pair, orientation, keying, stack height, retention, board tolerance, current per contact, ground-return allocation and repeated assembly behavior.

## Required verification evidence

1. Primary manufacturer drawings and datasheets for connector, mate and contacts.
2. Exact wire/crimp tooling/process evidence where crimped contacts are used.
3. Pin-map review against schematic/netlist authority.
4. Mechanical fit/mating review using actual board/harness geometry.
5. Current/temperature-rise evidence for power contacts under worst frozen duty.
6. Retention/vibration/shock evidence or test where required by ENV.
7. Ingress/sealing evidence if the connector crosses the product environmental boundary.
8. Mis-mating/keying review.
9. Manufacturing/inspection/serviceability review.

## Release rule

No connector may be marked `SELECTED_FOR_U1_PRODUCTION` until:

- parent electrical/interface/environment requirements are FROZEN,
- exact connector + mate + contact MPNs are known,
- exact footprint is checked against the primary drawing,
- pin map is reviewed,
- electrical derating is documented,
- mechanical/environmental suitability is documented,
- remaining critical connector TBD count is zero.

## Current conclusion

The connector **requirements structure is now defined**, but every U1 production connector remains OPEN. This is intentional and prevents the B1 PoC headers or a generic 2x20 interconnect from being mistaken for UAV-qualified hardware.
