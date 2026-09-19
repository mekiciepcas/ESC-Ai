# ESC autonomous handoff

Date: 2026-09-19 05:21+03:00  
Branch: `uav-rebaseline`  
Status: `PROGRESS_X15_CURVE_AND_TRANSIENT_METHOD`

## Run summary

This run closed two unblocked evidence tasks: the complete manufacturer-published Hobbywing X15 G2 69 V operating table was converted to structured repository data, and a parameterized DC-bus transient requirement method was added. No rotor architecture, product current rating or semiconductor voltage class was frozen.

## Tasks attempted / completed

1. Verified the current Hobbywing X15 G2 manufacturer page and load-performance table.
2. Captured all published 69 V / MFP 63x24 rows from 34% through 100% throttle into `x15g2_operating_curve.json`, preserving thrust, DC current, input power, RPM, efficiency, torque and output power.
3. Added `dc_bus_transient_model.py` implementing first-order inductive energy, L*di/dt sensitivity and ideal capacitor energy absorption calculations with unknown parasitics kept explicit.
4. Added `DC_BUS_TRANSIENT_REQUIREMENTS.md` defining the evidence required before 100 V or a higher semiconductor/DC-link class can be frozen.
5. Updated machine-readable autonomous state.

## Files changed

- `planning/x15g2_operating_curve.json` — new
- `planning/dc_bus_transient_model.py` — new
- `planning/DC_BUS_TRANSIENT_REQUIREMENTS.md` — new
- `planning/autonomy_state.json` — updated
- `planning/AUTONOMOUS_HANDOFF.md` — updated

## Engineering decisions / findings

- X15 G2 real 69 V curve now gives direct commercial-axis reference points instead of g/W extrapolation. Examples: 29.168 kgf = 45.9 A / 3.170 kW; 35.177 kgf = 61.0 A / 4.212 kW; 38.315 kgf = 69.5 A / 4.796 kW; 41.608 kgf = 78.8 A / 5.438 kW; 82.476 kgf = 246.6 A / 17.019 kW. These are manufacturer bench rows, not our product requirements.
- The commercial curve demonstrates why a single nominal/rated kW value is insufficient for ESC sizing: electrical demand rises steeply above the recommended hover/load region.
- 18S full charge remains 75.6 V. A 100 V device therefore remains only a candidate; final VDS/DC-link class requires switching/harness transient, regen/BMS-disconnect and clamp closure.
- The transient script is intentionally parametric. No harness inductance, interruption time, clamp voltage or bus capacitance was promoted to a product assumption.

## Calculations/evidence added

- Structured 22-row X15 G2 curve at 69 V from the current manufacturer table.
- `E_L = 0.5 L I^2` sensitivity method.
- `V_L = L dI/dt` first-order interruption sensitivity.
- `V1 = sqrt(V0^2 + 2E/C)` ideal capacitor-only energy absorption bound.
- Voltage-class closure checklist including battery maximum, overshoot, regen/BMS disconnect, clamp dynamic voltage, engineering margin and representative-layout oscilloscope validation.

## Evidence level

- X15 G2 curve: `PRIMARY_MANUFACTURER / SOURCE_BACKED`, applicable to the published 69 V + MFP 63x24 bench condition.
- Transient equations: `FIRST_ORDER_ENGINEERING_MODEL`.
- Any future sensitivity-grid numbers from the script: `PARAMETRIC_ONLY`, not measured product predictions.
- No physical validation performed.

## Unresolved blockers

- G0 mission/mass freeze still requires vehicle-specific mass, mission, environment and failure-policy inputs.
- Final rotor architecture and exact operating point remain open.
- Phase RMS/peak current remains open; X15 table current is DC input current and must not be relabelled phase current.
- Semiconductor voltage class remains open until parasitic/transient/regen/clamp requirements close.
- Exact DC-link capacitance and biased MLCC/electrolytic behaviour remain open.

## Risks/regressions discovered

- Heavy-lift axis peak electrical demand can be far above the recommended-load/rated-power region; ESC peak design must be tied to a selected thrust margin and duration, not motor marketing power alone.
- Using DC current from a propulsion table as phase RMS current would materially under-specify or mis-specify sensing and silicon; keep domains separate.
- 100 V steady-state headroom is not a transient design margin.

## Exact next recommended tasks

1. Map real X15 G2 curve rows to Q150 and H175 quad/hex scenario hover and 1.6x-thrust points without freezing architecture; use interpolation only when explicitly marked calculated.
2. Extract T-Motor A16-18S test rows if the manufacturer table can be accessed and compare the 29–40 kgf region against X15 G2.
3. Build a 100 V / 120 V / 150 V semiconductor voltage-class trade framework using required transient ceiling as an input rather than choosing an MPN.
4. Recalculate candidate bus-voltage ADC full scales consistent with an 18S diagnostic/transient ceiling.
5. Audit DRV8353/aux-power exposure separately from MOSFET VDS class.

## Dependency chain

`G0 vehicle inputs -> rotor freeze -> exact propulsion operating points -> battery freeze -> DC/phase electrical envelope -> transient ceiling -> semiconductor/driver/DC-link freeze -> sensing/protection -> schematic/firmware/PCB`

## Next-run briefing

Use `x15g2_operating_curve.json` as the primary numeric source for scenario mapping. Do not derive phase current from its DC-current column. Interpolation is allowed only as an explicitly calculated scenario estimate bracketed by real manufacturer rows. Continue the voltage-class work as a requirements trade, not a part-number selection, until the transient ceiling is known. If A16 full curve extraction remains unavailable, record that limitation and continue with voltage-sense/driver-domain work rather than fabricating rows.
