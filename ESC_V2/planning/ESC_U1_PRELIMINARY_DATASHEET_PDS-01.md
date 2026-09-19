# ESC-U1 Heavy-Lift UAV ESC - Preliminary Engineering Datasheet

**Document revision:** PDS-01  
**Date:** 2026-09-19  
**Branch:** `uav-rebaseline`  
**Status:** PRELIMINARY / CONCEPT-STAGE / NOT FOR PRODUCTION  
**Change from PDS-00:** product values are now explicitly classified as `FROZEN`, `TRADE_ONLY`, `CANDIDATE`, `PLANNED`, or `OPEN`.

> `FROZEN` means the value is currently accepted as a product requirement/target and is traceable to the G1 requirements authority. `TRADE_ONLY` values are benchmark-derived design-stress references and are not guaranteed ratings. `CANDIDATE` means an option is under engineering evaluation. `OPEN` means no value is frozen.

## Frozen-value summary

| Frozen item | Frozen value | Authority |
|---|---:|---|
| Payload target bounds | **70-100 kg payload** | `G1_REQUIREMENTS_MATRIX.json` row `G0-01` = PASS |

**Frozen product-value count:** 1 / 46 G1 required rows = **2.2%**.  
No other voltage, current, power, PWM, eRPM, MOSFET class, rotor count, battery series count, thermal limit, connector, dimension, mass, or environmental rating is frozen yet.

## 1. Product intent

| Item | Current value | Status |
|---|---:|---|
| Product | ESC-U1 heavy-lift multirotor electronic speed controller | DESIGN_INTENT |
| Intended vehicle class | Heavy-lift agricultural multirotor UAV | DESIGN_INTENT |
| User payload target | **70-100 kg payload class** | **FROZEN_USER_TARGET_BOUNDS** |
| Motor type | 3-phase BLDC/PMSM | DESIGN_INTENT |
| Control objective | FOC / SVPWM capable control architecture | PLANNED |
| Flight-controller link | CAN-family vehicle interface | PLANNED |
| Production release | Not allowed | GOVERNANCE_LOCKED |

The 70-100 kg figure is payload, not aircraft MTOW. Final MTOW, rotor count, propulsion operating point, battery architecture and ESC electrical requirements remain open while the mechanical concept is co-developed.

## 2. Electrical envelope

| Parameter | Preliminary value | Status / meaning |
|---|---:|---|
| DC input operating voltage | OPEN | OPEN |
| Architecture stress-screen voltage | up to 81 V DC | TRADE_ONLY |
| Candidate semiconductor VDS class | 120 V / 150 V | CANDIDATE / ACTIVE_TRADE |
| 100 V semiconductor class | Legacy comparison only | LEGACY_REFERENCE |
| Continuous DC bus current requirement | OPEN | OPEN |
| Stress-screen continuous bus current | 120 A | TRADE_ONLY |
| Peak DC bus current requirement | OPEN | OPEN |
| Stress-screen peak bus current | 300 A for 3 s | TRADE_ONLY |
| Continuous output power requirement | OPEN | OPEN |
| Stress-screen propulsion power | 4.64 kW class | TRADE_ONLY |
| Phase RMS current | OPEN | OPEN |
| Phase peak current | OPEN | OPEN |
| PWM frequency | OPEN | OPEN |
| Maximum electrical RPM | OPEN | OPEN |
| Regenerative/transient bus ceiling | OPEN | OPEN |

### Voltage-class screening note

Using the current 81 V architecture stress reference only:

- 100 V device class leaves 19 V static headroom.
- 120 V device class leaves 39 V static headroom.
- 150 V device class leaves 69 V static headroom.

All three statements are `TRADE_ONLY` screening calculations. No semiconductor voltage class is frozen.

## 3. Power-stage architecture

| Function | Current direction | Status |
|---|---|---|
| Inverter | 3-phase, six-switch bridge | PLANNED |
| Power switch | 120 V / 150 V MOSFET candidate classes | CANDIDATE |
| Parallel switches per position | OPEN | OPEN |
| Gate drive | High-current 3-phase or per-half-bridge architecture | ACTIVE_TRADE |
| Gate-driver candidates | DRV8353 legacy; UCC27282 / UCC27712 / UCC21540-Q1 | CANDIDATE |
| DC link | Bulk + local high-frequency decoupling | PLANNED |
| Precharge / inrush control | Required | PLANNED |
| Regeneration / overvoltage handling | Required architecture decision | OPEN |
| Input fuse / fault isolation | Required | PLANNED |

No production MOSFET, gate driver, capacitor, fuse or connector is frozen.

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

## 5. Communications and I/O

| Interface | Current direction | Status |
|---|---|---|
| Vehicle network | CAN / CAN-FD trade | OPEN |
| Legacy CAN reference | SN65HVD230DR | REVALIDATE |
| Modern CAN candidates | TCAN1044A-Q1, TCAN1042HGV-Q1, TJA1044GT/3 | CANDIDATE |
| Isolated CAN option | ISO1042-Q1 | CANDIDATE_IF_REQUIRED |
| Debug/programming | SWD/JTAG-class development interface | PLANNED |
| Telemetry | Bus voltage/current, temperatures, faults and state | PLANNED |
| External inhibit / E-stop | Interface required; fail-safe implementation OPEN | OPEN |

## 6. Mechanical and environmental

All product-specific mechanical/environmental ratings remain **OPEN**: ESC dimensions, ESC mass, cooling method, ambient temperature range, altitude derating, ingress protection, vibration/shock qualification, battery/phase/control connectors.

## 7. Verification status

| Verification item | Status | Product-value meaning |
|---|---|---|
| Requirements structure | PASS | Structure only; not a product rating |
| G1 SYSTEM FREEZE | 1/46 PASS | **Only payload target bounds frozen** |
| U1 architecture-only KiCad scaffold | PASS | Tooling/structure evidence only |
| U1 scaffold parser/netlist/ERC | PASS | Zero-component scaffold only |
| Legacy B1 KiCad reproducible baseline | PASS | Legacy software baseline only |
| ESC electrical pretrade consistency CI | PASS | Trade arithmetic/source consistency only |
| Component-bearing U1 schematic | NOT_STARTED | No product schematic freeze |
| Bench / thermal / EMI / dyno / flight | NOT_RUN | No physical qualification |

## 8. Design maturity

- Requirements structure: **100%**
- G1 SYSTEM FREEZE value closure: **2.2% (1/46)**
- Backlog DONE: **4% (1/25)**
- Major gates closed: **0/8**
- U1 KiCad architecture scaffold: **100%**
- Component-bearing U1 production-intent schematic: **0%**

## Release statement

**PDS-01 is not a production datasheet.** Only values explicitly labeled `FROZEN` may be treated as current product-level targets. At this revision the only frozen numerical product target is the **70-100 kg payload bound**. All other numerical electrical values remain `TRADE_ONLY`, `CANDIDATE`, or `OPEN` until their parent G0/G1/G2 requirements close.
