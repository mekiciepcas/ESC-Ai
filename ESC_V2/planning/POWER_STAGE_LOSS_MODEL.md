# UAV ESC power-stage loss model framework

Date: 2026-09-19
Status: PARAMETRIC / NO MPN FREEZE

## Purpose
Provide a calculation contract for comparing 100 V / 120 V / 150 V semiconductor candidates after the UAV electrical envelope is frozen. This file intentionally does not select a MOSFET or claim a thermal result.

## Required inputs per candidate
- VDS rating and transient design ceiling
- RDS(on) at relevant junction temperature (not 25 C headline only)
- total gate charge Qg and Miller charge Qgd at relevant VDS/ID
- switching rise/fall time or energy data at representative operating point
- body-diode Vf and reverse-recovery Qrr/Erec where applicable
- package/PCB thermal data and verified cooling boundary
- parallel devices per switch
- PWM frequency
- phase RMS current and phase peak current
- modulation/operating point
- DC-link voltage

Unknown values remain null/TBD; a datasheet maximum current is never substituted for phase-current capability.

## First-order equations
For a three-phase two-level inverter, use device-level duty/current waveforms when available. For early comparison only:

`P_cond_total ~= 3 * I_phase_rms^2 * Rds_hot / N_parallel`

This is a screening approximation for the six-switch bridge and assumes current is carried by one active device group per phase at a time. It must be replaced/checked against modulation-aware integration before freeze.

Switching screening estimate:

`P_sw_total ~= N_events * 0.5 * Vbus * I_switch * (tr + tf) * f_pwm`

or preferably manufacturer Eon/Eoff curves scaled/interpolated to the operating point. Do not combine both methods as independent losses.

Gate-drive power:

`P_gate_total ~= 6 * N_parallel * Qg * Vgate * f_pwm`

Additional loss buckets that must be explicit:
- reverse-recovery / third-quadrant conduction,
- dead-time conduction,
- current-sharing imbalance,
- shunt loss,
- DC-link ESR loss,
- busbar/PCB copper loss,
- gate-driver loss,
- snubber/clamp loss if fitted.

## Voltage-class trade rule
A higher VDS class is not automatically safer/better. Compare at the same verified electrical envelope because higher-voltage silicon commonly trades voltage margin against RDS(on), Qg/Qgd, package choice and switching loss. 100 V candidates cannot be accepted until the bus transient requirement and DRV8353/LM5164 domains are proven compatible. 120/150 V candidates cannot be accepted solely for voltage rating; their loss and gate-drive feasibility must close.

## Required outputs
For hover, continuous-rated, overload and peak points report:
- conduction loss,
- switching loss,
- diode/recovery loss,
- gate-drive loss,
- estimated total inverter semiconductor loss,
- per-device loss distribution,
- assumed Tj/RDS(on) iteration,
- thermal boundary and predicted junction temperature,
- uncertainty/evidence level.

## Freeze acceptance
Semiconductor class/MPN remains OPEN until:
1. VBUS max/transient is defined,
2. phase RMS/peak currents are defined,
3. PWM candidate is defined,
4. manufacturer curves/parameters are captured,
5. hot RDS(on) and switching losses close thermally,
6. SOA/avalanche policy is explicit (normal operation must not rely on repetitive avalanche unless specifically qualified),
7. double-pulse/prototype measurements are planned and later completed.
