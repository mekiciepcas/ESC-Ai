# Power-off-tolerant voltage-sense device candidates

Date: 2026-09-19
Branch: `uav-rebaseline`
Status: G2 TRADE INPUT ONLY — no production sensing MPN or divider ratio is frozen.

## Objective

Close the specific evidence gap identified in `NON_BACKPOWER_HV_SENSE_ARCHITECTURES.md`: find real devices whose manufacturer documentation explicitly covers the case where a measurement input remains live while the local amplifier/control supply is absent. The goal is to remove the B1 failure mode where a rail-referenced BAT54H clamp can back-power `+3V3A/+3V3` from a live HV divider.

This document does **not** freeze VBUS range, divider values, ADC range, bandwidth, accuracy, isolation, or production MPNs. G1 remains OPEN.

## Candidate 1 — Analog Devices LT6015 / LT6016 / LT6017 family

Disposition: **PREFERRED NON-ISOLATED STUDY CANDIDATE**.

Primary manufacturer evidence:
- Product page: https://www.analog.com/en/products/lt6015.html
- Datasheet: https://www.analog.com/media/en/technical-documentation/data-sheets/601567ff.pdf
- ADI/Linear Technology Design Note 533 / technical article: https://www.analog.com/en/resources/technical-articles/robust-high-voltage-over-the-top-op-amps-maintain-high-input-impedance-with-inputs-driven-apart-or.html

Evidence relevant to U1:
- supply operation: total supply 3 V to 50 V;
- input common-mode capability: `V-` to `V- + 76 V`, independent of `V+` in Over-The-Top operation;
- manufacturer explicitly states **no supply sequencing problems**;
- the datasheet explicitly characterizes input bias with `VS = 0 V` and `VCM = 0 V to 76 V`;
- ADI's technical note explicitly states that the LT6015/LT6016/LT6017 inputs remain high impedance with complete loss of power supply and shows a high-side monitor that goes high impedance when supply vanishes;
- the product family is offered as single LT6015, dual LT6016, and quad LT6017. A quad device is therefore architecturally relevant to the existing four voltage channels: VBUS + three phase voltages.

Why it addresses the known B1 problem:

The existing B1 topology intentionally clamps the ADC node into `+3V3A`. The LT6015-family evidence provides a different protection mechanism: the amplifier input itself is designed to tolerate input voltage above the local positive supply and is explicitly characterized with zero supply. Therefore a correctly designed divider feeding an LT6015-family input need not rely on the unpowered 3.3 V rail as the sink for the HV-divider current.

Important qualification limits:
- this does **not** mean the raw 75–150 V bus should be applied directly to the amplifier. The HV resistor divider remains required and must be rated for the final G1 transient envelope;
- operation down to 3 V is permitted, but several precision specifications are published at 5 V and ±15 V. A 3.3 V implementation therefore needs an explicit error-budget check rather than assuming all 5 V precision numbers transfer unchanged;
- powered-down input tolerance does not automatically prove every output/ADC sequencing state. If the buffer can be powered while the MCU is off, the output-to-ADC path can become a separate back-power path. U1 shall either keep buffer and MCU in the same shutdown domain or prove/limit the buffer-on/MCU-off ADC current;
- phase-voltage channels still require dv/dt, RC/filter, common-mode transient and layout validation;
- output settling, ADC acquisition time and full temperature gain/offset remain open until the final divider ratio and bandwidth are frozen.

### Preliminary U1 topology for simulation only

`HV node -> series HV resistor string -> divided sense node -> local RC -> LT6017 channel as unity-gain buffer -> small ADC series resistor -> MCU ADC`

Rules for this study topology:
1. no intentional clamp from the divided node to `+3V3A`;
2. any additional positive overvoltage clamp must dump into a defined sink that remains valid with control power off;
3. LT6017 and MCU preferably share the same 3.3 V shutdown domain;
4. add an output resistor sized from the STM32 injection limits for the buffer-on/MCU-off fault state if that state is possible;
5. final divider scale must leave measurement and protection headroom at the frozen G1 transient/OV threshold, not merely at full-charge battery voltage.

## Candidate 2 — Analog Devices ADA4177 family

Disposition: **ROBUST SECONDARY REFERENCE; NOT A DROP-IN 3.3 V CANDIDATE**.

Primary manufacturer evidence:
- Product page: https://www.analog.com/en/products/ADA4177-1.html
- Datasheet / AN-1387 application guidance.

Relevant evidence:
- integrated input OVP supports input excursions up to 32 V beyond either supply;
- ADI's AN-1387 explains that its positive overvoltage current path is arranged to prevent pumping the positive supply rail, specifically addressing accidental power-up of an unpowered system;
- the device operates over ±2.5 V to ±18 V and is specified at ±5 V to ±15 V.

Reason not preferred for U1 now:
- it requires a bipolar/higher-voltage analog supply and therefore is not a direct replacement in the existing single 3.3 V analog domain;
- adding a dedicated dual rail would create extra supply, sequencing, BOM and failure-mode work without a demonstrated system requirement.

Keep as a robustness reference only unless later analog-rail architecture changes justify it.

## Explicitly screened-out example — TI OPAx206 family

Disposition: **REJECT FOR THE CURRENT NON-BACKPOWER OBJECTIVE** despite useful OVP capability.

TI documents ±40 V input overvoltage protection, but the datasheet also explicitly states that during an overvoltage event current flows through protection diodes into the power supplies. If the supplies cannot sink the current, external Zener clamps are required. That behavior recreates the exact architectural dependency we are trying to eliminate: an overvoltage/current path into an unpowered or non-sinking supply rail.

This does not make OPAx206 a bad amplifier; it makes it a poor fit for this specific U1 requirement unless a dedicated always-valid sink/clamp network is added and proven.

Primary source: https://www.ti.com/lit/ds/symlink/opa206.pdf

## Result of this search

A credible exact candidate now exists for Candidate-B architecture from `NON_BACKPOWER_HV_SENSE_ARCHITECTURES.md`: the LT6015/LT6016/LT6017 family has primary-source evidence for powered-down high-input-impedance behavior. Therefore the previous blocker "no exact power-off-tolerant device evidence" is reduced to a normal engineering qualification task rather than an architecture unknown.

No MPN is frozen. The next decision requires:
- final G1 measurement range / transient ceiling;
- required voltage-measurement bandwidth and accuracy;
- error budget at the actual supply voltage and temperature;
- buffer-on/MCU-off output-path analysis;
- SPICE / acquisition-settling analysis;
- bench test with HV input present and control rails OFF using a current-limited source.

## Traceability

- TR-006 — DC-bus + U/V/W sensing
- `NON_BACKPOWER_HV_SENSE_ARCHITECTURES.md`
- `ADC_CLAMP_INJECTION_CLOSURE.md`
- `ANALOG_RAIL_BACKPOWER_AUDIT.md`
- G1 VBUS/transient/accuracy/bandwidth requirements remain OPEN.
