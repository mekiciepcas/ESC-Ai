# UAV ESC DC-link selection / qualification framework

Date: 2026-09-19
Status: FRAMEWORK — no capacitor MPN freeze

## Objective
Replace the legacy `3 x 470 uF / 100 V` candidate with a requirement-driven DC-link design once bus transient and propulsion-current envelopes are known.

## Inputs required
- VBUS min/nominal/full-charge/repetitive transient/absolute transient
- PWM frequency and modulation/control strategy
- DC input current continuous/peak and phase-current envelope
- effective harness/connector inductance
- allowed bus ripple and overshoot
- ambient/baseplate/capacitor hot-spot temperature
- propulsion mission duty cycle
- expected service life
- physical volume/mass constraints

## Capacitance roles
Separate the network into:
1. bulk energy storage / low-frequency bus ripple,
2. local high-frequency commutation loop capacitance,
3. damping/snubber/clamp elements if required.

Do not treat nameplate bulk capacitance as the effective high-frequency commutation capacitance.

## Required calculations
### Energy / transient screening
Stored energy: `E = 0.5 * C * V^2`.
For an injected event with known energy, first-order capacitor-only rise may be screened using `V2 = sqrt(V1^2 + 2*E/C)`. This is not a substitute for the real source/clamp/network model.

### Ripple current / ESR heating
Use the actual inverter modulation/current waveform or validated conservative envelope to obtain capacitor RMS ripple current. First-order ESR heating is `P_ESR = I_ripple_rms^2 * ESR(T,f)`.

### Effective capacitance
For MLCCs include DC-bias, temperature and tolerance. For electrolytic/polymer/film candidates include capacitance tolerance, ESR/ESL vs frequency and aging/lifetime behavior. Nameplate uF alone is insufficient.

### Lifetime / thermal
For lifetime-rated technologies, use the manufacturer's own lifetime model and measured/estimated capacitor hot-spot temperature. Do not apply an unsourced generic doubling-per-10C rule as qualification evidence.

## Voltage-rating rule
Capacitor voltage class shall be selected from the guaranteed repetitive/absolute ESC-terminal transient envelope plus manufacturer derating/lifetime guidance. `75.6 V < 100 V` alone is not acceptance evidence. The existing 100 V bulk and 100 V local ceramics remain reference-only until this closes.

## Candidate technology trade
Compare at least aluminum electrolytic, polymer/hybrid where voltage permits, film, and appropriate MLCC/local film solutions on:
- voltage margin
- effective capacitance
- ESR/ESL and ripple-current capability
- temperature/lifetime
- pulse capability
- mass/volume
- vibration/mechanical retention
- availability/cost
- failure mode

## Validation evidence
Before G3/G4 freeze:
- source-backed capacitor ratings and lifetime model
- calculated worst-case ripple/thermal point
- impedance/ESR assumptions documented
- PCB/harness parasitic model
- oscilloscope measurement of local VDS/VBUS overshoot with suitable probe technique
- thermal soak at continuous operating point
- peak/transient test
- disconnect/regen case validation

## Current B1 disposition
`3 x 470 uF / 100 V` and `3 x 2.2 uF / 100 V X7R` remain legacy candidates only. Exact MPNs and effective capacitance/ripple/lifetime are OPEN. No production capacitor is selected by this framework.
