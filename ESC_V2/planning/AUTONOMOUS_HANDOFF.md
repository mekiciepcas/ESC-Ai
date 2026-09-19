# ESC autonomous handoff

Date: 2026-09-19 14:58+03:00
Branch: `uav-rebaseline`
Status: `PROGRESS_SENSE_SEQUENCING_DYNAMIC_MODELS_AND_PRELIMINARY_BOM_MATRIX`
Repository HEAD immediately before this handoff update: `756ec5e08817a1db98f5d74bc3d94fae7cb02b15`.

## Run summary
This run first re-verified the latest planning state against the branch and then completed three previously queued independent engineering tasks: LT6017-study output-to-STM32 power sequencing, a no-default dynamic HV-sense/ADC settling model, and a no-default condition-normalized MOSFET loss calculator skeleton. It then used the now-structured evidence to create the first explicit U1 preliminary BOM candidate matrix. No product voltage/current rating, voltage class, sensing MPN, final BOM item, PCB implementation or qualification claim was frozen.

## Tasks attempted / completed
1. Re-read/verified the latest `AUTONOMOUS_HANDOFF.md`, `autonomy_state.json`, `UAV_PRODUCT_PLAN.md`, `uav_backlog.json`, `mission_requirements.json` and `UAV_TRACEABILITY.md` against `uav-rebaseline`.
2. Verified current branch state before work: the product remains in G0/G1 with G2 prework only; G0 vehicle-specific mass/mission/environment/failure fields remain legitimately OPEN/null.
3. Verified repository `hardware_b1/mcu_pin_contract.json` maps `V_BUS_ADC` to U1701 package pin 8.
4. Verified ST primary pin data maps STM32G474 LQFP64 pin 8 to PA0, `TT_a`, ADC12_IN1.
5. Verified ST absolute/input-injection guidance: TT_xx input absolute ceiling is 4.0 V; normal operation must not rely on out-of-rail injection and MCU supplies are required in their permitted ranges.
6. Re-checked ADI LT6015/LT6016/LT6017 primary evidence: powered-down inputs remain high impedance; `VS=0, VCM=0..76 V` behavior is characterized; output shutdown tolerance is not a defined ADC output state.
7. Added `HV_SENSE_OUTPUT_SEQUENCING.md` with explicit S1–S4 states.
8. Classified LT6017-ON / STM32-VDDA-OFF as **not permitted as a normal study state** unless separately proven. Preferred study rule: LT6017 and STM32 analog domain share controlled shutdown; no independent always-on buffer rail.
9. Added `hv_sense_dynamic_model.py`. It requires caller-supplied divider, RC, op-amp, ADC, sample-time, resolution and target-settling inputs; no product defaults are embedded.
10. Added `power_stage_loss_calculator.py`. It requires caller-supplied VBUS, switch RMS/commutation current, effective switching rate, hot RDS(on), transition times, Coss, Qrr, parallel count and sharing factor; no ESC rating/current/PWM is assumed.
11. Updated `UAV_TRACEABILITY.md` to link the new sensing sequencing and normalized loss evidence.
12. Added `U1_BOM_CANDIDATES.json`, separating exact evidence-backed candidate/reference items from G1-blocked/open items instead of pretending a production BOM exists.
13. Updated `autonomy_state.json`.

## Files changed
- `planning/HV_SENSE_OUTPUT_SEQUENCING.md` — new
- `planning/hv_sense_dynamic_model.py` — new
- `planning/power_stage_loss_calculator.py` — new
- `planning/U1_BOM_CANDIDATES.json` — new
- `planning/UAV_TRACEABILITY.md` — updated
- `planning/autonomy_state.json` — updated
- `planning/AUTONOMOUS_HANDOFF.md` — updated

## Engineering decisions / findings
- A robust powered-down **input** does not automatically make the amplifier **output-to-unpowered-MCU** connection safe.
- Current U1 study rule: do not intentionally power the LT6017 analog output stage while STM32 VDD/VDDA is absent. Use a shared controlled analog shutdown domain unless a future architecture proves a different state with manufacturer evidence and current limiting.
- B1 `V_BUS_ADC` is PA0 / TT_a in the current STM32G474RET3 mapping; ST's limits must be applied to that exact pin structure rather than a generic GPIO assumption.
- Buffer OFF / MCU ON is an invalid-measurement state until the buffer rail is valid; firmware must gate use of those samples.
- Buffer OFF / MCU OFF with HV input live is the key LT6015-family robustness state, but final acceptance still requires a current-limited powered/unpowered bench test.
- The dynamic HV-sense and power-stage loss tools deliberately refuse to generate product conclusions from hidden defaults.
- A preliminary U1 BOM matrix now exists. It is not a purchase/release BOM: MOSFET class, shunt, DC-link, precharge, fuse, clamp, connectors and multiple architecture items remain parent-requirement blocked.

## Calculations / evidence added
- Source-backed pin-structure closure for the B1 bus-sense ADC input.
- Four-state sensing power-sequencing logic and acceptance criteria.
- Parametric divider Thevenin RC, op-amp first-order/slew settling and ADC acquisition RC calculation framework.
- Parametric conduction + linear overlap + optional Coss/Qrr screening framework at caller-supplied common conditions.
- Preliminary BOM status taxonomy: `LEGACY_REFERENCE`, `CANDIDATE`, `REVALIDATE`, `BLOCKED_BY_G1`, `OPEN`, `REPLACE_IF_REQUIRED`.

## Primary evidence
- ST STM32G474 DS12288 datasheet: https://www.st.com/resource/en/datasheet/stm32g474ve.pdf
- ST STM32G474RE product page: https://www.st.com/en/microcontrollers-microprocessors/stm32g474re.html
- ADI LT6015/LT6016/LT6017 datasheet: https://www.analog.com/media/en/technical-documentation/data-sheets/601567ff.pdf
- ADI powered-down high-input-impedance article / DN533: https://www.analog.com/en/resources/technical-articles/robust-high-voltage-over-the-top-op-amps-maintain-high-input-impedance-with-inputs-driven-apart-or.html
- Repository B1 MCU contract and existing source-backed semiconductor/BOM audit files.

## Assumptions and evidence level
- PA0 / TT_a mapping: REPOSITORY + PRIMARY ST EVIDENCE.
- LT6015-family powered-down input behavior: PRIMARY ADI EVIDENCE.
- Shared LT6017 + STM32 analog shutdown domain: ARCHITECTURE STUDY RULE, not final schematic selection.
- Dynamic-model formulas: FIRST-ORDER ENGINEERING SCREENING, explicitly not SPICE/bench proof.
- `U1_BOM_CANDIDATES.json`: PRELIMINARY CANDIDATE/DEPENDENCY MATRIX, not production release.
- No physical measurements were performed.

## Unresolved blockers
- G0 nominal payload, airframe/battery/equipment mass, actual MTOW, flight profile, environment and failure/degraded-mode policy.
- Final rotor architecture/thrust margin and product motor/prop operating point.
- Motor pole pairs, phase RMS/peak current, eRPM and final PWM envelope.
- Battery min/nom/full-charge/transient envelope and pack current/energy/sag/disconnect behavior.
- Final VBUS transient ceiling including harness/PCB inductance, switching, regen and BMS/contact behavior.
- Final sensing range/error/bandwidth, output-series impedance, LT6017 selection/package and powered/unpowered bench proof.
- Final semiconductor voltage class/parallel count/hot-loss/SOA/cooling.
- Exact DC-link, precharge, fuse, clamp/brake, connectors/harness and production BOM.

## Regressions / risks discovered
- No repository regression found in this run.
- Treating the STM32 4.0 V absolute input ceiling as proof that a powered buffer may safely drive an unpowered MCU would be unsafe reasoning; the MCU supply/normal-operation conditions remain governing.
- LT6017 shutdown output fault tolerance must not be confused with a guaranteed shutdown output voltage.
- The simplified Coss/Qrr/linear-overlap loss model can create false precision if device data are not normalized to common current, voltage, di/dt and temperature; the script labels itself screening-only.
- Preliminary BOM status must not be interpreted as orderable production BOM completeness.

## Exact next recommended tasks
1. Build a primary-source gate-driver / auxiliary-supply trade for candidate bus domains above the legacy ~100 V component ceiling, so G2 has alternatives if G1 transient ceiling disqualifies DRV8353/LM5164.
2. Deepen `U1_BOM_CANDIDATES.json` only for support parts whose parent function is stable and exact MPN/footprint evidence can be verified without freezing G1-dependent ratings.
3. Add input-template examples for `hv_sense_dynamic_model.py` and `power_stage_loss_calculator.py` that contain field names/placeholders only, not invented product values.
4. Keep G0/G1 product fields OPEN until actual vehicle-specific targets are supplied/approved.

## Dependency chain
`G0 vehicle inputs -> G1A rotor selection -> G1B product operating point + motor electrical data -> G1C battery/transient envelope -> G1 SYSTEM FREEZE -> G2 architecture freeze -> G3 U1 schematic -> U1 production BOM/PCB/firmware -> physical validation`

## Next-run briefing
Do not repeat the LT6017 input/output sequencing work or the generic MOSFET calculator. Start with gate-driver and auxiliary-power alternatives that can survive a bus/transient domain above the legacy 100 V ceiling, using primary manufacturer evidence only and without selecting a winner before G1. In parallel, improve the preliminary U1 BOM matrix only where parent requirements are already stable. Any G0-dependent number remains OPEN/null; competitor values stay trade-only.
