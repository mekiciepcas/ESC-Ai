# HV sense buffer output / MCU sequencing audit

Date: 2026-09-19
Branch: `uav-rebaseline`
Status: ANALYSIS / G2 INPUT — no sensing MPN or final resistor value is frozen.

## Purpose
Close the specific sequencing question left open by the LT6015/LT6016/LT6017 study path: the input side can remain high impedance with the amplifier supply removed, but a robust input alone does not prove that the amplifier output can be connected to an unpowered STM32 ADC without a back-power or absolute-maximum problem.

## Repository mapping
The B1 MCU contract maps `V_BUS_ADC` to U1701 package pin 8. ST's STM32G474 LQFP64 pin table maps package pin 8 to `PA0`, I/O structure `TT_a`, with `ADC12_IN1` functionality. The same conclusion applies conceptually to the other analog voltage channels only after their exact package-pin structures are checked.

Repository evidence:
- `hardware_b1/mcu_pin_contract.json`
- `UAV_TRACEABILITY.md`

Primary MCU evidence:
- ST DS12288, STM32G474xB/xC/xE datasheet, pin table and absolute-maximum tables.
- For TT_xx inputs the absolute input-voltage ceiling is 4.0 V.
- ST states that current injection caused by external voltage outside the supply range should be avoided during normal operation; positive injection on TT_a is specified as 0 mA in the injection-characterization table.
- The datasheet also states that VDD/VDDA/VBAT/GND pins must be connected in their permitted ranges; therefore an unpowered-MCU state shall not be declared safe merely because a signal remains below 4.0 V.

Primary buffer evidence:
- ADI LT6015/LT6016/LT6017 datasheet and DN533 / technical article.
- Inputs remain high impedance with complete loss of supply; `VS=0, VCM=0..76 V` input-bias behavior is characterized.
- When V+ is removed, the device is effectively shut down; the datasheet states the output may be externally pulled up as high as 50 V above V+ in this shutdown state. This is fault tolerance, not a defined output level.
- Normal output capability is rail-to-rail and can source/sink substantial current, so a powered buffer driving an unpowered MCU must be treated as a separate sequencing condition.

## Four sequencing states

### S1 — Buffer ON, MCU/VDDA ON
Normal acquisition state.

Required before acceptance:
- output swing stays inside the ADC input range across tolerance and fault cases;
- ADC source impedance and sampling-time requirement close;
- op-amp settling and phase-delay budget close;
- output-series resistor does not violate settling while still limiting abnormal current.

Disposition: VALID STUDY STATE, not yet qualified.

### S2 — Buffer OFF, MCU/VDDA ON
LT6017 input side is robust to live HV divider input while V+ is removed, but the output voltage is not specified as a valid ADC signal in shutdown.

Requirements:
- firmware/diagnostics shall not trust voltage conversions while the buffer rail is not valid;
- the MCU shall have a power-good/validity condition for this measurement path;
- no external pull-up may force the disabled LT6017 output beyond the MCU safe range.

Disposition: ELECTRICALLY PLAUSIBLE, measurement invalid until proven.

### S3 — Buffer ON, MCU/VDDA OFF
This is the critical state. A powered LT6017 can actively drive its output while the STM32 supply is absent.

The current repository evidence does **not** prove this is a permitted normal operating state for STM32G474. ST requires the MCU supplies to remain in the permitted range for specified operation and advises against I/O injection as a normal mechanism.

Architecture rule for the U1 study path:
- Do not intentionally allow the LT6017 analog output stage to remain powered while the STM32 VDDA/VDD domain is absent.
- Preferred study implementation is to power LT6017 from the same switched analog 3.3 V domain that supplies STM32 VDDA/VREF+, with no independent always-on buffer rail.
- If a future architecture requires buffer-ON / MCU-OFF operation, add an explicit isolation/current-limiting element whose powered-off behavior is manufacturer-specified and calculate worst-case pin current against MCU limits. Do not rely on the MCU's ESD/input structure as a clamp.

Disposition: PROHIBITED AS A NORMAL SEQUENCING STATE for the present study architecture unless separately proven.

### S4 — Buffer OFF, MCU/VDDA OFF, HV input live
This is the key reason the LT6015 family remains attractive: ADI characterizes the input as high impedance with complete loss of supply and live input common-mode up to 76 V above V-.

Requirements:
- divider resistors and input RC must tolerate the final G1 HV/transient envelope independently of buffer power;
- buffer output shall have no external pull-up to a live domain;
- output-to-MCU series path remains present only as a current-limiting/fault-control element, not as proof of a valid logic state;
- final bench validation shall apply HV from a current-limited source with all control rails off and measure every low-voltage rail for back-power.

Disposition: PRIMARY-SOURCE-SUPPORTED INPUT BEHAVIOR; complete path still requires bench proof.

## Derived architecture requirements
1. LT6017 (or any replacement buffer) and STM32 VDDA/VDD shall share a controlled shutdown domain unless a different sequencing state is explicitly proven.
2. Buffer-valid / rail-valid status shall gate use of the sampled voltage in firmware.
3. Output-series resistance shall be selected from both ADC-settling and abnormal-current requirements; its value remains OPEN until the acquisition model and final topology close.
4. No design shall credit STM32 input injection or internal protection structures as the normal sink for an active buffer while MCU power is absent.
5. The final validation matrix shall test S1–S4 plus partial-rail ramp-up/ramp-down conditions.

## What is closed by this audit
- The input-side back-power problem has a credible component-level mitigation path.
- The buffer-output / MCU-off state is now explicitly classified rather than implicitly assumed safe.
- The present preferred study rule is shared power-domain shutdown for LT6017 + STM32 analog domain.

## What remains open
- Exact LT6017 supply connection in U1 schematic.
- Exact output-series resistor and any analog switch/isolation element.
- Final ADC sample time, bandwidth and error budget.
- Powered/unpowered bench evidence.
- Final VBUS/phase measurement range and transient ceiling.

## Primary sources
- Analog Devices LT6015/LT6016/LT6017 product/datasheet: https://www.analog.com/en/products/lt6017.html and https://www.analog.com/media/en/technical-documentation/data-sheets/601567ff.pdf
- Analog Devices powered-down high-input-impedance note: https://www.analog.com/en/resources/technical-articles/robust-high-voltage-over-the-top-op-amps-maintain-high-input-impedance-with-inputs-driven-apart-or.html
- ST STM32G474RE product/datasheet: https://www.st.com/en/microcontrollers-microprocessors/stm32g474re.html and https://www.st.com/resource/en/datasheet/stm32g474ve.pdf
