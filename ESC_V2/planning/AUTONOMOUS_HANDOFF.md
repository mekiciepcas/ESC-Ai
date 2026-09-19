# ESC autonomous handoff

Date: 2026-09-19 03:23+03:00
Branch: `uav-rebaseline`
Status: `PROGRESS_G1_DEPENDENCIES`

## Run summary

This run verified the existing heavy-UAV benchmark against current manufacturer primary sources and advanced two G1 dependency-opening analyses without freezing unknown product values.

## Tasks attempted

- Continue UAV-003 source-backed propulsion benchmark verification.
- Advance UAV-005 battery architecture trade study while final UAV-004 remains blocked.
- Advance UAV-006 electrical-envelope methodology parametrically while final operating points remain blocked.
- Update legacy B1 traceability with new evidence.

## Tasks completed / measurable progress

1. Existing XAG P150 Max values were re-verified from the current manufacturer specification: 136 kg max spraying MTOW, 4 motors, 56 kgf max thrust/motor, 4.85 kW rated power/motor, 140 A continuous ESC, 380 A/30 s maximum output current.
2. Hobbywing X15 G2 was re-verified from its 2026 manufacturer specification: 18S/69 V, 25–80 V input, 4.64 kW rated input, 3.971 kW rated output, 120 A continuous ESC, 300 A/3 s peak, 82 kgf max thrust and 37.5 kg recommended takeoff weight/axis.
3. Added `battery_architecture_pretrade.md`: carries ~50–53 V high-current and 18S/69 V candidates forward instead of inheriting 13S.
4. Quantified ideal bus-current reduction at equal power: 69 V versus 52.5 V reduces current by about 23.9%; ideal conductor I²R loss ratio is about 0.579 (~42% lower), before mass/device/switching trade effects.
5. Added `esc_envelope_parametric.md` with Q150, H175 and O175 scenarios and explicit OPEN fields required for UAV-006 closure.
6. Updated `UAV_TRACEABILITY.md` so 3 kW, 13S and 100 V semiconductor assumptions are linked to the new evidence and remain unfrozen.

## Files changed

- `planning/battery_architecture_pretrade.md` — new
- `planning/esc_envelope_parametric.md` — new
- `planning/UAV_TRACEABILITY.md` — updated
- `planning/autonomy_state.json` — updated
- `planning/AUTONOMOUS_HANDOFF.md` — updated

## Engineering decisions

- Do not preserve 13S as product baseline.
- Carry at least two voltage families: ~50–53 V and 18S/69 V.
- 18S is the preferred family for deeper analysis, not a frozen choice, because it has current heavy-agricultural precedent and materially reduces bus current at 4–5 kW/axis.
- Legacy 100 V MOSFET class is not frozen. 18S reaches 75.6 V at 4.2 V/cell, leaving transient margin that must be quantified before VDS selection.
- Legacy 3 kW is not accepted as a universal heavy-lift rating; current quad-class references are ~4.64–4.85 kW rated/axis.

## Evidence level / assumptions

- Manufacturer specifications: SOURCE_BACKED.
- 52.5 V vs 69 V current and I²R comparisons: CALCULATED_FIRST_ORDER.
- Q150/H175/O175: PARAMETRIC_SCENARIOS, not product requirements.
- 18S preference: TRADE_STUDY_PREFERENCE, not design freeze.
- No physical measurements or flight qualification claims were introduced.

## Unresolved blockers

- G0 cannot freeze without airframe mass, battery mass, nominal payload, mission duration, environmental envelope and failure/degraded-mode policy.
- UAV-004 cannot freeze until rotor architecture/MTOW is selected and exact propulsion operating points are sourced.
- Phase RMS/peak current cannot be inferred safely from bus P/V; motor operating data/model remains required.
- DC-bus transient ceiling remains unknown, so semiconductor VDS class cannot close.

## Risks/regressions discovered

- If 18S is selected, 100 V MOSFET margin may be too narrow depending on switching/regen/BMS-disconnect overshoot.
- B1's 80 V bus-check convention cannot automatically be treated as the final verification ceiling for an 18S design.
- A high-current ~50 V architecture may preserve easier voltage margin but increases conductor, connector and parallel-device burden.

## Exact next recommended tasks

1. Obtain/extract a source-backed X15 G2 thrust-current-power table and create scenario operating-point interpolation for Q150.
2. Find a second current propulsion system with a published 55–60 kgf-class thrust/power/current table for H175 comparison.
3. Create `propulsion_operating_points.json` with scenario labels and evidence references; do not mark UAV-004 complete until MTOW/rotor freeze.
4. Perform B1 voltage-compatibility precheck against the 18S candidate: aux buck, voltage dividers, gate driver, capacitors, connectors and FET class.

## Dependency chain

`G0 inputs -> rotor freeze -> source-backed motor/prop operating points -> battery freeze -> ESC electrical envelope -> semiconductor/PWM/control selection -> schematic/firmware/PCB`

## Next-run briefing

Start with primary-source propulsion performance tables, not generic ratings. Convert thrust points relevant to Q150/H175 into electrical input power/current and RPM only where manufacturer tables provide those values. Keep all scenario outputs explicitly non-frozen. If a full X15 G2 table cannot be retrieved, use the published 37.5 kg/axis efficiency (8 g/W) only as a source-backed rated-point check and label derived power accordingly; do not fabricate intermediate curve points. Then use the 18S candidate to audit B1 component voltage compatibility without editing historical A2/B1 design files.
