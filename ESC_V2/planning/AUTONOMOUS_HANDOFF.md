# ESC autonomous handoff

Date: 2026-09-19 14:24+03:00
Branch: `uav-rebaseline`
Status: `PROGRESS_POWER_OFF_SENSE_CANDIDATE_AND_DYNAMIC_FET_EVIDENCE`
Repository HEAD immediately before this handoff update: `fe6f3f10b84691dfb568e219d45be0862acf7445`.

## Run summary
This run verified the latest planning/handoff state, then closed the specific exact-device evidence gap for a non-backpower buffered HV-sense study path. Analog Devices LT6015/LT6016/LT6017 were identified from primary manufacturer evidence as a family whose inputs are explicitly characterized with `VS=0` and whose manufacturer documentation states the inputs remain high impedance with complete loss of supply. The run also screened ADA4177 as a secondary robustness reference and OPAx206 as unsuitable for the current non-backpower objective because its OVP current is intentionally routed into supply rails. In parallel, the 100/120/150 V MOSFET trade table was deepened with Qgd/Coss/Qoss/Qrr/RthJC evidence and a no-default HV sense static-error calculator was added. No product voltage/current rating, sensing MPN, MOSFET class or PCB implementation was frozen.

## Tasks attempted / completed
1. Re-read and verified the prior handoff, `UAV_TRACEABILITY.md`, `autonomy_state.json`, existing non-backpower sensing architecture trade and semiconductor candidate table against `uav-rebaseline`.
2. Researched primary manufacturer evidence for a buffer/front-end whose measurement input may remain live while local supply is absent.
3. Added `POWER_OFF_TOLERANT_SENSE_CANDIDATES.md`.
4. Promoted LT6015/LT6016/LT6017 to **preferred non-isolated study candidate family**, not production selection.
5. Recorded ADI evidence: 3–50 V total supply operation; input common-mode to 76 V above V-; datasheet input-bias characterization at `VS=0, VCM=0..76 V`; manufacturer design note states inputs stay high impedance with complete supply loss / no supply-sequencing problem.
6. Defined a preliminary four-channel LT6017 study topology for VBUS + U/V/W: HV resistor string -> divider node -> RC -> unity buffer -> small ADC series resistor -> MCU ADC, with no intentional +3V3A rail clamp.
7. Added a new sequencing requirement: if buffer can be ON while MCU ADC is OFF, the output path is a separate possible back-power mechanism; either buffer/MCU share shutdown domain or that state must be current-limited/proven.
8. Screened ADA4177 as a strong OVP/rail-pumping reference but not a drop-in 3.3 V candidate because it operates from bipolar/higher-voltage supplies.
9. Screened TI OPAx206 out as the default solution because its datasheet routes OVP current into supply rails and requires a valid sink/Zener path if the supply cannot sink current.
10. Extended `SEMICONDUCTOR_VOLTAGE_CLASS_CANDIDATES.md` with condition-tagged Qgd/Coss/Qoss/Qrr/RthJC data for the 100/120/150 V trade anchors.
11. Added `hv_sense_error_model.py`, a mandatory-input parametric calculator for divider tolerance, op-amp offset/bias and ADC quantization without hidden product assumptions.
12. Updated `UAV_TRACEABILITY.md` and `autonomy_state.json`.

## Files changed
- `planning/POWER_OFF_TOLERANT_SENSE_CANDIDATES.md` — new
- `planning/hv_sense_error_model.py` — new
- `planning/SEMICONDUCTOR_VOLTAGE_CLASS_CANDIDATES.md` — extended
- `planning/UAV_TRACEABILITY.md` — updated
- `planning/autonomy_state.json` — updated
- `planning/AUTONOMOUS_HANDOFF.md` — updated

## Engineering decisions / findings
- The previous statement "no exact power-off-tolerant sensing device evidence" is no longer true. A credible primary-source candidate family exists.
- LT6015-family powered-down input behavior directly addresses the known B1 input-to-+3V3A back-power mechanism at the amplifier input boundary; it does not by itself qualify the complete MCU ADC path.
- A quad LT6017 is structurally attractive because the ESC already requires four voltage channels, but package, 3.3 V precision/error, bandwidth and thermal/availability considerations remain to be reviewed before any selection.
- The output side needs its own sequencing analysis. Robust input behavior does not automatically guarantee buffer-on/MCU-off safety.
- ADA4177 demonstrates a different robust OVP strategy that prevents positive rail pumping, but its supply architecture does not match the current 3.3 V domain without added rails.
- OPAx206 OVP is not compatible with the current non-backpower objective by default because its overvoltage current path goes to the supply rails.
- Dynamic MOSFET evidence is now sufficient to prepare a common-condition loss calculator, but published Qrr/Coss values cannot be compared directly because test current, voltage and di/dt differ.

## Calculations / evidence added
- No product requirement value was invented.
- `hv_sense_error_model.py` calculates nominal divider transfer, resistor-tolerance extremes, op-amp offset and bias-current error referred to HV input, ADC LSB and half-LSB quantization for caller-supplied parameters only.
- CSD19536KTT evidence now includes Coss 1820 pF typ / 2370 pF max, Qoss 335 nC typ, Qrr 548 nC typ at 50 V / 100 A / 300 A/us, and RthJC 0.4 C/W.
- IPT017N12NM6 evidence now includes Qgd 25/38 nC typ/max, Coss 2400/3100 pF typ/max, Qoss 266/333 nC typ/max, Qrr 111/222 nC at 300 A/us and 301/602 nC at 1000 A/us, and RthJC 0.38 C/W.
- IAUTN15S6N025 evidence now includes Qgd 27 nC typ, Coss 2370 pF typ, Qrr 23/46 nC typ/max at 75 V / 50 A / 100 A/us, and RthJC max 0.42 K/W.
- The different reverse-recovery test conditions are explicitly captured so they cannot be used as a false direct ranking.

## Primary evidence
- ADI LT6015 product page: https://www.analog.com/en/products/lt6015.html
- ADI LT6015/LT6016/LT6017 datasheet: https://www.analog.com/media/en/technical-documentation/data-sheets/601567ff.pdf
- ADI/Linear Technology Design Note 533 / technical article on powered-down high input impedance.
- ADI ADA4177 datasheet / AN-1387 power-supply overvoltage guidance.
- TI OPAx206 datasheet: https://www.ti.com/lit/ds/symlink/opa206.pdf
- TI CSD19536KTT Rev C datasheet.
- Infineon IPT017N12NM6 Rev 2.0 datasheet.
- Infineon IAUTN15S6N025 Rev 1.0 datasheet.

## Assumptions and evidence level
- LT6015-family power-off input behavior: PRIMARY MANUFACTURER EVIDENCE.
- LT6017 four-channel use: ARCHITECTURE STUDY PROPOSAL only; no procurement/production selection.
- 3.3 V operation is within the 3–50 V operating range, but detailed accuracy at 3.3 V remains OPEN because key precision tables are commonly specified at 5 V / ±15 V.
- Existing 18S, 120 V and 150 V values remain candidate/screening cases only.
- No physical measurements or SPICE results were claimed.

## Unresolved blockers
- Product G0 mass/mission/environment/failure policy and actual MTOW.
- Final rotor architecture and thrust margin.
- Product motor/prop selection, pole-pair count, phase RMS/peak current and eRPM.
- Battery series/min/nom/full-charge/transient envelope.
- Harness/PCB inductance and switching/regen/BMS-disconnect transient ceiling.
- Final sense measurement range, accuracy, bandwidth and divider ratio.
- Buffer-on/MCU-off ADC injection/back-power proof and powered/unpowered bench test.
- Common operating point for semiconductor hot-RDS/switching-loss/SOA comparison.
- Final semiconductor voltage class/MPN, PWM, DC-link/precharge/clamp sizing.

## Regressions / risks discovered
- No repository regression found.
- Replacing rail clamps with a robust-input buffer can move rather than eliminate the sequencing problem if the buffer output drives an unpowered MCU. That state is now an explicit verification item.
- The LT6015 family can operate from 3 V, but product-level accuracy at 3.3 V must not be assumed from specifications characterized at other supply voltages.
- Comparing MOSFET Qrr across unlike di/dt/current/voltage conditions can create a false winner; the final comparison needs a common switching envelope.

## Exact next recommended tasks
1. Close the LT6017-study output-to-ADC sequencing states: buffer OFF/MCU ON, buffer ON/MCU OFF, both OFF, both ON. Derive a safe series-resistance/domain rule from STM32 injection limits without selecting final values prematurely.
2. Add a parametric divider-RC / ADC acquisition / op-amp settling model so the final sensing bandwidth can be sized from a frozen G1 requirement.
3. Build a condition-normalized power-stage loss calculator skeleton using the newly captured FET parameters, with phase current/PWM/temperature as mandatory inputs rather than defaults.
4. Continue to keep G0/G1 product fields OPEN until vehicle-specific targets are supplied/approved.

## Dependency chain
`G0 vehicle inputs -> G1A rotor selection -> G1B product operating point + motor electrical data -> G1C battery/transient envelope -> G1 SYSTEM FREEZE -> G2 architecture freeze (sensing/semiconductor included) -> G3 schematic review -> firmware/PCB -> physical validation`

## Next-run briefing
Do not repeat the device search. Begin with the buffer-output/MCU-off sequencing state for the LT6017 study path, then create the dynamic settling/acquisition model. In parallel, the semiconductor table now has enough dynamic parameters to create a normalized loss-calculator skeleton, but the calculator must require caller-supplied current, PWM, bus voltage, gate conditions and temperature. Do not select LT6017, a MOSFET voltage class or a product rating until their parent G1 requirements close.
