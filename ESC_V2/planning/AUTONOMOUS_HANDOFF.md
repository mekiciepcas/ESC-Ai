# ESC autonomous handoff

Date: 2026-09-19 14:18+03:00
Branch: `uav-rebaseline`
Status: `PROGRESS_SOURCE_BACKED_SEMICONDUCTOR_CLASS_TABLE`
Repository HEAD immediately before this handoff update: `b5f2dc5e57c79bdeb6d188bdd6915fb08eafa5e5`.

## Run summary
This run re-read and verified the required planning state and prior handoff, then completed the highest-priority independent task from the prior briefing: a primary-source 100/120/150 V MOSFET candidate table for later normalized power-stage trade. The table deliberately does not select a voltage class or production MPN because G1 transient/current/PWM/thermal requirements remain open. Traceability and machine-readable autonomy state were updated to reflect the new evidence.

## Tasks attempted / completed
1. Re-read `UAV_PRODUCT_PLAN.md`, `UAV_TRACEABILITY.md`, `uav_backlog.json`, `mission_requirements.json`, prior `AUTONOMOUS_HANDOFF.md` and autonomy state.
2. Verified G0/G1 remain OPEN and product-specific mass, rotor, propulsion, battery, phase-current and transient fields remain legitimately unresolved.
3. Researched current primary manufacturer data for real 100/120/150 V MOSFET trade anchors.
4. Added `SEMICONDUCTOR_VOLTAGE_CLASS_CANDIDATES.md`.
5. Recorded TI CSD19536KTT as 100 V legacy reference only: 100 V, 2.4 mOhm max @10 V, Qg 118 nC typ, Qgd 17 nC typ, package-limited ID 200 A, -55..175 C.
6. Recorded Infineon IPT017N12NM6 as a 120 V trade anchor: 120 V, 1.7 mOhm max @10 V, Qg 113 nC typ, ID 331 A @25 C, 395 W package dissipation entry, -55..175 C, TOLL; manufacturer status active/preferred.
7. Recorded Infineon IAUTN15S6N025 as a 150 V trade anchor: 150 V, 2.5 mOhm max @10 V, Qg 107 nC typ, ID 245 A @25 C, RthJC max 0.42 K/W, -55..175 C, TOLL; manufacturer status active/preferred.
8. Recorded IAUTN15S6N038T as an alternate 150 V top-side-cooled packaging anchor, not a selection.
9. Defined the common-envelope normalization required before G2 semiconductor freeze: verified VBUS/transient derating, phase RMS/peak, PWM/gate drive, hot RDS(on), switching/recovery data, package thermal path, SOA/transient policy and layout/package constraints.
10. Updated `UAV_TRACEABILITY.md` and `autonomy_state.json`.

## Files changed
- `planning/SEMICONDUCTOR_VOLTAGE_CLASS_CANDIDATES.md` — new
- `planning/UAV_TRACEABILITY.md` — updated
- `planning/autonomy_state.json` — updated
- `planning/AUTONOMOUS_HANDOFF.md` — updated

## Engineering decisions / findings
- Lack of real device examples no longer blocks preparation of the 100/120/150 V trade: credible active devices exist in all three classes.
- The legacy TI 100 V part remains reference-only; no evidence from this run justifies retaining 100 V for the UAV product.
- Modern 120 V and 150 V candidates show that higher voltage class does not automatically imply prohibitive milliohm resistance or gate charge, but this is not yet a loss conclusion.
- Manufacturer ID ratings are explicitly prohibited from being treated as ESC continuous-current ratings.
- Voltage class remains governed first by verified G1 transient ceiling/derating, then by common-envelope electrical/thermal/package trade.

## Calculations / evidence added
Primary-source parameter evidence was added rather than product calculations because the governing current/PWM/temperature envelope remains open. The new table captures VDS, RDS(on), Qg and available current/thermal/package evidence with manufacturer source URLs. No unsupported hot-loss or ESC-current value was calculated.

## Primary evidence
- TI CSD19536KTT official product/datasheet page: https://www.ti.com/product/CSD19536KTT
- Infineon IPT017N12NM6 official product page and Rev 2.0 datasheet: https://www.infineon.com/part/IPT017N12NM6
- Infineon IAUTN15S6N025 official product page: https://www.infineon.com/part/IAUTN15S6N025
- Infineon IAUTN15S6N038T official product page: https://www.infineon.com/part/IAUTN15S6N038T

## Assumptions and evidence level
- Device parameters listed in the candidate table: PRIMARY MANUFACTURER EVIDENCE under the manufacturers' stated test/rating conditions.
- Candidate ranking: NOT PERFORMED; operating envelope is insufficient.
- 18S, 120 V and 150 V remain candidate/screening cases only.
- Manufacturer current ratings are device/package ratings, not product requirements.
- No physical measurements were performed.

## Unresolved blockers
- Product G0 mass/mission/environment/failure policy and actual MTOW.
- Final rotor architecture and thrust margin.
- Product motor/prop selection, pole-pair count, phase RMS/peak current and eRPM.
- Battery series/min/nom/full-charge/transient envelope.
- Harness/PCB inductance and switching/regen/BMS-disconnect transient ceiling.
- Exact power-off-tolerant sensing device/topology and its primary-source limits.
- Common operating point needed for semiconductor hot-loss/SOA comparison.
- Final semiconductor voltage class/MPN, PWM and DC-link/precharge/clamp sizing.

## Regressions or risks discovered
- No repository regression found.
- Comparing headline RDS(on), Qg or ID across different packages/test conditions can produce a false winner. The trade must normalize conditions and include actual cooling/layout.
- 120/150 V device availability does not solve the DRV8353/LM5164 100 V-domain issue; driver and auxiliary architecture remain separately constrained by the final transient ceiling.

## Exact next recommended tasks
1. Search exact voltage-sense buffer/front-end candidates whose manufacturer documentation explicitly specifies safe input behavior while VCC=0; reject any device that merely redirects divider current into an unpowered rail.
2. Extend the semiconductor table with hot RDS(on), Qgd/Qrr/Coss and thermal data only where primary-source test conditions can be captured without misleading cross-device comparison.
3. Keep G0/G1 product fields OPEN until vehicle-specific targets are supplied/approved; do not infer phase current/eRPM from X15 DC-input data.

## Dependency chain
`G0 vehicle inputs -> G1A rotor selection -> G1B product operating point + motor electrical data -> G1C battery/transient envelope -> G1 SYSTEM FREEZE -> G2 architecture freeze (semiconductor/sensing included) -> G3 schematic review -> firmware/PCB -> physical validation`

## Next-run briefing
Start with exact power-off-tolerant HV sense front-end evidence. The architecture trade already exists; do not repeat it. A candidate is useful only if primary manufacturer documentation covers its input/IO behavior when its local supply is absent or provides an architecture that prevents rail backpower by construction. If no credible part can be proven, document the evidence gap and move to deeper comparable semiconductor parameter extraction. Do not freeze a voltage class, sensing MPN or product rating while G1 remains open.
