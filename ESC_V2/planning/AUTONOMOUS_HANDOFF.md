# ESC autonomous handoff

Date: 2026-09-19 12:21+03:00
Branch: `uav-rebaseline`
Status: `PROGRESS_X15_ARCHITECTURE_ELECTRICAL_STRESS_MAP`
Repository HEAD during finalization: `b49f114180938e3b358683f8f60fed6c044b4e97` before this handoff commit.

## Run summary
This run completed the next critical unblocked propulsion-screening task. The existing manufacturer X15 G2 69 V / MFP 63x24 bench curve was mapped by piecewise-linear interpolation across all governed T125/T150/T175 x quad/hex/octo cases at hover, 1.6x and 1.8x thrust. The map explicitly identifies points above the X15 published 120 A continuous ESC current while preserving the hard boundary between trade-only screening and product requirements. No rotor architecture, MTOW, 18S battery, phase-current requirement, semiconductor class or production hardware was frozen.

## Tasks attempted / completed
1. Re-read the prior handoff and verified the requested next task against the current X15 curve artifact.
2. Calculated per-axis DC input current, input power and mechanical RPM for 27 governed scenario points using interpolation only inside measured manufacturer data.
3. Added `X15_TRADE_OPERATING_MAP.md`.
4. Marked >120 A reference points as non-continuous screening points: T125 quad 1.8x; T150 quad 1.6x/1.8x; T175 quad 1.6x/1.8x.
5. Confirmed T175 hex 1.8x maps to about 113.5 A / 7.83 kW / 1903 RPM and therefore remains below the published 120 A continuous-current number in this bench-reference comparison; this is not a thermal/endurance qualification.
6. Confirmed all governed octo points remain below 120 A in the same curve mapping.
7. Explicitly prevented misuse of DC input current as phase current and mechanical RPM as electrical RPM.
8. Updated `autonomy_state.json`.

## Files changed
- `planning/X15_TRADE_OPERATING_MAP.md` — new
- `planning/autonomy_state.json` — updated
- `planning/AUTONOMOUS_HANDOFF.md` — updated

## Engineering decisions / findings
- T150/T175 quad high-thrust screening creates materially higher per-axis electrical stress than hex/octo for the X15 reference and crosses the published continuous-current number well before the measured curve maximum.
- T175 quad hover itself remains within the curve at about 85.2 A / 5.88 kW, but the governed high-thrust sensitivity points rise to about 185 A at 1.6x and 228 A at 1.8x; they must not be interpreted as continuous operating points.
- T175 hex is materially less stressed: about 45.9 A hover, 94.2 A at 1.6x and 113.5 A at 1.8x in the reference curve.
- Rotor-count increase therefore provides a quantified per-axis electrical-stress benefit, but final architecture selection still depends on actual MTOW, redundancy/failure policy, packaging, efficiency and cost.

## Calculations / evidence added
- Complete T125/T150/T175 x 4/6/8 rotor x hover/1.6x/1.8x map: 27 operating points.
- Each in-range point contains interpolated DC current, input power and mechanical RPM from the repository's 22-row manufacturer curve.
- No extrapolation beyond 14.297-82.476 kgf measured thrust range.

## Assumptions and evidence level
- X15 curve rows: PRIMARY MANUFACTURER EVIDENCE already stored in repository.
- Piecewise-linear interpolation between measured rows: ENGINEERING CALCULATION.
- T125/T150/T175 and 1.6x/1.8x: ASSUMPTION_FOR_TRADE_ONLY.
- 120 A continuous comparison: manufacturer reference rating, not our ESC requirement.
- No physical measurements, thermal validation or flight evidence generated.

## Unresolved blockers
- Product G0 mass/mission/environment/failure policy and actual MTOW.
- Final rotor architecture and thrust margin.
- Product motor/prop selection and pole-pair count; eRPM remains open.
- Phase RMS/peak current cannot be inferred from the DC input-current curve alone.
- Battery series/min/nom/full-charge/transient envelope.
- Harness/PCB inductance, switching/regen/BMS-disconnect transient ceiling.
- Production non-backpower sensing architecture and final semiconductor voltage class/MPN.

## Regressions / risks discovered
- No repository regression found.
- A requirements misuse risk was reduced: the new artifact explicitly states DC input current is not phase current and RPM is not eRPM.
- Quad remains potentially viable only if actual vehicle/failure requirements permit it; high-end trade cases show rapidly shrinking electrical margin with the X15 reference.

## Exact next recommended tasks
1. Draft non-backpower high-voltage sensing architecture candidates independent of final VBUS and compare fault/power-sequencing behavior against B1 rail clamps.
2. Build a primary-source 100/120/150 V semiconductor candidate parameter table for trade only, including VDS, hot RDS(on) evidence, Qg/Qgd, package/current/thermal data; do not select a class.
3. Use actual G0 inputs when available to collapse the trade tree and close G1A; until then keep product fields OPEN.
4. Do not derive phase-current or eRPM requirements from this map until motor electrical parameters are evidenced.

## Dependency chain
`G0 vehicle inputs -> G1A rotor selection -> G1B product operating point + motor electrical data -> G1C battery/transient envelope -> G1 SYSTEM FREEZE -> G2 architecture freeze -> G3 schematic review -> firmware/PCB -> physical validation`

## Next-run briefing
The X15 architecture-vs-electrical-stress map is complete; do not repeat this interpolation work. Continue with architecture work that is independent of missing G0: non-backpower HV sensing candidates first, then source-backed semiconductor trade parameters. Preserve all T125/T150/T175 results as trade-only. Do not freeze phase current, eRPM, 18S, voltage class, rotor count or production MPNs from this reference map.
