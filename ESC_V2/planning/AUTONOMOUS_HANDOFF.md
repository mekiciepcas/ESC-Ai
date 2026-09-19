# ESC autonomous handoff

Date: 2026-09-19 20:35+03:00  
Branch: `uav-rebaseline`  
Run status: `S1_2_MEASUREMENT_PATH_DEFINED_POWER_STAGE_PREWORK_ADVANCED_S1_3_SENSITIVITY_ADDED`

## Repository state and controlling metrics

PB-03 remains the current controlled product baseline. Sprint S1.1 is DONE and S1.2 is ACTIVE. No new G1 row was promoted merely because trade/prework evidence improved.

- Requirements planned-domain/schema structure: **12/12 = 100%**.
- G1 SYSTEM FREEZE value closure: **25/46 PASS = 54.3%**.
- Backlog tasks explicitly DONE: **2/25 = 8%**.
- Major product gates closed: **0/8 = 0%**.
- U1 component-bearing production-intent schematic: **0%**.

## Completed this run

### 1. S1.2 motor-inductance blocker now has an executable verification path

Created:

- `MOTOR_IMPEDANCE_MEASUREMENT_PROCEDURE_PB03.md`
- `MOTOR_IMPEDANCE_MEASUREMENT_RESULT.template.json`

The procedure requires propeller-removed, low-energy characterization of:

- U-V / V-W / W-U line-line DC resistance,
- line-line impedance/inductance over rotor position and multiple frequencies,
- low-voltage current step-response cross-check,
- temperature, fixture compensation, instrument and uncertainty.

The result template deliberately leaves all physical result values null. A KV value, geometry or a related older motor's inductance is not accepted as proof of the exact production motor Ld/Lq/effective ripple inductance.

### 2. Exact 150 V MOSFET prework advanced

Created `POWER_STAGE_TRADE_PB03_G2_PREWORK.md`.

Exact current calculation anchors:

- Infineon `IAUTN15S6N025G` — 150 V, 2.5 mOhm max at 25 C, TOLG, RthJC max 0.42 K/W, Qg 107 nC typ / 139 nC max.
- Infineon `IAUTN15S6N025T` — same low-resistance 150 V class in top-side-cooled TOLT, RthJC max 0.40 K/W.
- Vishay `SQJQ570ER` — independent-vendor 150 V comparison with explicit hot RDS(on) maximums and RthJC 0.4 C/W.

A conduction-only N=1/2/3 parallel screen was calculated against PB-03 125 A RMS continuous / 265 A RMS overload. It is explicitly not a production parallel-count selection because switching loss, hot worst-case conduction, SOA, current sharing and baseplate thermal path remain open.

Current pre-freeze direction:

- Infineon OptiMOS 6 150 V family remains the primary electrical calculation anchor.
- TOLT is the first thermal-package branch to investigate because it can support a direct top-side baseplate path, but package/MPN are not frozen.
- Vishay is retained as an independent supplier/evidence comparison.

### 3. S1.3 energy/mass sensitivity started safely

Created `BATTERY_ENERGY_SENSITIVITY_PB03.md` from the frozen/source-backed max-MTOW hover sizing reference.

Eight PB-03 reference propulsion channels at the max-MTOW hover point imply approximately **24.420 kW total propulsion input** at the manufacturer reference condition. Raw hover-equivalent propulsion energy is therefore approximately:

- 8 min -> 3.256 kWh,
- 10 min -> 4.070 kWh,
- 12 min -> 4.884 kWh,
- 15 min -> 6.105 kWh.

Reserve fractions and 160/180/200/220 Wh/kg complete-pack specific-energy values are shown only as sensitivity cases. No flight-time, Ah/Wh, pack mass or reserve requirement is frozen.

The important system result is that the frozen <=80 kg operating-empty budget is strongly coupled to endurance. After the 33.48 kg eight-propulsion-unit reference mass, only 46.52 kg remains for battery + frame/arms + fixed mission equipment + avionics + landing gear + wiring. Long max-payload hover endurance therefore rapidly consumes the mechanical mass budget.

## S1.2 status

`G1-07 PWM` remains OPEN.

Current 20/24/32/40 kHz values remain analysis points only. The >=60 keRPM parent gives timing density, but a defensible ripple/loss selection still requires exact motor inductance and intended-device switching-loss/waveform evidence.

No PB-04 was created because no additional product value is yet sufficiently evidenced to freeze.

## Current blockers

1. Exact production motor Ld/Lq/effective PWM ripple inductance or physical measurement result.
2. Exact switching-loss correlation at intended bus/current/RG/layout plus hot conduction/thermal model.
3. Mission duration and reserve policy for S1.3.
4. Exact battery candidate, loaded minimum bus/sag/current and disconnect behavior.
5. G0 airframe/battery/fixed-equipment allocation and environment.
6. S1.4 ambient/altitude/baseplate/OV/UV/OCP/OTP/watchdog/timeout values.
7. G2 exact MOSFET count/driver/sensing/DC-link/thermal architecture.

## Configuration / release boundary

No B1 source, component-bearing U1 schematic, PCB, Gerber, production BOM or release package was changed. `U1-SCH-R001` remains unallocated because AR-001 G1 and AR-002 G2 are still OPEN.

## Exact next engineering path

1. Continue S1.2 using the new motor impedance procedure or exact supplier L/R data.
2. Extend the 150 V MOSFET model into hot conduction + switching waveform + TOLT/baseplate thermal screening.
3. In parallel, continue S1.3 by closing a defensible mission-time/reserve target and exact 18S pack candidate when evidence permits.
4. Then S1.4 environment/protection targets, S1.5 exact power-stage pre-freeze and S1.6 configuration closeout.

Dependency chain:

`PB-03 -> S1.2 motor R/L + PWM/loss -> S1.3 18S energy/min bus -> S1.4 environment/protection -> S1.5 exact power stage -> S1.6 closeout -> G1 -> G2 -> U1-SCH-R001`

## Next-run briefing

Start from PB-03, `PWM_RIPPLE_LOSS_STUDY_PB03.md`, `MOTOR_IMPEDANCE_MEASUREMENT_PROCEDURE_PB03.md`, `POWER_STAGE_TRADE_PB03_G2_PREWORK.md` and `BATTERY_ENERGY_SENSITIVITY_PB03.md`. Preserve PWM, Ah/Wh, exact MOSFET count/MPN and environment as OPEN until their evidence supports a controlled product decision.

Mandatory progress snapshot: **Requirements structure 100% / G1 SYSTEM FREEZE 54.3% / Backlog DONE 8% / Major gates 0% / component-bearing U1 schematic 0%**.
