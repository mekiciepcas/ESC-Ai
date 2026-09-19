# Control platform pretrade — STM32G474 vs TMS320F280041C

Date: 2026-09-19  
Branch: `uav-rebaseline`  
Status: **G2 PREWORK / NO MCU SELECTION**

## Purpose

Compare the two control-platform families already present in the Faz2/Faz3/B1 history using exact current manufacturer evidence. This is a pretrade only. Final selection remains blocked by the frozen PWM/ADC timing, motor electrical/eRPM, fault-response, communication and firmware-execution requirements.

## Evidence policy

- Exact device-family/product-page data below is **PRIMARY MANUFACTURER EVIDENCE**.
- Existing B1 use of STM32G474RET3 is **REPOSITORY SOURCE EVIDENCE**.
- Architecture implications are **ENGINEERING TRADE JUDGMENT**.
- No FOC execution-time, trip latency or control-loop margin is claimed without an executable benchmark or hardware measurement.

## Exact anchors

### ST STM32G474RE / B1 STM32G474RET3

Current ST product evidence for STM32G474RE:
- active / volume-production device family;
- Arm Cortex-M4 with single-precision FPU and DSP instructions;
- up to 170 MHz;
- 512 Kbytes Flash and 128 Kbytes SRAM for the xE density;
- CORDIC and FMAC mathematical accelerators;
- five 12-bit ADCs;
- seven comparators and six op amps;
- HRTIM with 184 ps high-resolution timing capability;
- three FDCAN peripherals;
- 1.71–3.6 V VDD/VDDA range;
- package family includes 64-pin options.

B1 repository evidence already uses `STM32G474RET3` in LQFP64 and has an existing pin contract / schematic around that device.

Primary source: https://www.st.com/en/microcontrollers-microprocessors/stm32g474re.html

### TI TMS320F280041C / orderable 64-pin anchor F280041CPMS

Current TI product evidence for exact TMS320F280041C:
- active C2000 real-time MCU;
- one C28 CPU at 100 MHz;
- FPU32 and Trigonometric Math Unit (TMU);
- 128 Kbytes Flash and 100 Kbytes RAM;
- exact `C` variant includes Configurable Logic Block (CLB) and InstaSPIN-FOC support;
- three 12-bit SAR ADC modules with four post-processing blocks per ADC;
- seven CMPSS window comparators with DAC references and digital filtering;
- seven programmable-gain amplifiers;
- 16 ePWM channels with high-resolution capability and integrated dead-band / trip zones;
- two CAN peripherals;
- six DMA channels;
- 64-pin LQFP package option; `F280041CPMS` is a current exact 64-pin orderable anchor.

Important exact-variant correction: the TI product table for **TMS320F280041C** lists one C28 CPU and does not list a CLA. CLA capability from other F28004x variants must not be silently attributed to the 041C candidate.

Primary sources:
- https://www.ti.com/product/TMS320F280041C
- https://www.ti.com/product/TMS320F280041C/part-details/F280041CPMS

## Source-backed comparison

| Criterion | STM32G474RET3 / RE family | TMS320F280041C / F280041CPMS | Current implication |
|---|---|---|---|
| CPU | Cortex-M4, up to 170 MHz, FPU/DSP | C28, 100 MHz, FPU32 + TMU | Clock rate alone is not a valid FOC winner metric. Benchmark the actual control workload. |
| Motor-control timing | HRTIM, 184 ps high-resolution capability; motor-control timers | 16 ePWM channels, HRPWM, dead-band and hardware trip zones | Both have purpose-built PWM resources; exact PWM/ADC/fault schedule must be benchmarked. |
| ADC | 5 x 12-bit ADCs | 3 x 12-bit SAR ADCs, 4 PPBs per ADC | Peripheral count differs; simultaneous sampling/timing fit must be proven on the selected pin/package configuration. |
| Analog protection resources | 7 comparators, 6 op amps | 7 CMPSS + 7 PGAs, comparator DAC/filter paths | TI offers a motor-control-centric integrated protection chain; ST offers a rich mixed-signal fabric. Final external-vs-internal protection split remains open. |
| Math/control acceleration | CORDIC + FMAC + Cortex DSP/FPU | TMU + FPU; InstaSPIN-FOC support in exact C variant | Both have acceleration paths. Actual FOC runtime and observer strategy are not yet benchmarked. |
| CAN | 3 FDCAN | 2 CAN | Final FC protocol is still open; raw peripheral count is not a selection criterion by itself. |
| DMA / data movement | STM32 DMA architecture present; exact schedule not benchmarked here | 6 DMA channels | ADC/PWM/CAN contention must be measured in representative firmware. |
| Existing project reuse | B1 schematic, LQFP64 pin contract and prior sensing audit already exist | Faz2/Faz3 candidate history but no equivalent current B1 board implementation | STM32 currently has lower migration effort, but reuse cannot override a failed timing/safety requirement. |
| Motor-control ecosystem | STM32 motor-control ecosystem / Cube tooling available | C2000 motor-control ecosystem, CLB and InstaSPIN-FOC support | Toolchain/ecosystem should be evaluated with a reproducible build and test workload, not marketing claims. |

## What can be concluded now

1. Both platforms have credible hardware resources for a three-phase FOC/SVPWM ESC architecture.
2. The B1 STM32G474 implementation provides tangible reuse value: pin mapping, schematics and earlier ADC/sensing audits already exist.
3. TMS320F280041C provides a particularly integrated real-time-control path through ePWM trip zones, CMPSS/PPB resources, TMU and the exact C-variant CLB/InstaSPIN features.
4. Neither platform is selected by this document.
5. CPU MHz, ADC count or presence of InstaSPIN alone cannot establish the production choice.

## Required executable comparison before G2 MCU freeze

The same representative firmware contract shall be demonstrated on both surviving candidates or otherwise bounded from primary technical evidence:

1. six PWM outputs with complementary/dead-time behavior and safe boot-disabled state;
2. PWM-synchronous 3-shunt current acquisition with explicit valid sampling windows;
3. VBUS + phase-voltage acquisition schedule without corrupting current sampling;
4. hardware fault input -> PWM inhibit path, with measured or manufacturer-bounded latency;
5. current-loop / FOC execution time at the frozen PWM rate including observer/sensor processing;
6. CAN command + telemetry traffic at the frozen interface rate;
7. flash/RAM headroom with diagnostics, logging and fault manager enabled;
8. deterministic startup, watchdog, brownout and reset behavior;
9. debug/programming path that does not compromise production safety state;
10. exact 64-pin pin-mux feasibility for PWM, ADC, CAN, SPI/driver, temperature and service interfaces.

## Derived CTRL / SAF requirements

- **CTRL-PRE-01:** MCU selection shall be based on the frozen PWM/ADC/control workload and measured or source-bounded execution/timing margin, not nominal CPU frequency.
- **CTRL-PRE-02:** The selected MCU shall provide a deterministic PWM-disable path independent of normal motor-control software execution.
- **CTRL-PRE-03:** ADC triggering and acquisition shall be explicitly synchronized to valid current-sense windows at the selected PWM frequency.
- **CTRL-PRE-04:** Exact package pin allocation shall close before U1 schematic freeze; family-level peripheral availability is insufficient.
- **SAF-PRE-01:** Fault-to-PWM-inhibit latency shall be bounded against the final semiconductor/protection safe-action requirement and verified on hardware before propulsion release.
- **IF-PRE-01:** CAN/CAN-FD choice shall follow the frozen flight-controller protocol; B1 `SN65HVD230` Classic-CAN use does not itself define U1 protocol.

## Decision status

`STM32G474RET3`: **CANDIDATE / REUSE ADVANTAGE, NOT SELECTED**  
`TMS320F280041C (F280041CPMS anchor)`: **CANDIDATE / MOTOR-CONTROL-CENTRIC ALTERNATIVE, NOT SELECTED**

Final decision remains blocked by G1 operating envelope, PWM frequency, sensing schedule, hardware-protection architecture, FC protocol and executable firmware benchmark evidence.
