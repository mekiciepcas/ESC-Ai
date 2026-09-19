# B1 legacy traceability gap audit

Date: 2026-09-19  
Branch: `uav-rebaseline`  
Status: **LEGACY EVIDENCE AUDIT / U1 PREWORK — NOT ARCHITECTURE FREEZE**

## Purpose

Close the remaining traceability gaps that can be resolved from the existing B1 repository without inventing G0/G1 product values. This audit classifies safety/interlock, communication, temperature, Hall and board-interface functions as reusable principles, revalidation items, replacement candidates or open contracts.

Evidence classes used here:
- **REPOSITORY SOURCE EVIDENCE**: B1 KiCad/manifest evidence.
- **PRIMARY MANUFACTURER EVIDENCE**: current manufacturer product/datasheet evidence.
- **DERIVED REQUIREMENT**: a requirement inferred from a demonstrated B1 gap, with numeric value left OPEN unless evidenced.
- **OPEN**: product-specific value/selection is not defensible yet.

## 1. Fault latch / arming architecture

B1 repository evidence from `hardware_b1/16_FAULT_LATCH.kicad_sch` shows:
- `HARD_FAULT_N` merges comparator, driver fault, PGOOD and emergency-stop fault sources;
- `SN74LVC1G74DCUR` is used as a hardware state latch;
- `D` is tied high, `ARM_CLK` provides deliberate set/arm action, and asynchronous clear is driven by `HARD_FAULT_N`;
- `RUN_REQUEST` and `LATCH_STATE` are intentionally separate, so waking the gate driver is not equivalent to granting switching permission;
- automatic re-arm is explicitly forbidden in B1 notes;
- power-up state is not credited as armed; PWM remains hardware-closed until a deliberate arm path is applied.

Primary TI evidence confirms the exact `SN74LVC1G74DCUR` orderable part is active, uses the DCU/VSSOP-8 package, is rated -40 to +125 °C and supports Ioff/partial-power-down behavior.

**U1 classification:**
- fail-inhibit / deliberate-arm principle: **KEEP + REVALIDATE**;
- exact `SN74LVC1G74DCUR`: **REVALIDATE**, not selected for U1;
- reset/re-arm policy: **OPEN at vehicle/failsafe level**, but no implicit automatic re-arm may be assumed.

## 2. External emergency-stop / inhibit path

B1 connects an external contact that pulls `HARD_FAULT_N` to ground. The B1 design note explicitly states that cable break is not detected and the implementation is not a certified safety loop.

**U1 classification:** **REPLACE/REDESIGN IF AN EXTERNAL SAFETY LOOP IS REQUIRED.**

Derived requirement: if the vehicle requires an external emergency-stop or inhibit loop, normal, open-circuit, short-to-ground, short-to-supply and connector-disconnected behavior shall be explicitly defined and verified. B1's simple active-low contact shall not be credited with cable-break detection.

No safety-integrity level or certification claim is made.

## 3. PWM hardware inhibit

B1 evidence from `hardware_b1/17_PWM_INHIBIT.kicad_sch` shows:
- each of the six PWM signals passes through its own `SN74LVC1G08DBVR` AND gate;
- the second input of every gate is common `LATCH_STATE`;
- `LATCH_STATE=0` forces all six gated PWM outputs low without waiting for motor-control firmware;
- the gate structure deliberately preserves the driver's 6-PWM mode;
- B1 notes explicitly require physical fault-to-gate-off timing measurement.

Primary TI evidence confirms exact `SN74LVC1G08DBVR` is active, SOT-23-5, -40 to +125 °C, supports 1.65 to 5.5 V operation and Ioff/partial-power-down behavior.

**U1 classification:**
- independent hardware PWM-inhibit principle: **KEEP + REVALIDATE**;
- exact six-gate implementation and MPN: **REVALIDATE**;
- fault-to-PWM-inactive latency: **OPEN until measured against the final semiconductor safe-action budget**.

This interlock is a second protection layer; it does not remove the requirement that MCU PWM pins and the selected driver have a safe reset state.

## 4. Hardware trip comparators

B1 uses two `TLV1704PWR` quad comparators in the hardware trip path. TI currently lists the TLV1704 family active, with 2.2–36 V supply range, open-collector outputs, -40 to +125 °C operation and a typical propagation-delay headline around 560 ns.

The B1 schematic itself warns that comparator delay plus current-sense settling is not a guaranteed semiconductor short-circuit limit.

**U1 classification:**
- independent hardware trip principle: **KEEP + REVALIDATE**;
- exact TLV1704 implementation: **REVALIDATE**;
- thresholds, deglitch/filtering and total fault latency: **OPEN** pending G1 current envelope, sensing topology and semiconductor SOA/fault budget.

Manufacturer headline delay shall not be substituted for end-to-end fault-to-PWM-off timing.

## 5. CAN / service communication

B1 `hardware_b1/12_CAN_UART.kicad_sch` contains `SN65HVD230DR`, with `CAN_RS` tied for high-speed mode, optional 120 ohm termination DNP by default, and a TVS placeholder whose production selection is open. UART is explicitly 3.3 V logic, not RS-232.

TI currently lists exact `SN65HVD230DR` active as a 3.3 V Classic-CAN transceiver, up to 1 Mbps, SOIC-8, -40 to +85 °C.

**U1 classification:**
- CAN function: **KEEP functionally**;
- exact transceiver: **REVALIDATE**;
- Classic CAN vs CAN-FD, bit rate, bus length, node count, timeout, termination, ESD/TVS, common-mode/ground strategy and environmental qualification: **OPEN**.

The 85 °C device operating-range ceiling shall be compared with the future frozen ENV requirement; it is not yet a disqualification because U1 maximum ambient is still OPEN.

## 6. Temperature sensing

B1 `hardware_b1/07_TEMPERATURE.kicad_sch` identifies FET and PCB NTCs as exact `NTCG203NH103JT1`. Current TDK evidence lists this part in production with 10 kOhm at 25 °C, ±5% resistance tolerance, B25/85 = 3650 K typical with ±3% B tolerance, and maximum operating temperature 125 °C.

B1 notes already removed an older generic B3435 assumption and require the manufacturer R-T table. Motor temperature input, however, only assumes a resistive sensor; the actual motor thermistor type is not proven.

**U1 classification:**
- FET/PCB NTC sensing function: **KEEP + REVALIDATE**;
- exact `NTCG203NH103JT1`: **REVALIDATE** against final location, thermal range, isolation and accuracy requirements;
- motor temperature sensor type/R-T curve/fault behavior: **OPEN**;
- open/short diagnostic requirement: **KEEP principle**.

## 7. Hall interface

B1 `hardware_b1/13_HALL.kicad_sch` assumes:
- a +5 V Hall supply;
- Hall outputs compatible with 3.3 V pull-ups, effectively an open-collector/open-drain study assumption;
- push-pull 5 V Hall outputs require level conversion or separate proof;
- 1 kOhm / 1 nF filters are starting values only and must be checked against maximum electrical speed;
- invalid Hall states/sequences are fault conditions.

The legacy 5-pin connector is `61300511121`, a current Würth WR-PHD 2.54 mm straight THT pin header. It is a bench/PoC interconnect, not a keyed/locking UAV harness solution.

**U1 classification:**
- optional Hall acquisition function: **REVALIDATE**;
- Hall output electrical type, supply current, edge-rate/filter budget and connector/harness: **OPEN**;
- `61300511121`: **LEGACY_REFERENCE_ONLY**.

## 8. Board-to-board interface

B1 `hardware_b1/18_BOARD_INTERFACE.kicad_sch` preserves a 2x20 control/power interface and explicitly records pin 38 as `TEMP_MOTOR` and pin 39 as `+5V`; old A1/A2 pin-38 mappings shall not be reused blindly. The B1 notes also state that modeling the two sides with the same net names is not proof of physical mating, orientation or harness correctness.

**U1 classification:**
- functional partition between control and power domains: **KEEP conceptually**;
- exact 2x20 connector, pinout, current capacity, keying, orientation, vibration retention and environmental suitability: **REVALIDATE / OPEN**.

## 9. External fan and exported auxiliary power

B1 contains a +12 V fan connector and a legacy fan budget `<=0.2 A`, while explicitly leaving inrush unmeasured. +5 V is also exported through the board interface and Hall connector, but maximum external loading is not a frozen product contract.

**U1 classification:** **OPEN interface contract.**

The U1 design shall not size its converter by assuming the legacy 0.2 A fan budget or by treating regulator current ratings as loads.

## Gap disposition summary

| Function | Reusable principle | Exact B1 implementation | U1 blocker / next proof |
|---|---|---|---|
| Fault latch / deliberate arm | KEEP + REVALIDATE | SN74LVC1G74DCUR REVALIDATE | final arming/failsafe policy + bench state tests |
| External E-stop | safety intent only | B1 contact path insufficient for cable-break detection | vehicle safety-loop requirement and fault-state contract |
| PWM inhibit | KEEP + REVALIDATE | 6x SN74LVC1G08DBVR REVALIDATE | measured end-to-end fault latency |
| Hardware comparators | KEEP + REVALIDATE | 2x TLV1704PWR REVALIDATE | current thresholds, sensing delay, SOA-safe latency |
| CAN | KEEP function | SN65HVD230DR REVALIDATE | CAN/CAN-FD, ENV, TVS, termination, harness |
| FET/PCB temperature | KEEP + REVALIDATE | NTCG203NH103JT1 REVALIDATE | thermal range/location/accuracy |
| Motor temperature | KEEP function | sensor type not known | motor supplier/measurement evidence |
| Hall | optional function REVALIDATE | 5 V / 3.3 V pull-up assumption | exact motor sensor electrical contract |
| Hall/motor-temp headers | none for production | WR-PHD headers legacy-only | keyed/locking environmental connector selection |
| 2x20 board interface | partition concept KEEP | physical system OPEN | exact connector/pin/current/mechanical proof |
| Fan/exported +5 V | function OPEN | legacy budget only | current/inrush/protection interface bounds |

## Immediate derived requirements

This audit shall feed the SAF/IF/SNS/MFG requirement domains without freezing any numeric value:
- power-up/reset state must be PWM-inactive until deliberate arm;
- a latched fault shall not silently auto-rearm unless an explicit system safety policy permits it;
- hardware fault-to-PWM-off latency requires physical measurement and comparison with final semiconductor limits;
- external inhibit/E-stop cable-fault behavior must be explicit if that interface is required;
- CAN physical layer must close protocol, temperature, cable, termination and transient protection;
- motor temperature and Hall electrical interfaces must be explicit supplier/vehicle contracts;
- production connectors require exact mechanical/environmental qualification and cannot inherit PoC headers by default.

## Conclusion

The B1 safety/control interfaces contain several useful architectural principles, but none of the reviewed exact implementations are promoted to U1 production selection by this audit. The work closes traceability, not G1/G2 architecture. Product values and final MPNs remain OPEN where parent requirements are not frozen.