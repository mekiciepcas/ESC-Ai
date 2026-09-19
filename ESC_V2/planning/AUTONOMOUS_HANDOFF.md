# ESC autonomous handoff

Date: 2026-09-19 15:22+03:00  
Branch: `uav-rebaseline`  
Status: `PROGRESS_AUX_INVENTORY_AND_CONTROL_BENCH_CONTRACT_COMPLETE`  
Repository branch tree observed at start of run: `d090db87a818e7ff342faa747f3ab052e52a4cc3`. Latest known content commit before this handoff write: `1b7d995a37db0cc4326bdb8273d495714b04e4c6`.

## Progress percentages

- Requirements planned-domain/schema structure: **12/12 = 100%**.
- G1 SYSTEM FREEZE value closure: **1/46 PASS = 2.2%**.
- Backlog tasks explicitly DONE: **1/25 = 4%**.
- Major product gates closed: **0/8 = 0%**.

The percentages did not change because this run deliberately completed safe G2 prework without fabricating or promoting any still-open G0/G1 product value. Engineering evidence depth increased even though the conservative gate/backlog counters remain unchanged.

## Run summary

The run verified the actual `uav-rebaseline` tree and re-read the current autonomy state, handoff, product plan, mission requirements, requirements master/progress, backlog and traceability authorities. The previously targeted B1 auxiliary-load inventory and STM32G474-vs-TMS320F280041C pretrade are now present in the branch and were checked for scope discipline. The main new engineering output is a common executable control-platform bench contract (`CONTROL_PLATFORM_BENCH_CONTRACT.md`) defining CPB-01..12 measurements for both MCU candidates without inventing timing results or selecting a winner. Traceability now contains explicit auxiliary-load-budget and MCU-benchmark rows.

## Tasks attempted / completed

1. Verified repository branch/tree and required planning authorities against `uav-rebaseline`.
2. Verified `B1_AUXILIARY_LOAD_DOMAIN_INVENTORY.md`: B1 rail tree and visible consumers are inventoried, source current ratings are explicitly not treated as U1 loads, and unknown fan/gate/Hall/interface/MCU/analog loads remain OPEN.
3. Verified `CONTROL_PLATFORM_PRETRADE.md`: exact STM32G474 and TMS320F280041C candidate evidence is compared without selecting an MCU.
4. Created `CONTROL_PLATFORM_BENCH_CONTRACT.md` with a common logical workload and CPB-01..12 measurement contract covering reset-safe PWM, complementary PWM, PWM/ADC synchronization, acquisition skew, hardware fault latency, FOC execution, ISR jitter, CAN load, memory footprint, watchdog/reset, brownout and exact 64-pin pin mux.
5. Added derived CTRL/SAF/IF bench requirements while keeping numeric limits dependent on frozen parent requirements.
6. Updated `UAV_TRACEABILITY.md`: TR-011/TR-012/TR-020/TR-028 now point to the new evidence; TR-034 records auxiliary load-budget status and TR-035 records MCU benchmark acceptance status.
7. Updated `autonomy_state.json` to AUTO-STATE-20.

## Files changed

- `planning/CONTROL_PLATFORM_BENCH_CONTRACT.md` — new common executable MCU comparison/acceptance contract.
- `planning/UAV_TRACEABILITY.md` — linked auxiliary inventory and MCU pretrade/bench evidence; added TR-034 and TR-035.
- `planning/autonomy_state.json` — AUTO-STATE-20 with completed work, blockers and next candidates.
- `planning/AUTONOMOUS_HANDOFF.md` — this continuity record.

Verified existing evidence used this run:
- `planning/B1_AUXILIARY_LOAD_DOMAIN_INVENTORY.md`
- `planning/CONTROL_PLATFORM_PRETRADE.md`
- `planning/REQUIREMENTS_MASTER.json`
- `planning/REQUIREMENTS_PROGRESS.json`
- `planning/UAV_PRODUCT_PLAN.md`
- `planning/mission_requirements.json`
- `planning/uav_backlog.json`

## Engineering decisions made

- No MCU selected. STM32 B1 reuse and TI motor-control integration remain trade factors only.
- The MCU decision must use the same representative workload and traceable timing/safety evidence on both surviving candidates; CPU MHz alone is explicitly insufficient.
- Fault-to-PWM-inactive latency must eventually be physically measured and compared with the final semiconductor safe-action budget.
- FOC execution margin must be calculated from measured worst-case execution time and the frozen control/PWM period; no runtime number was invented.
- Existing B1 regulator headline ratings remain source capabilities, not U1 load requirements.
- Exact U1 auxiliary converter selection remains blocked by final VBUS transient plus a real U1 load budget.

## Calculations / evidence added

No new physical measurement was claimed. The new evidence is a reproducible measurement contract rather than fabricated timing values.

The verified B1 auxiliary inventory carries one bounded arithmetic result: the three visible passive trip-reference divider currents total approximately 0.371 mA at 3.3 V. This is only a passive-divider subtotal and is not promoted to total +3V3A demand.

The control benchmark now defines evidence records for exact MCU/package, board revision, toolchain, compiler flags, clock tree, PWM/ADC setup, firmware SHA, measurement equipment/sample count, timing statistics and anomalies. This closes a process/evidence gap without closing the MCU selection itself.

## Assumptions and evidence level

- 70–100 kg remains USER TARGET payload, not MTOW.
- B1 auxiliary topology/load visibility is LEGACY REPOSITORY EVIDENCE, not a U1 requirement.
- STM32G474 and TMS320F280041C family/device capabilities in the pretrade are PRIMARY MANUFACTURER EVIDENCE; final execution margin is not yet evidence-backed.
- CPB-01..12 are DEFINED VERIFICATION REQUIREMENTS / PREWORK. Numeric thresholds that depend on PWM, semiconductor protection, sensing or FC protocol remain OPEN.
- No physical bench, dyno, flight, thermal or EMI result was introduced.

## Unresolved blockers

- G0 nominal payload, airframe/battery/equipment mass, MTOW, mission duration/profile, environment and degraded/single-motor-failure policy.
- Final rotor architecture/thrust margin and selected motor/prop operating point.
- Motor pole pairs, phase RMS/peak current, eRPM and final PWM envelope.
- Battery series/min/nom/full-charge/transient envelope, current, usable energy, sag and disconnect behavior.
- Final switching/harness/regen/BMS-disconnect transient ceiling.
- Final semiconductor class/count, gate driver, auxiliary converter, sensing topology and thermal architecture.
- U1 auxiliary loads: gate-drive dynamic power, fan inrush, Hall/interface loads, MCU/control dynamic load and analog rail sequencing/fault load.
- MCU freeze: final PWM/ADC workload, hardware-fault latency budget, CAN contract and executable candidate benchmark evidence.
- Exact DC-link capacitors, shunt, fuse, precharge, regen clamp, connectors and production BOM.
- Physical bench/dyno/flight evidence.

## Regressions / risks discovered

- No repository regression identified.
- Benchmark-contract completion must not be mistaken for benchmark-result completion; no CPB timing measurement exists yet.
- B1 fan <=0.2 A remains a legacy starting budget only; fan inrush is explicitly unmeasured.
- A regulator maximum-current rating cannot substitute for rail demand. Doing so would conceal startup/transient and thermal risk.
- MCU family peripheral counts cannot substitute for exact package pin-mux and trigger-routing proof.

## Exact next recommended tasks

1. Audit remaining critical B1 legacy decisions for traceability gaps that can be closed without G1 values.
2. Add a machine-readable empty CPB result schema/template so future STM32/TI measurements cannot omit toolchain, exact part, timing distribution or evidence class; leave measurement fields null.
3. Deepen `U1_BOM_CANDIDATES.json` only for support components whose exact selection is independent of unresolved G1 ratings.
4. Map any newly derived requirements into the existing 12-domain authority without altering OPEN product values.
5. Keep G0/G1 values OPEN until vehicle-specific inputs are supplied or explicitly approved.

## Dependency chain

`G0 vehicle inputs -> G1A rotor selection -> G1B operating point -> G1C battery/transient -> G1 SYSTEM FREEZE -> G2 architecture freeze -> G3 U1 schematic/BOM -> G4 firmware -> G5 prototype -> G6 propulsion verification -> G7 flight readiness`

## Next-run briefing

Do not redo the auxiliary inventory or source-level MCU comparison. They are now usable prework. The next safe action is to make the CPB evidence format machine-readable with null measurement fields, then continue traceability/BOM support-part work that does not depend on open G1 ratings. Do not claim MCU selection or benchmark performance. Report requirements structure %, G1 value closure %, and backlog DONE % in every user-facing progress output.