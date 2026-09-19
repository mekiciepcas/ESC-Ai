# ESC U1 Requirements Specification

Date: 2026-09-19  
Branch: `uav-rebaseline`  
Authority: `REQUIREMENTS_MASTER.json`

## Purpose

This document is the human-readable companion to the machine-readable master requirements. It completes the **planned requirements structure** without inventing unresolved product values. Numeric/selection fields remain OPEN/BOUNDED/FROZEN independently from structural completeness.

## Completion semantics

- **Structure complete** means every planned requirement domain has an authority, gate ownership, child-record schema and verification path.
- **Value frozen** means the product-specific numeric value or architecture selection is evidence-backed and baselined.
- **Bounded** means only an approved range or trade boundary is known.
- **Open** means the value/selection is intentionally not guessed.

## Current progress

- Planned requirement domains covered: **12/12 = 100%**.
- G1 SYSTEM FREEZE rows currently PASS: **1/46 = 2.2%**.
- Product gate closure: **0/8 major gates closed = 0%**; G0/G1 are open and later gates are dependency-blocked.
- Conservative backlog completion: **1/25 tasks DONE = 4%**; IN_PROGRESS and safe G2 prework are intentionally not counted as DONE.

These percentages measure different things. A 100% requirements structure does **not** mean requirements values or product design are complete.

## Requirement-domain hierarchy

- **SYS — System scope and governance:** application scope, evidence authority, release-claim rules and traceability.
- **VEH — Vehicle / mission:** payload, masses, MTOW, mission duration, rotor architecture, thrust margin and degraded-operation policy.
- **PROP — Propulsion:** motor/propeller candidates, hover/peak operating points, RPM/eRPM, KV, pole pairs and thermal/electrical evidence.
- **PWR — Battery / power input:** series count, VBUS min/nom/full/transient, energy, current, sag, BMS/disconnect, fuse, precharge and regen acceptance.
- **INV — Inverter / power stage:** topology, semiconductor class/count, phase/DC power/current, PWM, dead-time, gate drive, SOA and DC-link.
- **SNS — Sensing:** phase current, bus/phase voltage, temperature, calibration, bandwidth, accuracy and powered/unpowered sequencing.
- **CTRL — Control / firmware:** MCU, FOC/SVPWM, PWM/ADC synchronization, trip latency, execution margin, watchdog, state machine and build reproducibility.
- **SAF — Safety / protection:** OCP/OVP/UVP/OTP, communication timeout, gate-driver fault, sensor invalid, stall, restart policy and FMEA/single-fault behavior.
- **IF — Interfaces:** flight controller, CAN, arming, telemetry, service/debug and high-current terminal interfaces.
- **ENV — Environment:** temperature, altitude, wind, ingress, vibration/shock and cooling/baseplate boundaries.
- **MFG — Manufacturing / service:** exact MPNs, footprints, derating, alternates, DFM, serviceability and configuration control.
- **VER — Verification / release:** low-energy bring-up, switching validation, dyno/prop stand, thermal soak, fault injection and flight-readiness review.

## Mandatory child-requirement fields

Every child requirement must carry:

`ID | Parent/domain | Requirement statement | Status | Value/range | Source/evidence | Rationale | Verification method | Acceptance criteria | Dependencies | Revision`

The child authorities remain distributed by function so existing validated evidence is not duplicated or silently rewritten:

- `mission_requirements.json` — G0 mission/vehicle inputs.
- `G1_REQUIREMENTS_MATRIX.json` — G0/G1A/G1B/G1C/G1 electrical freeze rows.
- `UAV_TRACEABILITY.md` — legacy keep/recalculate/replace authority.
- `U1_BOM_CANDIDATES.json` — candidate/BOM dependency status.
- `REQUIREMENTS_VERIFICATION_MATRIX.json` — verification class, gate and evidence mapping.

## Gate chain

`G0 vehicle inputs -> G1A rotor -> G1B propulsion point -> G1C battery/transient -> G1 SYSTEM FREEZE -> G2 architecture -> G3 schematic/BOM -> G4 firmware -> G5 prototype release -> G6 propulsion verification -> G7 flight-test readiness`

A requirement may be structurally DEFINED before its parent gate closes. Its product-specific value may not be promoted from OPEN to FROZEN until parent dependencies and evidence exist.

## Anti-hallucination rules

1. OPEN/null/TBD remains OPEN/null/TBD.
2. Competitor data is benchmark/trade evidence, not our product baseline.
3. Legacy A2/B1/Faz2/Faz3 values are references, not authority.
4. First-order calculations and simulations are screening evidence, not physical validation.
5. Final BOM promotion requires a frozen parent requirement, exact MPN/footprint and derating evidence.
6. Physical-test, thermal, EMI, flight or production qualification is never inferred from ERC/DRC, simulation or datasheet analysis.

## Percentage-reporting rule

Every user-facing project-progress output should report at minimum:

- **Requirements structure %** — planned domain/schema coverage.
- **G1 value closure %** — PASS rows / required G1 matrix rows.
- **Backlog DONE %** — tasks explicitly marked DONE / total backlog tasks.

Any broader engineering-progress percentage must be explicitly labeled an estimate.