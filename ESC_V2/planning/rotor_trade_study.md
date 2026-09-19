# Rotor architecture trade study — bounded screening

Date: 2026-09-19
Status: IN_PROGRESS / G0 NOT CLOSED
Branch: `uav-rebaseline`
Backlog: UAV-002

## Purpose

Compare rotor-count implications before selecting the propulsion architecture. Product-specific G0 values remain OPEN. Numerical MTOW cases in this document are controlled `ASSUMPTION_FOR_TRADE_ONLY` cases governed by `G0_TRADE_BOUNDING_CASES.md`; they do not freeze our vehicle MTOW, thrust margin or rotor count.

## Primary-source benchmark anchors

Current heavy agricultural products provide three useful architecture anchors:
- XAG P150: 54 kg aircraft weight with spraying system and batteries, 70 kg max payload, 125 kg max spraying MTOW, quad, 55 kgf max thrust/motor, 4.7 kW rated power/motor, 120 A continuous ESC.
- XAG P150 Max: 56 kg empty weight with spraying system and batteries, 80 kg max payload, 136 kg max spraying MTOW, four motors, 56 kgf max thrust/motor, 4.85 kW rated power/motor, 140 A continuous ESC.
- DJI Agras T100: 75 kg spraying weight, 100 kg operating spraying payload, 175 kg max spraying MTOW, 60 rpm/V motors and 62-inch propellers. DJI also publishes a Turkey-specific 149.9 kg MTOW use limit for T100; that statement is a constraint on that product/use context and is not copied into our product requirements.

Primary sources:
- https://www.xa.com/en/p150/p150specs
- https://xa.com/en/p150max/p150maxspecs
- https://ag.dji.com/t100/specs

## Controlled analysis cases

`T125`, `T150`, and `T175` are analysis cases only. T125 and T175 bracket current published heavy-agriculture examples; T150 is a sensitivity/interpolation case. The 1.6 and 1.8 static thrust/weight multipliers are also screening values, not requirements.

For N lifting axes and aircraft mass M:

`hover_thrust_per_axis_kgf = M / N`

| MTOW | Axes | Hover kgf/axis | Max kgf/axis @ T/W 1.6 | Max kgf/axis @ T/W 1.8 |
|---:|---:|---:|---:|---:|
| 125 kg | 4 | 31.25 | 50.00 | 56.25 |
| 125 kg | 6 | 20.83 | 33.33 | 37.50 |
| 125 kg | 8 | 15.63 | 25.00 | 28.13 |
| 150 kg | 4 | 37.50 | 60.00 | 67.50 |
| 150 kg | 6 | 25.00 | 40.00 | 45.00 |
| 150 kg | 8 | 18.75 | 30.00 | 33.75 |
| 175 kg | 4 | 43.75 | 70.00 | 78.75 |
| 175 kg | 6 | 29.17 | 46.67 | 52.50 |
| 175 kg | 8 | 21.88 | 35.00 | 39.38 |

## Reality checks against current propulsion systems

### Quad class

XAG P150 and P150 Max establish direct commercial precedent for heavy agricultural quads in the 125-136 kg published spraying-MTOW range. Their published per-axis rated powers are 4.7 and 4.85 kW respectively, so the legacy B1 3 kW target is not a defensible heavy-quad product rating.

Hobbywing X15 G2 provides a separate 18S/69 V propulsion reference with 37.5 kg recommended takeoff weight per axis and 82 kgf maximum thrust. Four recommended-load axes correspond to 150 kg total supported mass as a benchmark, not as our MTOW requirement.

### Upper-bound / multi-rotor class

DJI T100 provides current evidence that the 100 kg payload / 175 kg spraying-MTOW region is implemented with a multi-propeller architecture rather than an ordinary quad. Public DJI data is not used to infer its ESC current rating.

## Architecture screening

### Ordinary quad

Strengths:
- minimum ESC/motor count;
- simplest harness and maintenance burden;
- direct commercial precedent at 125-136 kg spraying MTOW.

Constraints:
- complete loss of one motor/ESC cannot satisfy a future requirement for continued controlled hover using only the remaining three fixed-pitch lifting axes; therefore a later G0 `single_motor_failure_requirement = continued_hover` would eliminate ordinary quad before detailed ESC sizing;
- T175 requires 43.75 kgf/axis just to hover and 70-78.75 kgf/axis in the two static-margin screening cases, making it the highest per-axis electrical-stress branch.

Screening status: `RETAIN` if motor-out continued hover is waived; `CONDITIONALLY_ELIMINATED` if motor-out continued hover is required.

### Hex

Strengths:
- lower per-axis thrust/power than quad;
- more control authority after a propulsion-unit loss, subject to flight-control/airframe proof;
- T175 screening gives 29.17 kgf hover and 46.67-52.50 kgf/axis at the two margin cases, near current heavy-agriculture propulsion capability.

Costs:
- six ESC/motor channels, +50% versus quad;
- additional harness, mass, maintenance and aerodynamic interaction.

Screening status: `RETAIN` across T125-T175 pending mass/reliability analysis.

### Octo / coaxial multi-rotor

Strengths:
- lowest per-unit thrust requirement of the compared architectures;
- strongest candidate when degraded-operation capability or compact multi-propeller packaging dominates.

Costs:
- eight propulsion channels;
- higher component/fault count;
- coaxial aerodynamic interaction and thermal/integration penalties require physical validation.

At T175, hover is 21.88 kgf/axis and the 1.6-1.8 screening points are 35.0-39.38 kgf/axis.

Screening status: `RETAIN`, particularly for redundancy-driven G0 outcomes; not selected by default.

## Decision tree for G1A

1. If G0 requires continued hover after one motor/ESC loss -> eliminate ordinary quad; compare hex versus octo/coaxial using mass, control authority, efficiency and span.
2. If that requirement is waived -> keep quad, hex and octo; use actual MTOW and span constraint to select.
3. If actual MTOW lands near the T125/T136 benchmark region and failure survival is waived -> quad has strong commercial precedent.
4. If actual MTOW approaches T175 -> do not default to quad; hex/multi-rotor must remain in the final trade because per-axis static thrust and electrical stress rise sharply.

This tree narrows the architecture space without inventing our vehicle requirement.

## What is now resolved

- UAV-002 has a controlled numerical sensitivity envelope and explicit elimination logic.
- Single-motor-failure policy is confirmed as a first-order G0 architecture discriminator.
- Quad is no longer treated as a neutral default for the entire 70-100 kg payload class.
- The benchmark/current evidence is sufficient for architecture screening; collecting more competitor products is not the critical path.

## Inputs still blocking G1A freeze

G0 must still supply or explicitly approve:
- nominal payload;
- actual/target airframe structural mass;
- battery mass / energy target;
- mission-equipment mass;
- resulting MTOW min/nom/max;
- mission duration / hover duration / reserve;
- environment and altitude;
- maximum span/coaxial constraints;
- degraded-operation and single-motor/ESC failure policy.

Until those are fixed, rotor count and thrust margin remain **OPEN** and UAV-004 cannot be frozen.
