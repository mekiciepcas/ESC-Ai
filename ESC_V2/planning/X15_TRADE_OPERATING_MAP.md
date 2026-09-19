# X15 G2 trade-only operating map

Date: 2026-09-19
Status: `ASSUMPTION_FOR_TRADE_ONLY / SOURCE_INTERPOLATED`

This map linearly interpolates only inside the repository's manufacturer X15 G2 69 V / MFP 63x24 measured curve. It does not extrapolate, does not select the product rotor architecture, and does not populate product requirements. T125/T150/T175 and 1.6x/1.8x thrust factors are governed trade-only cases.

Values shown are per axis: `current A / input power kW / RPM`.

| MTOW case | rotors | hover kgf | hover | 1.6x thrust | 1.8x thrust |
|---|---:|---:|---|---|---|
| T125 | 4 | 31.25 | 51.0 / 3.52 / 1469 | 105.0 / 7.25 / 1857 | **127.1 / 8.77 / 1971** |
| T125 | 6 | 20.83 | 27.6 / 1.91 / 1198 | 56.3 / 3.88 / 1517 | 67.3 / 4.64 / 1609 |
| T125 | 8 | 15.63 | 18.5 / 1.27 / 1042 | 36.4 / 2.51 / 1312 | 43.5 / 3.00 / 1393 |
| T150 | 4 | 37.50 | 67.3 / 4.64 / 1609 | **141.7 / 9.78 / 2036** | **173.7 / 11.99 / 2160** |
| T150 | 6 | 25.00 | 36.4 / 2.51 / 1312 | 74.3 / 5.12 / 1662 | 89.0 / 6.14 / 1763 |
| T150 | 8 | 18.75 | 23.8 / 1.64 / 1137 | 47.9 / 3.31 / 1439 | 57.3 / 3.96 / 1527 |
| T175 | 4 | 43.75 | 85.2 / 5.88 / 1738 | **185.2 / 12.78 / 2200** | **227.9 / 15.72 / 2326** |
| T175 | 6 | 29.17 | 45.9 / 3.17 / 1419 | 94.2 / 6.50 / 1795 | 113.5 / 7.83 / 1903 |
| T175 | 8 | 21.88 | 29.8 / 2.06 / 1227 | 60.5 / 4.18 / 1555 | 72.5 / 5.00 / 1649 |

## Continuous-current screening
Hobbywing's repository evidence records the X15 G2 ESC at 120 A continuous and 300 A/3 s. Bold entries exceed 120 A and therefore must not be treated as continuous operating points for this reference propulsion unit. This is only a screening comparison; a product overload duration is not yet defined.

- T125 quad: hover and 1.6x are below 120 A; 1.8x is above.
- T150 quad: both 1.6x and 1.8x are above 120 A.
- T175 quad: both 1.6x and 1.8x are far above 120 A; 1.8x is close to the measured curve maximum (246.6 A) and remains bench-reference only.
- T175 hex: 1.8x remains just below the published 120 A continuous-current number in the 69 V curve interpolation, but no thermal/endurance qualification is implied.
- All octo points in these governed cases remain below 120 A in this curve.

## Architecture implication
For the X15 reference only, increasing rotor count sharply reduces per-axis electrical stress. T150/T175 quad creates high-thrust points beyond the X15 published continuous-current rating, while hex/octo retain more current margin. This is not sufficient to select hex/octo: vehicle mass, redundancy policy, packaging, efficiency, cost, failure behavior and final propulsion selection remain open.

## Evidence and limitations
- Source data: `x15g2_operating_curve.json`, manufacturer bench curve at 69 V and MFP 63x24.
- Interpolation: piecewise linear between adjacent measured thrust rows only.
- No voltage scaling, altitude correction, propeller scaling or thermal extrapolation is used.
- DC input current is not phase current. These values must not populate phase-current requirements.
- RPM is mechanical prop/motor RPM. Electrical RPM requires confirmed pole-pair count.
