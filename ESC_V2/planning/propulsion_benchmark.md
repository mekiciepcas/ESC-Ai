# Heavy-lift agricultural UAV propulsion benchmark

Date: 2026-09-19
Status: SOURCE-BACKED PRELIMINARY EVIDENCE — NOT A DESIGN FREEZE
Branch: `uav-rebaseline`
Backlog: UAV-003

## Purpose

Establish a reality check for the 70–100 kg payload ESC program using current heavy agricultural UAV and integrated propulsion systems. This file is evidence for sizing; it does not by itself freeze rotor count, battery voltage, ESC current, or semiconductor class.

## Source hierarchy

Only manufacturer primary sources are used for numerical benchmark values in this revision.

## 1. XAG P150 Agricultural Drone

Primary sources:
- https://www.xa.com/en/p150
- https://www.xa.com/en/p150/p150specs

Verified data:
- Architecture: quad-rotor (manufacturer product page explicitly describes quad-rotor design)
- Aircraft mass with RevoSpray system and batteries: 54 kg
- Maximum spraying takeoff weight: 125 kg
- Maximum payload: 70 kg
- Motor: A55
- Maximum thrust per motor: 55 kgf
- Rated power per motor: 4700 W
- ESC: XESC-F360
- ESC continuous current: 120 A
- ESC maximum operating current: 360 A for 30 s
- Propeller diameter: 1530 mm
- Battery rated output: 48.75 V / 140 A
- Battery capacity: 20 Ah (~975 Wh)
- Recommended operating temperature: 0–40 °C
- Ingress protection: IPX6K

Derived, for comparison only:
- Hover thrust at 125 kg MTOW: 31.25 kgf/rotor
- Total published maximum thrust: 220 kgf
- Static max-thrust/weight ratio at 125 kg MTOW: 1.76
- Installed motor rated-power sum: 18.8 kW

Important note: the battery rated-output entry is not assumed to equal the complete aircraft transient propulsion current. Battery topology/quantity and power-path behavior must be verified from an authoritative system diagram/manual before it is used for our pack sizing.

## 2. XAG P150 Max Agricultural Drone

Primary source:
- https://xa.com/en/p150max/p150maxspecs

Verified data:
- Motor quantity: 4
- Empty mass with RevoSpray and B141050 batteries: 56 kg
- Maximum spraying takeoff weight: 136 kg
- Maximum payload: 80 kg
- Maximum thrust per motor: 56 kgf
- Rated power per motor: 4850 W
- ESC continuous operating current: 140 A
- ESC maximum output current: 380 A for 30 s
- Propeller diameter: 1600 mm
- Battery rated output: 52.5 V / 140 A
- Battery capacity: 20 Ah (~1050 Wh)
- Recommended operating temperature: 0–40 °C
- Ingress protection: IPX6K

Derived, for comparison only:
- Hover thrust at 136 kg MTOW: 34.0 kgf/rotor
- Total published maximum thrust: 224 kgf
- Static max-thrust/weight ratio at 136 kg MTOW: 1.65
- Installed motor rated-power sum: 19.4 kW

## 3. DJI Agras T100

Primary sources:
- https://ag.dji.com/t100/specs
- https://ag.dji.com/t100
- https://ag.dji.com/it/t100

Verified data:
- Maximum spraying takeoff weight: 175 kg
- Operating payload: 100 kg
- Spraying aircraft weight: 75 kg
- Propulsion architecture: coaxial dual-rotor
- Single-axis maximum thrust: 82 kgf
- Motor stator: 155 × 16 mm
- Motor KV: 60 rpm/V
- Propeller diameter: 62 in
- Product specification lists 8 propeller pairs
- Operating temperature: 0–40 °C
- Maximum wind resistance: <6 m/s

Use restriction:
DJI does not expose ESC continuous/peak current and detailed motor electrical operating-point data on the public product specification page. T100 is therefore used as a vehicle/propulsion-architecture benchmark, not as a source for our ESC current rating.

## 4. Hobbywing X15 G2 integrated propulsion system

Primary source:
- https://www.hobbywing.com/en/uploads/file/20260114/8edfaf2969be848410994360b6ac2487.pdf

Verified data:
- Intended use: heavy agricultural UAV propulsion
- Maximum thrust: 82 kgf at sea level
- Recommended takeoff weight per axis: 37.5 kg
- Rated voltage: 69 V, 18S LiPo
- Input-voltage range: 25–80 V
- Rated power input: 4640 W
- Rated power output: 3971 W
- ESC continuous current: 120 A
- ESC peak current: 300 A for 3 s
- Motor KV: 45 rpm/V
- Motor: 36N44P, stator 156 × 23 mm
- Propeller: 63 × 24 in
- Communication: Cyphal/UAVCAN, RS485 optional/customizable
- Operating temperature: -20–50 °C
- Ingress protection: IPX6

Manufacturer-reported thrust table demonstrates that peak full-throttle input power is far above the rated continuous input power. This reinforces the need to define separate continuous, overload and short peak envelopes in our ESC requirements.

## 5. Hobbywing X13 G2 integrated propulsion system

Primary sources:
- https://www.hobbywing.com/en/uploads/file/20260203/1e9df37cb5554eb55b76ed0d76c8dfc9.pdf
- https://www.hobbywing.com/en/products/x13-g2

Verified data:
- Maximum thrust: 60 kgf at sea level
- Recommended takeoff weight per axis: 27 kg
- Rated voltage: 69 V, 18S LiPo
- Input range: 25–80 V
- Rated input power: 3160 W
- Rated output power: 2700 W
- ESC continuous current: 70 A
- ESC peak current: 200 A for 3 s
- Motor KV: 45 rpm/V
- Propeller: 56 × 20 in
- Operating temperature: -20–50 °C
- Ingress protection: IPX6

## Engineering conclusions from the benchmark

### C1 — Legacy B1 3 kW must not be treated as the heavy-lift product rating

Current real agricultural systems around the requested payload class use roughly 4.6–5.0 kW rated motor input/power per axis in quad-class solutions, with much larger short-duration electrical headroom. The previous 3 kW candidate may still be useful for lower-load architectures or a test platform, but it is not evidence of suitability for the target aircraft.

### C2 — Two legitimate voltage/current design families are visible

1. ~50–53 V bus with very high ESC current capability (XAG P150/P150 Max).
2. 18S / ~69 V nominal with lower current for comparable continuous power and 78–80 V class input limit (Hobbywing X15/X13 G2).

The UAV program must explicitly trade these architectures rather than inherit 13S by default.

### C3 — Continuous and transient ratings must be separate

Examples:
- XAG P150: 120 A continuous, 360 A / 30 s maximum operating current.
- XAG P150 Max: 140 A continuous, 380 A / 30 s.
- Hobbywing X15 G2: 120 A continuous, 300 A / 3 s.
- Hobbywing X13 G2: 70 A continuous, 200 A / 3 s.

Therefore our requirements must include at least: continuous current, overload current + duration, peak current + duration, and thermal recovery assumptions.

### C4 — A realistic vehicle MTOW benchmark for the payload range is approximately 125–175 kg

This is not our design requirement yet. It is an observed product range:
- 70 kg payload: XAG P150 up to 125 kg spraying MTOW.
- 80 kg payload: XAG P150 Max up to 136 kg spraying MTOW.
- 100 kg payload: DJI T100 up to 175 kg spraying MTOW.

Our MTOW remains OPEN until airframe, battery, task-system and reserve requirements are fixed.

### C5 — Legacy B1 electrical class needs re-sizing before schematic/power-PCB freeze

The following remain OPEN until UAV-001/002/004/005/006 close:
- bus voltage and transient ceiling,
- semiconductor voltage class,
- continuous/peak phase current,
- DC-link capacitance and ripple current,
- parallel FET count,
- switching frequency,
- gate-driver current capability,
- shunt value/range,
- connector/cable/busbar class,
- cooling/baseplate architecture.

## Next use of this evidence

- UAV-001: use only to bound a plausible benchmark MTOW range; do not replace user/system requirements.
- UAV-002: compare quad/hex/octo/coaxial rotor loading against 125–175 kg benchmark MTOW cases.
- UAV-004: select actual propulsion candidates only after mission/MTOW freeze.
- UAV-005/006: derive battery and ESC electrical envelopes from selected operating points, not from legacy B1 values.
