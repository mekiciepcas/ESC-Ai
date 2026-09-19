# G0 vehicle-input closure form

Status: **OPEN — user/product inputs required**  
Source authority: `G0_INPUT_CLOSURE_PACKET.json`, `mission_requirements.json`, `UAV_PRODUCT_PLAN.md`

This form is intentionally limited to values that cannot be inferred safely from competitor aircraft or legacy B1 assumptions. Unknown items may be answered as `OPEN` rather than guessed.

## Mass and mission

1. Nominal payload: `___ kg`  
   Known target range remains 70–100 kg.
2. Estimated empty airframe mass, excluding payload/battery/mission equipment: `___ kg`
3. Estimated battery mass: `___ kg`
4. Other mission equipment mass not included in payload definition (tank/pump/landing gear/etc. as applicable): `___ kg`
5. Target total flight time: `___ min`
6. Target hover-equivalent time within the mission: `___ min`

## Environment

7. Minimum ambient temperature: `___ °C`
8. Maximum ambient temperature: `___ °C`
9. Maximum operating altitude: `___ m`
10. Maximum design wind: `___ m/s`
11. Rain/dust/ingress target: `___` (for example a desired IP class, or `OPEN`)

## Vehicle architecture / failure policy

12. Required behavior after complete loss of one motor/ESC: choose one or write another policy:
   - `continued_hover`
   - `controlled_landing`
   - `no_continued_operation_requirement`
   - other: `___`
13. Is coaxial rotor architecture allowed? `yes / no / OPEN`
14. Maximum acceptable vehicle span: `___ m / OPEN`

## Closure rule

These answers will be written back to `mission_requirements.json` and `G0_INPUT_CLOSURE_PACKET.json` only as user-supplied product inputs. MTOW, rotor count, thrust per rotor, battery energy and the ESC electrical envelope will then be derived from the frozen inputs; they will not be copied from competitor UAVs.
