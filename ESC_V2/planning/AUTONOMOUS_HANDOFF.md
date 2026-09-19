# ESC autonomous handoff

Date: 2026-09-19 15:55+03:00  
Branch: `uav-rebaseline`  
Status: `PROGRESS_CAN_CONNECTOR_FMEA_AND_U1_MIGRATION_PREWORK`  
Repository HEAD immediately before this handoff update: `53f41f02101b56969872164af0585cf40eadf24c`.

## Progress percentages

- Requirements planned-domain/schema structure: **12/12 = 100%**.
- G1 SYSTEM FREEZE value closure: **1/46 PASS = 2.2%**.
- Backlog tasks explicitly DONE: **1/25 = 4%**.
- Major product gates closed: **0/8 = 0%**.

These conservative counters are intentionally unchanged. This run advanced safe pre-G2/G3 architecture, verification and migration structure, but did not fabricate any vehicle/product values or promote blocked work to DONE.

## Run summary

This run first re-read and verified the current handoff/state, product plan, traceability, backlog, mission requirements, requirements master and progress files against the actual `uav-rebaseline` branch. The branch was verified at **128 commits ahead of `main`, 0 behind** before this run's writes. Work then followed the prior handoff: a primary-source CAN physical-layer pretrade was created, production connector qualification requirements were structured, the first machine-readable fault/FMEA skeleton was built, and a U1 KiCad migration contract/page map was defined without creating a guessed `hardware_u1/` design. The preliminary U1 BOM, requirements authority, traceability and backlog were updated to reference these artifacts while all unresolved G0/G1/G2 values remain OPEN.

## Tasks attempted / completed

1. Verified `AUTONOMOUS_HANDOFF.md`, `autonomy_state.json`, `UAV_PRODUCT_PLAN.md`, `UAV_TRACEABILITY.md`, `uav_backlog.json`, `mission_requirements.json`, `REQUIREMENTS_MASTER.json` and `REQUIREMENTS_PROGRESS.json` against `uav-rebaseline`.
2. Verified branch state before writes: `uav-rebaseline` was 128 commits ahead of `main` and 0 behind.
3. Added `CAN_PHYSICAL_LAYER_PRETRADE.md`.
4. Recorded current primary-source trade anchors without selecting a winner:
   - B1 legacy `SN65HVD230DR` remains Classic-CAN `REVALIDATE` only.
   - TI `TCAN1044A-Q1` family: current non-isolated CAN/CAN-FD candidate with +/-58 V bus-fault protection and unpowered high-impedance behavior.
   - TI `TCAN1042HGV-Q1` family: current non-isolated CAN-FD candidate with +/-70 V bus-fault protection and VIO option.
   - NXP `TJA1044GT/3`: current non-isolated CAN-FD candidate; its bus-pin limiting-voltage rating is not treated as directly equivalent to TI bus-fault ratings.
   - TI `ISO1042-Q1`: isolated CAN-FD architecture anchor only if grounding/common-mode/fault-containment needs justify isolation.
5. Added `PRODUCTION_CONNECTOR_REQUIREMENTS_FRAMEWORK.md` defining connector identity, mate/contact, keying, locking, electrical derating, vibration, shock, ingress, mating-cycle, serviceability and release evidence fields while leaving all product numeric values OPEN.
6. Added `FAULT_FMEA_SKELETON.json` with 12 initial failure modes covering phase overcurrent, bus over/undervoltage, gate-driver faults, MCU/watchdog/reset, CAN loss, current/voltage sensing faults, thermal faults, external inhibit, auxiliary-power faults and connector/harness faults.
7. Left severity, occurrence, detection, RPN, safe-state, thresholds, timeouts and response latencies null/OPEN in the FMEA skeleton.
8. Added `U1_SCHEMATIC_MIGRATION_CONTRACT.md` defining the future U1 KiCad page map and KEEP_PRINCIPLE / RECALCULATE / REPLACE / DELETE / OPEN migration rules.
9. Explicitly blocked silent copying of known B1 risks into U1, including rail-clamp backpower, 100 V-domain assumptions, legacy CAN/TVS assumptions, PoC headers, simple E-stop wiring, regulator-rating-as-load misuse and device-delay-as-total-fault-latency misuse.
10. Updated `U1_BOM_CANDIDATES.json` to revision 03 with the new CAN trade candidates; none is production-selected.
11. Updated `REQUIREMENTS_MASTER.json` to revision 06 linking CAN, connector, FMEA and U1 schematic-migration authorities.
12. Updated `UAV_TRACEABILITY.md` through TR-042.
13. Updated `uav_backlog.json` to `UAV-PLAN-04`; UAV-014/UAV-015/UAV-016 now reference the new prework while remaining correctly BLOCKED.
14. Updated `autonomy_state.json` to `AUTO-STATE-23`.
15. Preserved A2/B1 history, did not touch `main`, did not create Gerbers or release packages, and did not create `hardware_u1/` production-intent KiCad pages.

## Files changed / added

- `planning/CAN_PHYSICAL_LAYER_PRETRADE.md` — new source-backed CAN physical-layer trade.
- `planning/PRODUCTION_CONNECTOR_REQUIREMENTS_FRAMEWORK.md` — new connector qualification/release framework.
- `planning/FAULT_FMEA_SKELETON.json` — new machine-readable safety/failure-mode prework.
- `planning/U1_SCHEMATIC_MIGRATION_CONTRACT.md` — new KiCad migration/page-readiness policy.
- `planning/U1_BOM_CANDIDATES.json` — revision 03; CAN candidates added as trade-only.
- `planning/REQUIREMENTS_MASTER.json` — revision 06; new authorities linked.
- `planning/UAV_TRACEABILITY.md` — extended through TR-042.
- `planning/uav_backlog.json` — revision `UAV-PLAN-04`; blocked-task prework recorded without false closure.
- `planning/autonomy_state.json` — `AUTO-STATE-23`.
- `planning/AUTONOMOUS_HANDOFF.md` — this continuity record.

## Engineering decisions / findings

- **No CAN transceiver winner is selected.** Protocol, bit rate, harness, node count, termination, TVS/CMC, environment and isolation need must freeze first.
- `TCAN1044A-Q1`, `TCAN1042HGV-Q1`, `TJA1044GT/3` and `ISO1042-Q1` are evidence-backed trade anchors only.
- Bus-fault-protection ratings and generic bus-pin limiting-voltage ratings are not normalized as if they were identical specifications.
- Galvanic CAN isolation is not added by default; it must be justified by system grounding/common-mode/fault-containment requirements.
- Production connector selection is blocked until exact electrical, environmental, harness and mating requirements exist.
- The FMEA structure may be created before G2, but numerical FMEA scoring, safe-state classification and response-time limits may not be invented.
- KiCad migration planning is allowed before G2; actual U1 production-intent schematic creation remains blocked by page-level architecture readiness. `hardware_u1/` still intentionally does not exist.

## Calculations / evidence added

No physical measurement was introduced.

Current primary manufacturer evidence used for CAN trade:
- TI `TCAN1044A-Q1`: ACTIVE, Classical CAN/CAN FD, VCC 4.5–5.5 V, VIO option, CAN-FD performance up to 8 Mbps headline depending on network conditions, +/-58 V bus-fault protection, unpowered bus/logic high impedance, AEC-Q100 Grade 1.
- TI `TCAN1042HGV-Q1`: ACTIVE, CAN/CAN-FD up to 5 Mbps G option, +/-70 V bus-fault protection, +/-30 V receiver common-mode headline, unpowered high impedance, VIO option.
- NXP `TJA1044GT/3`: CAN-FD timing up to 5 Mbps, VCC 4.5–5.5 V, VIO 2.91–5.5 V, unpowered zero-load behavior, bus-pin limiting voltage -42 to +42 V, AEC-Q100.
- TI `ISO1042-Q1`: isolated CAN-FD up to 5 Mbps, +/-70 V bus-fault protection, +/-30 V common mode, -40 to +125 degC operating range, 5000 Vrms one-minute isolation withstand headline and high-impedance unpowered bus terminals.

Primary-source URLs are recorded in `CAN_PHYSICAL_LAYER_PRETRADE.md`.

## Assumptions / evidence level

- 70–100 kg remains USER TARGET payload, not MTOW.
- Vehicle CAN/CAN-FD protocol, bit rate, bus length, node count, termination, EMC/transient environment and isolation need: **OPEN**.
- CAN candidate capability data: **PRIMARY MANUFACTURER EVIDENCE**.
- Candidate ranking/architecture implications: **ENGINEERING TRADE JUDGMENT**, not selection/qualification.
- Connector framework and U1 schematic page map: **DEFINED STRUCTURE**, product values still OPEN.
- FMEA failure-mode list: **ENGINEERING SAFETY PREWORK** based on current requirements/repository evidence; no safety classification or numerical risk score claimed.
- No physical bench, fault-latency, thermal, EMC, dyno or flight measurement was performed.

## Unresolved blockers

- G0 nominal payload, airframe/battery/equipment mass, MTOW, mission duration/profile, environment and degraded/single-motor-failure policy.
- Final rotor architecture/thrust margin and selected product motor/prop operating point.
- Motor pole pairs, phase RMS/peak current, eRPM and final PWM envelope.
- Battery series/min/nom/full-charge/transient envelope, pack current/energy/sag/disconnect behavior and final transient ceiling.
- Final semiconductor, gate driver, MCU, current sensing, voltage sensing, DC-link, thermal and auxiliary-power architecture.
- Vehicle Classic CAN vs CAN FD protocol, exact bit rates, harness length/topology, node count, termination, TVS/CMC, grounding and isolation need.
- Exact production connectors, mates, contacts, wire gauges, keying/locking, environmental and vibration requirements.
- FMEA safe-state policy, severity/occurrence/detection methodology, thresholds/timeouts and physical response evidence.
- Physical end-to-end fault latency and all CPB benchmark results.
- Production-intent U1 schematic/BOM/PCB and all G3+ release evidence.

## Regressions / risks discovered

- No repository regression was intentionally introduced; all writes were confined to `uav-rebaseline`.
- Selecting a CAN transceiver solely by the largest voltage headline would be unsafe because rating definitions differ across vendors and device families.
- An isolated CAN transceiver without a deliberately designed isolated bus-side supply and barrier/layout policy would create a false sense of isolation completeness.
- Connector datasheet current ratings alone are not enough for UAV power interfaces; thermal rise, wire gauge, vibration, mating retention and environment still matter.
- A structurally complete FMEA can still be dangerously misleading if numerical scores or safe states are filled before vehicle/system policy exists; those fields remain null.
- Creating `hardware_u1/` now with guessed MOSFET, shunt, DC-link, CAN or connector parts would violate the gate logic and risk presenting a speculative schematic as baseline hardware.

## Exact next recommended tasks

1. Audit remaining B1 support parts whose exact evidence is independent of unresolved G1 power ratings; promote only to `REVALIDATE/CANDIDATE`, never production-selected.
2. Create a CAN bus timing / physical verification contract with all vehicle-specific timing, cable and topology inputs null until frozen.
3. Create a U1 page-readiness matrix mapping each future KiCad sheet to its exact parent requirements, current blockers and earliest legal migration gate.
4. Prepare a compact G0 input-closure packet exposing only the missing user/vehicle values needed to unblock MTOW -> rotor -> propulsion -> battery -> ESC envelope.
5. Continue preliminary BOM evidence only for requirement-independent support parts.
6. Do not instantiate production-intent `hardware_u1/` pages until the relevant architecture inputs are frozen.

## Dependency chain

`G0 vehicle inputs -> G1A rotor selection -> G1B product operating point -> G1C battery/transient -> G1 SYSTEM FREEZE -> G2 architecture freeze -> G3 U1 schematic/BOM -> G4 firmware -> G5 prototype -> G6 propulsion verification -> G7 flight readiness`

## Next-run briefing

Do not redo the CAN candidate search, connector framework or FMEA skeleton. Start with remaining B1 support-part evidence and a CAN verification/timing contract, then build the U1 page-readiness matrix. Keep all vehicle CAN/harness/ENV fields OPEN. Do not create real U1 KiCad component selections merely to show visual progress; the migration contract exists specifically to prevent guessed schematic content. Progress counters remain **100% requirements structure / 2.2% G1 value closure / 4% backlog DONE / 0% major gates** unless the controlling matrices genuinely change.
