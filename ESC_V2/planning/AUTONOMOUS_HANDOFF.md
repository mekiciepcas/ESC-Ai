# ESC autonomous handoff

Date: 2026-09-19 07:22+03:00  
Branch: `uav-rebaseline`  
Status: `PROGRESS_BUS_SENSE_AND_VBUS_COMPONENT_AUDIT`

## Run summary
This run closed two unblocked follow-ups: the 18S bus-sense arithmetic was rebaselined and the first B1 VBUS-exposed component audit was created. No product voltage class, divider values, rotor count, MTOW, phase-current rating, gate driver or auxiliary regulator was frozen.

## Tasks attempted / completed
1. Verified the previous handoff/state against the branch.
2. Recalculated the B1 divider (2x49.9k / 3.32k): ratio 0.0321955; 75.6 V maps to ~2.434 V; ideal 3.3 V ADC full-scale maps to ~102.5 V bus.
3. Added `BUS_SENSE_18S_REBASELINE.md` with ~120 V and ~150 V measurement-range study options and explicit separation of measurement full scale from hardware OVP.
4. Audited the first VBUS-exposed B1 domains and added `B1_VBUS_COMPONENT_AUDIT.md`.
5. Verified TI primary data for LM5164: 6–100 V input domain; Rev D typical 12 V application uses a 15–100 V design range.
6. Updated autonomous state and this handoff.

## Files changed
- `planning/BUS_SENSE_18S_REBASELINE.md` — new
- `planning/B1_VBUS_COMPONENT_AUDIT.md` — new
- `planning/autonomy_state.json` — updated
- `planning/AUTONOMOUS_HANDOFF.md` — updated

## Engineering decisions / findings
- The legacy B1 divider does not saturate at 80 V; 80 V was only a documented check point. Its ideal mathematical 3.3 V ceiling is ~102.5 V.
- This arithmetic does not qualify it for 18S UAV use because tolerance, ADC/reference error, clamp injection/leakage, resistor working voltage, ADC settling and the unresolved transient ceiling remain open.
- Measurement full scale and hardware over-voltage protection are now explicitly separate requirements.
- LM5164 joins DRV8353 and the 100 V MOSFET class as a voltage-domain-critical item: 75.6 V steady-state is inside its 100 V input domain, but an undefined >100 V transient cannot be accepted without a proven clamp/filter or a different auxiliary architecture.
- Repository evidence shows 160 V local HV capacitor values exist, but exact MPN, DC-bias capacitance and ripple qualification remain open; nominal printed voltage is not a PASS.

## Evidence level
- Divider results: arithmetic from B1 source values.
- LM5164 6–100 V domain: PRIMARY_MANUFACTURER / TI Rev D.
- B1 component exposure: repository source audit, partial.
- No physical validation performed.

## Unresolved blockers
- G0 vehicle mass/mission/environment/failure policy.
- Rotor architecture and exact product operating point.
- Phase RMS/peak current.
- Switching/harness/regen/disconnect/clamp transient ceiling.
- Exact effective DC-link capacitance at bias/temperature.

## Risks / regressions
- A higher-VDS MOSFET alone cannot qualify 18S because DRV8353 and LM5164 are also 100 V-domain components.
- Leaving the B1 divider unchanged would leave little diagnostic range if the defined bus transient approaches 100 V and would risk conflating ADC saturation with protection.
- Bulk capacitor voltage rating is not yet proven for 18S; the legacy 39–54.6 V design basis cannot be reused as evidence.

## Exact next recommended tasks
1. Extract exact B1 bulk capacitor and VBUS protection references/MPNs/ratings.
2. Build a parameterized semiconductor loss-model input framework for 100/120/150 V candidate classes without selecting an MPN.
3. Audit individual divider-resistor working voltage and ADC clamp/injection path.
4. Update UAV traceability with bus-sense and LM5164 constraints.
5. Only if the required transient ceiling exceeds 100 V, research a higher-voltage auxiliary front end or a proven protected sub-domain.

## Dependency chain
`G0 vehicle inputs -> rotor freeze -> propulsion point -> battery freeze -> DC/phase envelope -> transient ceiling -> semiconductor/driver/aux/DC-link voltage domains -> sensing/protection -> schematic/firmware/PCB`

## Next-run briefing
Start with exact B1 VBUS BOM extraction and the parameterized loss-model framework; both reduce risk without pretending the transient ceiling or phase current is known. Keep 75.6 V as an 18S battery candidate maximum, not a transient requirement. Do not freeze ~120 V or ~150 V sensing; they are study ranges. Verify exact component MPNs before declaring voltage compatibility.
