# ESC autonomous handoff

Date: 2026-09-19 06:23+03:00  
Branch: `uav-rebaseline`  
Status: `PROGRESS_SCENARIO_MAPPING_AND_DRIVER_VOLTAGE_AUDIT`

## Run summary

This run converted the X15 G2 primary 69 V curve into architecture-level benchmark operating points and advanced the 18S voltage-domain risk from a generic concern to an explicit gate-driver/power-silicon requirement. No product rotor count, MTOW, phase current, semiconductor class or gate driver was frozen.

## Tasks attempted / completed

1. Verified previous handoff against repository `x15g2_operating_curve.json`.
2. Linearly mapped source-backed X15 G2 rows to 125/136/150/175 kg quad benchmarks and 175 kg hex/octo cases.
3. Added `X15_SCENARIO_MAPPING.md` with calculated DC-current/input-power points and explicit interpolation/evidence labels.
4. Added `POWER_DOMAIN_VOLTAGE_CLASS_TRADE.md` comparing static 100/120/150 V headroom for the 18S candidate and defining the transient closure gates.
5. Verified TI primary product information for DRV8353: 9–100 V operating supply domain and 102 V absolute maximum.
6. Updated machine-readable autonomous state and this handoff.

## Files changed

- `planning/X15_SCENARIO_MAPPING.md` — new
- `planning/POWER_DOMAIN_VOLTAGE_CLASS_TRADE.md` — new
- `planning/autonomy_state.json` — updated
- `planning/AUTONOMOUS_HANDOFF.md` — updated

## Engineering decisions / findings

- At 150 kg quad, X15 G2 hover = 37.5 kgf/axis and maps to about 67.3 A DC / 4.64 kW at the published 69 V bench condition, aligning with the manufacturer's recommended 37.5 kg/axis and 4.64 kW rated-input region.
- At 175 kg quad, hover maps to ~85.2 A / 5.88 kW per axis; 1.6x and 1.8x static-thrust study points map to ~185.2 A / 12.78 kW and ~227.9 A / 15.72 kW respectively. These high-thrust points are not continuous ratings.
- At 175 kg hex, hover maps to the real ~29.17 kgf row at ~45.9 A / 3.17 kW; the 1.8x point maps to ~113.5 A / 7.83 kW. This materially lowers per-ESC stress versus quad.
- At 175 kg octo, the 1.8x point maps to ~72.5 A / 5.00 kW per axis, at the cost of eight propulsion units.
- DRV8353 is now explicitly a voltage-margin-critical candidate for 18S. TI publishes 100 V operating and 102 V absolute maximum. 75.6 V battery full charge alone does not prove adequate transient margin.
- 100 V MOSFET class remains `NOT_QUALIFIED / HIGH_RISK_CANDIDATE`; 120 V and 150 V are trade classes only.

## Calculations/evidence added

- Linear interpolation of adjacent primary X15 rows for benchmark thrust points.
- Static full-charge headroom: 100 V -> 24.4 V (1.323x); 120 V -> 44.4 V (1.587x); 150 V -> 74.4 V (1.984x).
- Explicit voltage-requirement framework covering battery max, switching overshoot, harness event, regen/disconnect and engineering margin, with clamp behavior requiring evidence.

## Evidence level

- X15 base curve and product ratings: `PRIMARY_MANUFACTURER / SOURCE_BACKED` at published 69 V + MFP 63x24 conditions.
- Scenario values: `CALCULATED_LINEAR_INTERPOLATION`, not product requirements.
- DRV8353 limits: `PRIMARY_MANUFACTURER / TI`.
- Voltage-class headroom: `ARITHMETIC_REQUIREMENTS_TRADE`, not transient qualification.
- No physical validation performed.

## Unresolved blockers

- G0 mission/mass freeze still requires vehicle-specific mass, mission, environment and failure-policy inputs.
- Rotor architecture and exact product operating point remain open.
- Phase RMS/peak current remains open; propulsion table current is DC input current.
- Semiconductor and driver voltage class remain open until switching/harness/regen/clamp ceiling is established and later measured.
- Effective DC-link capacitance at voltage/temperature remains open.

## Risks/regressions discovered

- A 175 kg quad using X15-class propulsion creates a much more severe peak electrical requirement than legacy B1 and pushes well beyond the manufacturer's 120 A continuous ESC rating at the static margin study points.
- DRV8353's supply-domain ceiling can become the limiting voltage component even if higher-VDS MOSFETs are selected.
- Increasing MOSFET VDS class alone does not solve driver, capacitor, sensing or auxiliary-supply exposure.

## Exact next recommended tasks

1. Recalculate bus-voltage ADC divider/full-scale candidates for 18S with diagnostic/transient headroom; keep protection trip distinct from measurement full scale.
2. Audit LM5164 and all B1 components directly exposed to VBUS against the candidate 18S/transient domain.
3. Build a silicon loss-model input framework for 100/120/150 V classes without choosing a part before the transient ceiling is known.
4. Update traceability with the new driver-domain constraint and X15 scenario evidence.
5. Continue T-Motor A16 curve extraction only if primary-source rows are accessible; do not infer unavailable data.

## Dependency chain

`G0 vehicle inputs -> rotor freeze -> exact propulsion operating points -> battery freeze -> DC/phase electrical envelope -> transient ceiling -> MOSFET + gate-driver + DC-link voltage domains -> sensing/protection -> schematic/firmware/PCB`

## Next-run briefing

Start with bus-sense range and the B1 VBUS-exposed component audit because both are unblocked by rotor freeze. Treat 75.6 V as the known 18S full-charge candidate, not the final transient ceiling. Do not use 102 V DRV8353 absolute maximum as a design target. Keep DC current and phase current separate. If a component's exact voltage rating cannot be verified from repository BOM or a primary datasheet, mark it OPEN rather than inferring from package/name.
