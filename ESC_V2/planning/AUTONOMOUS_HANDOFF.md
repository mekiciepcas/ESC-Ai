# ESC autonomous handoff

Date: 2026-09-19 13:18+03:00
Branch: `uav-rebaseline`
Status: `PROGRESS_NONBACKPOWER_HV_SENSE_ARCHITECTURE_TRADE`
Repository HEAD before this handoff commit: `89ee8dc25dbd7cb49d23e47d0faa94cccaab6f73`.

## Run summary
This run verified the prior planning state against the branch and completed the next independent architecture task: a non-backpower high-voltage sensing topology trade. Four topology families were screened without inventing final VBUS, bandwidth, accuracy, isolation or component data. The principal derived requirement is now explicit: a live VBUS/phase sense input shall not depend on an unpowered MCU/control supply rail sinking clamp current. No product requirement, rotor architecture, battery architecture, semiconductor class, sensing MPN or production schematic was frozen.

## Tasks attempted / completed
1. Re-read and verified `UAV_PRODUCT_PLAN.md`, `UAV_TRACEABILITY.md`, `uav_backlog.json`, `mission_requirements.json`, prior handoff and autonomy state.
2. Confirmed G0/G1 remain OPEN and that final propulsion/current/voltage values cannot yet be frozen.
3. Added `NON_BACKPOWER_HV_SENSE_ARCHITECTURES.md`.
4. Defined seven derived architecture requirements covering power-off backfeed, injection-limit misuse, resistor working/pulse stress, clamp energy return, single faults, measurement headroom and phase-node dv/dt.
5. Screened: (A) passive divider + ground-referenced local clamp, (B) protected powered buffer with valid power-off input behavior, (C) isolated voltage measurement, and (D) power-off-tolerant measurement front end/ADC.
6. Classified B1 BAT54H rail clamps as not a default KEEP for U1; Candidate B/D are preferred non-isolated study directions subject to exact primary-source device evidence.
7. Defined the verification package required before G2 sensing closure, including control-rails-OFF HV-input bench testing from a current-limited source.
8. Updated `autonomy_state.json`.

## Files changed
- `planning/NON_BACKPOWER_HV_SENSE_ARCHITECTURES.md` — new
- `planning/autonomy_state.json` — updated
- `planning/AUTONOMOUS_HANDOFF.md` — updated

## Engineering decisions / findings
- B1's divider concept remains reusable as a calculation starting point, but the rail-referenced BAT54H clamp implementation shall not be copied into U1 without a new proof.
- The sensing architecture must have deterministic behavior when HV is present and MCU/control rails are absent.
- Candidate B (protected buffer with explicit power-off input specification) and Candidate D (measurement front end with explicit power-off tolerance) provide the clearest path to eliminating the known rail-backfeed ambiguity while retaining non-isolated sensing.
- Candidate C isolation remains an option only if system-level CMTI/ground-separation requirements justify its cost, latency, bias-supply and layout burden.
- No topology or MPN is selected by this screening.

## Calculations / evidence added
No new product numeric requirement was introduced. This run added topology/fault-path evidence and verification criteria rather than unsupported numerical sizing.

## Assumptions and evidence level
- Existing B1 backpower path: REPOSITORY SOURCE EVIDENCE from prior schematic audit.
- Need to avoid uncontrolled off-state rail injection: DERIVED SAFETY/ROBUSTNESS REQUIREMENT from the proven B1 fault path and prior manufacturer guidance.
- Candidate topology rankings: ENGINEERING TRADE JUDGMENT pending exact device evidence.
- 18S, 120 V and 150 V remain candidates/screening cases only.
- No physical measurements were performed.

## Unresolved blockers
- Product G0 mass/mission/environment/failure policy and actual MTOW.
- Final rotor architecture and thrust margin.
- Product motor/prop selection, pole-pair count, phase RMS/peak current and eRPM.
- Battery series/min/nom/full-charge/transient envelope.
- Harness/PCB inductance and switching/regen/BMS-disconnect transient ceiling.
- Exact power-off-tolerant sensing device/topology and its primary-source limits.
- Final semiconductor voltage class/MPN, PWM and DC-link/precharge/clamp sizing.

## Regressions / risks discovered
- No new repository regression found.
- Candidate A ground-only clamping can still fail to protect the positive ADC boundary unless its threshold is guaranteed under tolerance/current/temperature; it cannot be accepted merely because it avoids +3V3 backfeed.
- Candidate D digital interfaces can themselves back-power an unpowered MCU unless interface sequencing is included in the audit.

## Exact next recommended tasks
1. Build a primary-source 100/120/150 V MOSFET candidate parameter table for trade use only: VDS, RDS(on) including temperature evidence, Qg/Qgd, package/thermal limits and availability/lifecycle where evidenced. Do not select a voltage class until G1 transient/current envelope closes.
2. Search exact buffer/measurement-front-end candidates with explicitly documented input behavior while VCC=0; reject parts whose protection simply steers HV-divider current into an unpowered supply.
3. Continue G0/G1A only when actual vehicle inputs become available; keep product fields OPEN meanwhile.
4. Do not derive phase current/eRPM from the X15 DC-input/RPM reference map.

## Dependency chain
`G0 vehicle inputs -> G1A rotor selection -> G1B product operating point + motor electrical data -> G1C battery/transient envelope -> G1 SYSTEM FREEZE -> G2 architecture freeze (including sensing) -> G3 schematic review -> firmware/PCB -> physical validation`

## Next-run briefing
Do not repeat the X15 map or generic sensing topology trade. Start with the source-backed semiconductor candidate table because it is independent of missing G0 and will make the eventual 100/120/150 V loss/derating comparison executable. In parallel, only promote a voltage-sense buffer/front end if its manufacturer documentation explicitly covers power-off input behavior. Keep all final ratings and MPN selections OPEN until the governing G1 envelope exists.
