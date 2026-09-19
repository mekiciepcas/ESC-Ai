# ESC electrical envelope — parametric pre-model

Date: 2026-09-19
Status: PRELIMINARY / NOT FROZEN
Backlog: dependency-opening work for UAV-006

## Purpose

Keep ESC sizing quantitative while G0 mission mass and UAV-004 operating points remain open. Values below are scenario calculations, not product ratings.

## Evidence anchors

Current primary-source propulsion references in `propulsion_benchmark.md` show:
- XAG P150 Max: 4.85 kW rated motor power, 140 A continuous ESC, 380 A/30 s maximum output current, 56 kgf maximum thrust/motor.
- Hobbywing X15 G2: 4.64 kW rated input, 69 V nominal/18S, 120 A continuous ESC, 300 A/3 s peak, 82 kgf max thrust, 37.5 kg recommended takeoff weight/axis.

These establish credible order-of-magnitude bounds only.

## Bus-current scenarios

`I_DC_ideal = P_electrical / V_bus`

| Per-axis electrical power | 52.5 V | 69 V | 75.6 V |
|---:|---:|---:|---:|
| 3.0 kW | 57.1 A | 43.5 A | 39.7 A |
| 4.0 kW | 76.2 A | 58.0 A | 52.9 A |
| 4.64 kW | 88.4 A | 67.2 A | 61.4 A |
| 5.0 kW | 95.2 A | 72.5 A | 66.1 A |
| 8.0 kW | 152.4 A | 115.9 A | 105.8 A |
| 10.0 kW | 190.5 A | 144.9 A | 132.3 A |

The 75.6 V column is full-charge 18S voltage and must not be used as nominal power-sizing voltage. Low-bus/end-of-discharge current is more severe and remains open until chemistry and minimum loaded voltage are fixed.

## Architecture scenarios from rotor study

### Scenario Q150 — 150 kg MTOW quad reference

- hover load: 37.5 kg/axis
- direct match to Hobbywing X15 G2 manufacturer recommended takeoff weight per axis
- source-backed rated input: 4.64 kW/axis
- source-backed ESC: 120 A continuous, 300 A/3 s

Implication: legacy 3 kW B1 is below the rated-input class of this direct commercial reference.

### Scenario H175 — 175 kg MTOW hex reference

- hover load: 29.17 kg/axis
- 1.6 study max thrust: 46.67 kg/axis
- 1.8 study max thrust: 52.5 kg/axis

This thrust range can fit current 55–60 kgf-class agricultural propulsion at the static-thrust level, but exact electrical power/current cannot be assigned until a manufacturer thrust/power table is selected. Therefore power/current remain OPEN.

### Scenario O175 — 175 kg MTOW octo reference

- hover load: 21.88 kg/axis
- 1.6 study max thrust: 35.0 kg/axis
- 1.8 study max thrust: 39.38 kg/axis

Per-axis electrical stress is lower than quad/hex, but total ESC count, mass, harness complexity and coaxial losses may dominate. No product rating is frozen.

## Required product-envelope fields

UAV-006 cannot close until all are evidence-backed:

| Field | Current state |
|---|---|
| VBUS minimum loaded | OPEN |
| VBUS nominal | OPEN |
| VBUS maximum charged | OPEN |
| VBUS transient ceiling | OPEN |
| continuous electrical power / ESC | OPEN |
| overload power + duration | OPEN |
| peak power + duration | OPEN |
| continuous DC current | OPEN |
| peak DC current | OPEN |
| continuous phase RMS current | OPEN |
| phase peak current | OPEN |
| motor electrical RPM maximum | OPEN |
| motor phase R/L | OPEN |
| PWM frequency | OPEN |
| current ripple target | OPEN |
| current-sense full scale | OPEN |
| baseplate/ambient design limits | OPEN |

## Hard design rules established now

1. DC bus current is not phase current. Do not size shunts/MOSFET phase current directly from `P/V`.
2. ESC continuous current and short peak current require explicit durations and recovery conditions.
3. Full-charge battery voltage is not sufficient for VDS selection; switching and energy-management transients require a separate ceiling.
4. Low loaded bus voltage must be used for worst-case DC current once chemistry/sag is known.
5. Phase-current requirements must come from motor operating data or validated motor model.
6. eRPM must come from motor pole count and maximum mechanical RPM; KV alone is insufficient for final timing validation.
7. Existing B1 80 A RMS / 120 A software / 150 A sense values remain reference-only.

## Immediate requalification flags for B1

- `3 kW`: insufficient as a universal target; source-backed quad reference is 4.64–4.85 kW rated/axis.
- `13S`: not frozen; 18S is a credible current-market alternative.
- `100 V FET`: requires transient-margin study, especially if 18S is selected.
- `20 kHz`: no product evidence yet; retain only as candidate.
- `2 FET/switch`: cannot be accepted before hot loss/current-sharing/thermal calculations.
- `0.5 mOhm shunt / gain 10`: cannot be accepted before phase-current envelope closes.

## Next calculation dependency

The highest-value next step is to obtain source-backed thrust/power/current tables for one or more propulsion candidates around the selected rotor architecture, then interpolate hover and max-thrust operating points into `propulsion_operating_points.json`. Until MTOW is frozen, maintain at least Q150, H175 and O175 scenarios rather than inventing a single aircraft mass.
