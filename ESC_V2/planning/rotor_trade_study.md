# Rotor architecture trade study — preliminary

Date: 2026-09-19
Status: PRELIMINARY / G0 NOT CLOSED
Branch: `uav-rebaseline`
Backlog: UAV-002

## Purpose

Compare rotor-count implications before selecting the propulsion architecture. This study uses source-backed market MTOW examples only as benchmark cases. It does **not** freeze our MTOW or thrust margin.

## Benchmark MTOW cases

Current heavy agricultural products span approximately:
- 125 kg: XAG P150 maximum spraying takeoff weight, 70 kg payload.
- 136 kg: XAG P150 Max maximum spraying takeoff weight, 80 kg payload.
- 175 kg: DJI Agras T100 maximum spraying takeoff weight, 100 kg payload.

Primary sources:
- https://www.xa.com/en/p150/p150specs
- https://xa.com/en/p150max/p150maxspecs
- https://ag.dji.com/t100/specs

A 150 kg intermediate case is included only to show sensitivity.

## Calculation method

For N lifting axes and aircraft mass M:

`hover_thrust_per_axis_kgf = M / N`

Two preliminary static thrust-to-weight study cases are shown:
- 1.6: lower benchmark study case.
- 1.8: higher benchmark study case.

These are **not standards and not frozen requirements**. They were selected because current products show similar order-of-magnitude static margin: XAG P150 is approximately 1.76 using published maximum single-motor thrust and maximum spraying MTOW, while XAG P150 Max is approximately 1.65.

## Required thrust per lifting axis

| MTOW | Axes | Hover kgf/axis | Max kgf/axis @ T/W 1.6 | Max kgf/axis @ T/W 1.8 |
|---:|---:|---:|---:|---:|
| 125 kg | 4 | 31.25 | 50.00 | 56.25 |
| 125 kg | 6 | 20.83 | 33.33 | 37.50 |
| 125 kg | 8 | 15.63 | 25.00 | 28.13 |
| 136 kg | 4 | 34.00 | 54.40 | 61.20 |
| 136 kg | 6 | 22.67 | 36.27 | 40.80 |
| 136 kg | 8 | 17.00 | 27.20 | 30.60 |
| 150 kg | 4 | 37.50 | 60.00 | 67.50 |
| 150 kg | 6 | 25.00 | 40.00 | 45.00 |
| 150 kg | 8 | 18.75 | 30.00 | 33.75 |
| 175 kg | 4 | 43.75 | 70.00 | 78.75 |
| 175 kg | 6 | 29.17 | 46.67 | 52.50 |
| 175 kg | 8 | 21.88 | 35.00 | 39.38 |

## Reality checks against current propulsion systems

### Quad class

XAG P150:
- quad-rotor,
- max MTOW 125 kg,
- 55 kgf max thrust per motor.

This corresponds to 31.25 kgf hover load per rotor and approximately 1.76 maximum static thrust/weight ratio from published values.

XAG P150 Max:
- 4 motors,
- max MTOW 136 kg,
- 56 kgf max thrust per motor.

This corresponds to 34 kgf hover load per rotor and approximately 1.65 maximum static thrust/weight ratio.

Hobbywing X15 G2:
- recommended takeoff weight per axis 37.5 kg,
- max thrust 82 kgf per axis,
- 18S / 69 V,
- rated input power 4.64 kW.

Four X15 G2 axes correspond to 150 kg manufacturer-recommended takeoff mass total, which is directly relevant to the middle of our benchmark range.

### Coaxial architecture

DJI T100:
- maximum spraying MTOW 175 kg,
- coaxial dual-rotor propulsion,
- 82 kgf single-axis maximum thrust.

This is important evidence that the upper end of the requested payload class can drive the vehicle toward coaxial/multi-rotor architecture when compact footprint and redundancy are desired. Public DJI product data is insufficient to derive the ESC current rating, so T100 is not used for electrical sizing.

## Architecture implications

### Quad

Advantages:
- minimum ESC/motor count,
- lowest component and harness count,
- fewer failure points and simpler maintenance,
- current commercial precedent exists at 70–80 kg agricultural payload.

Challenges:
- each ESC/motor is high power,
- no single-motor-out hover capability in an ordinary quad,
- at the 175 kg class, each axis must produce 43.75 kgf just to hover and roughly 70–79 kgf for the two study margins.

Preliminary conclusion:
- very credible around ~125–150 kg MTOW with X15-class propulsion,
- increasingly demanding at ~175 kg MTOW unless using very large propulsion units.

### Hex

Advantages:
- lowers per-axis thrust and ESC power,
- potentially better degraded-control options than quad,
- easier to reach upper MTOW without 70–80 kgf class single-axis propulsion.

Challenges:
- +50% motors/ESCs versus quad,
- more wiring, mass, cost and maintenance,
- propeller/airframe interference and disk-loading must be checked.

At 175 kg MTOW:
- hover = 29.2 kgf/axis,
- 1.6 study max = 46.7 kgf/axis,
- 1.8 study max = 52.5 kgf/axis.

This sits near the capability of current 55–60 kgf agricultural propulsion systems.

### Octo / coaxial-octo

Advantages:
- significantly lower thrust requirement per propulsion unit,
- strongest path toward motor-out/degraded-mode capability,
- compact coaxial implementations are demonstrated commercially.

Challenges:
- eight ESCs/motors increase cost, mass and fault-count,
- coaxial pairs incur aerodynamic interaction losses,
- thermal, harness and flight-control integration are more complex.

At 175 kg MTOW:
- hover = 21.9 kgf/axis,
- 1.6 study max = 35.0 kgf/axis,
- 1.8 study max = 39.4 kgf/axis.

This shifts each ESC into a substantially easier electrical range, but increases system count and redundancy-management requirements.

## What can be concluded now

1. A 70–100 kg **payload** target cannot be translated directly into an ESC rating. Airframe, battery and mission-system mass are first-order inputs.
2. Current agricultural products indicate a plausible MTOW envelope roughly from 125 kg to 175 kg for the requested payload class, but this is benchmark evidence only.
3. Quad is demonstrably realizable at 70–80 kg payload and about 125–136 kg MTOW.
4. Around 150 kg MTOW, an X15 G2 class 18S propulsion system is a realistic quad reference.
5. At ~175 kg MTOW, quad becomes a very high per-axis power problem; hex or coaxial/multi-rotor deserves a formal reliability/mass/efficiency comparison.
6. The legacy 3 kW B1 power target cannot be frozen until rotor architecture is selected. For a heavy quad, source-backed commercial references are closer to ~4.6–5 kW rated input per axis, with much higher transient capability.

## Open inputs blocking rotor freeze

G0 must still supply:
- actual/target airframe structural mass,
- battery mass and energy target,
- nominal payload inside the 70–100 kg range,
- mission duration / hover duration,
- target altitude and maximum ambient temperature,
- maximum vehicle span constraint,
- requirement for single-motor/ESC failure survival or explicit waiver.

Until these are fixed, rotor count remains **OPEN**.
