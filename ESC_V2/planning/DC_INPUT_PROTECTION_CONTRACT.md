# UAV ESC external DC-input / protection module contract

Date: 2026-09-19
Status: ARCHITECTURE CONTRACT — component values OPEN

## Purpose
The B1 inverter board currently exposes protection/precharge and brake/clamp functions as external interfaces. For UAV rebaseline these functions cannot remain implicit. This document defines what the upstream battery/input assembly must guarantee before the ESC power stage can be voltage-qualified.

## Electrical boundaries
Battery system -> fuse/current interruption -> reverse-polarity / connection protection -> precharge path -> main contact/disconnect element -> harness -> ESC local DC-link/inverter.

A bus-energy handling path for switching overshoot, propulsion deceleration, BMS/contact opening and fault cases must be defined at system level. It may reside locally, upstream, or be shared, but its guaranteed behavior must be visible at the ESC terminals.

## Required upstream guarantees
### Voltage
- VBUS_MIN_OPERATING: OPEN
- VBUS_NOMINAL: candidate 18S architecture, not frozen
- VBUS_MAX_CHARGED: 75.6 V for 18S Li-ion screening only
- VBUS_MAX_REPETITIVE_AT_ESC: OPEN; must be measured/modelled and guaranteed
- VBUS_ABSOLUTE_TRANSIENT_AT_ESC: OPEN; must be below every exposed component limit with design margin

### Current
- continuous pack/branch current: OPEN pending propulsion architecture
- peak current and duration: OPEN
- fuse clearing/current-limiting characteristic: OPEN
- branch isolation strategy for multi-ESC vehicle: OPEN

### Precharge
The upstream system shall limit inrush into the ESC effective DC-link capacitance. Closure requires:
- final effective Cdc at voltage/temperature,
- allowed precharge time,
- maximum resistor pulse energy and temperature,
- main-contact closure threshold,
- failed-precharge detection,
- welded/open contact detection policy where applicable,
- auxiliary-power behavior during precharge.

No resistor/contact value is selected until Cdc and system architecture close.

### Disconnect / BMS behavior
The system contract must state what happens when the battery/BMS/main contact opens while the motor is generating or the phase current is non-zero. The ESC shall not assume the battery remains an infinite energy sink. Required cases include commanded shutdown, BMS over-current/under-voltage/over-temperature opening, connector interruption and single-branch fuse operation.

### Regen / clamp energy path
Required evidence:
- whether normal flight control permits regenerative energy back to the battery,
- battery/BMS charge acceptance at full SOC and low temperature,
- local or central clamp/brake path if the battery cannot accept energy,
- clamp threshold tolerance,
- pulse/repetitive energy capability,
- thermal recovery interval,
- failure behavior.

A small signal/ADC clamp is not an acceptable DC-bus energy clamp.

### Harness interface
The final contract shall include branch cable length/gauge/geometry or measured equivalent inductance. This parameter feeds the transient model. ESC local DC-link placement and connector inductance must be included rather than assuming zero harness inductance.

## ESC-side acceptance criteria
Before voltage-domain freeze, demonstrate by calculation plus bench measurement that:
1. normal charged bus remains inside operating ratings with temperature/lifetime derating;
2. repetitive switching overshoot remains below the repetitive design ceiling;
3. disconnect/regen events remain below the absolute transient ceiling without relying on unspecified repetitive avalanche;
4. precharge limits connector/contact/DC-link stress;
5. fault interruption coordinates with semiconductor SOA and wiring;
6. sensing and auxiliary domains survive powered/unpowered sequencing and backfeed cases.

## Open implementation choices
Fuse type/rating, contactor vs solid-state disconnect, reverse-polarity topology, precharge topology, clamp/TVS/brake topology, branch-vs-central protection and exact component MPNs remain OPEN. These are deliberately not guessed before current, energy and transient envelopes close.

## Dependency
`propulsion/current envelope + final Cdc + harness inductance + BMS/contact behavior -> transient/energy model -> protection component sizing -> measured bench validation -> voltage-domain freeze`
