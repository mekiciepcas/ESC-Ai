# PB-03 power-stage hot conduction / thermal sensitivity

Date: 2026-09-19 21:18+03:00  
Branch: `uav-rebaseline`  
Status: **S1.2/S1.5 BOUNDED PREWORK — NOT A HOT RDS(ON) GUARANTEE, NOT A MOSFET COUNT FREEZE**

## Purpose

Extend `POWER_STAGE_TRADE_PB03_G2_PREWORK.md` without inventing a guaranteed hot RDS(on) value for the current Infineon anchor. This study converts the unresolved hot-resistance uncertainty into an explicit sensitivity variable and quantifies its effect on N=2/N=3 parallel branches.

## Frozen parents

- >=150 V MOSFET class.
- >=125 A RMS continuous phase current.
- >=265 A RMS phase-current overload for >=3 s.
- IAUTN15S6N025T/G remains a calculation anchor only; exact MPN/count/package are OPEN.

## Primary-source anchor

Infineon currently lists `IAUTN15S6N025T` as active/preferred, 150 V, 2.5 mOhm max RDS(on) at 10 V, 245 A headline ID at 25 C, 139 nC maximum gate charge, 0.4 K/W maximum RthJC, -55..175 C, TOLT PG-HDSOP-16-1. The datasheet revision used by this project is Rev. 1.0 dated 2025-05-14.

Sources:
- https://www.infineon.com/part/IAUTN15S6N025T
- https://www.infineon.com/assets/row/public/documents/10/49/infineon-iautn15s6n025t-datasheet-en.pdf

The published temperature curve is typical rather than a guaranteed hot maximum. Therefore no curve multiplier is promoted to a production limit here.

## Sensitivity method

Let `Khot = RDS(on)_hot / RDS(on)_25C_max_anchor`.

For screening only:

`Rhot_screen = 2.5 mOhm * Khot`

`Pcond_total ~= 3 * Iphase_rms^2 * Rhot_screen / Nparallel`

The study points Khot=1.6, 2.0 and 2.3 are deliberately **sensitivity points**, not requirements, measurements, guaranteed limits or inferred datasheet maxima. They show how strongly the architecture depends on the unresolved hot-resistance policy.

## Results

| Khot sensitivity | N / switch | 125 A RMS total conduction | per physical FET | 265 A RMS total conduction | per physical FET |
|---:|---:|---:|---:|---:|---:|
| 1.6 | 2 | 93.8 W | 7.8 W | 421.4 W | 35.1 W |
| 1.6 | 3 | 62.5 W | 3.5 W | 280.9 W | 15.6 W |
| 2.0 | 2 | 117.2 W | 9.8 W | 526.7 W | 43.9 W |
| 2.0 | 3 | 78.1 W | 4.3 W | 351.1 W | 19.5 W |
| 2.3 | 2 | 134.8 W | 11.2 W | 605.7 W | 50.5 W |
| 2.3 | 3 | 89.8 W | 5.0 W | 403.8 W | 22.4 W |

These values exclude switching loss, reverse conduction, copper/interconnect loss, PWM ripple, current-sharing error and thermal coupling.

## Junction-to-case-only sanity screen

Using the TOLT anchor's published maximum RthJC=0.4 K/W, the **device-internal junction-to-case rise from conduction alone** would be `DeltaT_JC = Pdevice * 0.4 K/W`. This is not junction temperature because case-to-TIM/baseplate/ambient resistance is still unknown.

At the most severe sensitivity point Khot=2.3:

- N=2, 125 A: 11.2 W/device -> about 4.5 K junction-to-case rise from conduction only.
- N=3, 125 A: 5.0 W/device -> about 2.0 K.
- N=2, 265 A: 50.5 W/device -> about 20.2 K during the 3 s overload screen before transient thermal impedance is considered.
- N=3, 265 A: 22.4 W/device -> about 9.0 K under the same deliberately simplified steady RthJC multiplication.

For a 3 s pulse, steady RthJC multiplication is not the correct final transient-junction model. The exact transient thermal impedance curve, initial temperature, switching loss and baseplate/TIM path must be applied before overload acceptance.

## Engineering disposition

1. N=1 is no longer a priority architecture branch for detailed thermal work; its 25 C conduction screen was already 117.2 W total at 125 A and 526.7 W at 265 A before hot scaling. This is a trade-study disposition, not a formal prohibition.
2. N=2 remains viable enough to retain, but hot conduction uncertainty makes it highly sensitive to baseplate/TIM and switching-loss closure.
3. N=3 remains the lower-conduction reference branch and should be carried through the same switching/current-sharing/layout model; its extra gate charge, area and sharing complexity must not be ignored.
4. TOLT remains the first package branch for thermal integration because the top-side path is explicit, but it is not frozen.
5. No G1 row changes from this study. PWM and exact MOSFET count remain OPEN.

## Exact next evidence needed

- guaranteed production hot-RDS policy or manufacturer-supported worst-case bound for the intended Infineon device,
- switching-energy/waveform correlation at intended bus/current/RG/layout,
- transient ZthJC extraction for the >=3 s overload case,
- case-to-TIM/baseplate resistance and baseplate temperature target,
- parallel current-sharing/layout tolerance model,
- exact motor inductance/effective PWM-ripple evidence before PWM freeze.

## No-release boundary

This is calculation sensitivity only. It does not qualify a MOSFET, thermal stack, PCB, inverter, or propulsion system and does not authorize U1 schematic allocation or production release.
