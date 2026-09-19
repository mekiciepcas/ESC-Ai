# X15 G2 scenario mapping — benchmark only

Date: 2026-09-19
Status: CALCULATED_FROM_PRIMARY_CURVE / NOT_PRODUCT_FREEZE
Source data: `x15g2_operating_curve.json`, Hobbywing X15 G2, 69 V, MFP 63x24.

This mapping linearly interpolates between adjacent manufacturer bench rows. It is useful for architecture comparison only. It is not a substitute for our final motor/prop selection, altitude/temperature correction, or phase-current measurement.

## Selected benchmark cases

| MTOW / architecture | Axis point | Required thrust kgf | DC current A | Input kW | Evidence |
|---|---|---:|---:|---:|---|
| 125 kg quad | hover | 31.25 | 51.0 | 3.52 | interpolated |
| 125 kg quad | 1.6x total thrust | 50.00 | 105.0 | 7.25 | interpolated |
| 125 kg quad | 1.8x total thrust | 56.25 | 127.1 | 8.77 | interpolated |
| 136 kg quad | hover | 34.00 | 58.0 | 4.00 | interpolated |
| 136 kg quad | 1.6x | 54.40 | 120.3 | 8.31 | interpolated |
| 136 kg quad | 1.8x | 61.20 | 146.5 | 10.11 | interpolated |
| 150 kg quad | hover | 37.50 | 67.3 | 4.64 | interpolated; matches manufacturer recommended-axis region |
| 150 kg quad | 1.6x | 60.00 | 141.7 | 9.78 | interpolated |
| 150 kg quad | 1.8x | 67.50 | 173.7 | 11.99 | interpolated |
| 175 kg quad | hover | 43.75 | 85.2 | 5.88 | interpolated |
| 175 kg quad | 1.6x | 70.00 | 185.2 | 12.78 | interpolated |
| 175 kg quad | 1.8x | 78.75 | 227.9 | 15.72 | interpolated |
| 175 kg hex | hover | 29.17 | 45.9 | 3.17 | essentially manufacturer 29.168 kgf row |
| 175 kg hex | 1.6x | 46.67 | 94.2 | 6.50 | interpolated |
| 175 kg hex | 1.8x | 52.50 | 113.5 | 7.83 | interpolated |
| 175 kg octo | hover | 21.88 | 29.8 | 2.06 | interpolated |
| 175 kg octo | 1.6x | 35.00 | 60.5 | 4.18 | interpolated |
| 175 kg octo | 1.8x | 39.38 | 72.5 | 5.00 | interpolated |

## Findings

- A 150 kg quad puts hover almost exactly at X15 G2's manufacturer-recommended 37.5 kg/axis region; the published rated input is 4.64 kW.
- A 175 kg quad moves hover above the recommended-axis load and a 1.6–1.8 static margin requires roughly 12.8–15.7 kW DC input per axis on this specific bench curve. This is a very different peak problem from the legacy 3 kW B1.
- A 175 kg hex moves hover to about 29.2 kgf and 1.8x static thrust to about 52.5 kgf, materially reducing per-ESC electrical stress.
- A 175 kg octo lowers the 1.8x point to about 5.0 kW/axis but doubles propulsion-unit count versus quad.
- The X15 G2 ESC is published as 120 A continuous and 300 A/3 s peak. Some interpolated static high-thrust points exceed 120 A, therefore those points cannot be treated as continuous operating points.
- DC current in this table is not phase RMS or phase peak current. Phase-current sensing and silicon conduction design remain OPEN until motor electrical parameters/control operating points are established.

## Decision consequence

Do not freeze the legacy 3 kW/80 A B1 as the heavy-UAV power stage. Keep it as a reusable control/protection reference. Rotor architecture and mission inputs must close before product ESC continuous/peak ratings are frozen.
