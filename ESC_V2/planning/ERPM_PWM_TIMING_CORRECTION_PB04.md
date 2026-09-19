# PB-04 eRPM capability correction and PWM timing screen

Date: 2026-09-19  
Branch: `uav-rebaseline`  
Status: **eRPM FROZEN / PWM STILL OPEN**

## Why PB-03 needed a correction

PB-03 inherited a controller capability target of **>=60,000 eRPM** from PB-02. That value was referenced to the loaded Hobbywing X13 G2 manufacturer curve maximum of 2478 rpm with a 42-pole motor:

`2478 rpm * 21 pole pairs = 52,038 eRPM`

The loaded curve is useful operating evidence, but it is not a complete controller-speed bound because the product baseline separately freezes:

- propulsion class: **45 rpm/V**;
- reference pole count: **42 poles / 21 pole pairs**;
- ESC outer full-charge input ceiling: **80 V DC**.

A no-load linear speed screen at that frozen outer bus boundary gives:

`80 V * 45 rpm/V = 3600 rpm mechanical`

and therefore:

`3600 rpm * 21 = 75,600 eRPM`

A 60 keRPM controller capability would therefore sit below the simple frozen-envelope speed screen.

## PB-04 corrective freeze

PB-04 changes the controller electrical-speed capability requirement to:

**>=90,000 eRPM**

This provides approximately:

`90,000 / 75,600 - 1 = 19.0%`

headroom above the no-load linear screen.

This is a **controller capability requirement**, not a claim that a 56x20 propeller will operate at 90 keRPM-equivalent electrical speed in normal flight.

## PWM timing density at 90 keRPM

90,000 eRPM corresponds to:

`90,000 / 60 = 1500 electrical Hz`

Electrical period:

`1 / 1500 = 666.7 us`

| PWM | PWM period | PWM periods / electrical period at 90 keRPM | Disposition |
|---:|---:|---:|---|
| 20 kHz | 50.0 us | 13.3 | boundary / low-loss sensitivity |
| 24 kHz | 41.7 us | 16.0 | preferred analysis candidate |
| 32 kHz | 31.25 us | 21.3 | preferred analysis candidate |
| 40 kHz | 25.0 us | 26.7 | boundary / higher-switching-loss sensitivity |

No universal minimum PWM-to-electrical-frequency ratio is asserted here. Final acceptance must come from current-ripple, sampling/control timing and physical switching evidence.

## Exact-device switching timing screen

Current 150 V calculation anchor: Infineon `IAUTN15S6N025T`.

Primary datasheet switching conditions:

- VDD = 75 V;
- VGS = 10 V;
- ID = 123 A;
- RG = 3.5 ohm;
- typical rise time `tr = 65 ns`;
- typical fall time `tf = 60 ns`;
- Qg typical 107 nC, maximum 139 nC;
- Qrr typical 23 nC, maximum 46 nC under the datasheet's separate reverse-recovery test condition.

Source: Infineon IAUTN15S6N025T datasheet Rev. 1.0, 2025-05-14.

A simple hard-switch overlap screen using:

`E_overlap_screen = 0.5 * VDD * ID * (tr + tf)`

gives approximately:

`E_overlap_screen ~= 0.577 mJ per complete turn-on + turn-off transition pair`

At the datasheet test point, the corresponding per-active-device-lane screening term is:

| PWM | overlap screen |
|---:|---:|
| 20 kHz | 11.5 W |
| 24 kHz | 13.8 W |
| 32 kHz | 18.5 W |
| 40 kHz | 23.1 W |

These values are **not guaranteed Eon/Eoff losses**. They are a normalized timing-based sensitivity screen only. They exclude Coss energy, reverse recovery, dead-time conduction, stray inductance, gate-loop behavior, actual modulation transition count, hot-device timing, parallel-device dynamic current sharing and PCB layout.

## Gate-charge burden

Using Qg(max)=139 nC and 10 V gate drive:

`Pgate/device = Qg * Vg * fPWM`

| PWM | idealized gate-charge power / MOSFET |
|---:|---:|
| 20 kHz | 0.0278 W |
| 24 kHz | 0.0334 W |
| 32 kHz | 0.0445 W |
| 40 kHz | 0.0556 W |

Gate-charge power is not the dominant inverter switching loss term in this screen, but it scales directly with both PWM frequency and parallel MOSFET count.

## S1.2 decision

- **FROZEN:** controller capability >=90 keRPM.
- **BOUNDED / preferred analysis window:** 24-32 kHz.
- **BOUNDARY sensitivity points:** 20 kHz and 40 kHz.
- **OPEN:** final PWM frequency.

Final PWM freeze still requires exact production-motor Ld/Lq or an equivalent measured ripple inductance. The existing `MOTOR_IMPEDANCE_MEASUREMENT_PROCEDURE_PB03.md` remains the required physical path if manufacturer winding data cannot be obtained.
