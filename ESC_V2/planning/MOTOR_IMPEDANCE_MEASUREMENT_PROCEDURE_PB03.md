# Motor impedance / inductance measurement procedure — PB-03

Date: 2026-09-19  
Branch: `uav-rebaseline`  
Status: **DEFINED / RESULTS NOT PERFORMED**  
Parent sprint: S1.2 PWM / ripple / switching-loss closure

## Purpose

Provide a controlled, reproducible way to close the exact production-motor winding resistance and inductance blocker before freezing PWM/current-ripple requirements.

This procedure intentionally contains **no fabricated result values**. All result fields remain `OPEN/null` until a selected production motor is physically measured or the same quantities are supplied by the manufacturer with an explicit measurement convention.

## Safety / test boundary

- Remove the propeller. No propeller is permitted for this electrical characterization.
- Mechanically secure the motor and lock the rotor only with a fixture rated for the small-signal/low-energy test torque.
- Use an isolated/current-limited low-energy test source or LCR/impedance analyzer.
- Do not energize the production 18S propulsion bus for this test.
- Keep excitation below a level that causes measurable winding heating or rotor movement.
- Record winding temperature before and after each measurement set.

This is an engineering characterization procedure, not a high-power motor test.

## Required identification

Record before testing:

- manufacturer,
- exact motor MPN / revision / serial number,
- winding connection if documented: WYE / DELTA / UNKNOWN,
- pole count / pole pairs,
- nominal KV,
- test instrument make/model/serial/calibration date,
- fixture/cable length and compensation method,
- winding temperature,
- rotor mechanical locking method.

## Measurement A — line-to-line DC resistance

Measure all three pairs:

- U-V,
- V-W,
- W-U.

Preferred method: 4-wire Kelvin milliohm measurement or controlled DC injection with independent current and voltage measurement.

Record:

- injected current,
- measured voltage,
- calculated R_LL,
- winding temperature,
- lead/fixture compensation,
- uncertainty.

Acceptance for model use:

- all three line-line values reported,
- spread quantified,
- no conversion to phase resistance until winding topology is confirmed.

## Measurement B — small-signal line-to-line impedance vs rotor angle

With rotor locked, measure U-V impedance while stepping rotor electrical position through at least one electrical period. If precise electrical-angle indexing is unavailable, use enough mechanical positions to capture minimum and maximum line-line inductive impedance.

Recommended frequencies:

- 100 Hz,
- 1 kHz,
- 5 kHz,
- 10 kHz,
- optionally 20 kHz if instrument accuracy remains adequate.

At every point record:

- rotor mechanical/electrical position or indexed fixture position,
- frequency,
- test amplitude,
- R-series / ESR reported by instrument,
- L-series or complex impedance magnitude/phase,
- winding temperature.

Repeat for V-W and W-U at representative min/max inductance positions.

## Measurement C — low-voltage step response cross-check

Purpose: independently cross-check effective electrical time constant in the current path used by the inverter.

Method:

1. Lock rotor and keep propeller removed.
2. Apply a low-voltage current-limited step line-to-line through a known switching/test fixture.
3. Measure voltage and current with time-synchronized probes.
4. Fit the early current response to an RL model only over the region where back-EMF is zero and magnetic nonlinearity is negligible.
5. Record effective `tau = L/R` and the fitted line-line R/L with uncertainty.

Do not force a single RL fit if the waveform shows saturation, fixture resonance or non-first-order behavior; retain the raw waveform and mark the fit INVALID.

## Conversion policy

Raw line-line results are the authority. Conversion to per-phase `R`, `Ld`, `Lq` or effective PWM ripple inductance is allowed only after:

1. winding topology is confirmed,
2. measurement convention is documented,
3. rotor-angle dependence is understood,
4. the conversion equation is written into the calculation record.

For an inaccessible-neutral PMSM, a single headline line-line inductance is **not automatically equivalent** to either `Ld` or `Lq`.

## S1.2 outputs required from the measurement

The PWM/ripple study needs, at minimum:

- minimum effective line-line/phase inductance relevant to worst-case ripple,
- maximum effective inductance,
- resistance at known temperature,
- rotor-angle dependence,
- frequency dependence over the PWM-analysis band,
- uncertainty / repeatability.

The ripple calculation shall use the **minimum defensible inductance** for worst-case current-ripple screening unless the modulation/state-specific model justifies another value.

## Pass/fail for closing the blocker

The motor-inductance blocker can move from OPEN to EVIDENCED when either:

- the exact selected motor manufacturer supplies phase/Ld/Lq data with measurement convention and temperature, or
- this measurement procedure is executed and yields reproducible values with traceable raw data.

The blocker remains OPEN if only KV, motor dimensions, pole count or an older related motor's L value is available.

## Result template linkage

Machine-readable result fields are in:

`MOTOR_IMPEDANCE_MEASUREMENT_RESULT.template.json`

Until populated from real evidence, every measurement result remains null/OPEN.
