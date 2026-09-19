# ESC-U1 Heavy-Lift UAV ESC - Preliminary Engineering Datasheet

**Document revision:** PDS-00  
**Date:** 2026-09-19  
**Branch:** `uav-rebaseline`  
**Status:** PRELIMINARY / CONCEPT-STAGE / NOT FOR PRODUCTION  
**Next component-bearing schematic revision:** `U1-SCH-R001` - not yet allocated

> This document is an engineering datasheet for the current design intent. Values marked `OPEN` are not frozen. Values marked `TRADE_ONLY` are architecture stress-screening references derived from market/propulsion benchmarks and must not be treated as guaranteed product ratings.

## 1. Product intent

| Item | Current value | Status |
|---|---:|---|
| Product | ESC-U1 heavy-lift multirotor electronic speed controller | DESIGN_INTENT |
| Intended vehicle class | Heavy-lift agricultural multirotor UAV | DESIGN_INTENT |
| User payload target | 70-100 kg payload class | USER_TARGET |
| Motor type | 3-phase BLDC/PMSM | DESIGN_INTENT |
| Control objective | FOC / SVPWM capable control architecture | PLANNED |
| Flight-controller link | CAN-family vehicle interface | PLANNED |
| Production release | Not allowed | BLOCKED |

The 70-100 kg figure is payload, not aircraft MTOW. Final MTOW, rotor count, propulsion operating point, battery architecture and ESC electrical requirements remain open while the mechanical concept is co-developed.

## 2. Electrical envelope

| Parameter | Preliminary value | Status / meaning |
|---|---:|---|
| DC input operating voltage | OPEN | Final battery/propulsion architecture not frozen |
| Architecture stress-screen voltage | up to 81 V DC | TRADE_ONLY benchmark reference |
| Candidate semiconductor VDS class | 120 V / 150 V | ACTIVE_TRADE |
| 100 V semiconductor class | Legacy comparison only | NOT_PREFERRED_FOR_CURRENT_SCREEN |
| Continuous DC bus current requirement | OPEN | Phase/bus operating point not frozen |
| Stress-screen continuous bus current | 120 A | TRADE_ONLY benchmark example |
| Peak DC bus current requirement | OPEN | Final duration and thermal limits not frozen |
| Stress-screen peak bus current | 300 A for 3 s | TRADE_ONLY benchmark example |
| Continuous output power requirement | OPEN | Final motor/prop operating point not frozen |
| Stress-screen propulsion power | 4.64 kW class | TRADE_ONLY benchmark example |
| Phase RMS current | OPEN | Must be derived from selected motor and operating point |
| Phase peak current | OPEN | Must be derived from torque/transient requirement |
| PWM frequency | OPEN | Must close from motor/control/loss/acoustic trade |
| Maximum electrical RPM | OPEN | Motor pole count and max mechanical RPM not frozen |
| Regenerative/transient bus ceiling | OPEN | BMS/cable/DC-link/regen architecture not frozen |

### Voltage-class screening note

Using the current 81 V architecture stress reference only:

- 100 V device class leaves 19 V static headroom before switching spikes, wiring inductance, regeneration and tolerance.
- 120 V device class leaves 39 V static headroom.
- 150 V device class leaves 69 V static headroom.

This is not a final derating decision. Dynamic VDS overshoot, avalanche policy, switching loss, package thermal path and layout parasitics still require analysis and bench measurement.

## 3. Power-stage architecture

| Function | Current direction | Status |
|---|---|---|
| Inverter | 3-phase, six-switch bridge | PLANNED |
| Power switch | 120 V / 150 V MOSFET candidate classes | ACTIVE_TRADE |
| Parallel switches per position | OPEN | Loss/thermal/current-sharing study pending |
| Gate drive | High-current 3-phase or per-half-bridge architecture | ACTIVE_TRADE |
| Gate-driver candidates | DRV8353 legacy reference; UCC27282 / UCC27712 / UCC21540-Q1 trade anchors | CANDIDATE_ONLY |
| DC link | Bulk + local high-frequency decoupling | PLANNED |
| Precharge / inrush control | Required | PLANNED |
| Regeneration / overvoltage handling | Required architecture decision | OPEN |
| Input fuse / fault isolation | Required | PLANNED |

No production MOSFET, gate driver, capacitor, fuse or connector has been selected.

## 4. Control and sensing

| Function | Current direction | Status |
|---|---|---|
| Control algorithm | FOC / SVPWM capable | PLANNED |
| MCU candidate | STM32G474RET3 | CANDIDATE |
| MCU alternative | TI TMS320F280041C family | CANDIDATE |
| Phase-current sensing | Required | PLANNED |
| Bus-voltage sensing | Required | PLANNED |
| MOSFET/PCB temperature sensing | Required | PLANNED |
| Motor temperature input | Planned vehicle interface | PLANNED |
| Hall/position input | Candidate / motor-dependent | OPEN |
| Hardware overcurrent trip | Independent hardware trip path required | PLANNED |
| Hardware PWM inhibit | Independent inhibit path required | PLANNED |
| Fault latch / deliberate re-arm | Required safety-control principle | PLANNED |

Exact shunt value, amplifier topology, comparator thresholds, ADC ranges, fault latency and filter constants remain open until the electrical envelope is frozen.

## 5. Communications and I/O

| Interface | Current direction | Status |
|---|---|---|
| Vehicle network | CAN / CAN-FD trade | OPEN |
| Legacy CAN reference | SN65HVD230DR | REVALIDATE |
| Modern CAN candidates | TCAN1044A-Q1, TCAN1042HGV-Q1, TJA1044GT/3 | CANDIDATE |
| Isolated CAN option | ISO1042-Q1 | CANDIDATE_IF_REQUIRED |
| Debug/programming | SWD/JTAG-class development interface | PLANNED |
| Telemetry | Bus voltage/current, phase/current state, temperatures, faults | PLANNED |
| External inhibit / E-stop | Interface required; fail-safe implementation OPEN | OPEN |

Final CAN protocol, bitrate, termination, TVS/CMC, harness grounding, connector and isolation policy are not frozen.

## 6. Protection functions

Planned protection coverage includes:

- Phase overcurrent / short-circuit response
- DC-bus overvoltage
- DC-bus undervoltage
- Gate-driver fault handling
- MCU watchdog/reset fault handling
- CAN command-loss timeout
- Current-sense plausibility fault
- Voltage-sense plausibility fault
- MOSFET/PCB/motor overtemperature
- External inhibit/E-stop fault path
- Auxiliary-power fault
- Connector/harness open/short fault handling

Thresholds, timing and safe-state behavior are `OPEN` until parent system requirements close.

## 7. Mechanical and environmental

| Parameter | Current value | Status |
|---|---:|---|
| ESC dimensions | OPEN | Mechanical packaging not designed |
| ESC mass | OPEN | Mechanical/thermal concept not designed |
| Cooling method | OPEN | Conduction / forced-air / vehicle-integrated trade pending |
| Ambient temperature range | OPEN | G0 environment input missing |
| Altitude derating | OPEN | G0 environment input missing |
| Ingress protection | OPEN | Vehicle/environment requirement missing |
| Vibration/shock qualification | OPEN | Test standard not selected |
| Battery connector | OPEN | Current/temperature/mechanical requirements missing |
| Phase connectors | OPEN | Current/temperature/mechanical requirements missing |
| Control connector | OPEN | Vehicle interface requirements missing |

## 8. Current benchmark context - not product ratings

The current concept-stage propulsion screening uses manufacturer data only as a reference envelope. Relevant commercial benchmark regions include 12-14S and 18S propulsion systems, high-end input voltages around 78.3-81 V, and examples up to 120 A continuous / 300 A short-duration input current in integrated propulsion systems.

These values are used to stress-test ESC architecture choices. They do **not** establish the custom ESC's final voltage, current or power ratings.

## 9. Verification status

| Verification item | Status |
|---|---|
| Requirements schema / tracking structure | PASS for structure |
| U1 architecture-only KiCad scaffold | PASS |
| U1 scaffold KiCad parser/netlist/ERC | PASS for zero-component scaffold only |
| Legacy B1 KiCad reproducible baseline | PASS for recorded software-baseline scope only |
| ESC electrical pretrade consistency script | PASS |
| Component-bearing U1 schematic | NOT_STARTED |
| U1 electrical ERC | NOT_RUN |
| U1 PCB DRC | NOT_RUN |
| Switching bench test | NOT_RUN |
| Thermal test | NOT_RUN |
| EMI/EMC test | NOT_RUN |
| Dyno / prop-stand test | NOT_RUN |
| Flight qualification | NOT_RUN |

## 10. Design maturity

- Requirements structure: 100%
- G1 SYSTEM FREEZE value closure: 2.2% (1/46)
- Backlog DONE: 4% (1/25)
- Major gates closed: 0/8
- U1 KiCad architecture scaffold: 100%
- Component-bearing U1 production-intent schematic: 0%

These percentages measure different things and must not be combined into a single product-readiness percentage.

## 11. Primary project evidence

Internal design authorities / evidence:

- `G0_INPUT_CLOSURE_PACKET.json`
- `CONCEPT_VEHICLE_ENVELOPE_PRETRADE.json`
- `PROPULSION_SCREENING_PRETRADE.json`
- `ESC_ELECTRICAL_ENVELOPE_PRETRADE.json`
- `SEMICONDUCTOR_VOLTAGE_CLASS_CANDIDATES.md`
- `U1_BOM_CANDIDATES.json`
- `U1_G3_ERC_POLICY.json`
- `KICAD_CI_VERIFICATION.json`
- `B1_KICAD_BASELINE_AUDIT.json`

Manufacturer benchmark sources currently referenced in the concept trade include DJI AGRAS T70P/T100 and Hobbywing X11/X13/X15/X15 G2 product documentation. Benchmark data remains `TRADE_ONLY` until converted into a requirement by the system-design process.

## 12. Release statement

**PDS-00 is not a production datasheet.** It is a controlled preliminary engineering snapshot intended to keep mechanical, propulsion, battery and ESC co-design aligned while final requirements are still being established. No value marked `OPEN`, `TRADE_ONLY`, `CANDIDATE` or `PLANNED` may be presented as a guaranteed product rating.
