# Non-backpower high-voltage sensing architecture trade

Date: 2026-09-19
Status: ANALYSIS / G2 INPUT — NO PRODUCTION MPN SELECTED

## Problem statement

B1 uses a high-value divider followed by BAT54H clamps referenced to the analog supply rail. Repository tracing has shown that the upper clamp can conduct from a live HV measurement node into +3V3A/+3V3 when control rails are absent or collapsing. The UAV revision therefore needs a voltage-sense architecture whose normal and single-fault behavior does not depend on an unpowered control rail sinking injected current.

This document defines topology candidates only. Final resistor values, isolation rating, amplifier/ADC MPNs, bandwidth and transient withstand remain OPEN until G1 freezes VBUS min/nom/max/transient and measurement bandwidth/accuracy requirements.

## Derived architecture requirements

1. A live VBUS or phase input shall not create an uncontrolled DC back-power path into an unpowered MCU/control supply rail.
2. MCU ADC absolute-maximum/injection-current limits are protection boundaries, not normal operating targets.
3. Divider resistor working voltage, pulse rating and power derating shall be proven at final transient ceiling.
4. Any clamp intended to conduct during credible repetitive transients shall return energy to a defined sink that remains valid in every power-sequencing state.
5. A single open/short fault in the sensing front end shall be assessed for hazardous MCU-domain overvoltage and false-low/false-high readings.
6. Measurement range shall include the frozen G1 transient/OV detection requirement with explicit tolerance margin; screening values such as 120/150 V are not requirements.
7. Phase-voltage sensing shall account for switching-node dv/dt and common-mode stress separately from DC-bus sensing.

## Candidate A — passive divider + ground-referenced local clamp, no rail clamp

Topology concept: series HV resistor string -> ADC RC node; dedicated low-capacitance clamp path to ground and/or a purpose-designed shunt reference local to the sense front end, rather than steering current into +3V3.

Advantages:
- simplest migration from B1 divider concept;
- no intentional current path into an unpowered +3V3 rail;
- low component count and low static power.

Open issues:
- a ground-only clamp cannot by itself prevent positive ADC overvoltage unless its clamp threshold is guaranteed below the MCU-safe boundary across tolerance/current/temperature;
- shunt element leakage/capacitance can degrade accuracy/bandwidth;
- repetitive transient energy and resistor pulse stress must be proven;
- phase sensing remains exposed to high dv/dt.

Disposition: KEEP AS CANDIDATE, not qualified.

## Candidate B — divider + powered buffer with input protection that is valid when buffer is off

Topology concept: HV divider -> current-limited protected input network -> buffer/amplifier -> MCU ADC. The input protection is selected so a live HV input cannot feed the buffer output/supply when the buffer/control domain is unpowered.

Advantages:
- isolates ADC sampling kickback from high-value divider;
- permits anti-alias/filter design independent of divider impedance;
- can provide a deterministic output impedance to ADC.

Open issues:
- exact amplifier must have documented input behavior with V_IN present while VCC=0 and must not phantom-power its supply/output;
- input common-mode and absolute maximum limits must cover fault states;
- adds offset/gain/error and supply-sequencing dependencies.

Disposition: PREFERRED NON-ISOLATED STUDY PATH if an exact device can prove power-off input tolerance / no back-power behavior.

## Candidate C — isolated voltage measurement

Topology concept: HV divider/modulator on power domain -> galvanic isolation -> low-voltage reconstruction/ADC interface.

Advantages:
- strongest separation between HV switching domain and MCU rail;
- naturally breaks direct rail-injection path;
- potentially attractive if control/power grounds are later separated for EMI/safety reasons.

Open issues:
- isolation is not automatically required by present system architecture;
- cost, area, isolated bias supply, latency, bandwidth and CMTI become new requirements;
- insulation working voltage/creepage cannot be specified until final architecture/environment are known.

Disposition: RETAIN AS ROBUSTNESS OPTION; do not add isolation without system-level need.

## Candidate D — divider + ADC/front-end with overvoltage-tolerant input and explicit power-off specification

Topology concept: resistor string directly feeds a measurement IC/ADC input whose manufacturer explicitly specifies input tolerance when its supply is absent, with internal protection not returning uncontrolled current to MCU rails.

Advantages:
- potentially fewer analog protection ambiguities than discrete rail clamps;
- can combine diagnostics/filtering/conversion.

Open issues:
- exact MPN and power-off input behavior must be primary-source proven;
- fault energy still must be limited externally;
- SPI/I2C/digital lines can themselves create back-power paths unless sequencing is assessed.

Disposition: RETAIN FOR DEVICE SEARCH.

## Architecture screening decision

B1 rail-referenced BAT54H clamps are **not a default KEEP** for U1. Candidate B or D is preferred for the non-isolated path because either can decouple the ADC from the high-value divider while allowing power-off behavior to be specified at component level. Candidate A remains viable only if a ground-referenced clamp/shunt can be proven across tolerance, leakage, energy and bandwidth. Candidate C is reserved for a system-level isolation/CMTI need.

No topology is frozen by this document.

## Verification required before G2 closure

- exact schematic and MPNs;
- powered and unpowered input-current paths from VBUS/phase node through every protection element;
- DC gain/error over resistor tolerance and temperature;
- ADC settling and source impedance;
- switching-node transient/dv/dt test plan;
- fault cases: upper resistor short/open, lower resistor short/open, clamp short/open, buffer unpowered, MCU unpowered;
- bench test with control rails OFF while HV sense input is applied from a current-limited source;
- proof that no control rail exceeds its allowed off-state bias/current.

## Traceability

- TR-006: DC-bus + U/V/W sensing
- `ADC_CLAMP_INJECTION_CLOSURE.md`
- `ANALOG_RAIL_BACKPOWER_AUDIT.md`
- `BUS_SENSE_18S_REBASELINE.md`
- G1 VBUS/transient fields remain OPEN.
