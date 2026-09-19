# Control-platform executable bench contract

Date: 2026-09-19  
Branch: `uav-rebaseline`  
Status: **G2 PREWORK / TEST CONTRACT — NO MCU SELECTION**

## Purpose

Turn `CONTROL_PLATFORM_PRETRADE.md` into a reproducible acceptance contract for the surviving STM32G474 and TMS320F280041C candidates. This document does not choose an MCU and does not invent the still-open product PWM/current/communication values.

## Parent dependencies

The final numeric acceptance limits remain dependent on G1/G2 closure:

- frozen PWM frequency and dead time;
- motor electrical/eRPM envelope;
- current-sense topology and valid sampling windows;
- semiconductor safe-action/fault latency requirement;
- final CAN/CAN-FD flight-controller contract;
- watchdog/reset and arming/failsafe policy.

Until those parents close, the bench shall report measured values and PASS/FAIL only for structural/deterministic behavior whose criterion is independent of the open numeric envelope.

## Common workload

Both candidates shall implement the same logical workload:

1. six complementary PWM outputs, default disabled after reset;
2. center-aligned PWM timing with programmable dead time;
3. three phase-current ADC channels triggered from PWM timing;
4. VBUS, phase-voltage and temperature background acquisition without disturbing the current trigger schedule;
5. external asynchronous hardware fault input that forces PWM inactive without waiting for the normal control ISR;
6. gate-driver SPI transaction path and fault-status readback;
7. CAN command receive and telemetry transmit path;
8. watchdog/reset/brownout-safe startup state;
9. fixed representative FOC kernel interface: Clarke -> Park -> PI d/q -> inverse Park -> SVPWM timing calculation;
10. cycle/time instrumentation around ADC ISR, FOC kernel and communication service.

The mathematical kernel may initially use synthetic ADC vectors. Synthetic vectors are software verification only and shall not be described as motor validation.

## Required measurements

| ID | Measurement | Method | Acceptance state before parent freeze |
|---|---|---|---|
| CPB-01 | Reset-to-PWM state | power/reset cycle + scope/logic analyzer | PWM outputs remain inactive until explicit arm path; structural PASS/FAIL allowed |
| CPB-02 | Six-PWM complementary relationship | scope/logic analyzer | no illegal complementary overlap in configured test case; final dead-time value remains OPEN |
| CPB-03 | PWM-to-current-ADC trigger phase | timer/ADC timestamp + scope GPIO marker | deterministic repeatable trigger demonstrated; final sample phase/window remains OPEN |
| CPB-04 | 3-current acquisition skew | timer/ADC timestamps | measured and recorded; final allowable skew derived after sensing/PWM freeze |
| CPB-05 | Fault input to PWM inactive latency | fault generator + scope | measured distribution recorded; final PASS threshold remains OPEN until semiconductor protection budget freezes |
| CPB-06 | FOC kernel execution time | cycle counter/timer, min/mean/max over >=10000 iterations | measured with compiler/options recorded; final utilization margin remains OPEN until PWM freezes |
| CPB-07 | ADC ISR total execution time | cycle counter/timer | measured min/mean/max and worst observed jitter recorded |
| CPB-08 | CAN service load | timestamped RX/TX loop under representative traffic | no lost frames in declared test load; final traffic profile remains OPEN |
| CPB-09 | RAM/Flash footprint | linker map | exact bytes and build configuration recorded; final margin criterion remains OPEN |
| CPB-10 | Watchdog/reset recovery | induced watchdog/reset | returns to PWM-disabled safe state before any arm command |
| CPB-11 | Brownout/power-cycle behavior | controlled supply ramp where hardware permits | no uncontrolled PWM assertion observed; final voltage thresholds remain device/config dependent |
| CPB-12 | Exact 64-pin pin-mux closure | compile/config + pin table audit | all required logical functions mapped without unresolved collision for candidate package |

## Evidence record schema

Each candidate result shall record:

- exact orderable MCU and package;
- board/evaluation hardware revision;
- toolchain and version;
- compiler flags / optimization level;
- clock tree;
- PWM timer and ADC configuration;
- firmware commit SHA;
- measurement equipment and sample count;
- raw min/mean/max timing values;
- observed faults/anomalies;
- requirement IDs evaluated;
- evidence classification (`SIL`, `BENCH_LOW_ENERGY`, or later physical stage).

## Candidate-specific mapping

### STM32G474RET3

Use the existing B1 LQFP64 pin contract as a reuse starting point, but re-audit alternate-function, ADC instance and trigger routing against the executable workload. HRTIM/timer, ADC, comparator and FDCAN resources shall be configured from the exact package/device reference, not family headlines alone.

### TMS320F280041C / F280041CPMS anchor

Map the same workload onto ePWM, ADC/PPB, CMPSS/trip-zone, CAN and exact 64-pin mux resources. Do not attribute CLA resources to the 041C candidate unless exact-device evidence changes; the current pretrade explicitly records no CLA for this exact candidate.

## Derived requirements

- **CTRL-BENCH-01:** Surviving MCU candidates shall execute the same representative control workload with traceable build and timing evidence before MCU freeze.
- **CTRL-BENCH-02:** PWM and current-ADC timing shall be demonstrated deterministically on the exact package/pin configuration before U1 schematic freeze.
- **CTRL-BENCH-03:** FOC execution margin shall be calculated from measured worst-case execution time and the subsequently frozen control/PWM period; no CPU-MHz-only selection is permitted.
- **SAF-BENCH-01:** External fault-to-PWM-inactive latency shall be physically measured on the selected control path and compared with the final semiconductor safe-action budget before propulsion release.
- **SAF-BENCH-02:** Reset, watchdog and brownout tests shall demonstrate a PWM-disabled safe state before arming.
- **IF-BENCH-01:** CAN interface performance shall be evaluated against the subsequently frozen flight-controller message/rate/timeout contract.

## Decision rule

MCU selection remains OPEN until parent requirements close and candidate evidence exists. Existing STM32 B1 reuse is a migration-cost advantage, not an automatic winner. TI motor-control peripherals are an architectural advantage, not an automatic winner. The final trade shall compare requirement margin, measured determinism, safety-path coverage, exact pin feasibility, toolchain/reuse cost and supply/production constraints.
