# PB-08 common electrical platform and Quad/Hexa mass roll-up

Date: 2026-09-19  
Branch: `uav-rebaseline`  
Status: **CONTROLLED DESIGN BASELINE / PHYSICAL VERIFICATION OPEN**

## Purpose

PB-07 changed the active vehicle from the former heavy-lift scope to a 1.5–3.0 kW **aggregate** propulsion family. This study closes the common electrical platform that can serve both the active Quad and Hexa candidates without prematurely freezing rotor count, payload, exact motor or exact battery cell.

The design philosophy is to size the first custom ESC and main battery bus for the **3.0 kW upper continuous product point**, then obtain 1.5–2.5 kW variants by command/thermal derating rather than by redesigning the basic power stage.

## Primary-source anchors

### Hobbywing X8 G2

Manufacturer: https://www.hobbywing.com/en/products/xrotor-x8-g2  
Specification PDF: https://www.hobbywing.com/en/uploads/file/20260104/45ecf2bddd8e4de289472f8d3acd4061.pdf

Published values used here:
- 12S–14S LiPo compatible,
- 12S rated voltage 46 V,
- 18–63 V input range,
- 1095 g propulsion-system weight including cable and propeller,
- rated power input 920 W / rated output 810 W,
- ESC continuous current 20 A and 80 A peak for 3 s,
- motor 100 KV / 36N40P,
- MFP 30x11S propeller.

### T-Motor U8 Lite KV85

Manufacturer: https://store.tmotor.com/product/u8-lite-kv85-u-efficiency.html

Published values used as an independent low-mass propulsion reference:
- 12S rated,
- motor mass including cable 243 g,
- 36N42P,
- G28x9.2 propeller recommendation,
- 916.8 W maximum power for 180 s,
- published 12S thrust/power curve.

The T-Motor reference shows that the 1095 g Hobbywing integrated axis is conservative for a custom motor + custom ESC implementation; however an exact installed custom-axis mass is **not** frozen until motor, propeller, ESC enclosure, cable and arm-end hardware are selected.

### Molicel P50B calculation cell

Manufacturer datasheet: https://www.molicel.com/wp-content/uploads/Product-Data-Sheet-of-INR-21700-P50B-80122.pdf

Published values used only for calculation:
- 3.6 V nominal / 4.2 V charge,
- 5.0 Ah typical,
- 18.0 Wh typical / 17.5 Wh minimum,
- 71 g maximum cell mass,
- 60 A continuous discharge headline,
- 12.8 mOhm typical DC impedance at the datasheet reference condition.

Exact production cell remains OPEN.

## Quad versus Hexa mass roll-up at the 3 kW screen

PB-07 manufacturer-curve screens at 1.6 T/W gave:
- Quad MTOW screen: 16.278 kg,
- Hexa MTOW screen: 18.303 kg.

Therefore the Hexa gains 2.025 kg of screened MTOW capacity at equal 3 kW aggregate power.

Using the conservative Hobbywing X8 G2 integrated mass anchor of 1.095 kg per axis:

| Item | Quad | Hexa |
|---|---:|---:|
| MTOW screen | 16.278 kg | 18.303 kg |
| Propulsion-system mass | 4.380 kg | 6.570 kg |
| Remaining after propulsion | 11.898 kg | 11.733 kg |
| Remaining after propulsion + P50B 12S3P cells-only (2.556 kg) | 9.342 kg | 9.177 kg |
| Remaining after propulsion + P50B 12S4P cells-only (3.408 kg) | 8.490 kg | 8.325 kg |

On this conservative integrated reference, Quad retains 0.165 kg more residual mass before frame/avionics/pack-hardware/payload because the two additional propulsion units cost 2.190 kg while the Hexa MTOW screen only rises 2.025 kg.

The architecture break-even installed propulsion mass is:

`(18.303 - 16.278) / 2 = 1.0125 kg per additional axis`

Interpretation:
- if the eventual **installed custom propulsion axis** is heavier than about 1.01 kg, Quad has the better residual mass budget even before accounting for two additional arms;
- if it is substantially lighter than about 1.01 kg, Hexa can retain a mass-budget advantage before additional structural mass;
- exact frame/arm mass and failure-policy value are therefore still required before rotor count can be frozen.

No payload number is fabricated from this table. `remaining` includes frame, arms, avionics, pack enclosure/interconnect/BMS, landing gear, wiring, mission hardware and payload.

## Frozen PB-08 common bus

The common platform is frozen to **12S high-rate lithium** for the first design family.

Controlled bus values:
- series count: **12S**,
- nominal bus convention: **43.2 V** using a 3.6 V/cell high-rate Li-ion reference,
- full charge: **50.4 V** using 4.2 V/cell,
- minimum loaded bus for full rated ESC power: **36.0 V**,
- below 36.0 V: power derating and mission-termination policy is required; exact hard battery cutoff remains pack-specific.

Rationale:
- both current propulsion anchors directly support 12S,
- 3.0 kW aggregate requires only 69.4 A at 43.2 V nominal and 83.3 A at the 36 V loaded floor,
- 12S keeps strong compatibility with legacy B1's broad ~48 V hardware class,
- 14S reduces current modestly but increases voltage stress and provides no demonstrated system-level benefit large enough to justify a second first-prototype bus.

## Frozen PB-08 custom ESC hardware capability

The custom ESC is intentionally over-capable relative to the normal per-axis load so the same board can serve either Quad or Hexa and can absorb short maneuver/failure redistribution without a redesign.

Per ESC hardware capability requirements:
- continuous DC input power: **>=1.0 kW**,
- short-duration DC input power: **>=1.5 kW for >=3 s**,
- continuous DC input current: **>=30 A**,
- short-duration DC input current: **>=50 A for >=3 s**.

At the 36 V full-rated-power floor:
- 1.0 kW requires 27.8 A, so 30 A gives electrical capability margin;
- 1.5 kW requires 41.7 A, so 50 A gives additional transient margin.

These are **per-channel hardware capabilities**, not a statement that all channels may be commanded to 1.0/1.5 kW simultaneously. Vehicle-level aggregate normal propulsion remains bounded by the PB-07 1.5–3.0 kW family requirement; vehicle peak policy remains OPEN until rotor count/thrust margin is frozen.

## Frozen semiconductor voltage class

For the 12S platform:
- power-semiconductor VDS class: **>=100 V**,
- repetitive controlled switch-terminal stress design target: **<=75 V**,
- normal operation shall not rely on repetitive MOSFET avalanche.

The <=75 V value is a design requirement to be demonstrated by DC-link/layout/snubber/clamp design and later switching tests. It is **not** a measured overshoot result. Exact MOSFET MPN, parallel count and gate driver remain OPEN.

This makes the legacy B1 100 V MOSFET / DRV8353-era architecture relevant for requalification, but does not approve any historical component automatically.

## 3 kW variant energy target

For 10 minutes at a hypothetical constant 3.0 kW propulsion input:
- terminal energy = 500 Wh,
- preserving 20% gross energy reserve requires 625 Wh gross before auxiliary/conversion/aging margin.

PB-08 therefore freezes a **>=750 Wh gross rated pack-energy target for the 3 kW upper variant**. The extra margin is deliberate so the pack is not designed to the mathematical 625 Wh edge.

P50B calculation references:
- 12S3P: 630 Wh minimum / 648 Wh typical, <=2.556 kg cells only — useful for lower-power variants but too close to the 3 kW/10 min edge;
- 12S4P: 840 Wh minimum / 864 Wh typical, <=3.408 kg cells only — preferred calculation topology for the 3 kW variant.

`12S4P P50B` is a **calculation/reference topology**, not an exact cell selection or qualified pack. Pack hardware mass, cold/low-SOC/aged sag, fusing, BMS, service disconnect, interconnect temperature rise and enclosure remain OPEN.

## Current architecture decision status

Frozen now:
- 1.5–3.0 kW aggregate product family (PB-07),
- 3.0 kW upper continuous design point,
- 12S common bus,
- 43.2 V nominal / 50.4 V full / 36.0 V full-power loaded floor,
- >=750 Wh gross target for the 3 kW variant,
- per-ESC >=1.0 kW / >=30 A continuous,
- per-ESC >=1.5 kW / >=50 A for >=3 s,
- >=100 V MOSFET class and <=75 V repetitive controlled terminal-stress target.

Still OPEN:
- Quad versus Hexa,
- exact payload/MTOW and structural mass,
- exact motor/propeller,
- exact battery cell/P-count/pack mass,
- vehicle peak aggregate power and single-motor-failure behavior,
- phase RMS/peak current and sensing range,
- PWM/eRPM,
- exact MOSFET/count, driver, DC-link, protection and thermal design.

## Next design action

The next closure should use this common electrical platform to:
1. set a realistic installed propulsion-axis mass target for the custom motor/ESC/prop assembly;
2. close Quad versus Hexa together with degraded-mode policy;
3. derive payload/MTOW from a full frame + battery-hardware + avionics + mission-equipment mass roll-up;
4. then select exact motor/propeller and derive phase current/PWM.

No schematic revision is allocated by this study.