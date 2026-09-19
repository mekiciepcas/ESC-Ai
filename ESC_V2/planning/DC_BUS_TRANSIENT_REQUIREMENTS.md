# DC-bus transient requirement — 18S analysis family

Date: 2026-09-19  
Status: **OPEN / PARAMETRIC PRE-DESIGN**

## Purpose

Prevent a false conclusion that a 100 V MOSFET/capacitor class is acceptable merely because 18S full charge is 75.6 V. Final semiconductor, DC-link and voltage-sense ratings require a measured/modelled transient ceiling.

## Known input

- 18S LiPo full-charge reference: `18 x 4.2 = 75.6 V`.
- Hobbywing X15 G2 manufacturer operating range is 25–80 V and its 69 V bench table reaches 246.6 A at the 82.476 kgf row. This is reference evidence for the current scale of a commercial heavy-lift axis, not our product rating.

## Unknowns that remain explicit

- battery-to-ESC harness inductance,
- local commutation-loop inductance,
- current interruption `di/dt`,
- actual DC-link C/ESR/ESL under bias and temperature,
- battery/BMS energy acceptance,
- BMS/contact opening behaviour,
- regen energy and rotor inertia,
- active/passive clamp topology and tolerance,
- PCB/busbar parasitics.

None is assigned a product value until measured, sourced or approved as an engineering assumption.

## First-order checks

The companion `dc_bus_transient_model.py` exposes:

- inductive stored energy: `E = 0.5 L I^2`,
- raw first-order interruption voltage: `V_L = L * dI/dt`,
- ideal capacitor-only energy absorption: `V1 = sqrt(V0^2 + 2E/C)`.

These equations are sensitivity tools, not a switching-waveform simulator. They intentionally do not include distributed ESL, MOSFET avalanche, TVS dynamic resistance, control delay, ringing, motor regeneration or battery dynamics.

## Voltage-class decision rule

A voltage class may only be frozen after all of the following are defined:

1. maximum battery/open-circuit bus including charging tolerance,
2. maximum credible switching/harness overshoot at the device terminals,
3. maximum regen/BMS-disconnect bus excursion,
4. clamp tolerance/dynamic voltage if a clamp is used,
5. required engineering margin across temperature/tolerance/aging,
6. oscilloscope validation on representative layout/harness during staged bench testing.

Until then:

- **100 V class = NOT QUALIFIED / candidate only**,
- higher voltage classes = candidates, not automatic selections,
- bus-voltage ADC full scale must exceed the diagnostic/transient range selected by this process,
- 100 V capacitors are not approved solely from nameplate voltage.

## Bench evidence required later

Use a differential/high-voltage probe with adequate bandwidth and common-mode rating at the local DC-link/device terminals. Record worst-case bus overshoot during controlled current steps, hard fault shutdown, commanded deceleration/regen cases and battery/BMS disconnect simulations. Early switching work remains low-voltage/current-limited and without propellers; propulsion-energy tests require a guarded static stand.
