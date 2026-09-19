# ESC autonomous handoff

Date: 2026-09-19 15:03+03:00
Branch: `uav-rebaseline`
Status: `PROGRESS_SENSE_MODELS_PRELIM_BOM_AND_HIGH_VOLTAGE_DRIVER_AUX_TRADE`
Repository HEAD immediately before this handoff update: `ad87e83a768452273d9b1f2800c64ff6ad8d2158`.

## Run summary
This run verified the planning state against the real branch, closed the LT6017-study output-to-STM32 sequencing ambiguity, added mandatory-input dynamic sensing and MOSFET loss screening tools, created/deepened the first explicit U1 preliminary BOM candidate matrix, and completed a primary-source higher-voltage gate-driver / auxiliary-supply architecture trade. No vehicle-dependent G0/G1 value, semiconductor class, driver, auxiliary converter, sensing MPN, production BOM item or PCB implementation was frozen.

## Tasks attempted / completed
1. Re-read and verified the latest handoff, autonomy state, `UAV_PRODUCT_PLAN.md`, `uav_backlog.json`, `mission_requirements.json` and `UAV_TRACEABILITY.md` against `uav-rebaseline`.
2. Confirmed G0/G1 remain OPEN; vehicle mass/mission/environment/failure fields remain legitimately null and were not inferred from competitor aircraft.
3. Verified B1 `V_BUS_ADC` maps to U1701 package pin 8 and ST primary pin data maps STM32G474 LQFP64 pin 8 to PA0 / TT_a / ADC12_IN1.
4. Added `HV_SENSE_OUTPUT_SEQUENCING.md` with four explicit power-sequencing states. LT6017-ON / STM32 VDD/VDDA-OFF is prohibited as a normal study state unless separately proven; preferred study rule is a shared controlled analog shutdown domain.
5. Added `hv_sense_dynamic_model.py`; divider RC, op-amp first-order/slew settling and ADC acquisition RC are calculated only from explicit caller inputs.
6. Added `power_stage_loss_calculator.py`; conduction, linear transition overlap and optional Coss/Qrr screening are calculated only from explicit caller inputs.
7. Created `U1_BOM_CANDIDATES.json` and then deepened it. It distinguishes `LEGACY_REFERENCE`, `CANDIDATE`, `REVALIDATE`, `BLOCKED_BY_G1`, `OPEN` and `REPLACE_IF_REQUIRED` rather than claiming a production BOM.
8. Added `GATE_DRIVER_AUX_SUPPLY_VOLTAGE_DOMAIN_TRADE.md` using current primary manufacturer evidence.
9. Recorded gate-driver architecture anchors: legacy DRV8353 REVALIDATE; UCC27282 as a 120 V-bootstrap reference but **not** proof of >100 V normal HS operation; UCC27712 as a high-voltage non-isolated half-bridge candidate; UCC21540-Q1 as a reinforced-isolated candidate.
10. Recorded auxiliary-power anchors: legacy LM5164 REVALIDATE; LTC3639 as a 4–150 V / up-to-100 mA housekeeping candidate; LTC7801 as a 4–140 V operating / 150 V absolute-maximum synchronous buck-controller candidate for a higher-current rail.
11. Updated `U1_BOM_CANDIDATES.json` with those gate-driver and auxiliary-power candidates while keeping G1-dependent DC-link, shunt, fuse, precharge, clamp and connectors OPEN/BLOCKED.
12. Updated `UAV_TRACEABILITY.md` and `autonomy_state.json` to match the actual repository changes.

## Files changed
- `planning/HV_SENSE_OUTPUT_SEQUENCING.md` — new
- `planning/hv_sense_dynamic_model.py` — new
- `planning/power_stage_loss_calculator.py` — new
- `planning/U1_BOM_CANDIDATES.json` — new and then deepened
- `planning/GATE_DRIVER_AUX_SUPPLY_VOLTAGE_DOMAIN_TRADE.md` — new
- `planning/UAV_TRACEABILITY.md` — updated
- `planning/autonomy_state.json` — updated to AUTO-STATE-18
- `planning/AUTONOMOUS_HANDOFF.md` — updated

## Engineering decisions / findings
- Robust powered-down amplifier input behavior does not prove that an actively driven amplifier output is safe when the MCU analog supply is absent.
- Present LT6017 study rule: buffer and STM32 analog domain share controlled shutdown; do not intentionally allow buffer-ON / MCU-OFF operation without separate manufacturer-backed isolation/current-limiting proof.
- UCC27282's 120 V bootstrap absolute-maximum headline must not be misread as a >100 V normal switch-node solution; TI still specifies a 100 V HS operating ceiling.
- UCC27712 provides a credible non-isolated higher-voltage driver path, but requires three half-bridge channels and separate sensing/protection architecture.
- UCC21540-Q1 provides a credible reinforced-isolated path, but adds isolated/local bias, propagation/skew, creepage/CMTI, area and cost requirements.
- LTC3639 is a credible 150 V low-current housekeeping path, not a direct high-current replacement for the complete legacy auxiliary tree if fan/gate/control loads exceed its 100 mA class.
- LTC7801 is a credible higher-power high-voltage-controller path, but output-current capability is a complete converter-design result, not a controller headline rating.
- Higher-VDS MOSFETs cannot be paired with unchanged ~100 V support ICs by default; the support-domain architecture must follow the final G1 transient envelope.
- `U1_BOM_CANDIDATES.json` is now the explicit bridge toward a final BOM, but it intentionally preserves unresolved items as null/OPEN.

## Calculations / evidence added
- Exact sensing sequencing/fault-state classification for S1–S4.
- Parametric divider/op-amp/ADC dynamic-settling model with no hidden product values.
- Parametric common-condition MOSFET-loss screening framework with no hidden VBUS/current/PWM assumptions.
- Source-backed gate-driver and auxiliary-power voltage-domain architecture alternatives.
- Candidate-BOM dependency/status map identifying which parts are source-backed candidates versus G1-blocked/open functions.

## Primary evidence
- ST STM32G474 DS12288 and STM32G474RE product documentation.
- Analog Devices LT6015/LT6016/LT6017 datasheet and powered-down high-input-impedance technical note.
- TI UCC27282/UCC27282-Q1 product and datasheet documentation.
- TI UCC27712/UCC27712-Q1 product and datasheet documentation.
- TI UCC21540-Q1 product and datasheet documentation.
- ADI LTC3639 product/datasheet documentation.
- ADI LTC7801 product/datasheet documentation.
- Existing repository B1 source/BOM/traceability evidence.

## Assumptions and evidence level
- STM32 PA0 / TT_a mapping: REPOSITORY + PRIMARY ST EVIDENCE.
- LT6015-family powered-down input behavior: PRIMARY ADI EVIDENCE.
- Shared LT6017 + STM32 analog shutdown domain: ARCHITECTURE STUDY RULE, not final selection.
- UCC27282/UCC27712/UCC21540-Q1 and LTC3639/LTC7801: PRIMARY-SOURCE TRADE CANDIDATES, not selections.
- Dynamic calculation scripts: FIRST-ORDER SCREENING TOOLS, not SPICE/bench or qualification evidence.
- Preliminary U1 BOM: CANDIDATE/DEPENDENCY MATRIX ONLY.
- No physical measurements were performed.

## Unresolved blockers
- G0 nominal payload, airframe/battery/equipment mass, actual MTOW, mission duration/profile, environment and degraded/single-motor-failure policy.
- Final rotor architecture/thrust margin and product motor/prop operating point.
- Motor pole pairs, phase RMS/peak current, eRPM and final PWM envelope.
- Battery min/nom/full-charge/transient envelope and pack current/energy/sag/disconnect behavior.
- Final switching/harness/regen/BMS-disconnect transient ceiling.
- Final MOSFET voltage class/parallel count/hot-loss/SOA/cooling.
- Final gate-driver architecture and required gate-current/timing/fault coverage.
- Final auxiliary load budget and converter topology.
- Final sensing range/error/bandwidth/series impedance and powered/unpowered bench proof.
- Exact DC-link capacitors, precharge, fuse, regen clamp/brake path, connectors and production BOM.

## Regressions / risks discovered
- No repository regression identified in this run.
- A higher-VDS MOSFET choice alone does not solve support-IC voltage-domain limitations.
- Bootstrap absolute-maximum voltage can be materially different from the normal switch-node operating limit; those values must not be conflated.
- Isolated gate drivers can solve level-shift voltage-domain issues while introducing isolated-bias and CMTI/creepage/timing complexity.
- The simplified loss and sensing models can create false precision if caller inputs are guessed; therefore they require explicit inputs and label outputs as screening-only.
- Preliminary BOM candidates must not be interpreted as orderable production BOM completeness.

## Exact next recommended tasks
1. Inventory the existing B1 auxiliary loads and power domains from repository evidence, producing a bounded legacy load budget without promoting it to a U1 requirement.
2. Begin a primary-source STM32G474 vs TMS320F280041C control-platform pretrade focused on PWM/ADC synchronization, hardware trip, CAN, processing/motor-control resources and toolchain, without selecting a winner before G1/G2.
3. Add placeholder-only input templates for `hv_sense_dynamic_model.py` and `power_stage_loss_calculator.py`; no numeric product defaults.
4. Deepen the candidate BOM only where exact MPN/footprint evidence is independent of unresolved G1 ratings.
5. Keep all vehicle-dependent G0/G1 fields OPEN until actual product inputs are supplied or explicitly approved.

## Dependency chain
`G0 vehicle inputs -> G1A rotor selection -> G1B product operating point + motor electrical data -> G1C battery/transient envelope -> G1 SYSTEM FREEZE -> G2 architecture freeze -> G3 U1 schematic -> U1 production BOM/PCB/firmware -> physical validation`

## Next-run briefing
Do not repeat the sensing sequencing or generic gate-driver voltage search. Start by extracting the B1 auxiliary load/domain budget from repository evidence, then begin the STM32G474 vs TMS320F280041C primary-source control-platform pretrade. Use the new driver/aux candidates only as trade anchors; do not select them until G1 transient, gate-charge/PWM and auxiliary load requirements close. Preserve all vehicle-dependent fields as OPEN/null.
