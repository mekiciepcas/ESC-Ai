# Low-power propulsion rebaseline — PB-07

Date: 2026-09-19  
Branch: `uav-rebaseline`  
Status: **PRODUCT REBASELINE / 1.5–3.0 kW TOTAL PROPULSION RANGE**

## Why this rebaseline exists

The product direction has changed. The earlier PB-02..PB-06 chain was sized around a 70–100 kg payload heavy-lift aircraft and therefore drove the vehicle toward roughly 20–25 kW hover power and very high whole-pack current. The new user-approved direction is to examine a substantially smaller vehicle whose **aggregate propulsion electrical input is in the 1.5–3.0 kW class**.

This document therefore retires the heavy-lift power/current sizing from the active product scope. PB-06 remains preserved as historical engineering work, but its 70–100 kg payload, 150/165/180 kg MTOW, X8/18S, >=5 kWh, 500 A continuous, 1050 A/3 s pack, >=150 V semiconductor and high phase-current requirements do not control PB-07.

The new goal is not to force a payload number before the propulsion and mass budget are re-derived. Payload and MTOW are reopened.

## Current primary-source propulsion anchors

### Hobbywing X8 G2 — 12S / MFP 30x11S

Manufacturer page: https://www.hobbywing.com/en/products/xrotor-x8-g2

Useful published values for the 12S class:
- compatible battery: 12S–14S LiPo,
- rated voltage: 12S 46 V / 14S 54 V,
- input range: 18–63 V,
- propulsion-system weight with cable and propellers: 1095 g,
- rated output power (max continuous): 810 W,
- recommended takeoff weight per axis: 5–7.5 kg at sea level,
- 12S load curve with MFP 30x11S provides thrust-versus-input-power data used below.

Selected 12S curve points used for interpolation:

| Input power / axis | Thrust / axis |
|---:|---:|
| 256.5 W | 2.968 kgf |
| 317.3 W | 3.493 kgf |
| 380.4 W | 3.999 kgf |
| 443.5 W | 4.476 kgf |
| 515.8 W | 4.994 kgf |
| 583.9 W | 5.456 kgf |
| 674.2 W | 6.043 kgf |
| 740.0 W | 6.452 kgf |
| 828.9 W | 6.977 kgf |

### T-Motor U8 Lite — independent cross-check

Manufacturer page: https://store.tmotor.com/product/u8-lite-kv85-u-efficiency.html

The published 12S / 48 V U8 Lite KV85 curve with G28x9.2 propeller is a useful independent check. Example points include roughly 4.468 kgf at 456 W, 5.248 kgf at 586 W and 6.352 kgf at 792 W. This broadly agrees with the Hobbywing power/thrust scale and therefore reduces dependence on one manufacturer's curve.

These products are **benchmarks, not selected production motor/ESC units**.

## Aggregate-power architecture screen

Linear interpolation of the Hobbywing 12S curve gives the following first-order screen. `MTOW @ 1.6 T/W` is only a sizing screen: total static thrust divided by 1.6. It is not a flight-qualified vehicle mass.

| Total propulsion input | Architecture | Power / axis | Interpolated thrust / axis | Total static thrust | MTOW screen @ 1.6 T/W |
|---:|---|---:|---:|---:|---:|
| 1.5 kW | Quad | 375 W | 3.956 kgf | 15.823 kgf | 9.889 kg |
| 1.5 kW | Hexa | 250 W | 2.907 kgf | 17.440 kgf | 10.900 kg |
| 2.0 kW | Quad | 500 W | 4.881 kgf | 19.523 kgf | 12.202 kg |
| 2.0 kW | Hexa | 333 W | 3.622 kgf | 21.729 kgf | 13.581 kg |
| 2.5 kW | Quad | 625 W | 5.723 kgf | 22.893 kgf | 14.308 kg |
| 2.5 kW | Hexa | 417 W | 4.273 kgf | 25.639 kgf | 16.024 kg |
| 3.0 kW | Quad | 750 W | 6.511 kgf | 26.044 kgf | 16.278 kg |
| 3.0 kW | Hexa | 500 W | 4.881 kgf | 29.285 kgf | 18.303 kg |

T-Motor's independent 12S curve gives approximately 6.13 kgf at 750 W and 4.73 kgf at 500 W, corresponding to about 15.3 kg quad and 17.7 kg hexa MTOW screens at 1.6 T/W. That is close enough to the Hobbywing-derived 16.3 / 18.3 kg screens to treat **roughly 15–18 kg MTOW at the 3 kW upper study point** as a credible market-anchored exploration band, pending exact motor/prop selection and vehicle mass closure.

## Architecture interpretation

For the same aggregate electrical input, the hexa screen produces more total thrust because each rotor operates at a lower, more efficient point on these large-propeller curves. The trade is two additional motors/ESCs/arms and extra vehicle mass.

Therefore:
- **Hexa is the leading architecture candidate** for the 3 kW upper study point.
- **Quad remains the mass/cost-minimizing alternate.**
- Neither rotor count is FROZEN yet.
- Coaxial X8 is no longer the baseline and should not be carried forward automatically.

## Battery-voltage screen

A 12S architecture is a strong first candidate because both current propulsion references operate directly in this class and the total current becomes manageable:

- 12S LiPo convention, 44.4 V nominal: 3.0 kW / 44.4 V ~= 67.6 A total.
- 12S 3.6 V/cell convention, 43.2 V nominal: 3.0 kW / 43.2 V ~= 69.4 A total.
- 12S at 3.0 V/cell loaded floor, 36.0 V: 3.0 kW / 36.0 V ~= 83.3 A total.

This is fundamentally different from the PB-06 500–1050 A whole-pack architecture. A 14S option remains worth screening for lower current and voltage headroom; exact series count is not yet frozen.

## 10-minute energy sensitivity

The previously accepted >=10 minute mission target and 20% gross-energy reserve can be retained as a provisional mission target while the new vehicle is re-sized. If the aggregate propulsion input were held constant for the full 10 minutes, the first-order gross pack energy before battery/auxiliary losses would be:

| Constant aggregate power | 10 min terminal energy | Gross energy with 20% reserve |
|---:|---:|---:|
| 1.5 kW | 250 Wh | 312.5 Wh |
| 2.0 kW | 333 Wh | 416.7 Wh |
| 2.5 kW | 417 Wh | 520.8 Wh |
| 3.0 kW | 500 Wh | 625 Wh |

The 3 kW row is a worst-case constant-power sizing sensitivity, not the expected average mission power.

### P50B 12S3P / 12S4P calculation anchors

Using the already-recorded Molicel P50B manufacturer data from PB-05 (3.6 V nominal, 18.0 Wh typical / 17.5 Wh minimum, max cell mass 71 g, 60 A continuous headline):

- 12S3P = 36 cells, 15 Ah nominal, 648 Wh typical / 630 Wh minimum cell energy, <=2.556 kg cells only.
- 12S4P = 48 cells, 20 Ah nominal, 864 Wh typical / 840 Wh minimum cell energy, <=3.408 kg cells only.
- At 83.3 A pack current, 3P is ~27.8 A/cell and 4P is ~20.8 A/cell by arithmetic.

12S3P is therefore a useful lightweight calculation candidate, but its 630 Wh minimum cell energy leaves essentially no allowance above the 625 Wh constant-3-kW/10-min/20%-reserve screen. 12S4P gives much more energy/aging/thermal margin. Neither topology is selected or physically qualified.

## Implication for the custom ESC

The new product direction moves the custom ESC back toward a practical 12S, sub-kilowatt-per-channel regime:

- Hexa at 3 kW aggregate: about 500 W continuous study load per ESC.
- Quad at 3 kW aggregate: about 750 W continuous study load per ESC.
- Exact short-duration per-channel peak remains OPEN until thrust margin and rotor count are selected.
- Previous PB-06 >=4.8 kW continuous / >=11.5 kW short-duration **per ESC** is retired from active scope.
- Previous PB-03 125 A RMS / 265 A RMS / 375 A peak phase requirements are retired from active scope.
- Previous >=150 V semiconductor requirement is retired from active scope; 80/100 V-class parts may re-enter the candidate trade after the new transient requirement is derived.
- Legacy B1's 3 kW / approximately 48 V / 100 V-MOSFET / DRV8353-era work becomes relevant again as a **candidate reuse source**, but it must be requalified against the new UAV motor/propeller and fault requirements rather than copied unchanged.

## PB-07 decisions supported by this study

1. **FROZEN PRODUCT DIRECTION:** aggregate propulsion electrical-input study/product-family range = **1.5–3.0 kW**.
2. **FROZEN REBASELINE ACTION:** PB-06 heavy-lift payload/MTOW/X8/18S/high-current electrical sizing is historical and no longer active product authority.
3. **RETAINED NON-CONFLICTING TARGET:** >=10 min nominal mission target and 20% gross-energy reserve remain active targets pending new mass/mission closure.
4. **CANDIDATE, NOT FROZEN:** Hexa is the leading rotor architecture candidate; Quad is the alternate.
5. **CANDIDATE, NOT FROZEN:** 12S is the leading battery-voltage candidate; 14S remains an alternate.
6. **OPEN:** exact payload, MTOW, rotor count, motor/prop MPN, battery S/P topology, ESC channel power/current, phase current, PWM, semiconductor class, protection thresholds and thermal design.

## Next closure sequence

`PB-07 power range -> select Quad/Hexa + MTOW/payload band -> select 12S/14S + mission energy -> freeze per-ESC electrical envelope -> re-audit B1/Faz2/Faz3 reuse -> motor inductance/PWM -> protection/thermal -> G1 -> G2 -> U1-SCH-R001`

## Evidence boundary

All vehicle mass values in this document are curve-derived sizing screens. No flight, thermal, endurance, battery, motor or ESC physical validation is claimed. Exact production selections remain OPEN unless explicitly marked FROZEN in PB-07.