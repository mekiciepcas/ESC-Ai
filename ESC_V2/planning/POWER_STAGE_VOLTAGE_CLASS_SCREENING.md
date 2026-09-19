# Power-stage voltage-class screening — UAV U1 pretrade

Status: **TRADE STUDY ONLY — NOT G1/G2 BASELINE**  
Date: 2026-09-19

## Why this exists

Current propulsion benchmarks include commercial heavy-lift systems with input-voltage references up to **81 V**. That does not make 81 V our product requirement, but it is enough to stress-test whether the old 100 V B1 semiconductor path is still a sensible primary architecture direction.

## Static voltage headroom to the 81 V benchmark

| Device class | Static headroom | Headroom as fraction of device rating | Pretrade disposition |
|---|---:|---:|---|
| 100 V | 19 V | 19.0% | Deprioritize for an 80 V-class reference |
| 120 V | 39 V | 32.5% | Carry forward |
| 150 V | 69 V | 46.0% | Carry forward |

These are **static arithmetic margins only**. They do not include switching overshoot, battery tolerance, harness inductance, regenerative energy, BMS disconnect events, layout parasitics, temperature derating or device avalanche behavior.

## Engineering interpretation

The old 100 V class is no longer treated as the main design path for the present heavy-lift UAV trade space. With an 81 V commercial reference it leaves only 19 V before any dynamic transient is considered. It remains a legacy comparison point and could only return if the final battery/transient envelope later proves materially lower.

The **120 V** and **150 V** classes remain active candidates. Neither is selected yet. The 120 V path may offer lower conduction/switching penalty for a given technology/package, while the 150 V path buys additional voltage headroom. The correct choice requires a common-current, common-PWM, common-junction-temperature loss comparison plus transient evidence.

## Current-domain boundary

The commercial reference set contains examples up to **120 A continuous bus current** and **300 A peak/short current**, but those numbers are not copied into U1 as phase-current requirements. DC bus current, motor phase RMS current and semiconductor RMS/peak current are different quantities. Phase/switch current remains OPEN until an exact motor/propeller operating point, modulation/control assumption and thrust point are selected.

For scale only, `4640 W / 69 V = 67.246 A`. This is arithmetic from a benchmark rated input power and voltage, not a custom ESC current requirement.

## Speed-domain boundary

The benchmark motor data includes a 45 rpm/V class. A linear no-load screen at 81 V gives `45 x 81 = 3645 rpm`. This is not a loaded propeller operating speed. Electrical RPM is still OPEN because exact pole-pair count and loaded RPM are not frozen.

## What changes now

For the next power-stage calculations:

- 100 V remains legacy/reference only for the present 80 V-class stress screen.
- 120 V and 150 V move forward into normalized loss/package/gate-drive comparison.
- Parallel MOSFET count remains OPEN.
- Gate driver remains OPEN.
- DC-link capacitance and voltage class remain OPEN.
- Auxiliary converter input-domain compatibility must be rechecked against whichever transient ceiling eventually closes.

This narrowing is architecture pretrade, not product freeze.
