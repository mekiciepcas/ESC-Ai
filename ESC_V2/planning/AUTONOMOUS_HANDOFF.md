# ESC autonomous handoff

Date: 2026-09-19 15:40+03:00  
Branch: `uav-rebaseline`  
Status: `PROGRESS_LEGACY_SAFETY_INTERFACE_AUDIT_AND_BOM_DEEPENING`  
Repository HEAD immediately before this handoff update: `5695b848379a28c82b33cedc3ea6d7a8e2617371`.

## Progress percentages

- Requirements planned-domain/schema structure: **12/12 = 100%**.
- G1 SYSTEM FREEZE value closure: **1/46 PASS = 2.2%**.
- Backlog tasks explicitly DONE: **1/25 = 4%**.
- Major product gates closed: **0/8 = 0%**.

These conservative counters are unchanged because this run advanced safe G2 prework and traceability without fabricating or freezing any open G0/G1 product value.

## Run summary

This run verified the required planning authorities and then audited actual B1 fault latch, PWM inhibit, hardware-trip comparator, CAN, temperature, Hall, board-interface and external auxiliary circuitry. A legacy gap audit now separates reusable safety principles from exact-component revalidation and identifies where B1 PoC interfaces cannot be credited as U1 production/safety implementations. Null-only external-interface and fault/arming state templates were created so later vehicle inputs and measurements have explicit destinations. Safety/interface derived requirements were linked into the 12-domain master, the preliminary U1 BOM was deepened with exact source-backed legacy support parts, and traceability was extended through TR-038. No architecture winner, production connector, CAN protocol, fault latency, thermal limit or physical-test result was claimed.

## Tasks attempted / completed

1. Re-read and verified `AUTONOMOUS_HANDOFF.md`, `autonomy_state.json`, `UAV_PRODUCT_PLAN.md`, `UAV_TRACEABILITY.md`, `uav_backlog.json`, `mission_requirements.json`, `REQUIREMENTS_MASTER.json` and `REQUIREMENTS_PROGRESS.json` against the actual `uav-rebaseline` branch.
2. Audited actual B1 schematics/manifest evidence for `16_FAULT_LATCH`, `17_PWM_INHIBIT`, `14_TRIP_COMPARATORS`, `12_CAN_UART`, `07_TEMPERATURE`, `13_HALL`, `18_BOARD_INTERFACE` and external fan/+5 V interfaces.
3. Added `B1_LEGACY_TRACEABILITY_GAP_AUDIT.md` with KEEP / REVALIDATE / REPLACE / OPEN dispositions.
4. Confirmed the B1 deliberate-arm principle separates driver wake from switching permission; exact latch implementation remains REVALIDATE.
5. Confirmed B1 external E-stop is a simple active-low contact and explicitly does not detect cable break; it cannot be credited as a certified/fail-safe wiring loop.
6. Confirmed six B1 PWM outputs are individually AND-gated by common `LATCH_STATE`; independent PWM-inhibit principle is reusable, but end-to-end fault latency requires physical measurement.
7. Confirmed B1 hardware trip uses two `TLV1704PWR` devices; individual comparator headline delay is not accepted as total semiconductor protection latency.
8. Confirmed B1 CAN uses exact `SN65HVD230DR`, optional 120-ohm termination and an unresolved TVS placeholder; Classic CAN/CAN-FD, environmental and harness requirements remain OPEN.
9. Confirmed FET/PCB NTC exact part `NTCG203NH103JT1`; motor sensor type remains OPEN.
10. Confirmed Hall interface assumes a 5 V supply and 3.3 V-pull-up-compatible outputs; push-pull 5 V behavior is not implicitly supported.
11. Added `EXTERNAL_AUX_INTERFACE_CONTRACT.template.json` with fan, Hall, exported +5 V, motor-temperature, E-stop/inhibit, CAN and control/power-interconnect fields intentionally null where product values are unknown.
12. Added `SAFETY_INTERFACE_DERIVED_REQUIREMENTS.json` with SAF/IF/SNS/MFG/PWR requirements for reset-safe PWM, re-arm policy, physical fault-latency proof, external-inhibit fault states, CAN physical layer, temperature/Hall contracts, production connectors and exported auxiliary power.
13. Added `FAULT_ARM_STATE_MATRIX.template.json` covering POWER_OFF, reset, boot-unarmed, driver-awake-unarmed, armed, asynchronous fault, post-fault, watchdog/reset, brownout/partial-power and external-inhibit states without invented timing values.
14. Updated `U1_BOM_CANDIDATES.json` to revision 02 and added exact legacy support-part evidence for `SN74LVC1G74DCUR`, `SN74LVC1G08DBVR`, `TLV1704PWR`, `NTCG203NH103JT1`, `SN65HVD230DR`, `61300511121` and `61300211121` as REVALIDATE or LEGACY_REFERENCE only.
15. Updated `REQUIREMENTS_MASTER.json` to revision 05 and linked the new safety/interface/fault-state authorities.
16. Updated `UAV_TRACEABILITY.md` with revised CAN/hardware-trip/temperature dispositions and TR-036 through TR-038.
17. Updated `autonomy_state.json` to AUTO-STATE-22.

## Files changed / added

- `planning/B1_LEGACY_TRACEABILITY_GAP_AUDIT.md` — new legacy safety/interface audit.
- `planning/EXTERNAL_AUX_INTERFACE_CONTRACT.template.json` — new null-only external interface authority template.
- `planning/SAFETY_INTERFACE_DERIVED_REQUIREMENTS.json` — new derived requirement child authority.
- `planning/FAULT_ARM_STATE_MATRIX.template.json` — new structural safety-state verification matrix.
- `planning/U1_BOM_CANDIDATES.json` — revision 02 with exact legacy support parts and evidence classifications.
- `planning/REQUIREMENTS_MASTER.json` — revision 05 linking new child/verification authorities.
- `planning/UAV_TRACEABILITY.md` — updated through TR-038.
- `planning/autonomy_state.json` — AUTO-STATE-22.
- `planning/AUTONOMOUS_HANDOFF.md` — this continuity record.

## Engineering decisions / findings

- B1's **deliberate arm + independent PWM inhibit** concept is retained as a safety principle, but exact B1 logic is not automatically frozen for U1.
- An external emergency-stop/inhibit interface, if required, must define open-wire and other wiring-fault behavior. B1's ground-pulling contact cannot be credited with cable-break detection.
- Fault-to-PWM-inactive timing is an **end-to-end physical measurement requirement**. Comparator, latch, logic and driver datasheet delays may support analysis but cannot substitute for measured path latency.
- B1 CAN function is reusable, but the exact Classic-CAN physical layer remains REVALIDATE because CAN/CAN-FD, maximum environment, TVS, termination and harness are open.
- FET/PCB NTC sensing has an exact source-backed legacy MPN; the motor-temperature sensor electrical model remains unknown.
- B1 Hall and motor-temperature WR-PHD headers are PoC references only; they are not promoted to production UAV connectors.
- Logical same-net modeling of the B1 2x20 board interface is not proof of connector mating, keying, orientation, vibration retention or environmental suitability.

## Calculations / evidence added

No new physical measurement was introduced.

Current primary manufacturer anchors used in the audit:
- TI `SN74LVC1G74DCUR`: active, DCU/VSSOP-8, -40 to +125 °C, Ioff/partial-power-down support.
- TI `SN74LVC1G08DBVR`: active, DBV/SOT-23-5, 1.65–5.5 V, -40 to +125 °C, Ioff support.
- TI TLV1704 family: active, 2.2–36 V, open-collector outputs, -40 to +125 °C, typical propagation-delay headline ~0.56 us; not credited as total fault-path latency.
- TI `SN65HVD230DR`: active 3.3 V Classic-CAN transceiver, up to 1 Mbps, SOIC-8, -40 to +85 °C; final ENV/protocol compatibility remains open.
- TDK `NTCG203NH103JT1`: production, 10 kOhm at 25 °C, ±5%, B25/85 3650 K typ ±3%, max operating temperature 125 °C.
- Würth `61300511121` and `61300211121`: active WR-PHD straight THT PoC headers; repository use does not establish production harness suitability.

## Assumptions / evidence level

- 70–100 kg remains USER TARGET payload, not MTOW.
- B1 circuit topology and notes: LEGACY REPOSITORY SOURCE EVIDENCE.
- Exact support-part capability anchors: PRIMARY MANUFACTURER EVIDENCE.
- KEEP/REVALIDATE/REPLACE dispositions: ENGINEERING TRACEABILITY DECISION, not production qualification.
- External interface and fault-arm matrices: DEFINED REQUIREMENT/VERIFICATION STRUCTURE with product numeric fields intentionally OPEN.
- No physical bench, fault-latency, thermal, EMC, dyno or flight measurement was performed.

## Unresolved blockers

- G0 nominal payload, airframe/battery/equipment mass, MTOW, mission duration/profile, environment and degraded/single-motor-failure policy.
- Final rotor architecture/thrust margin and product motor/prop operating point.
- Motor pole pairs, phase RMS/peak current, eRPM and final PWM envelope.
- Battery series/min/nom/full-charge/transient envelope, pack current/energy/sag/disconnect behavior and final transient ceiling.
- Final semiconductor, driver, sensing, DC-link, thermal and auxiliary-power architecture.
- Vehicle CAN/CAN-FD protocol, traffic/timeout contract, bus/harness length, termination and transient/EMC requirements.
- Fan current/inrush, Hall electrical type/load, motor thermistor type, E-stop/inhibit safety policy and production connector requirements.
- Physical end-to-end fault latency and all CPB benchmark results.
- Production BOM and all G3+ release evidence.

## Regressions / risks discovered

- No repository regression identified in the reviewed artifacts.
- B1 E-stop wiring can create a false sense of fail-safe behavior if its explicit no-cable-break limitation is forgotten.
- Individual comparator or logic-gate propagation delay must not be mistaken for complete short-circuit protection latency.
- `SN65HVD230DR` has a narrower -40 to +85 °C operating-temperature range than several other legacy logic/sensing parts; compatibility cannot be decided until ENV is frozen.
- PoC headers may be electrically adequate for a bench while remaining unsuitable for vibration, retention, keying or ingress in a UAV.
- Exact support-part evidence in `U1_BOM_CANDIDATES.json` is still only REVALIDATE/LEGACY_REFERENCE and must not be interpreted as a production BOM selection.

## Exact next recommended tasks

1. Build a primary-source CAN physical-layer pretrade covering current Classic-CAN and CAN-FD transceiver options, temperature range, fault protection and topology implications without selecting a winner before the vehicle interface freezes.
2. Create a production-connector requirements framework for keying, locking, current, voltage, temperature, vibration, ingress, mating-cycle and serviceability evidence with numeric values left OPEN where vehicle requirements are missing.
3. Build an initial fault-tree/FMEA skeleton from B1 fault sources plus current SAF requirements, leaving occurrence probabilities and severity classifications OPEN until system policy/evidence exists.
4. Continue support-part BOM evidence only where exact selection is independent of unresolved G1 power ratings.
5. Keep all vehicle-dependent G0/G1 fields OPEN until supplied or explicitly approved.

## Dependency chain

`G0 vehicle inputs -> G1A rotor selection -> G1B operating point -> G1C battery/transient -> G1 SYSTEM FREEZE -> G2 architecture freeze -> G3 U1 schematic/BOM -> G4 firmware -> G5 prototype -> G6 propulsion verification -> G7 flight readiness`

## Next-run briefing

Do not redo the safety/interface legacy audit. Start with current CAN physical-layer alternatives, then define connector qualification criteria and the first fault-tree/FMEA structure. Preserve the external-interface null fields until actual vehicle/motor/harness decisions exist. The progress counters remain 100% requirements structure / 2.2% G1 value closure / 4% backlog DONE unless the controlling matrices genuinely change.
