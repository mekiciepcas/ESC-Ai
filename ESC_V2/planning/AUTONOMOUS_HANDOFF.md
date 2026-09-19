# ESC autonomous handoff

Date: 2026-09-19 15:25+03:00  
Branch: `uav-rebaseline`  
Status: `PROGRESS_CONTROL_AUX_REQUIREMENTS_AND_RESULT_SCHEMAS`  
Repository HEAD immediately before this handoff update: `42b679bb0a2aac9741e9e97f07ec6cec4b0eebdb`.

## Progress percentages

- Requirements planned-domain/schema structure: **12/12 = 100%**.
- G1 SYSTEM FREEZE value closure: **1/46 PASS = 2.2%**.
- Backlog tasks explicitly DONE: **1/25 = 4%**.
- Major product gates closed: **0/8 = 0%**.

These conservative percentages did not change in this run because all new work is safe architecture/verification prework and no open G0/G1 product value was fabricated or promoted to frozen status.

## Run summary

This integrated run verified the current branch planning authorities, then completed the planned B1 auxiliary-load/power-domain inventory and STM32G474-vs-TMS320F280041C control-platform pretrade. The auxiliary work now distinguishes regulator source capability from actual load demand and identifies the unclosed gate-drive, fan, Hall/interface, MCU and analog-domain loads. The control pretrade now compares exact manufacturer-backed MCU anchors without selecting a winner. A common CPB-01..12 bench contract and null-only machine-readable result template define how later evidence must be collected. New control/auxiliary derived requirements are linked into the existing 12-domain requirements authority, and a mandatory-input auxiliary power budget model was added so open U1 loads cannot be silently replaced by guessed values.

## Tasks attempted / completed

1. Re-read and verified `AUTONOMOUS_HANDOFF.md`, `autonomy_state.json`, `UAV_PRODUCT_PLAN.md`, `UAV_TRACEABILITY.md`, `uav_backlog.json`, `mission_requirements.json`, `REQUIREMENTS_MASTER.json` and `REQUIREMENTS_PROGRESS.json` against `uav-rebaseline`.
2. Traced B1 auxiliary source/load domains from actual KiCad/connection-manifest evidence.
3. Added `B1_AUXILIARY_LOAD_DOMAIN_INVENTORY.md` and explicitly separated source-device ratings from real rail demand.
4. Recorded the B1 rail chain `VBUS -> LM5164 -> +12V -> TPS62160 -> +5V -> TLV75533 -> +3V3 -> +3V3A` as legacy evidence only.
5. Recorded visible B1 loads: DRV8353 and fan on +12 V; Hall/exported interface and downstream logic on +5 V; STM32/CAN/fault logic on +3V3; comparator/reference/sensing functions on +3V3A.
6. Preserved B1 fan `<=0.2 A` only as a legacy starting budget; fan inrush and U1 fan demand remain OPEN.
7. Derived the three visible passive trip-reference divider currents at nominal 3.3 V: approximately 91.4 uA + 91.4 uA + 188.6 uA = **0.371 mA subtotal**. This is not the total +3V3A rail load.
8. Added `CONTROL_PLATFORM_PRETRADE.md` comparing current primary-source evidence for STM32G474RE/RET3 and TMS320F280041C/F280041CPMS without selecting an MCU.
9. Corrected a potential family-level hallucination: exact TMS320F280041C evidence shows one C28 CPU and does not list a CLA; CLA features from other F28004x variants shall not be attributed to this candidate.
10. Verified/created `CONTROL_PLATFORM_BENCH_CONTRACT.md` with CPB-01..12 common measurements for both candidates.
11. Added `CONTROL_PLATFORM_BENCH_RESULTS.template.json` with all measurement/result fields intentionally null / NOT_RUN.
12. Added `CONTROL_AUX_DERIVED_REQUIREMENTS.json` mapping PWR/CTRL/SAF/IF requirements without freezing any numeric values.
13. Updated `REQUIREMENTS_MASTER.json` to link the new child authority into PWR, CTRL, SAF and IF domains; structural progress remains 100% and G1 closure remains 2.2%.
14. Added `auxiliary_power_budget_model.py` and `auxiliary_power_budget_input.template.json`; all product numbers are mandatory caller inputs and the template values are intentionally null.
15. Verified traceability now records auxiliary load-budget and MCU benchmark acceptance work (TR-034/TR-035).
16. Updated `autonomy_state.json` to AUTO-STATE-21 and reconciled the handoff with actual branch artifacts.

## Files changed / added across the integrated run

- `planning/B1_AUXILIARY_LOAD_DOMAIN_INVENTORY.md` — new legacy B1 auxiliary-domain evidence inventory.
- `planning/CONTROL_PLATFORM_PRETRADE.md` — new primary-source MCU pretrade.
- `planning/CONTROL_PLATFORM_BENCH_CONTRACT.md` — common CPB-01..12 benchmark contract.
- `planning/CONTROL_PLATFORM_BENCH_RESULTS.template.json` — new null-only machine-readable evidence template.
- `planning/CONTROL_AUX_DERIVED_REQUIREMENTS.json` — new child requirement authority.
- `planning/auxiliary_power_budget_model.py` — new mandatory-input screening calculator.
- `planning/auxiliary_power_budget_input.template.json` — new null-only input template.
- `planning/REQUIREMENTS_MASTER.json` — updated authority references / child authority linkage.
- `planning/UAV_TRACEABILITY.md` — linked auxiliary inventory and control benchmark prework; TR-034/TR-035 present.
- `planning/autonomy_state.json` — updated to AUTO-STATE-21.
- `planning/AUTONOMOUS_HANDOFF.md` — updated and reconciled.

## Engineering decisions / findings

- No MCU selected. STM32G474 has B1 reuse value; TMS320F280041C has motor-control-centric ePWM/CMPSS/PPB/TMU/CLB/InstaSPIN resources. These remain trade factors, not a winner declaration.
- CPU MHz, ADC count or a vendor motor-control library alone is prohibited as the MCU selection rule. Both candidates require the same representative control workload and traceable timing/safety evidence.
- Exact TMS320F280041C shall not be credited with a CLA unless exact-device primary evidence changes.
- Fault-to-PWM-inactive latency must be physically measured and compared with the final semiconductor safe-action budget before propulsion release.
- Regulator headline current ratings are source capabilities, not rail demand. LM5164/TPS62160/TLV755 ratings cannot close U1 auxiliary sizing.
- U1 auxiliary converter selection remains blocked by the final VBUS transient envelope and an evidenced U1 load budget.
- External fan, Hall and exported interface power must become bounded interface contracts rather than implicit board loads.
- The existing B1 +3V3/+3V3A sequencing/backfeed concern remains relevant to any U1 auxiliary architecture.

## Calculations / evidence added

- B1 passive trip-reference subtotal at 3.3 V: approximately **0.371 mA** from the three visible divider chains only.
- A generic auxiliary-power budget model now sums caller-supplied rail loads, applies explicit design margin and optionally screens first-order gate-charge power using caller-supplied Qg, gate voltage, PWM frequency, device/event count and switching-event count.
- No efficiency, load, Qg, PWM or U1 rail value is embedded as a hidden product default.
- CPB-01..12 evidence schema records exact MCU/package, board revision, toolchain/compiler settings, clock/PWM/ADC/CAN configuration, firmware SHA, equipment/sample count, timing distributions, anomalies and raw-data references.

## Primary evidence used

Repository evidence:
- `hardware_b1/08_AUX_12V.kicad_sch`
- `hardware_b1/09_AUX_LOGIC.kicad_sch`
- `hardware_b1/connection_manifest.json`
- `hardware_b1/mcu_pin_contract.json`

Manufacturer evidence:
- ST STM32G474RE: https://www.st.com/en/microcontrollers-microprocessors/stm32g474re.html
- TI TMS320F280041C: https://www.ti.com/product/TMS320F280041C
- TI exact 64-pin anchor F280041CPMS: https://www.ti.com/product/TMS320F280041C/part-details/F280041CPMS
- TI LM5164: https://www.ti.com/product/LM5164
- TI TPS62160DGKR: https://www.ti.com/product/TPS62160/part-details/TPS62160DGKR
- TI TLV755P: https://www.ti.com/product/TLV755P

## Assumptions and evidence level

- 70–100 kg remains USER TARGET payload, not MTOW.
- B1 auxiliary topology and visible loads: LEGACY REPOSITORY SOURCE EVIDENCE.
- Converter maximum output ratings: PRIMARY MANUFACTURER EVIDENCE and explicitly not load requirements.
- Passive-divider 0.371 mA subtotal: DERIVED CALCULATION from B1 resistor values at nominal 3.3 V.
- STM32/TMS device features: PRIMARY MANUFACTURER EVIDENCE.
- Control-platform architectural implications: ENGINEERING TRADE JUDGMENT.
- Auxiliary-power calculator and CPB schema: SCREENING/VERIFICATION TOOLING, not physical validation.
- No physical bench, dyno, flight, thermal or EMI measurement was performed.

## Unresolved blockers

- G0 nominal payload, airframe/battery/equipment mass, actual MTOW, mission duration/profile, environment and degraded/single-motor-failure policy.
- Final rotor architecture/thrust margin and product motor/prop operating point.
- Motor pole pairs, phase RMS/peak current, eRPM and final PWM envelope.
- Battery series/min/nom/full-charge/transient envelope and pack current/energy/sag/disconnect behavior.
- Final switching/harness/regen/BMS-disconnect transient ceiling.
- Final MOSFET class/count/hot-loss/SOA/cooling and gate-driver architecture.
- U1 auxiliary steady/inrush/transient loads, especially gate-drive dynamic power, fan inrush, Hall/exported-interface demand and MCU/analog dynamic load.
- MCU selection: frozen PWM/ADC workload, fault-latency budget, CAN contract and actual CPB result data.
- Final sensing range/error/bandwidth/series impedance and powered/unpowered bench proof.
- Exact DC-link capacitors, shunt, fuse, precharge, regen clamp, connectors and production BOM.
- Physical bench/dyno/flight evidence.

## Regressions / risks discovered

- No repository regression identified.
- CPB contract/template completion is not benchmark-result completion; every CPB result is currently NOT_RUN/null.
- B1 fan <=0.2 A must not become the UAV fan requirement without vehicle cooling evidence.
- A source device rated for 1 A or 500 mA can still fail thermally or transiently at a much lower real load; converter selection needs the actual rail and environment budget.
- Exact MCU package/pin-mux and trigger routing can invalidate family-level peripheral assumptions.
- Auxiliary-power screening can create false precision if caller inputs are guessed; null template fields are intentional blockers, not missing data to auto-fill.

## Exact next recommended tasks

1. Audit remaining critical B1 legacy decisions for traceability gaps that can be closed without G1 values, especially fault latch/PWM inhibit, CAN physical layer, temperature sensing and board-interface power/fault semantics.
2. Deepen `U1_BOM_CANDIDATES.json` only for exact support components whose selection/evidence is independent of unresolved G1 voltage/current/thermal ratings.
3. Define a machine-readable external auxiliary interface contract for fan, Hall supply and exported auxiliary power with voltage/current/inrush fields left OPEN until vehicle inputs exist.
4. When hardware/evaluation boards are available, populate separate CPB result files from the template; do not infer one candidate's measurements from the other.
5. Keep G0/G1 product values OPEN until actual vehicle inputs are supplied or explicitly approved.

## Dependency chain

`G0 vehicle inputs -> G1A rotor selection -> G1B operating point -> G1C battery/transient -> G1 SYSTEM FREEZE -> G2 architecture freeze -> G3 U1 schematic/BOM -> G4 firmware -> G5 prototype -> G6 propulsion verification -> G7 flight readiness`

## Next-run briefing

Do not redo the B1 auxiliary inventory, MCU source comparison or CPB schema. Start with legacy traceability gaps that are independent of G1, then deepen BOM/support-interface evidence where exact MPNs can be justified without pretending open power ratings are known. Preserve the 100% requirements-structure / 2.2% G1 / 4% backlog conservative metrics unless the controlling repository authorities actually change.
