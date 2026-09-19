# S1.1 Phase-current model — PB-02 propulsion class

Date: 2026-09-19  
Branch: `uav-rebaseline`  
Status: **CLOSED_FOR_G1_DESIGN_REQUIREMENT / PHYSICAL_CORRELATION_PENDING**  
Parent baseline: `PRODUCT_BASELINE_PB-02.json`

## Purpose

Derive the U1 Rated **phase-current design envelope** from motor torque/back-EMF evidence instead of copying DC-bus current into the phase-current domain.

This record closes Sprint S1.1 at the **system-requirement** level. It is not a claim that the custom motor, inverter or coaxial vehicle has already been measured at these currents.

## Source anchors

### Current X13 G2 propulsion anchor

Hobbywing X13 G2, MFP 56x20, 69 V manufacturer curve:

- 45 KV,
- 36-slot / 42-pole,
- 138 x 25 mm stator,
- 18S,
- 70 A continuous / 200 A 3 s ESC DC rating,
- 27 kg recommended axis load,
- 60 kg maximum isolated thrust,
- load table includes thrust, DC current, input power, RPM, torque and mechanical output power.

Primary sources:

- https://www.hobbywing.com/en/products/x13-g2
- https://www.hobbywing.com/en/uploads/file/20260203/1e9df37cb5554eb55b76ed0d76c8dfc9.pdf

### Electrical-constant proxy

The previous Hobbywing X13 18S / 45 KV motor is used **only as an electrical-constant proxy** because it shares the same 45 KV, 138 x 25 mm stator class and 42-pole electromagnetic class, while the X13 G2 public documents do not publish winding resistance / inductance / back-EMF constants.

Published X13 18S / 45 KV values:

- stator resistance: 21.6 mOhm,
- stator self-inductance: 29.147 uH as published by the regional manufacturer channel,
- mutual inductance: 41.839 uH as published,
- back-EMF: 13.7 Vpk/krpm,
- back-EMF: 8.92 Vrms/krpm,
- 21 pole pairs.

Reference:

- https://www.hobbywingdirect.com/collections/xrotor-x13-system/01-aircraft

The resistance/inductance values are **not** used to freeze S1.1 phase current; they are carried into S1.2 as proxy evidence requiring revalidation. S1.1 uses the two published back-EMF constants to form a bounded torque-constant model.

## Torque-constant bounding method

For a sinusoidal PMSM/BLDC phase-current model, treating the published back-EMF values as line-to-line constants gives two independent RMS torque-constant estimates:

- from 13.7 Vpk/krpm: `Kt_rms = sqrt(3/2) * Ke_LL_peak = 0.1602 N.m/A_rms`,
- from 8.92 Vrms/krpm: `Kt_rms = sqrt(3) * Ke_LL_rms = 0.1475 N.m/A_rms`.

Because the two published values are not perfectly related by `sqrt(2)`, S1.1 does **not** choose one as exact. The conservative current estimate uses the lower torque constant, 0.1475 N.m/A_rms; the 0.1602 value defines the lower-current side of the model band.

This is deliberately more conservative than deriving phase current from DC current or throttle percentage.

## G2 load-curve operating points

Interpolating only between adjacent manufacturer X13 G2 MFP56x20 69 V points gives:

| PB-02 point | Isolated thrust | Torque | DC current | Input power | RPM |
|---|---:|---:|---:|---:|---:|
| Max-MTOW hover | 26.471 kgf | 15.257 N.m | 44.23 A | 3.053 kW | 1632 |
| 27 kg rated-class point | 27.000 kgf | 15.563 N.m | 45.56 A | 3.145 kW | 1648 |
| One-channel-loss landing | 30.252 kgf | 17.431 N.m | 54.07 A | 3.731 kW | 1744 |
| Normal 1.6 T/W point | 42.353 kgf | 24.412 N.m | 90.81 A | 6.264 kW | 2058 |
| Published curve maximum | 60.077 kgf | 34.930 N.m | 165.5 A | 11.419 kW | 2478 |

These are manufacturer isolated-rotor data/reference interpolations, not custom coaxial measurements.

## Derived phase-current band

Using `I_phase_rms = torque / Kt_rms`:

| Point | Phase RMS model band |
|---|---:|
| Max-MTOW hover | 95.2–103.4 A RMS |
| 27 kg rated point | 97.1–105.5 A RMS |
| One-channel-loss landing | 108.8–118.1 A RMS |
| Normal 1.6 T/W | 152.4–165.5 A RMS |
| Published curve maximum | 218.0–236.8 A RMS |

## Frozen G1 design requirements from S1.1

The following values are **design-capability requirements**, not measured operating currents:

1. **Continuous phase-current capability: >=125 A RMS per motor phase.**
   - Conservative rated-point model upper bound: 105.5 A RMS.
   - 15% model/design allowance gives 121.3 A RMS.
   - Rounded upward to 125 A RMS.
   - Also covers the modeled one-channel-loss landing point of 118.1 A RMS before physical correlation.

2. **Short-duration phase-current capability: >=265 A RMS for >=3 s.**
   - Manufacturer curve maximum model upper bound: 236.8 A RMS.
   - 10% model/design allowance gives 260.4 A RMS.
   - Rounded upward to 265 A RMS.

3. **Instantaneous sinusoidal phase-current peak design capability: >=375 A peak during the >=3 s overload interval.**
   - `265 A_rms * sqrt(2) = 374.8 A_peak`.

4. **Current-sense measurement range: at least +/-400 A instantaneous phase current.**
   - Provides measurement headroom above the 375 A design peak.
   - Hardware trip threshold remains OPEN and will be set in S1.4/G2 below the measurement saturation boundary.

## What is frozen and what remains open

Frozen by the S1.1 additive baseline decision:

- `G1-03`: >=125 A RMS continuous phase-current capability,
- `G1-04`: >=265 A RMS phase overload for >=3 s and >=375 A instantaneous phase peak capability,
- `G1-08`: phase-current sensing range >= +/-400 A.

Still OPEN:

- exact production motor/propeller MPN,
- exact X13 G2 winding resistance/inductance,
- PWM frequency,
- current ripple target,
- OCP threshold and end-to-end fault latency,
- exact shunt/CSA implementation,
- exact MOSFET MPN/count and thermal path.

## Required physical correlation

Before G6 propulsion verification, the selected production motor shall be characterized or supplier-qualified for:

- line-line resistance,
- phase/line inductance versus rotor position where relevant,
- back-EMF constant and waveform,
- phase RMS and peak current at hover / rated / maneuver points,
- DC-to-phase current correlation,
- winding and magnet temperature behavior.

If measured production-motor phase current exceeds this frozen design envelope, the product baseline must be revised before release; the requirement shall not be silently stretched.

## Engineering boundary

This model is valid for sizing the U1 inverter and sensing architecture. It does not prove semiconductor junction temperature, current sharing, current-sense accuracy, motor thermal capability, coaxial aerodynamics, or flight performance. Those remain later-gate verification items.
