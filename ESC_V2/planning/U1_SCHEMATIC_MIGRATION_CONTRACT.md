# U1 schematic migration contract

Date: 2026-09-19  
Branch: `uav-rebaseline`  
Status: `PRE_G3_STRUCTURE_ONLY_NO_HARDWARE_U1_CREATED`

## Purpose

Define how the future U1 KiCad schematic shall be created from B1 evidence without prematurely freezing blocked component values or copying known B1 risks into the UAV design.

This file is preparation for `UAV-015`. It does **not** authorize creation of production-intent `hardware_u1/` sheets before the G2 architecture freeze criteria are met.

## Gate rule

Actual U1 schematic migration starts only after the relevant G2 architecture inputs are frozen sufficiently for each page. A page may not be copied from B1 merely because the topology looks familiar.

For every migrated block, one disposition is mandatory:

- `KEEP_PRINCIPLE`: functional/safety principle remains, exact implementation still reviewed.
- `RECALCULATE`: topology may remain, component values/rating must be regenerated from U1 requirements.
- `REPLACE`: known architecture issue or new requirement forces redesign.
- `DELETE`: function is no longer required.
- `OPEN`: parent requirement or architecture decision is still missing.

## Proposed U1 KiCad page map

| U1 page | Function | B1 source reference | Current disposition |
|---|---|---|---|
| `00_TOP` | hierarchy / design authority notes | `ESC_3kW_B1.kicad_sch` | RECALCULATE |
| `01_DC_INPUT` | fuse/reverse/precharge/contact/regen interface | B1 external/partial contract | OPEN / REPLACE |
| `02_DC_LINK` | bulk/local link capacitance and bus interface | `01_DC_LINK.kicad_sch` | RECALCULATE |
| `03_PHASE_A` | half bridge A | `02_PHASE_A.kicad_sch` | RECALCULATE |
| `03_PHASE_B` | half bridge B | `02_PHASE_B.kicad_sch` | RECALCULATE |
| `03_PHASE_C` | half bridge C | `02_PHASE_C.kicad_sch` | RECALCULATE |
| `04_GATE_DRIVER` | gate-driver / bootstrap or isolated drive | `03_DRIVER.kicad_sch`, `04_DRIVER_DEFAULTS.kicad_sch` | OPEN / REPLACE_IF_REQUIRED |
| `05_CURRENT_SENSE` | phase shunts/CSA/ADC path | `06_CURRENT.kicad_sch` | RECALCULATE |
| `06_VOLTAGE_SENSE` | VBUS and phase voltage sensing | `05_SENSE_*.kicad_sch` | REPLACE / RECALCULATE |
| `07_TEMPERATURE` | FET/PCB/motor thermal sensing | `07_TEMPERATURE.kicad_sch` | RECALCULATE |
| `08_AUX_POWER` | HV housekeeping + 12/5/3V3/analog rails | `08_AUX_12V*`, `09_AUX_LOGIC*` | OPEN / RECALCULATE |
| `09_MCU` | MCU core/support/programming | `10_MCU`, `11_MCU_SUPPORT*` | OPEN |
| `10_CAN_INTERFACE` | CAN transceiver/protection/termination | `12_CAN_UART.kicad_sch` | OPEN / REPLACE_IF_REQUIRED |
| `11_HALL_SENSOR` | optional rotor-position input | `13_HALL.kicad_sch` | OPEN |
| `12_HARDWARE_TRIP` | comparator/threshold/asynchronous trip | `14_TRIP_COMPARATORS`, `15_TRIP_REFERENCES` | KEEP_PRINCIPLE + RECALCULATE |
| `13_FAULT_LATCH` | deliberate arm / fault memory | `16_FAULT_LATCH.kicad_sch` | KEEP_PRINCIPLE + REVALIDATE |
| `14_PWM_INHIBIT` | hardware switching permission | `17_PWM_INHIBIT*` | KEEP_PRINCIPLE + REVALIDATE |
| `15_BOARD_INTERFACE` | control/power partition | `18_BOARD_INTERFACE.kicad_sch` | OPEN / REPLACE_IF_REQUIRED |
| `16_TEST_ACCESS` | bring-up/measurement points | `19_TEST_POINTS.kicad_sch` | RECALCULATE |

## Mandatory design-note fields on each U1 page

Every critical page shall record:

1. Parent requirement IDs.
2. Gate/revision that authorized the page decision.
3. Input electrical envelope used by calculations.
4. Exact calculation/evidence file.
5. Selected device MPN only after selection is evidence-backed.
6. Maximum ratings and explicit derating check.
7. Known power-off / partial-power behavior.
8. Expected verification method.
9. Remaining TBDs, which must be zero for G3 critical release.

## Known B1 issues that shall not be copied silently

- Rail-referenced BAT54H HV-sense clamps that can back-power +3V3A/+3V3.
- 100 V-domain assumptions before the U1 transient ceiling is frozen.
- B1 Classic-CAN transceiver / DNP termination / unresolved TVS placeholder as if they were final vehicle interface choices.
- PoC WR-PHD external connectors as production UAV harness connectors.
- Simple active-low E-stop contact as if it provided cable-break/fail-safe supervision.
- Regulator output-current ratings as if they were actual auxiliary load requirements.
- Individual comparator/gate propagation-delay figures as proof of complete fault-to-PWM-off latency.

## Page-entry readiness criteria

### Pages that are blocked by G1/G2

`01_DC_INPUT`, `02_DC_LINK`, `03_PHASE_*`, `04_GATE_DRIVER`, `05_CURRENT_SENSE`, `06_VOLTAGE_SENSE`, `08_AUX_POWER`, `09_MCU`, `10_CAN_INTERFACE`, `11_HALL_SENSOR`, `15_BOARD_INTERFACE` cannot be considered production-intent until their parent requirements/architecture decisions close.

### Pages whose safety principle is already defined but implementation remains open

`12_HARDWARE_TRIP`, `13_FAULT_LATCH`, `14_PWM_INHIBIT` have reusable safety principles from B1, but threshold values, exact parts, safe-state truth table and measured latency remain open.

### Documentation-only work allowed before G2

The following is allowed before G2 because it does not freeze hardware:

- page map and hierarchy planning,
- requirement-to-page traceability,
- KEEP/RECALCULATE/REPLACE/OPEN classification,
- symbol/footprint evidence preparation,
- verification test-point planning,
- candidate MPN notes clearly marked as unselected.

## KiCad start condition

The first actual `hardware_u1/` commit shall state which pages are architecture-ready and which remain blocked. If any page is created before all other pages are ready, blocked pages shall remain explicit stubs with no guessed component ratings or MPNs.

## Current conclusion

KiCad **migration planning is now defined**, but the repository intentionally does not yet contain `hardware_u1/`. This avoids presenting a partially guessed schematic as the UAV design baseline while still making the eventual migration deterministic and traceable.
