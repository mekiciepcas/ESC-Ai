# ESC autonomous handoff

Date: 2026-09-19 10:27+03:00  
Branch: `uav-rebaseline`  
Status: `PROGRESS_BACKPOWER_G1_AUDIT_BACKLOG_RECONCILIATION`

## Run summary
This run converted two previously implicit project risks into auditable engineering state: the B1 voltage-sense clamp now has a documented analog-rail/LDO back-power hazard, and G1 requirements closure now has a machine-readable open-field matrix. The stale backlog was also reconciled so completed propulsion benchmarking is no longer shown as TODO. No vehicle mass, rotor architecture, battery architecture, voltage class, semiconductor MPN, transient ceiling, phase-current rating or production release was frozen.

## Repository state verified at start
- Prior handoff/status was read and checked against `uav-rebaseline`.
- `UAV_PRODUCT_PLAN.md`, `UAV_TRACEABILITY.md`, `uav_backlog.json`, `mission_requirements.json`, `REQUIREMENTS_COMPLETION_CHECKLIST.md`, `design_basis.json` and `autonomy_state.json` were re-read.
- G0 and G1 remain OPEN; downstream G2+ remains gated.

## Tasks attempted / completed
1. Traced the complete B1 analog back-power path from high-voltage measurement input through upper BAT54H into +3V3A, through the 0R analog link into +3V3 and the TLV75533 output.
2. Verified TI TLV755P Rev. D reverse-current guidance: output bias while input is absent, or VOUT above VIN, is a documented reverse-current condition exceeding the stated VOUT > VIN + 0.3 V absolute-maximum relationship; excessive reverse current can degrade reliability/latch up.
3. Added `ANALOG_RAIL_BACKPOWER_AUDIT.md` and classified the B1 rail-referenced clamp as `RECALCULATE / REPLACE IF REQUIRED` for the UAV revision.
4. Added `G1_REQUIREMENTS_MATRIX.json`, leaving unsupported values OPEN and explicitly mapping G0/G1A/G1B/G1C/G1 closure fields.
5. Corrected the G1 matrix row count before ending this run: 30 explicit rows, 1 PASS and 29 OPEN. The additional derived G1 fields remain separately listed and are not falsely counted as closed.
6. Updated `UAV_TRACEABILITY.md` with the back-power/LDO evidence and the machine-auditable requirements gate.
7. Reconciled `uav_backlog.json`: UAV-002 rotor trade moved from TODO to IN_PROGRESS; UAV-003 heavy-lift market benchmark moved to DONE with evidence. UAV-004 remains BLOCKED because final MTOW/rotor architecture is not frozen.
8. Updated `autonomy_state.json` for the next run.

## Files changed
- `planning/ANALOG_RAIL_BACKPOWER_AUDIT.md` — new
- `planning/G1_REQUIREMENTS_MATRIX.json` — new, then count-corrected
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
- Requirements completion is now mechanically inspectable rather than narrative only. The dominant system-freeze blocker remains vehicle-specific G0 inputs, not lack of competitor data.

## Calculations / evidence added
- No new product numerical requirement was invented this run.
- TI TLV755P reverse-current behavior was added as primary-source architecture evidence.
- G1 matrix records the current explicit closure state as 30 tracked rows: 1 PASS / 29 OPEN. This is an audit status, not an overall project-completion percentage.

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
- `G1_REQUIREMENTS_MATRIX.json` currently enumerates the highest-priority explicit fields plus a separate list of additional G1 closure requirements. It should be extended until every checklist item has a row before G1 closure.

## Exact next recommended tasks
1. Extend `G1_REQUIREMENTS_MATRIX.json` so the additional DC-current, PWM, sense-range, DC-link, thermal, protection and communication/failsafe requirements become explicit rows rather than a side list.
2. Establish a controlled G0 assumption process: either obtain user vehicle targets or create bounded `ASSUMPTION_FOR_TRADE_ONLY` cases that cannot silently become baseline requirements.
3. Use the bounded G0 cases to finish the rotor architecture trade and narrow G1A without pretending final vehicle requirements are known.
4. Translate the selected trade scenarios into source-backed propulsion current/power/eRPM bounds; do not freeze UAV-004 until G0/G1A are approved.
5. Continue architecture work that is independent of final G0: upstream +5 V reverse-current assessment, non-backpower voltage-sense topology candidates, and a source-backed 100/120/150 V semiconductor candidate table for trade use only.

## Dependency chain
`G0 vehicle inputs -> G1A rotor -> G1B operating point -> G1C battery/current/transient envelope -> G1 SYSTEM FREEZE -> G2 architecture freeze -> G3 schematic review -> firmware/PCB -> bench/propulsion validation`

## Next-run briefing
First make the G1 matrix exhaustive so requirements closure cannot hide in prose. Then work the G0 blocker explicitly: keep unknown user-specific values OPEN, but define clearly labelled trade-only bounding cases if useful for rotor/propulsion screening. In parallel, continue non-blocked architecture audits. Do not promote 18S, 100/120/150 V screening classes, competitor current ratings or interpolated thrust points into product requirements without the G0/G1 decision chain. The propulsion market benchmark itself is DONE; focus next on product operating-point selection and requirements closure, not collecting redundant benchmark products.
