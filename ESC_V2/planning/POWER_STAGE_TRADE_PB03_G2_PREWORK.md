# Power-stage trade — PB-03 / G2 pre-freeze

Date: 2026-09-19  
Branch: `uav-rebaseline`  
Status: **S1.2/S1.5 PREWORK — NO PRODUCTION MPN OR PARALLEL COUNT FROZEN**

## Frozen parents

- U1 Rated bus: 18S, 66.6 V nominal convention / 75.6 V full charge / <=80 V outer full-charge ceiling.
- Repetitive controlled semiconductor-terminal stress: <=120 V.
- Power semiconductor class: >=150 V.
- Phase current: >=125 A RMS continuous, >=265 A RMS for >=3 s overload, >=375 A instantaneous phase-current peak.
- Phase-current measurement range: at least +/-400 A.

## Exact >=150 V candidate set

### A — Infineon IAUTN15S6N025G

- 150 V OptiMOS 6 automotive MOSFET.
- TOLG / PG-HSOG-8-1, bottom-side cooled.
- RDS(on) max 2.5 mOhm at VGS=10 V, ID=100 A, 25 C.
- ID headline/chip limit 245 A at 25 C; this is not used as inverter current capability.
- Qg 107 nC typ / 139 nC max at 75 V, 123 A, 10 V.
- Qgd 27 nC typ / 40 nC max.
- tr 54 ns typ, tf 51 ns typ at 75 V, 123 A, external RG=3.5 ohm.
- Qrr 23 nC typ / 46 nC max at 75 V, IF=50 A, di/dt=100 A/us.
- RthJC max 0.42 K/W.
- Tj range -55..175 C.

Primary source:
- https://www.infineon.com/part/IAUTN15S6N025G
- https://www.infineon.com/assets/row/public/documents/10/49/infineon-iautn15s6n025g-datasheet-en.pdf

Important evidence limitation: the datasheet provides a typical RDS(on)-versus-Tj curve but does not tabulate a guaranteed hot RDS(on) maximum in the same way as the Vishay comparison below. Production worst-case hot loss therefore cannot be frozen from the 25 C maximum alone.

### B — Infineon IAUTN15S6N025T

- Same 150 V / 2.5 mOhm OptiMOS 6 electrical class.
- TOLT / PG-HDSOP-16-1 top-side-cooled package.
- Qg 107 nC typ / 139 nC max.
- RthJC max 0.40 K/W.
- tr 65 ns typ, tf 60 ns typ under its datasheet switching condition.

Primary source:
- https://www.infineon.com/part/IAUTN15S6N025T
- https://www.infineon.com/assets/row/public/documents/10/49/infineon-iautn15s6n025t-datasheet-en.pdf

The TOLT package is an important U1 candidate because it permits a direct top-side thermal path to a baseplate/heatsink. This is a packaging advantage to test, not yet a product selection; the vehicle/baseplate mechanics are still open.

### C — Vishay SQJQ570ER

- 150 V automotive TrenchFET Gen V MOSFET.
- PowerPAK 8x8LR.
- RDS(on) max: 4.1 mOhm at 25 C, 8.1 mOhm at 125 C, 10.5 mOhm at 175 C, VGS=10 V.
- ID headline 189 A at TC=25 C / 109 A at TC=125 C; not used as the inverter design current.
- Qg 85 nC typ / 128 nC max at 75 V, 50 A, 10 V.
- Qrr 387 nC typ / 774 nC max at IF=40 A, di/dt=100 A/us.
- RthJC max 0.4 C/W.
- Tj range -55..175 C.

Primary source:
- https://www.vishay.com/docs/61616/sqjq570er.pdf

This part is useful as an independent-vendor 150 V comparison and has an explicit guaranteed hot RDS(on) table. Its hot conduction resistance and reverse-recovery charge are materially higher than the Infineon anchor under their respective datasheet test conditions, so it is retained as an alternate/reference rather than promoted as the primary electrical anchor.

## Conduction-only screen

For a balanced sinusoidal three-phase two-level inverter with synchronous conduction, a first-order total six-switch conduction screen is:

`Pcond_total ~= 3 * Iphase_rms^2 * RDS(on) / Nparallel`

This assumes ideal current sharing and excludes dead-time/body-diode conduction, switching loss, copper/package interconnect, temperature gradients and PWM ripple. It is therefore a **screening equation only**.

### Using Infineon 2.5 mOhm max at 25 C

| Parallel MOSFETs / switch | 125 A RMS continuous: six-switch Pcond | 265 A RMS overload: six-switch Pcond |
|---:|---:|---:|
| 1 | 117.2 W | 526.7 W |
| 2 | 58.6 W | 263.3 W |
| 3 | 39.1 W | 175.6 W |

Per physical MOSFET, the same screen is approximately:

| Parallel / switch | 125 A RMS | 265 A RMS |
|---:|---:|---:|
| 1 | 19.5 W/device | 87.8 W/device |
| 2 | 4.9 W/device | 21.9 W/device |
| 3 | 2.2 W/device | 9.8 W/device |

These are **25 C resistance screens**, not hot design losses. The Infineon typical temperature graph rises substantially with junction temperature, so hot worst-case loss will be higher and remains part of S1.2/S1.5.

### Vishay guaranteed-hot comparison at 125 C

Using the published 8.1 mOhm max at 125 C:

| Parallel MOSFETs / switch | 125 A RMS continuous: six-switch Pcond | 265 A RMS overload: six-switch Pcond |
|---:|---:|---:|
| 1 | 379.7 W | 1706.5 W |
| 2 | 189.8 W | 853.2 W |
| 3 | 126.6 W | 568.8 W |

This does not mean the Infineon device has already passed a hot-loss comparison; it illustrates why a guaranteed hot RDS(on) or a controlled worst-case scaling rule is required before exact parallel count is frozen.

## Gate-charge screen

At 10 V gate drive and maximum published Qg:

- Infineon 139 nC -> 1.39 uJ/gate cycle,
- Vishay 128 nC -> 1.28 uJ/gate cycle.

For one physical MOSFET this corresponds to idealized `Qg * Vg * fPWM` only:

| Candidate | 20 kHz | 24 kHz | 32 kHz | 40 kHz |
|---|---:|---:|---:|---:|
| Infineon 139 nC | 27.8 mW | 33.4 mW | 44.5 mW | 55.6 mW |
| Vishay 128 nC | 25.6 mW | 30.7 mW | 41.0 mW | 51.2 mW |

Actual gate-driver dissipation and switching loss are not equal to this gate-charge term.

## Reverse-recovery observation

The candidate datasheets use similar voltage and di/dt conditions but not identical current conditions. Under those datasheet conditions:

- Infineon Qrr max: 46 nC at 75 V / 50 A / 100 A/us,
- Vishay Qrr max: 774 nC at 40 A / 100 A/us.

This strongly favors keeping the Infineon OptiMOS 6 family as the current switching-loss anchor, but it is **not** a normalized apples-to-apples inverter loss result and does not freeze the MPN.

## Current pre-freeze disposition

1. **Primary electrical anchor:** Infineon IAUTN15S6N025G/T family.
2. **Thermal-package branch to study first:** IAUTN15S6N025T TOLT because U1 likely needs a direct baseplate thermal path; not frozen until the mechanical/thermal concept is defined.
3. **Independent supplier comparison:** Vishay SQJQ570ER.
4. **Parallel count:** OPEN. Analyze N=1/2/3; N=2 and N=3 are the priority layouts for hot-loss/current-sharing study. No production count is frozen from headline ID ratings.
5. **PWM:** OPEN. 20/24/32/40 kHz remain analysis points pending exact motor L and complete switching-loss evidence.

## Exact blockers before G2 selection

- exact production motor Ld/Lq/effective ripple inductance,
- hot worst-case RDS(on) policy for the chosen Infineon device or equivalent guaranteed production bound,
- operating-point switching energy / waveform correlation at intended VBUS, current, RG and layout,
- parallel current-sharing and gate-loop symmetry analysis,
- baseplate/TIM/copper thermal model,
- SOA / transient / repetitive-stress check at PB-03 overload current,
- availability/second-source/manufacturing review.

## No-release boundary

This file is G2 prework only. No exact MOSFET MPN, package, parallel count, PCB footprint, thermal solution or manufacturing BOM is released or frozen by this document.
