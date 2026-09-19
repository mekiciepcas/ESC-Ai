# ESC autonomous handoff

Date: 2026-09-19 04:18+03:00  
Branch: `uav-rebaseline`  
Status: `PROGRESS_G1_PROPULSION_AND_VOLTAGE_RISK`

## Run summary

This run converted current primary-source heavy-UAV propulsion ratings into a structured operating-point evidence file and completed the first legacy-B1 compatibility audit against the preferred-for-analysis 18S family. No product rating was frozen.

## Tasks attempted / completed

1. Re-verified Hobbywing X15 G2 from current manufacturer material: 18S/69 V, 37.5 kg recommended axis load, 8 g/W at recommended thrust, 4640 W rated input, 3971 W rated output, 120 A continuous ESC, 300 A peak/3 s, 82 kg max thrust, 45 KV and 63x24 propeller.
2. Added T-Motor A16-18S as a second single-axis heavy propulsion reference: 35–40 kg rated thrust, 38 kg at 8.7 g/W reference efficiency, 74.5 kg max thrust, 14–18S, 83 V ESC max and 260 A short-time current rating.
3. Added T-Motor X-A14-18S as a coaxial/heavier reference: 45–50 kg rated thrust, 45 kg at 7.4 g/W, 105 kg max thrust and 18S FOC 200 A ESC class.
4. Created `propulsion_operating_points.json` with explicit SOURCE_BACKED versus CALCULATED_FIRST_ORDER evidence and Q150/H175/coaxial scenario mapping.
5. Created `B1_18S_VOLTAGE_COMPATIBILITY.md` and audited the legacy B1 power domain against 18S full charge (75.6 V).

## Files changed

- `planning/propulsion_operating_points.json` — new
- `planning/B1_18S_VOLTAGE_COMPATIBILITY.md` — new
- `planning/autonomy_state.json` — updated
- `planning/AUTONOMOUS_HANDOFF.md` — updated

## Engineering decisions / findings

- X15 G2 directly supports the plausibility of a ~150 kg quad class at 37.5 kg recommended load per axis, but it does not freeze our vehicle architecture.
- A16-18S is a useful upper-envelope single-axis candidate for a 175 kg hex scenario because 175/6 = 29.2 kg hover load/axis is below its 35–40 kg rated thrust range; exact efficiency/current at 29.2 kg still needs the manufacturer curve.
- Legacy B1 is **not directly 18S-qualified**.
- 100 V MOSFET and 100 V DC-link component assumptions are not frozen for 18S. At 75.6 V full charge, a 100 V device has only 24.4 V absolute static headroom; transient, regen and BMS/contact-opening cases remain unclosed.
- B1's preliminary 99.8k/3.32k divider is nominally within a 3.3 V ADC range at 75.6–80 V, but an 80 V verification ceiling leaves inadequate diagnostic/transient measurement headroom for a final 18S design.
- 100 V MLCC candidates require actual DC-bias curves; nameplate capacitance cannot be assumed near ~76 V bias.

## Calculations/evidence added

- A16 reference point: 38,000 g / 8.7 g/W = ~4367.8 W first-order input-equivalent power; explicitly marked derived, not measured curve data.
- X-A14 reference point: 45,000 g / 7.4 g/W = ~6081.1 W first-order input-equivalent power; explicitly marked derived.
- 18S full-charge bus: 18 x 4.2 V = 75.6 V.
- Static headroom to 100 V class: 24.4 V; no transient margin approval inferred.

## Evidence level

- Hobbywing/T-Motor published ratings: `PRIMARY_MANUFACTURER / SOURCE_BACKED`.
- Thrust divided by g/W: `CALCULATED_FIRST_ORDER`.
- Q150/H175/coaxial mapping: `SCENARIO_REFERENCE_NOT_FROZEN`.
- B1 voltage review: `DESK_PRECHECK`, not physical or production validation.

## Unresolved blockers

- G0 mission/mass freeze still needs vehicle-specific mass, mission, environment and failure-policy inputs.
- Final rotor architecture and exact operating point remain open.
- Phase RMS/peak current remains open; it must not be inferred from DC current.
- 18S semiconductor voltage class cannot close until DC-bus transient, regen and BMS-disconnect ceiling is established.
- Exact DC-link MLCC/electrolytic parts and derating remain open.

## Risks/regressions discovered

- Moving from legacy 13S to 18S may force a power-domain voltage-class redesign even if much of the control architecture survives.
- The existing 100 V capacitor/MOSFET convention can appear acceptable at steady state while being inadequate under cable-inductance or energy-rejection transients.
- B1 voltage-sense full scale should be redesigned together with the transient requirement rather than merely checked at 75.6 V.

## Exact next recommended tasks

1. Extract the full X15 G2 69 V thrust/current/power/RPM rows from the primary-source table and store only real rows.
2. Extract A16-18S curve rows if available and evaluate the 29–40 kgf axis region for the H175 scenario.
3. Create a parameterized DC-bus transient requirement model: battery max, cable/loop inductance, di/dt, clamp/TVS strategy, regen/BMS-disconnect cases. Keep unknown parasitics explicit.
4. From that model, compare 100 V versus higher-voltage semiconductor classes without choosing a final MPN.
5. Recalculate voltage-sense full-scale target after the transient measurement ceiling is selected.

## Dependency chain

`G0 vehicle inputs -> rotor freeze -> exact propulsion operating points -> battery freeze -> DC/phase electrical envelope -> transient ceiling -> semiconductor/driver/DC-link freeze -> sensing/protection -> schematic/firmware/PCB`

## Next-run briefing

Start by extracting manufacturer table rows rather than extrapolating them. The X15 G2 primary page exposes a 69 V thrust table; capture real rows for thrust/current/input power/RPM if accessible. In parallel, build the transient model with symbolic/parameterized inductance and di/dt so lack of physical harness data does not stop progress. Do not decide 100 V vs 120/150 V class from steady-state voltage alone. Preserve historical B1 and write all new conclusions into planning/rebaseline artifacts only.
