# ESC autonomous handoff

Date: 2026-09-20 05:22+03:00  
Branch: `uav-rebaseline`  
Repository HEAD observed after engineering/state commits and before this handoff commit: `6bad6539c8a470084b243c76c3d579ea55ea2c94`  
Run status: `PB08_U8LITE_KV85_OPERATING_CURVE_ERPM_EVIDENCE_ADDED`

## Repository continuity verification

Read and verified `UAV_PRODUCT_PLAN.md`, `UAV_TRACEABILITY.md`, `uav_backlog.json`, `mission_requirements.json`, `REQUIREMENTS_MASTER.json`, `REQUIREMENTS_PROGRESS.json`, prior `AUTONOMOUS_HANDOFF.md`, and `autonomy_state.json` on `uav-rebaseline`. PB-08 remains active authority. The primary S1R.2 custom-axis/structure mass task remains blocked by absent controlled mass evidence, so this run moved to the independent exact-propulsion operating-envelope prework already listed as a next candidate.

## Controlling metrics

- Requirements planned-domain/schema structure: **12/12 = 100%**.
- G1 SYSTEM FREEZE value closure: **15/48 PASS = 31.3%**.
- Backlog tasks explicitly DONE: **1/25 = 4.0%**.
- Major product gates closed: **0/8 = 0%**.
- Component-bearing U1 schematic: **0%**.

Counters intentionally remain unchanged. The new manufacturer curve reduces S1R.4 uncertainty but does not select the production motor/propeller or close a G1 value row.

## Tasks attempted and completed

1. Verified PB-08 authority, handoff/autonomy continuity, requirements structure, G1 and backlog counters against repository state.
2. Reconfirmed S1R.2 mass closure cannot be completed safely without populated custom ESC/cooling/enclosure/harness/mount and Quad/Hexa structural/common mass evidence.
3. Retrieved current T-Motor primary-source U8 Lite KV85 data: 12S, 36N42P, 243 g incl. cable, 225 +/- 5 mOhm interphase resistance, 19.1 A / 180 s rating and published 48 V G28x9.2 CF bench curve.
4. Captured representative curve points through the 100% point: 6352 g thrust, 16.5 A DC, 3200 rpm and 792 W.
5. Derived 42 poles = 21 pole pairs; 3200 rpm therefore equals 67,200 eRPM and 1,120 Hz electrical fundamental.
6. Explicitly separated the G28x9.2 operating-curve identity from prior NS28x9.2 mass evidence rather than treating them as the same propeller.
7. Added `PB08_U8LITE_KV85_OPERATING_CURVE_ERPM_EVIDENCE.md`, run trace TR-062, and advanced autonomy state to AUTO-STATE-60.

## Files changed

- `ESC_V2/planning/PB08_U8LITE_KV85_OPERATING_CURVE_ERPM_EVIDENCE.md` — new primary-source operating-curve/eRPM evidence.
- `ESC_V2/planning/RUN_2026-09-20_0522_TRACEABILITY.md` — TR-062 run trace.
- `ESC_V2/planning/autonomy_state.json` — AUTO-STATE-60.
- `ESC_V2/planning/AUTONOMOUS_HANDOFF.md` — this record.

No A2/B1 electrical source, KiCad schematic, PCB, Gerber, manufacturing package or release package was modified. `U1-SCH-R001` remains unallocated.

## Engineering decisions made

No product component or rotor topology was selected. The only disposition is that current T-Motor U8 Lite KV85 data is now a controlled PB-08 operating-envelope anchor. The G28x9.2 curve may bound candidate electrical speed and DC input behavior, but it may not be silently applied to NS28x9.2 or used as phase-current/PWM proof.

## Calculations/evidence added

- pole pairs = `42 / 2 = 21`.
- maximum published curve electrical speed = `3200 rpm * 21 = 67,200 eRPM`.
- electrical fundamental = `67,200 / 60 = 1,120 Hz`.
- Published 100% G28x9.2 point: 6352 g thrust, 16.5 A DC input, 3200 rpm, 792 W.
- Published KV85 motor rating: 19.1 A peak for 180 s and 916.8 W max power for 180 s.

Primary source: T-Motor U8 Lite product page, accessed 2026-09-20: `https://store.tmotor.com/product/u8-lite-kv85-u-efficiency.html`.

## Assumptions introduced and evidence level

No new product-value assumption. The eRPM/fundamental values are deterministic calculations from manufacturer pole count and RPM. Manufacturer bench data is sizing/trade evidence only. It is not physical verification of our ESC or UAV. No phase current is inferred from DC input current. No relationship between G28x9.2 and NS28x9.2 is assumed.

## Unresolved blockers

1. Populated custom ESC PCB/power-stage mass.
2. Cooling/baseplate/enclosure installed mass.
3. Local DC/phase harness, connectors and axis mounting hardware mass.
4. Quad-versus-Hexa arm/joint/reinforcement structural/common-system mass delta.
5. Degraded/single-motor-failure policy and supporting thrust/control evidence.
6. Complete 12S pack implementation mass, sag, BMS, fuse/disconnect and enclosure.
7. Exact production motor/propeller identity and selected operating point.
8. Exact motor winding inductance/effective ripple inductance for phase-current/PWM closure.
9. B1 power-stage requalification still requires phase-current/PWM/loss and <=75 V repetitive switching-stress proof.
10. G2 remains blocked by G1; component-bearing U1 allocation remains prohibited.

## Regressions or risks discovered

No repository regression. A data-identity risk was found and contained: the current detailed T-Motor KV85 bench curve is labeled G28x9.2 CF, while prior PB-08 exact-pair mass evidence references NS28x9.2. Treating those propeller names as interchangeable would create false exact-pair evidence. The new artifact explicitly prohibits that inference.

## Exact next recommended tasks

1. Continue S1R.2 with controlled custom ESC/baseplate/enclosure/harness/connector/mount mass evidence and Quad/Hexa structural delta.
2. If mass evidence remains unavailable, continue S1R.3B exact 12S pack hardware mass/sag/BMS/fuse/disconnect closure.
3. After rotor/MTOW closure, map required hover/max thrust onto an exact production motor/prop curve; keep G28 and NS28 identities separate.
4. Obtain exact selected motor winding inductance or execute the controlled impedance measurement procedure before PWM freeze.
5. Then derive phase-current/PWM/loss and re-run B1/U1 power-stage requalification.

Dependency chain:

`PB-08 common platform -> exact installed-axis + structural/common mass -> Quad/Hexa -> payload/MTOW -> exact motor/prop + pack -> phase current/eRPM/PWM -> B1/U1 power-stage requalification -> G1 -> G2 -> U1-SCH-R001`

## Next-run briefing

Start from PB-08 and AUTO-STATE-60. Primary critical path is still S1R.2 installed-axis/structural mass closure. If that evidence remains unavailable, pack closure is the best independent path. TR-062 now provides a useful U8 Lite KV85 timing anchor: the manufacturer's G28x9.2 curve reaches 3200 rpm; with 42 poles this is 67.2 keRPM / 1.12 kHz electrical. Do not freeze PWM or phase current from this alone, and do not merge G28x9.2 operating data with NS28x9.2 mass evidence without exact identity/compatibility proof. Preserve A2/B1 and do not allocate U1 or release manufacturing data.

Mandatory snapshot: **Requirements structure 100% / G1 SYSTEM FREEZE 31.3% / Backlog DONE 4.0% / Major gates 0% / component-bearing U1 schematic 0%**.
