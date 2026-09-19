# Requirements completion checklist

Date: 2026-09-19
Purpose: define when requirements are structurally complete and when they are sufficiently value-closed to enter architecture/detail design without pretending unresolved vehicle inputs are known.

## Requirements authority and current progress

- `REQUIREMENTS_MASTER.json` is the top-level requirements-structure authority.
- `REQUIREMENTS_SPEC.md` is the human-readable hierarchy and status rule set.
- `G1_REQUIREMENTS_MATRIX.json` remains the controlling child matrix for G0/G1A/G1B/G1C/G1 numerical/selection closure.
- `REQUIREMENTS_VERIFICATION_MATRIX.json` defines domain verification methods and evidence levels.
- `REQUIREMENTS_PROGRESS.json` is the machine-readable percentage-reporting snapshot.

Current measurable state:
- planned requirements structure: **12/12 domains = 100%**;
- G1 SYSTEM FREEZE values: **1/46 PASS = 2.2%**;
- backlog tasks explicitly DONE: **1/25 = 4%**;
- major product gates closed: **0/8 = 0%**.

The 100% structure figure does not mean product-specific requirement values are complete.

## Definition of system requirements complete
Requirements are considered **SYSTEM-BASELINED at G1** when G0, G1A, G1B and G1C evidence is closed and every critical ESC electrical-envelope row in `G1_REQUIREMENTS_MATRIX.json` / `design_basis.json` is numeric or explicitly bounded and traceable to propulsion/vehicle evidence. This is not production qualification; detailed derived requirements continue through G2/G3.

## G0 — Mission / vehicle envelope — OPEN
Required closure:
- payload min/nom/max confirmed as payload, not MTOW
- airframe mass range
- battery mass/energy target
- mission equipment mass
- target flight time / duty cycle
- takeoff/climb/hover/cruise/landing profile
- ambient temperature and altitude envelope
- wind/environment assumptions
- single-motor/ESC failure policy
- resulting MTOW min/nom/max and energy budget

Current blocker: vehicle-specific values are not frozen. Keep OPEN; do not infer them from competitor aircraft.

## G1A — Rotor / thrust requirement — IN PROGRESS
Required closure:
- rotor count/architecture selected
- hover thrust per rotor
- peak thrust per rotor and duration
- thrust-to-weight margin
- degraded-mode requirement if applicable
- mechanical prop/rotor envelope

Evidence already available: quad/hex/octo/coaxial trade framework and heavy-lift propulsion benchmarks. Final choice depends on G0.

## G1B — Propulsion operating point — IN PROGRESS
Required closure:
- at least two source-backed motor/prop candidates
- thrust/current/power/RPM operating curves
- selected/reference hover and peak points
- eRPM envelope
- motor thermal/electrical constraints or explicit measurement plan

Evidence already available: X15 G2 operating curve and additional heavy-lift references. Final operating point depends on G0/G1A.

## G1C — Battery architecture — IN PROGRESS
Required closure:
- series-cell architecture
- VBUS min/nom/full-charge
- transient ceiling/acceptance rule
- pack continuous/peak current
- usable energy/sag assumptions
- BMS/contact/fuse/precharge behavior
- regen/disconnect energy acceptance
- harness/connector current envelope

Current candidate: 18S is under evaluation; it is not frozen. 75.6 V full-charge is a candidate steady-state point, not a transient ceiling.

## G1 — ESC electrical envelope / SYSTEM FREEZE — OPEN
All critical fields must be numeric/bounded and traceable:
- VBUS min/nom/max/transient
- input power continuous/peak + duration
- DC current continuous/peak + duration
- phase RMS continuous/overload
- phase peak current
- eRPM
- PWM candidate/selected range
- current-sense range
- DC-link ripple/energy requirement
- ambient/baseplate limits
- OV/UV/OCP/OT/fault response requirements
- communications/arming/watchdog/failsafe requirements

## Derived requirements after G1
These are structurally represented under the `INV`, `SNS`, `CTRL`, `SAF`, `IF`, `ENV`, `MFG` and `VER` domains. They do not block structural completion, but their product values/implementations must close before the owning G2/G3/G4/G5/G6 gate:
- semiconductor voltage class/count and thermal derating
- gate-drive current/dead-time
- ADC acquisition/filter/clamp implementation
- exact shunt/CSA gain
- exact DC-link MPN and ripple/lifetime proof
- precharge resistor/contactor/clamp MPNs
- creepage/clearance/layout constraints
- firmware timing and trip latency
- protection/failsafe/FMEA closure
- exact production BOM/footprints/DFM
- staged bench/dyno/fault-injection evidence

## Current critical path
`G0 vehicle inputs -> G1A rotor selection -> G1B operating point -> G1C battery/current/transient envelope -> G1 ESC SYSTEM FREEZE -> G2 architecture freeze -> G3 schematic review -> G4 firmware -> G5 prototype -> G6 propulsion verification -> G7 flight readiness`

## Autonomous-work rule while G0 is open
Continue source-backed trade studies, parametric models, component-domain audits, verification tooling, BOM evidence mapping and derived-requirement structure. Do not convert competitor values or screening cases into product requirements. Any value dependent on vehicle-specific input remains OPEN/null/TBD.