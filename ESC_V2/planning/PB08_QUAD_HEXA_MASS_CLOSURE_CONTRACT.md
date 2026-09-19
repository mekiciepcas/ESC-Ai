# PB-08 Quad/Hexa mass closure contract

Date: 2026-09-20  
Branch: `uav-rebaseline`  
Status: **CONTROLLED PARAMETRIC CLOSURE / ROTOR COUNT NOT FROZEN**

## Purpose

Convert the current Quad-versus-Hexa trade into an explicit, fail-closed mass decision without inventing frame, ESC, propeller, cable, battery-hardware, avionics or payload masses.

Authority inputs already controlled by PB-08:
- 3 kW manufacturer-curve MTOW screen: Quad 16.278 kg; Hexa 18.303 kg.
- Screened Hexa MTOW gain: 2.025 kg.
- Conservative Hobbywing X8 G2 integrated propulsion-axis mass anchor: 1.095 kg/axis.
- T-Motor U8 Lite motor-only reference: 0.243 kg; this is **not** an installed-axis mass.
- 12S4P P50B cells-only reference: <=3.408 kg; pack hardware remains OPEN.

These are sizing/trade inputs, not flight-test results.

## Exact architecture inequality

Define:
- `m_axis` = installed mass of one complete propulsion axis: motor + propeller + custom ESC + enclosure/thermal hardware + local power/phase/control cable + connectors + axis-specific mounting hardware [kg].
- `delta_structure` = Hexa-only structural mass increment relative to Quad: two extra arms plus joints/reinforcement/wiring not already included in `m_axis` [kg].
- `delta_common` = any architecture-dependent common-system mass increment not captured above [kg].

Then the Hexa residual-mass advantage at the current 3 kW screen is:

`Delta_residual = 2.025 - 2*m_axis - delta_structure - delta_common` [kg]

Decision rule:
- `Delta_residual > 0`: Hexa has greater residual mass available for payload/common equipment at this screen.
- `Delta_residual < 0`: Quad has greater residual mass available.
- `Delta_residual = 0`: mass break-even; degraded-mode, controllability, cost and serviceability decide.

Equivalent maximum installed-axis mass for Hexa mass advantage:

`m_axis < (2.025 - delta_structure - delta_common)/2`

This equation is the architecture mass closure criterion. No rotor architecture may be marked FROZEN from mass alone until `m_axis`, `delta_structure` and `delta_common` are evidence-backed.

## Sensitivity table

Assuming `delta_common = 0` only to expose the decision boundary (not as a product assumption):

| Hexa extra structure [kg] | Maximum installed axis mass for Hexa advantage [kg/axis] |
|---:|---:|
| 0.00 | 1.0125 |
| 0.25 | 0.8875 |
| 0.50 | 0.7625 |
| 0.75 | 0.6375 |
| 1.00 | 0.5125 |

The historical 1.095 kg X8 G2 integrated anchor is already above the zero-extra-structure break-even and therefore cannot justify Hexa on mass. Conversely, the 0.243 kg U8 Lite number is motor-only and cannot justify Hexa either because propeller, ESC, cooling/enclosure, cabling/connectors and mounting are missing.

## Required measured/source-backed roll-up fields

Before S1R.2 mass closure, record for each candidate architecture:
1. exact motor MPN and mass;
2. exact propeller MPN and mass;
3. custom ESC target/measured mass including enclosure/baseplate;
4. local power/phase/control harness and connector mass per axis;
5. axis-specific mount mass;
6. frame center-body mass;
7. arm/joint/reinforcement mass by architecture;
8. battery cells plus busbar/interconnect/BMS/fuse/disconnect/enclosure mass;
9. avionics, GNSS, telemetry and flight-controller mass;
10. landing gear and fixed wiring mass;
11. mission-equipment mass;
12. payload mass.

Unknown fields remain `OPEN/null`; a cells-only battery mass may not be reported as pack mass.

## Payload derivation

Once evidence-backed masses exist:

`payload_allowance = MTOW_screen - propulsion_installed - frame_structure - complete_pack - avionics - landing_gear - fixed_wiring - mission_equipment`

Payload is a derived residual, not an assumed input for this trade. A negative residual rejects the candidate at the screened operating point.

## Non-mass architecture gate

Mass advantage alone is insufficient. Rotor count also requires an explicit degraded-mode policy. PB-08 currently has single-motor-failure behavior OPEN. Therefore even a positive Hexa mass residual does not freeze Hexa until degraded behavior is defined and supported by control/thrust evidence.

## Closure states

- `MASS_DATA_OPEN`: any required architecture-dependent mass is unknown.
- `MASS_TRADE_CLOSED`: all mass terms are evidence-backed and the residual comparison is computed.
- `ARCHITECTURE_READY_FOR_DECISION`: mass trade closed **and** degraded-mode policy is controlled.
- `ARCHITECTURE_FROZEN`: product baseline explicitly records the selected architecture.

Current state: **MASS_DATA_OPEN**.

## Next evidence action

Select the exact motor/prop candidate pair(s) and obtain source-backed propeller mass; establish a bounded custom ESC + enclosure/baseplate mass target from the B1 mechanical baseline or a new mechanical allocation; then obtain/derive Quad-versus-Hexa frame/arm structural masses. Until those inputs exist, keep rotor count and payload OPEN.
