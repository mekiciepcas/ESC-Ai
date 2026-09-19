# B1 analog-rail back-power audit

Date: 2026-09-19  
Status: **ANALYSIS / UAV revision action required**  
Scope: B1 bus/phase ADC clamp path and +3V3A/+3V3/+5V power sequencing.

## Exact B1 path

Repository source shows the voltage-sense path as:

`VBUS/PHASE -> 49.9k -> 49.9k -> divider -> 1k -> V_ADC`

with an upper BAT54H oriented **anode = V_ADC, cathode = +3V3A**. The B1 auxiliary tree also connects:

`+5V -> TLV75533 -> +3V3 -> 0R analog link -> +3V3A`

Therefore, if VBUS/phase voltage remains present while +5V/+3V3/+3V3A are absent or collapsing, the upper Schottky provides a physical back-power path:

`VBUS/PHASE -> divider -> BAT54H -> +3V3A -> 0R -> +3V3 -> TLV75533 OUT`

This is an architecture-level sequencing condition, not merely an ADC-pin clamp-current question.

## Primary-source regulator constraint

Texas Instruments TLV755P Rev. D documents reverse current through the pass device when the output is biased while the input supply is not established or when output voltage exceeds input voltage. TI states these conditions exceed the device absolute-maximum condition `VOUT > VIN + 0.3 V`, and that excessive reverse current can degrade reliability or cause latch-up. The datasheet recommends external protection when reverse-current conditions are expected.

Evidence level: **PRIMARY MANUFACTURER DATASHEET** — TI TLV755P Rev. D, section 7.1.4 Reverse Current.

## Consequence for B1

The previously calculated source-limited current is small because the sensing divider has high impedance. That does **not** qualify the topology:

- the LDO output can be externally biased while its input is absent,
- the analog/digital 3.3 V rails can rise to an uncontrolled intermediate voltage,
- MCU and other 3.3 V loads may be partially back-powered,
- startup/shutdown state can become non-deterministic,
- absolute-maximum/current-injection values are not normal-operation design targets.

The upstream TPS62160 reverse-current behavior is still open, but TLV75533 evidence alone is sufficient to reject an assumption that the existing rail-clamp arrangement is automatically safe during VBUS-present/control-rails-off sequencing.

## UAV rebaseline decision

**B1 rail-referenced voltage clamp implementation: RECALCULATE / REPLACE IF REQUIRED.**

The divider concept can remain a candidate, but the production UAV sensing architecture must meet one of these verified conditions:

1. System sequencing guarantees VBUS and phase-energy sources are removed before +3V3A/+3V3 can collapse, including faults and BMS/contact events; **or**
2. Clamp energy is routed to a rail specifically designed to sink the worst-case injected current in every power state; **or**
3. The voltage-sense front end is redesigned so an energized high-voltage input cannot back-power MCU/control rails.

Option 1 cannot be assumed from normal shutdown behavior alone; fault/disconnect cases must be covered. No exact replacement component is selected here because the final VBUS/transient range is still open.

## Closure evidence required

- final VBUS min/nom/full-charge/transient requirement,
- worst-case divider tolerance and clamp-current model,
- verified power-up/down sequencing including BMS/contact/precharge fault cases,
- TLV75533 replacement/protection decision,
- upstream +5 V path reverse-current assessment,
- powered and unpowered current-limited bench validation,
- measured +3V3A/+3V3/+5V rail voltages during worst credible clamp event.

## Design rule carried forward

**No high-voltage measurement input may create an uncontrolled back-power path into MCU/control supply rails.**

This becomes a derived G2 sensing/protection requirement. The existing B1 BAT54H-to-rail arrangement remains historical/reference only until the above closure evidence exists.

No physical qualification is claimed.