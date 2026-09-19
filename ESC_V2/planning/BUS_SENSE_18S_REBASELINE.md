# 18S DC-bus sensing rebaseline

Date: 2026-09-19
Status: CALCULATED_CANDIDATE_NOT_FROZEN

## Existing B1 divider
B1 uses Rtop = 2 x 49.9 kΩ and Rbottom = 3.32 kΩ. Divider ratio = 3.32/(99.8+3.32) = 0.0321955.

At the 18S full-charge candidate (75.6 V), ideal ADC input is 2.434 V. Ideal 3.3 V ADC full-scale corresponds to 102.50 V bus. Therefore the old B1 text's 80 V point is a check point, not the mathematical measurement ceiling.

This does NOT qualify the existing divider for the UAV product: tolerance, ADC/reference error, clamp leakage/injection, RC settling, ADC acquisition time and the still-open transient ceiling must be included before freeze.

## Candidate measurement ranges
The measurement full-scale and protection trip are deliberately separate requirements. Firmware must not rely on ADC saturation as over-voltage protection.

Using 3.3 V nominal ADC reference:

| Intended nominal bus full-scale | Required divider ratio | Example concept | 75.6 V ADC level | Status |
|---|---:|---|---:|---|
| existing ~102.5 V | 0.03220 | 2x49.9k / 3.32k | 2.434 V | legacy candidate; too close to an unresolved 100 V-class transient domain |
| ~120 V | 0.02750 | resistor values TBD after tolerance/error optimization | 2.079 V | preferred study range if transient ceiling stays below ~120 V |
| ~150 V | 0.02200 | resistor values TBD after tolerance/error optimization | 1.663 V | study range if 150 V-class domain is required; lower nominal resolution |

No E-series resistor set is frozen here because the required transient ceiling is not frozen.

## Requirements created
1. `VBUS_MEAS_FS` must exceed the highest voltage that telemetry/diagnostics are expected to resolve, including defined diagnostic headroom.
2. Hardware over-voltage action must have a separately justified threshold/path; ADC full scale is not a protective clamp.
3. Divider resistor working voltage and pulse rating are checked per physical resistor, not only total resistance.
4. ADC pin injection during bus over-range is checked against MCU limits and clamp network behavior.
5. RC source impedance and acquisition time are verified at the selected STM32G474 ADC sampling configuration if STM32 remains the MCU.
6. Phase-voltage channels must be re-scaled consistently if they are expected to observe the same DC-link domain.

## Decision
Do not change the B1 schematic yet. Keep the existing divider as historical B1 evidence and carry ~120 V and ~150 V measurement ranges into the G2 sensing trade. Final resistor values follow the transient ceiling and semiconductor/driver domain decision.
