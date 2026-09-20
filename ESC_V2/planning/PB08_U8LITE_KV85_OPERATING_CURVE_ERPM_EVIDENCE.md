# PB-08 U8 Lite KV85 operating-curve / eRPM evidence

Date: 2026-09-20
Branch: `uav-rebaseline`
Status: TRADE EVIDENCE — NOT PRODUCT SELECTION / NOT PHYSICAL VERIFICATION

## Purpose

Reduce S1R.4 uncertainty using current primary-source manufacturer data without freezing a motor/propeller that has not yet passed the PB-08 mass/architecture trade.

## Primary-source evidence

T-Motor's current U8 Lite product page publishes for the KV85 variant:

- rated voltage: 12S,
- configuration: 36N42P,
- motor mass incl. cable: 243 g,
- interphase resistance: 225 +/- 5 mOhm,
- recommended propeller class: 28–29 inch,
- peak current (180 s): 19.1 A,
- max power (180 s): 916.8 W.

The same manufacturer page publishes a 12S (48 V) bench curve for U8 Lite KV85 with G28x9.2 CF. Relevant points are:

| Throttle | Thrust g | Current A | RPM | Input power W |
|---:|---:|---:|---:|---:|
| 60% | 2957 | 5.10 | 2190 | 245 |
| 70% | 3662 | 7.10 | 2439 | 341 |
| 80% | 4468 | 9.50 | 2680 | 456 |
| 90% | 5248 | 12.20 | 2917 | 586 |
| 100% | 6352 | 16.50 | 3200 | 792 |

Manufacturer source: https://store.tmotor.com/product/u8-lite-kv85-u-efficiency.html (accessed 2026-09-20).

Important identity boundary: the published curve is explicitly for **G28x9.2 CF**. The prior PB-08 mass evidence used manufacturer material pairing KV85 with NS28x9.2. These are not silently treated as the same propeller. Therefore this curve is valid as a KV85/28-inch operating-envelope anchor, but it does not by itself freeze the exact production motor+prop MPN.

## Derived electrical-speed envelope

42 poles = 21 pole pairs.

Electrical RPM is:

`eRPM = mechanical_RPM * pole_pairs`

For the published G28x9.2 curve:

| Throttle | Mechanical RPM | Derived eRPM |
|---:|---:|---:|
| 60% | 2190 | 45,990 |
| 70% | 2439 | 51,219 |
| 80% | 2680 | 56,280 |
| 90% | 2917 | 61,257 |
| 100% | 3200 | 67,200 |

Thus a controller intended to cover this published KV85 operating curve must accommodate at least **67.2 keRPM electrical** at the manufacturer's 48 V bench condition, before any explicit engineering margin. This is a derived trade bound, not a frozen PB-08 controller requirement because exact production propeller, bus operating point and motor selection remain OPEN.

Electrical fundamental at 67.2 keRPM is `67,200 / 60 = 1,120 Hz`.

## PB-08 implications

1. The current PB-08 ESC hardware capability of >=1.0 kW continuous input is not contradicted by this motor curve: the published KV85/G28x9.2 maximum point is 792 W input. This is compatibility evidence only, not thermal qualification.
2. The published 19.1 A / 180 s motor rating and 16.5 A curve maximum are below PB-08's >=30 A continuous / >=50 A for >=3 s ESC hardware capability, so this candidate does not consume the frozen DC-current capability. Again, this is not a selected motor.
3. The 42-pole count materially constrains PWM/control timing: the published maximum curve point reaches 1.12 kHz electrical fundamental. PWM remains OPEN because exact production motor inductance and switching-loss/ripple closure are absent.
4. DC input current is not phase RMS/peak current. No phase-current requirement is inferred from the manufacturer DC-current column.

## What this evidence does not prove

- exact NS28x9.2 operating curve,
- phase RMS/peak current,
- winding inductance Ld/Lq,
- PWM frequency,
- hot copper loss or ESC thermal performance,
- <=75 V switch-terminal stress,
- flight performance,
- production motor/propeller selection.

## Next use

Use this evidence after Quad/Hexa/MTOW closure to determine whether U8 Lite KV85 remains inside the selected thrust/power operating region. If it does, obtain the exact selected propeller curve/MPN and motor inductance evidence (or execute the controlled impedance measurement procedure) before closing phase-current/PWM requirements.
