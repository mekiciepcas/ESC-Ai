# G0 vehicle-input closure form

Status: **OPEN — 12 product inputs remain**  
Source authority: `PRODUCT_BASELINE_PB-01.json`, `G0_INPUT_CLOSURE_PACKET.json`, `mission_requirements.json`, `UAV_PRODUCT_PLAN.md`

PB-01 has already frozen the vehicle propulsion architecture as X8 coaxial (4 arms / 8 independently controlled propulsion channels), allowed coaxial packaging, and frozen the single motor/ESC failure policy to controlled landing. These items are therefore no longer requested from the user as open inputs.

Unknown remaining items may be answered as `OPEN` rather than guessed. Competitor values are not copied into product fields.

## Mass and mission — still open

1. Nominal payload: `___ kg`  
   Frozen target range remains 70–100 kg.
2. Estimated empty airframe mass, excluding payload/battery/mission equipment: `___ kg`
3. Estimated battery mass: `___ kg`
4. Other mission equipment mass not included in payload definition: `___ kg`
5. Target total flight time: `___ min`
6. Target hover-equivalent time within the mission: `___ min`

## Environment — still open

7. Minimum ambient temperature: `___ °C`
8. Maximum ambient temperature: `___ °C`
9. Maximum operating altitude: `___ m`
10. Maximum design wind: `___ m/s`
11. Rain/dust/ingress target: `___` (for example a desired IP class, or `OPEN`)

## Mechanical envelope — still open

12. Maximum acceptable vehicle span: `___ m / OPEN`

## Already frozen by PB-01 — do not ask again unless revising the baseline

- Propulsion architecture: `X8_COAXIAL_4_ARM_8_INDEPENDENT_PROPULSION_CHANNELS`
- Rotor count: `8`
- Coaxial packaging allowed: `yes`
- Complete loss of one motor/ESC: `controlled_landing`
- Continued hover at maximum payload after one propulsion-channel loss: `not required`

Changing any item above requires a new product-baseline revision or linked engineering change record.

## Closure rule

The remaining 12 answers will be written back only as real product inputs or explicitly controlled engineering decisions. MTOW, thrust per rotor, battery energy and the remaining ESC electrical envelope will be derived from the controlled inputs and source-backed propulsion data; they will not be copied from competitor UAVs.
