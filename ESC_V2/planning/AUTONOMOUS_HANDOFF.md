# ESC autonomous handoff

Date: 2026-09-19 10:18+03:00  
Branch: `uav-rebaseline`  
Status: `PROGRESS_ADC_CLAMP_REFERENCE_FET_PRECHARGE_REQUIREMENTS_GATE`

## Run summary
This run verified the exact B1 voltage-sense clamp orientation, quantified powered/unpowered rail-injection screening, added STM32G474 primary-source injection constraints, populated the legacy CSD19536KTT reference row from TI primary data, added a no-guesses precharge/disconnect-energy model, and formalized requirements completion at G1 SYSTEM FREEZE. No vehicle mass, rotor architecture, battery architecture, transient ceiling, semiconductor class, protection MPN or release package was frozen.

## Tasks attempted / completed
1. Re-read the prior handoff/state and product-plan gate definitions.
2. Verified B1 source topology: each upper BAT54H has cathode at +3V3A and anode at V_ADC; lower BAT54H has cathode at V_ADC and anode at GND.
3. Recomputed divider ratio = ~0.0321955 and clamp-source Thevenin resistance including 1 kOhm ADC series = ~4.213 kOhm.
4. Screened powered clamp current using 3.6 V only as an illustrative clamp node: ~62 uA at 120 V and ~292 uA at 150 V screening cases.
5. Screened the MCU/3V3A-off hazard: at 75.6 V bus, ideal divider node is ~2.434 V and an illustrative 0.3 V Schottky drop gives ~0.51 mA source-limited current into the dead analog rail. This is not a qualified value.
6. Recorded ST STM32G474 primary-source guidance that normal-operation injection should be avoided and absolute injected-current characterization limits are not design targets.
7. Added `ADC_CLAMP_INJECTION_CLOSURE.md`.
8. Added TI primary-source CSD19536KTT reference parameters: 100 V, 2.4 mOhm max RDS(on) at 10 V, Qg typ 118 nC, Qgd typ 17 nC, package-limited ID 200 A; retained as legacy/reference only.
9. Added `precharge_energy_model.py`, requiring explicit numeric inputs and leaving disconnect analysis OPEN unless current/stray-L are supplied.
10. Added `REQUIREMENTS_COMPLETION_CHECKLIST.md`, defining system requirements as baselined only at G1 after G0/G1A/G1B/G1C closure.
11. Updated machine-readable autonomy state.

## Files changed
- `planning/ADC_CLAMP_INJECTION_CLOSURE.md` — new
- `planning/CSD19536KTT_REFERENCE_PARAMETERS.md` — new
- `planning/precharge_energy_model.py` — new
- `planning/REQUIREMENTS_COMPLETION_CHECKLIST.md` — new
- `planning/autonomy_state.json` — updated
- `planning/AUTONOMOUS_HANDOFF.md` — updated

## Engineering decisions / findings
- B1 source definitively makes the upper BAT54H an ADC-to-+3V3A rail clamp/backfeed path.
- The existing high-value divider strongly limits clamp current, but low current alone does not qualify MCU-off behavior because +3V3A/TLV75533/upstream rails may be unintentionally back-powered.
- STM32 absolute/characterization injection ratings are not accepted as normal-operation design targets.
- CSD19536KTT is useful as a B1 loss anchor but its 100 V VDS remains unresolved for an 18S UAV bus because 75.6 V full charge leaves only 24.4 V static headroom before transient effects.
- Requirements completion is now explicitly gated: G1 SYSTEM FREEZE requires G0 mission/MTOW, G1A rotor, G1B propulsion and G1C battery/current/transient evidence plus a non-null traceable ESC electrical envelope.

## Calculations / evidence added
- Divider ratio and Thevenin resistance.
- Powered/unpowered clamp-current screening.
- ST STM32G474 injection guidance/limits as primary evidence.
- TI CSD19536KTT primary headline parameters.
- Parametric RC precharge time/current/power/energy and optional disconnect inductive-energy equations.
- Requirements completion checklist and critical path.

## Assumptions and evidence level
- 18S full-charge candidate = 75.6 V: prior candidate, not frozen.
- 120/150 V cases: screening only.
- 0.3 V BAT54H drop and 3.6 V powered clamp node: illustrative screening assumptions only, not worst-case datasheet guarantees.
- STM32G474 and CSD19536KTT limits: PRIMARY MANUFACTURER EVIDENCE.
- No physical measurements performed.

## Unresolved blockers
- G0 vehicle mass/mission/environment/failure policy.
- Final rotor architecture and propulsion operating point.
- Phase RMS/peak current and final PWM.
- Harness/PCB inductance plus switching/regen/BMS-disconnect transient ceiling.
- Exact DC-link capacitor and input protection/clamp sizing.
- +3V3A/TLV75533/upstream rail behavior during external clamp backfeed.
- Final semiconductor voltage class and MPN.

## Risks / regressions
- With VBUS present while control rails are off, the existing upper BAT54H can inject into +3V3A; this must not be ignored in the UAV revision.
- 100 V legacy MOSFET/driver/aux/DC-link domains remain coupled to the unresolved transient ceiling.
- G1 cannot honestly close from competitor benchmarks alone; vehicle-specific G0 inputs are required for final product requirements.

## Exact next recommended tasks
1. Audit TLV75533 and upstream 5 V rail reverse-current/back-power behavior from primary sources and decide whether B1 clamp architecture is retain/recalculate/replace for UAV.
2. Continue propulsion evidence and translate selected scenario ranges into phase-current/eRPM/PWM requirement bounds without freezing unsupported values.
3. Build a source-backed 100/120/150 V semiconductor candidate parameter table for trade-study use only.
4. Map `REQUIREMENTS_COMPLETION_CHECKLIST.md` directly to null/open fields in `design_basis.json` and traceability so G1 completion is mechanically auditable.
5. Run the precharge model only when Cbus, precharge target, resistor class, harness inductance/current or other numeric inputs have evidence; do not guess them.

## Dependency chain
`G0 vehicle inputs -> G1A rotor -> G1B propulsion point -> G1C battery/current/transient envelope -> G1 SYSTEM FREEZE -> G2 architecture freeze -> G3 schematic review -> firmware/PCB -> bench/propulsion validation`

## Next-run briefing
Start with the +3V3A backfeed closure because the exact diode topology is now known. Then improve G1 auditability by mapping open design-basis fields to the new requirements checklist, and continue propulsion/current evidence in parallel. Treat CSD19536KTT as a 100 V legacy reference, not a UAV selection. Do not turn 120/150 V screening cases into requirements and do not freeze 18S or any protection component until the real transient and vehicle envelope are evidenced.