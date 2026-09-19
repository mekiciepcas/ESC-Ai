# G0 vehicle-input closure form

Status: **OPEN — 11 product inputs remain**  
Source authority: `PRODUCT_BASELINE_PB-02.json`, `G0_INPUT_CLOSURE_PACKET.json`, `mission_requirements.json`, `UAV_PRODUCT_PLAN.md`

PB-02 has now frozen the nominal payload at **85 kg**, the X8 coaxial architecture, the 150/165/180 kg MTOW design targets, the 18S propulsion/battery class and the controlled-landing failure policy. These values are no longer requested as open inputs.

Unknown remaining items may be answered as `OPEN` rather than guessed. Competitor values are not copied into product fields.

## Mass allocation and mission — still open

1. Estimated structural/airframe mass inside the frozen 80 kg operating-empty budget: `___ kg`
2. Estimated battery mass: `___ kg`
3. Other fixed mission-equipment mass inside the 80 kg budget: `___ kg`
4. Target total flight time: `___ min`
5. Target hover-equivalent time within the mission: `___ min`

## Environment — still open

6. Minimum ambient temperature: `___ °C`
7. Maximum ambient temperature: `___ °C`
8. Maximum operating altitude: `___ m`
9. Maximum design wind: `___ m/s`
10. Rain/dust/ingress target: `___` (for example a desired IP class, or `OPEN`)

## Mechanical envelope — still open

11. Maximum acceptable vehicle span: `___ m / OPEN`

## Already frozen by PB-02 — do not ask again unless revising the baseline

- Payload range: `70–100 kg`
- Nominal payload: `85 kg`
- Operating-empty mass budget: `<=80 kg`
- MTOW design targets: `150 / 165 / 180 kg`
- Propulsion architecture: `X8_COAXIAL_4_ARM_8_INDEPENDENT_PROPULSION_CHANNELS`
- Rotor count: `8`
- Coaxial sizing factor: `0.85` pending physical correlation
- Static thrust-to-weight requirement: `>=1.6`
- Complete loss of one motor/ESC: `controlled_landing`
- Propulsion class: `56x20 inch / 45KV / 18S`
- Battery series architecture: `18S`, `66.6 V nominal`, `75.6 V full charge`
- ESC DC capability: `>=70 A continuous`, `>=200 A for >=3 s`
- Controller electrical speed capability: `>=60,000 eRPM`
- Power semiconductor class: `>=150 V`

Changing a frozen item requires a new product-baseline revision or linked engineering change record.

## Closure rule

The remaining 11 answers will be written back only as real product inputs or explicitly controlled engineering decisions. Phase current, PWM, pack energy, exact power-stage parts and thermal implementation remain open until their parent requirements are calculated and verified.
