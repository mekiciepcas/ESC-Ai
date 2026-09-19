# ESC autonomous handoff

Date: 2026-09-19 10:27+03:00  
Branch: `uav-rebaseline`  
Status: `PROGRESS_BACKPOWER_G1_MATRIX_EXHAUSTIVE_BACKLOG_RECONCILIATION`

## Run summary
This run converted previously implicit project risks and requirements into auditable engineering state. The B1 voltage-sense clamp now has a documented analog-rail/LDO back-power hazard; G1 requirements closure is now represented by an exhaustive machine-readable matrix rather than prose; and the stale backlog was reconciled so completed propulsion benchmarking is no longer shown as TODO. No vehicle mass, rotor architecture, battery architecture, voltage class, semiconductor MPN, transient ceiling, phase-current rating or production release was frozen.

## Repository state verified at start
- Prior handoff/status was read and checked against `uav-rebaseline`.
- `UAV_PRODUCT_PLAN.md`, `UAV_TRACEABILITY.md`, `uav_backlog.json`, `mission_requirements.json`, `REQUIREMENTS_COMPLETION_CHECKLIST.md`, `design_basis.json` and `autonomy_state.json` were re-read.
- G0 and G1 remain OPEN; downstream G2+ remains gated.

## Tasks attempted / completed
1. Traced the complete B1 analog back-power path from high-voltage measurement input through upper BAT54H into +3V3A, through the 0R analog link into +3V3 and the TLV75533 output.
2. Verified TI TLV755P Rev. D reverse-current guidance: output bias while input is absent, or VOUT above VIN, is a documented reverse-current condition exceeding the stated VOUT > VIN + 0.3 V absolute-maximum relationship; excessive reverse current can degrade reliability/latch up.
3. Added `ANALOG_RAIL_BACKPOWER_AUDIT.md` and classified the B1 rail-referenced clamp as `RECALCULATE / REPLACE IF REQUIRED` for the UAV revision.
4. Added `G1_REQUIREMENTS_MATRIX.json`, leaving unsupported values OPEN and explicitly mapping G0/G1A/G1B/G1C/G1 closure fields.
5. Extended the G1 matrix so DC current, PWM, current-sense range, DC-link ripple/energy, thermal, OV/UV/OCP/OT and communication/arming/watchdog/failsafe requirements are explicit rows instead of a side list.
6. Verified the final matrix count for this run: **46 tracked rows, 1 PASS and 45 OPEN**. This is an audit count, not a project-completion percentage.
7. Updated `UAV_TRACEABILITY.md` with the back-power/LDO evidence and machine-auditable requirements gate.
8. Reconciled `uav_backlog.json`: UAV-002 rotor trade moved from TODO to IN_PROGRESS; UAV-003 heavy-lift market benchmark moved to DONE with evidence. UAV-004 remains BLOCKED because final MTOW/rotor architecture is not frozen.
9. Updated `autonomy_state.json` for the next run.

## Files changed
- `planning/ANALOG_RAIL_BACKPOWER_AUDIT.md` — new
- `planning/G1_REQUIREMENTS_MATRIX.json` — new and extended to exhaustive current checklist coverage
- `planning/UAV_TRACEABILITY.md` — updated
- `planning/uav_backlog.json` — reconciled
- `planning/autonomy_state.json` — updated
- `planning/AUTONOMOUS_HANDOFF.md` — updated

## Engineering decisions / findings
- The B1 sensing divider itself can remain a reference concept, but the **BAT54H-to-control-rail clamp implementation is not UAV-qualified**.
- With VBUS/phase input present while control rails are absent/collapsing, the upper BAT54H can externally bias +3V3A/+3V3 and therefore the TLV75533 output. TI explicitly documents reverse current when an LDO output is biased without established input.
- Low source current from the high-value divider is useful for screening but does not establish deterministic/safe sequencing; normal-operation design must not rely on absolute-maximum or reverse-conduction behavior.
- Derived sensing requirement carried forward: **no high-voltage measurement input may create an uncontrolled back-power path into MCU/control supply rails.**
- Propulsion market benchmarking acceptance is complete: multiple current heavy-lift/agricultural candidates and a source-backed X15 G2 operating curve exist. Selecting the product operating point is a separate task and remains blocked by G0/G1A.
- Requirements completion is now mechanically inspectable. The dominant system-freeze blocker is vehicle-specific G0 input closure, not lack of benchmark data or hidden checklist items.

## Calculations / evidence added
- No new product numerical requirement was invented this run.
- TI TLV755P reverse-current behavior was added as primary-source architecture evidence.
- G1 matrix currently records 46 explicit requirement rows: 1 PASS / 45 OPEN.

## Assumptions and evidence level
- 70–100 kg remains the user payload target: USER REQUIREMENT.
- 18S/75.6 V remains a candidate steady-state family, not frozen: ENGINEERING CANDIDATE.
- TLV755P reverse-current behavior: PRIMARY MANUFACTURER EVIDENCE.
- Existing B1 rail topology: REPOSITORY SOURCE EVIDENCE.
- No physical measurements or qualification tests were performed.

## Unresolved blockers
- G0 nominal payload, airframe mass, battery mass, mission-equipment mass and resulting MTOW.
- Flight/hover duration, reserve-energy requirement and operating environment.
- Single motor/ESC failure/degraded-mode policy.
- Final rotor architecture/thrust margin.
- Final motor/prop hover and peak operating points, phase RMS/peak current and eRPM.
- Battery series count/min/nom/full-charge/transient envelope.
- Harness/PCB inductance, switching/regen/BMS-disconnect transient ceiling.
- Production voltage-sense clamp/power-sequencing architecture and powered/unpowered bench proof.
- Final semiconductor voltage class/MPN, PWM and DC-link/precharge/clamp sizing.

## Risks / regressions
- Current B1 sensing clamps can create a back-power path during abnormal power sequencing; this is now a known design risk rather than an untracked assumption.
- Existing 100 V MOSFET/DRV8353/LM5164/DC-link domains remain coupled to the unresolved transient ceiling.
- The G1 matrix is intentionally strict. Open rows must not be converted to PASS by copying competitor values or legacy B1 targets.

## Exact next recommended tasks
1. Establish a controlled G0 assumption process: obtain user vehicle targets where possible and, where unavailable, create explicitly labelled `ASSUMPTION_FOR_TRADE_ONLY` bounding cases that cannot silently become baseline requirements.
2. Use those bounded cases to finish the rotor architecture trade and narrow G1A without pretending final vehicle requirements are known.
3. Translate bounded rotor scenarios into source-backed propulsion current/power/eRPM ranges; do not freeze UAV-004 until G0/G1A are approved.
4. Continue non-G0-blocked architecture work: upstream +5 V reverse-current assessment, non-backpower voltage-sense topology candidates, and source-backed 100/120/150 V semiconductor candidates for trade use only.
5. When G0/G1A are sufficiently bounded, populate the 46-row G1 matrix from evidence and use it as the mechanical condition for SYSTEM FREEZE.

## Dependency chain
`G0 vehicle inputs -> G1A rotor -> G1B operating point -> G1C battery/current/transient envelope -> G1 SYSTEM FREEZE -> G2 architecture freeze -> G3 schematic review -> firmware/PCB -> bench/propulsion validation`

## Next-run briefing
Requirements tracking is now exhaustive for the current checklist; do not spend another run reorganizing requirements unless a new parent requirement appears. The next critical-path work is G0/G1A. Keep unknown user-specific values OPEN, but bounded trade-only cases may be used for calculations if clearly labelled and prevented from becoming baseline. In parallel continue non-blocked architecture audits. Do not promote 18S, 100/120/150 V screening classes, competitor current ratings or interpolated thrust points into product requirements without the G0/G1 decision chain. Propulsion market benchmark UAV-003 is DONE; focus on product operating-point selection, not redundant benchmarking.
