# UAV battery voltage architecture — pre-trade

Date: 2026-09-19
Status: PRELIMINARY / NOT FROZEN
Backlog: supports UAV-005 before UAV-004 closes

## Purpose

Compare voltage families using current heavy-agricultural propulsion evidence without prematurely selecting the final pack. This is a dependency-opening trade study, not G1 closure.

## Primary-source anchors

### Family A — approximately 50 V class

XAG P150 Max published system data:
- 4 motors
- 136 kg maximum spraying takeoff weight
- 56 kgf maximum thrust per motor
- 4.85 kW rated power per motor
- ESC 140 A continuous, 380 A maximum output current for 30 s
- published battery rated output 52.5 V / 140 A, 20 Ah

Primary source: https://xa.com/en/p150max/p150maxspecs

Caution: the public product page does not expose a complete battery interconnection/power-path schematic. The published battery rating must therefore not be interpreted as total aircraft transient bus current without additional evidence.

### Family B — 18S / 69 V nominal class

Hobbywing X15 G2 published propulsion data:
- 18S LiPo
- 69 V rated voltage
- 25–80 V input range
- 4.64 kW rated input power
- 3.971 kW rated output power
- 120 A continuous ESC current
- 300 A peak for 3 s
- 82 kgf maximum thrust
- 37.5 kg recommended takeoff weight per axis
- 63x24 in propeller

Primary source: https://www.hobbywing.com/en/uploads/file/20260114/8edfaf2969be848410994360b6ac2487.pdf

## First-order current comparison

For the same electrical power, ideal DC current is `I=P/V`. This is only a bus-level comparison; phase current and transient ESC rating require the selected motor operating point.

| Per-axis electrical power | 52.5 V ideal DC current | 69 V ideal DC current | Reduction at 69 V |
|---:|---:|---:|---:|
| 3.0 kW | 57.1 A | 43.5 A | 23.9% |
| 4.0 kW | 76.2 A | 58.0 A | 23.9% |
| 4.64 kW | 88.4 A | 67.2 A | 23.9% |
| 5.0 kW | 95.2 A | 72.5 A | 23.9% |
| 8.0 kW transient | 152.4 A | 115.9 A | 23.9% |

At equal conductor resistance, `I^2R` loss scales with current squared. Moving from 52.5 V to 69 V at equal power gives an ideal conductor-loss ratio `(52.5/69)^2 = 0.579`, about 42% lower. This does not include pack mass, semiconductor switching loss, insulation, connector availability or motor winding effects.

## Semiconductor-voltage consequence

An 18S LiPo pack reaches 75.6 V at 4.2 V/cell. Hobbywing permits 25–80 V at the X15 G2 input. Therefore a custom 18S ESC cannot treat 80 V as a comfortable semiconductor ceiling: switching overshoot, BMS disconnect/regen and tolerance require additional VDS margin. The legacy 100 V MOSFET class is consequently **not frozen and appears margin-constrained** for an 18S architecture until transient measurements/models define the ceiling.

For a lower-voltage ~50–53 V family, 100 V devices have more nominal voltage ratio, but current and conduction/current-sharing burden rises. Device class must be selected from a quantified transient ceiling and loss/SOA trade, not voltage ratio alone.

## Pack-energy consequence

Energy requirement remains OPEN because mission duration is unknown. A pack cannot be selected from ESC power alone. Required usable energy must include:
- hover/mission electrical power,
- mission duration,
- reserve fraction,
- voltage sag at end-of-discharge,
- temperature derating,
- allowable depth of discharge,
- non-propulsion loads.

## Preliminary architecture decision

**Do not preserve 13S as product baseline.** Carry at least two candidates into UAV-004/005:

1. `LV_HIGH_CURRENT`: approximately 50–53 V nominal/current commercial-agriculture precedent.
2. `HV_18S`: 18S / 69 V nominal, 75.6 V fully charged, lower bus current and direct X15 G2 precedent.

Current preference for further analysis: `HV_18S`, because it reduces bus current materially in the 4–5 kW/axis class and has a current heavy-agricultural propulsion precedent. This is a trade-study preference only, not a frozen requirement.

## Required evidence before UAV-005 closure

- selected propulsion operating points from UAV-004,
- actual pack chemistry and cell voltage limits,
- mission usable-energy requirement,
- pack continuous and pulse current capability,
- BMS/contactor topology,
- BMS disconnect behavior during motor regeneration,
- harness/connector current and thermal model,
- measured or conservatively modeled DC-bus overshoot,
- safe precharge strategy.

## Design impact on legacy B1

- 13S pack: RECALCULATE/likely REPLACE if 18S selected.
- 100 V MOSFET target: REVALIDATE; do not freeze.
- 80 V voltage-sense check: inadequate as a final verification ceiling if transient headroom exceeds it.
- LM5164 input suitability: must be rechecked against final bus/transient architecture; it is not automatically valid for an 18S bus.
- DC-link, connectors, shunts and precharge: RECALCULATE after UAV-004/005.
