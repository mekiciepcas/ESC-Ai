# ESC autonomous handoff

Date: 2026-09-19 11:22+03:00  
Branch: `uav-rebaseline`  
Status: `PROGRESS_G0_CONTROLLED_BOUNDS_ROTOR_DECISION_TREE`

## Run summary
This run attacked the actual G0/G1A critical path rather than reorganizing requirements. It created governed trade-only MTOW bounds, refreshed the rotor trade against current primary-source heavy-agriculture anchors, and converted the single-motor-failure requirement into explicit rotor-architecture elimination logic. Product-specific G0 fields remain OPEN; no trade-only value was promoted to a requirement. No rotor count, battery architecture, ESC rating, semiconductor class, production package or physical-validation claim was frozen.

## Repository state verified at start
- Re-read and cross-checked `UAV_PRODUCT_PLAN.md`, `UAV_TRACEABILITY.md`, `uav_backlog.json`, `mission_requirements.json`, `AUTONOMOUS_HANDOFF.md`, `autonomy_state.json`, `rotor_trade_study.md` and X15 scenario/curve evidence on `uav-rebaseline`.
- G0/G1 remain OPEN; G2+ remain gated.
- Prior handoff correctly identified G0/G1A as the next critical-path work.

## Tasks attempted / completed
1. Reverified primary-source heavy-agriculture anchors: XAG P150, XAG P150 Max and DJI Agras T100.
2. Added `G0_TRADE_BOUNDING_CASES.md` with T125/T150/T175 analysis cases and an explicit non-promotion rule. These cases may support sensitivity calculations but cannot populate product requirements or close G0/G1.
3. Recorded primary-source anchors: P150 54 kg aircraft weight with spraying system+batteries, 70 kg max payload, 125 kg max spraying MTOW, quad, 55 kgf max thrust/motor, 4.7 kW rated motor and 120 A continuous ESC; P150 Max 56 kg empty with spraying system+batteries, 80 kg max payload, 136 kg max spraying MTOW, four motors, 56 kgf max thrust, 4.85 kW rated motor and 140 A continuous ESC; T100 75 kg spraying weight, 100 kg spraying payload, 175 kg max spraying MTOW, 60 rpm/V motors and 62-inch propellers.
4. Recorded DJI's T100-specific Turkey note that users should keep T100 MTOW at 149.9 kg in Turkey as regulatory/use context only; it was NOT copied into our product requirement.
5. Reworked `rotor_trade_study.md` into bounded screening with explicit quad/hex/octo statuses.
6. Formalized architecture discriminator: if G0 later requires continued controlled hover after complete loss of one motor/ESC, ordinary quad is eliminated before detailed ESC sizing. If that requirement is waived, quad remains a candidate.
7. Retained hex across T125-T175 for final trade; retained octo/coaxial particularly for redundancy-driven outcomes; did not select either.
8. Updated `UAV_TRACEABILITY.md`, `uav_backlog.json` and `autonomy_state.json` with the new evidence and blockers.

## Files changed
- `planning/G0_TRADE_BOUNDING_CASES.md` — new
- `planning/rotor_trade_study.md` — updated from preliminary narrative to governed bounded screening
- `planning/UAV_TRACEABILITY.md` — added TR-031/TR-032 and refreshed primary-source conclusions
- `planning/uav_backlog.json` — UAV-001/UAV-002 evidence and remaining conditions updated
- `planning/autonomy_state.json` — updated
- `planning/AUTONOMOUS_HANDOFF.md` — updated

## Engineering decisions / findings
- The 125/150/175 kg numerical cases are now explicitly `ASSUMPTION_FOR_TRADE_ONLY`; they are useful for engineering sensitivity but have zero authority to close G0 or G1.
- Single-motor/ESC failure policy is a first-order architecture decision. Continued-hover requirement eliminates ordinary quad; a waiver keeps quad in the trade.
- Quad has direct current commercial precedent in the 125-136 kg spraying-MTOW region from XAG P150/P150 Max.
- The T175 quad branch remains the highest per-axis stress case: 43.75 kgf/axis hover and 70-78.75 kgf/axis in the existing 1.6-1.8 static-margin sensitivity cases.
- Hex at T175 reduces those figures to 29.17 kgf hover and 46.67-52.50 kgf/axis sensitivity points; octo reduces them further to 21.88 kgf hover and 35.0-39.38 kgf/axis.
- These calculations narrow architecture choices but do not constitute a final rotor selection.

## Calculations / evidence added
- Controlled T125/T150/T175 x quad/hex/octo hover and 1.6/1.8 static-thrust sensitivity table.
- Architecture decision tree driven by failure-survival policy and actual MTOW.
- Fresh primary-source verification of XAG P150/P150 Max and DJI T100 mass/payload/propulsion architecture data.

## Assumptions introduced and evidence level
- T125/T150/T175: `ASSUMPTION_FOR_TRADE_ONLY`; not product requirements.
- 1.6/1.8 static thrust/weight: existing sensitivity cases only; not requirements.
- XAG/DJI published values: PRIMARY MANUFACTURER EVIDENCE.
- 70-100 kg payload target: USER REQUIREMENT.
- No physical measurements, qualification tests or flight evidence were generated.

## Unresolved blockers
- Product G0 nominal payload; airframe, battery and mission-equipment mass; MTOW min/nom/max.
- Endurance/hover/reserve mission profile and environmental envelope.
- Span/coaxial packaging constraints.
- Degraded-operation and single-motor/ESC failure policy.
- Final rotor count/thrust margin and therefore UAV-004 operating-point selection.
- Battery series/min/nom/full-charge/transient envelope.
- Phase RMS/peak current, eRPM and PWM requirement.
- Harness/PCB inductance, switching/regen/BMS-disconnect transient ceiling.
- Production non-backpower voltage-sense architecture and final semiconductor class/MPN.

## Regressions / risks discovered
- No repository regression discovered.
- A design-process risk was reduced: benchmark MTOWs can no longer silently become baseline because the new governance file explicitly forbids promotion without product evidence/approval.
- DJI's Turkey-specific 149.9 kg T100 note demonstrates that vehicle operational/regulatory constraints may be jurisdiction-specific; our final vehicle requirement must be handled separately rather than inferred from competitor maximums.

## Exact next recommended tasks
1. Use the existing X15 manufacturer curve to complete T125/T150/T175 quad/hex/octo trade-only current/power/RPM mapping where interpolation is within the measured curve; explicitly flag points above the published 120 A continuous ESC rating as non-continuous screening points.
2. Use that mapping to identify architecture branches that create obviously excessive per-axis electrical stress without turning the result into product requirements.
3. In parallel, draft non-backpower high-voltage sensing architecture candidates that remain valid independent of final VBUS.
4. Build a primary-source 100/120/150 V semiconductor candidate parameter table for trade only; do not select voltage class before transient ceiling and phase current are frozen.
5. Keep all product G0 fields OPEN until vehicle-specific values are supplied/approved; once they exist, run the decision tree and close G1A.

## Dependency chain
`G0 vehicle inputs -> G1A rotor selection -> G1B/UAV-004 product operating point -> G1C battery/current/transient envelope -> G1 SYSTEM FREEZE -> G2 architecture freeze -> G3 schematic review -> firmware/PCB -> bench/propulsion validation`

## Next-run briefing
The requirements matrix itself is already exhaustive; do not spend the next run restructuring it. Continue numerical propulsion screening using only the governed T125/T150/T175 trade cases and the existing X15 primary curve. The useful next result is a complete architecture-vs-current/power/RPM map and identification of points that exceed the X15 published continuous ESC current. Maintain the hard boundary between trade-only values and product requirements. Do not freeze quad/hex/octo, 18S, semiconductor voltage class, phase-current rating or production hardware until the G0/G1 evidence chain permits it.
