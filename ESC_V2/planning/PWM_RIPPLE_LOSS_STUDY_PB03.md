# PWM / ripple / switching-loss study — PB-03

Date: 2026-09-19
Status: **S1.2 ACTIVE — BOUNDED, NOT FROZEN**
Baseline: `PRODUCT_BASELINE_PB-03.json`

## Purpose

Quantify the PWM timing constraint and establish an evidence-backed 150 V semiconductor calculation anchor without inventing the exact production motor inductance or switching-energy data.

## Frozen parents

- Controller capability: >=60,000 electrical rpm.
- Phase-current capability: >=125 A RMS continuous, >=265 A RMS for >=3 s, >=375 A instantaneous phase peak.
- Current-measurement range: at least +/-400 A.
- Semiconductor voltage class: >=150 V.
- U1 Rated bus: 18S, 66.6 V nominal convention, 75.6 V full charge, <=80 V outer full-charge ceiling.

## Electrical-speed timing bound

60,000 electrical rpm = 1,000 electrical Hz, therefore one electrical period is 1.000 ms.

Candidate PWM timing density at the controller capability limit:

| PWM | Period | PWM periods / electrical period at 60 keRPM |
|---:|---:|---:|
| 20 kHz | 50.00 us | 20 |
| 24 kHz | 41.67 us | 24 |
| 32 kHz | 31.25 us | 32 |
| 40 kHz | 25.00 us | 40 |

This table is a deterministic timing calculation, not a PWM selection. Control-loop/ADC scheduling must be demonstrated against the eventual MCU and modulation implementation.

## Motor evidence boundary

Hobbywing's current X13 G2 primary product data confirms the reference class as 45 KV, 36N42P, 18S and MFP 56x20, and publishes load curves with thrust/current/input power/RPM/torque/output power. The public specification used in this study does **not** provide a production winding phase inductance or resistance value suitable for a defensible current-ripple calculation.

Therefore the study SHALL NOT fabricate Ld/Lq/phase-L from geometry, KV, or competitor assumptions. Exact current ripple remains OPEN until one of these exists:

1. exact production-motor datasheet Ld/Lq or phase inductance with measurement convention; or
2. controlled impedance/step-response measurement on the selected motor.

Required measurement record: rotor state/angle, test frequency, line-line vs phase convention, temperature, instrument, and uncertainty.

## 150 V semiconductor anchor

A current primary-source candidate is Infineon `IAUTN15S6N025G` (OptiMOS 6, TOLG): 150 V VDS, 2.5 mOhm max RDS(on) at 10 V, 245 A ID at 25 C, 948 A pulsed-current headline rating, 107 nC typical / 139 nC maximum gate charge at 10 V, RthJC max 0.42 K/W, -55..175 C operating range. These are component data, not proof that one device per switch is adequate.

For comparison, `IAUTN15S6N025T` provides the same 150 V / 2.5 mOhm class in a top-side-cooled TOLT package with RthJC max 0.40 K/W. Package choice remains G2 work.

### Gate-charge-only drive-energy screening

Using Qg(max)=139 nC and 10 V gate drive, idealized gate-charge power per MOSFET is `Qg * Vg * fPWM`:

- 20 kHz: 0.0278 W/device
- 24 kHz: 0.0334 W/device
- 32 kHz: 0.0445 W/device
- 40 kHz: 0.0556 W/device

For six switches and N parallel MOSFETs per switch, idealized total gate-charge power is six times N times the above. This excludes driver quiescent loss, bootstrap loss and transition overlap; it is only a gate-drive sizing term.

## What cannot yet be calculated defensibly

- motor current ripple versus PWM frequency: blocked by winding Ld/Lq/phase-L;
- exact MOSFET switching loss: blocked by operating-point Eon/Eoff or waveform-based transition data under the intended gate resistance/layout;
- dead-time optimum: blocked by exact MOSFET reverse-conduction/body-diode behavior and gate-loop implementation;
- exact MOSFET parallel count: blocked by hot RDS(on), switching loss, PCB/baseplate thermal impedance and current-sharing implementation.

Headline ID/IDpulse values are not used as design current ratings.

## S1.2 disposition

S1.2 has made measurable progress but does **not** close G1-07. The safe result is:

- timing domain quantified at the frozen >=60 keRPM controller requirement;
- 20/24/32/40 kHz remain analysis points, not frozen product values;
- a current exact 150 V MOSFET family is established as a calculation anchor;
- the missing motor-inductance evidence is now the precise blocker for ripple-based PWM selection.

Next safe work: obtain/source the exact production winding inductance or define the motor impedance measurement procedure; in parallel continue 150 V candidate hot-conduction/switching/thermal prework without selecting an MPN prematurely.

## Evidence

Primary sources consulted 2026-09-19:

- Hobbywing X13 G2 product/specification and manufacturer load-performance data.
- Infineon IAUTN15S6N025G product page.
- Infineon IAUTN15S6N025T product page.

Physical correlation remains mandatory at later gates.