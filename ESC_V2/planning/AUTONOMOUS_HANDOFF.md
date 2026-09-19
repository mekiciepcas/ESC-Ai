# ESC autonomous handoff

Date: 2026-09-19 23:45+03:00  
Branch: `uav-rebaseline`  
Repository HEAD observed before this handoff commit: `5c8d1b74f29bc66d1efdda4ff6ebe1f74f850015`  
Run status: `PB07_LOW_POWER_REBASELINE_FROZEN_CI_VERIFIED`

## Product pivot completed

PB-07 is now active authority. The product family is no longer the PB-02..PB-06 70–100 kg payload heavy-lift aircraft. The user-approved active direction is **1.5–3.0 kW aggregate vehicle propulsion input**.

Historical heavy-lift work is preserved, but the following are no longer active PB-07 requirements: 70–100 kg payload, 150/165/180 kg MTOW, X8 coaxial, 18S, >=5 kWh, 500 A continuous / 1050 A 3 s pack, >=4.8 kW per ESC, 125–375 A phase current, >=150 V semiconductor and >=90 keRPM values derived from that vehicle.

## Controlling metrics

- Requirements planned-domain/schema structure: **12/12 = 100%**.
- G1 SYSTEM FREEZE value closure: **6/48 PASS = 12.5%**.
- Backlog tasks explicitly DONE: **1/25 = 4.0%**.
- Major product gates closed: **0/8 = 0%**.
- Component-bearing U1 schematic: **0%**.

The percentage drop is intentional rebaselining, not loss of historical work.

## Work completed this run

1. Created `LOW_POWER_PROPULSION_REBASELINE_PB07.md` from current primary manufacturer data.
2. Created `PRODUCT_BASELINE_PB-07.json`; froze only the 1.5–3.0 kW aggregate product-family direction and explicit non-conflicting retained policies.
3. Created `SPRINT_PB07_LOW_POWER_REBASELINE.md`; active step is S1R.2 Quad-vs-Hexa / MTOW / payload closure.
4. Rebased `mission_requirements.json`, `G1_REQUIREMENTS_MATRIX.json`, `REQUIREMENTS_PROGRESS.json`, `REQUIREMENTS_MASTER.json`, `G0_INPUT_CLOSURE_PACKET.json`, `uav_backlog.json`, `design_basis.json`, `UAV_PRODUCT_PLAN.md`, `UAV_TRACEABILITY.md` and `autonomy_state.json`.
5. Added PB-07 consistency checker and workflow. GitHub Actions run **35468304991** completed **SUCCESS**.
6. No KiCad schematic, PCB, Gerber, production BOM, A2/B1 electrical source or release package was changed. `U1-SCH-R001` remains unallocated.

## Current engineering picture

Current manufacturer-curve screens at the 3 kW aggregate study point:
- Quad: about 750 W/axis, ~16.3 kg MTOW screen at 1.6 T/W using Hobbywing data; independent T-Motor screen ~15.3 kg.
- Hexa: about 500 W/axis, ~18.3 kg MTOW screen at 1.6 T/W using Hobbywing data; independent T-Motor screen ~17.7 kg.

Therefore Hexa is the leading architecture candidate and Quad remains alternate. This is not yet a frozen architecture.

Battery direction:
- 12S leading candidate, 14S alternate.
- 3 kW at 12S screens to roughly 68–83 A total over nominal-to-low-loaded-bus assumptions.
- 10 min + 20% reserve first-order gross energy sensitivity is 312.5 / 416.7 / 520.8 / 625 Wh for constant 1.5 / 2.0 / 2.5 / 3.0 kW.
- P50B 12S3P and 12S4P are calculation candidates only.

## Important reuse consequence

B1's historical ~3 kW / ~48 V / 100 V MOSFET / DRV8353-class design is now materially closer to the PB-07 power region than it was to the former heavy-lift baseline. It should be re-audited as a reuse candidate, but no old value or component is automatically accepted.

## Unresolved blockers

1. Rotor architecture: Hexa vs Quad, thrust margin and degraded-mode policy.
2. MTOW/payload mass budget; payload must be derived rather than guessed.
3. 12S vs 14S, battery P-count, pack mass, sag and BMS.
4. Exact motor/propeller MPN and electrical winding parameters.
5. New per-ESC continuous/peak DC and phase-current envelope.
6. New bus-transient/semiconductor voltage class and exact power stage.
7. Environment, OVP/UVP/OCP/OTP/watchdog/command-timeout and thermal limits.
8. G2 remains blocked by G1; U1 component schematic allocation remains prohibited.

## Exact next recommended work

1. Complete S1R.2 with a source-backed mass roll-up for Quad and Hexa, including propulsion-system mass, battery candidate mass, frame/avionics allowance and resulting payload band.
2. Freeze rotor count only after that mass trade.
3. Continue S1R.3 immediately afterward: 12S3P vs 12S4P vs 14S alternatives, mission average-power sensitivity and loaded-bus/current bounds.
4. Then derive per-ESC envelope and perform the B1 KEEP/RECALCULATE/REPLACE re-audit.
5. Do not allocate `U1-SCH-R001` until G1 and required G2 readiness are PASS.

Dependency chain:

`PB-07 -> S1R.2 Quad/Hexa + MTOW/payload -> S1R.3 12S/14S + energy -> S1R.4 per-ESC envelope + B1 reuse -> S1R.5 PWM/protection/thermal -> S1R.6 G1 -> G2 -> U1-SCH-R001`

Mandatory snapshot: **Requirements structure 100% / G1 SYSTEM FREEZE 12.5% / Backlog DONE 4.0% / Major gates 0% / component-bearing U1 schematic 0%**.
