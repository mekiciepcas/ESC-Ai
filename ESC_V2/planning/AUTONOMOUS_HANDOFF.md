# ESC autonomous handoff

Date: 2026-09-19 19:50+03:00  
Branch: `uav-rebaseline`  
Status: `PROGRESS_PRODUCT_BASELINE_PB02_FROZEN_AND_CI_VERIFIED`

## Progress percentages

- Requirements planned-domain/schema structure: **12/12 = 100%**.
- G1 SYSTEM FREEZE value closure: **22/46 PASS = 47.8%**.
- Backlog tasks explicitly DONE: **2/25 = 8%**.
- Major product gates closed: **0/8 = 0%**.
- U1 KiCad architecture scaffold: **100% structure coverage**.
- U1 component-bearing production-intent schematic: **0%**.

This run materially advanced the controlled product baseline. It did not claim physical verification, G0/G1 closure or production readiness.

## Controlled product baseline

`PRODUCT_BASELINE_PB-02.json` supersedes PB-01 and inherits all PB-01 frozen decisions. Any change to a PB-02 frozen value requires PB-03 or an explicitly linked engineering-change record.

### Newly frozen by PB-02

1. **Nominal payload:** 85 kg.
2. **Operating-empty mass budget:** <=80 kg, excluding variable payload but including propulsion, battery, structure, avionics and fixed mission hardware.
3. **MTOW design targets:** 150 / 165 / 180 kg for 70 / 85 / 100 kg payload cases.
4. **Coaxial sizing factor:** 0.85 pending physical correlation; the final vehicle must still meet the frozen thrust requirements regardless of measured interaction.
5. **Normal static thrust-to-weight:** >=1.6 at maximum design MTOW.
6. **Propulsion performance class:** 56x20 inch folding propeller, 45KV, 18S, >=27 kgf rated isolated thrust, >=60 kgf isolated max thrust, propulsion-unit mass target <=4.3 kg. Exact production motor/propeller MPN remains open.
7. **Max-MTOW hover sizing:** 22.5 kgf physical vehicle-share per rotor; 26.471 kgf isolated-equivalent using the 0.85 coaxial factor.
8. **Normal 1.6 T/W point:** 42.353 kgf isolated-equivalent per rotor at 180 kg MTOW.
9. **One propulsion-channel loss / controlled landing sizing:** 30.252 kgf isolated-equivalent per remaining rotor at 180 kg MTOW.
10. **Battery architecture:** 18S high-rate lithium, 66.6 V nominal and 75.6 V full charge, within inherited <=80 V outer ceiling. Pack Ah/Wh and exact cell/pouch remain open.
11. **ESC DC capability:** >=70 A continuous, >=200 A for >=3 s, >=4.8 kW continuous input and >=11.5 kW short-duration input capability.
12. **Controller electrical-speed capability:** >=60,000 eRPM.

PB-01 inherited values remain frozen: X8 architecture, eight independent channels, controlled-landing failure policy, <=120 V repetitive controlled switch stress, >=150 V power semiconductor class, independent high-voltage half-bridge gate-driver architecture, CAN-FD/Classic-CAN compatibility, deliberate arming/no-auto-rearm policy, and BLDC/PMSM + two-level VSI + FOC/SVPWM core topology.

## Why the 56-inch / X13-class branch won the sizing baseline

The current manufacturer reference is Hobbywing X13 G2: 56x20 propeller class, 45KV, 18S, 27 kg rated thrust per axis, 60 kg max thrust, 4.185 kg propulsion-unit mass and 25-80 V operating input range. Eight reference propulsion units total 33.48 kg, leaving 46.52 kg inside the frozen 80 kg operating-empty budget for battery, structure, fixed mission equipment, avionics, landing gear and wiring.

At 180 kg MTOW, raw hover share is 22.5 kgf/rotor. Applying the frozen 0.85 coaxial sizing factor gives 26.471 kgf isolated-equivalent, just inside the 27 kgf rated class. This makes the X13-class branch materially lighter than the X15 G2 benchmark while still retaining substantial maximum-thrust headroom.

Source-backed manufacturer-curve interpolation at 69 V gives approximately:

- 26.471 kgf -> 44.23 A, 3.05 kW, 1632 rpm
- 30.252 kgf -> 54.07 A, 3.73 kW, 1744 rpm
- 42.353 kgf -> 90.81 A, 6.26 kW, 2058 rpm

These are sizing references from the manufacturer isolated-rotor curve, not physical results from the custom coaxial vehicle.

## G1 closure impact

G1 value closure advanced from **8/46 = 17.4%** to **22/46 = 47.8%**.

Newly closed rows include nominal payload, MTOW targets, hover/max-thrust requirements, thrust margin, 56-inch/45KV propulsion class, >=60 keRPM controller capability, 18S series architecture, nominal bus, continuous/peak DC power and continuous/peak DC current.

Phase RMS/peak current remains deliberately OPEN because DC current is not copied into the phase-current domain.

## Backlog impact

`UAV-002 Rotor architecture trade study` is now **DONE** because PB-02 numerically closes rotor count, hover thrust, maximum-thrust capability and thrust margin.

Backlog DONE is now **2/25 = 8%**. `UAV-003` remains the other completed task.

## Verification evidence

- `verify_product_baseline_pb02.py` enforces PB-02 consistency across mission requirements, G1 matrix, progress and backlog.
- `.github/workflows/product-baseline-pb02.yml` runs the checker on relevant changes.
- GitHub Actions run `35456003134` completed **SUCCESS**.
- Dashboard refresh run `35456024478` completed **SUCCESS** after the PB-02 state update.

This verification proves repository consistency only. It is not bench, thermal, EMI, dyno or flight evidence.

## G0 alignment

`G0_INPUT_CLOSURE_PACKET.json` is now `G0-CLOSURE-03`. Nominal payload is no longer an open user input, so the remaining G0 input count is reduced to **11**.

Remaining G0 items are: structural/airframe mass allocation, battery mass, fixed mission-equipment mass, total flight time, hover-equivalent time, minimum and maximum ambient, maximum altitude, maximum design wind, ingress target and maximum vehicle span.

## Exact next recommended tasks

1. Derive **phase RMS and peak current** from a motor electrical model consistent with the frozen 56x20 / 45KV / 18S class; do not equate DC and phase current.
2. Freeze **PWM frequency range** using >=60 keRPM requirement, motor inductance evidence and 150 V MOSFET switching-loss/ripple trade.
3. Close **18S battery energy**: Ah, Wh, minimum loaded bus, sag, reserve and BMS/disconnect behavior from a mission-energy model.
4. Allocate the frozen **<=80 kg operating-empty mass budget** across propulsion, battery, frame, fixed mission hardware, avionics/wiring and landing gear.
5. Then select exact **150 V MOSFET MPN + parallel count + high-voltage gate-driver MPN**, followed by current sensing, DC-link, precharge and thermal architecture.
6. Produce `PDS-02` with all PB-02 frozen values visibly marked.

## Engineering boundary

No B1/U1 component-bearing electrical schematic, PCB, Gerber, production BOM or release package was modified. `U1-SCH-R001` remains unallocated until G1/G2 readiness closes.

## Next-run briefing

Start from `PRODUCT_BASELINE_PB-02.json`. Do not reopen PB-02 values without PB-03/ECO. Product critical path is now `phase-current model -> PWM -> battery energy/min bus -> exact 150 V power stage -> sensing/DC-link/thermal -> U1-SCH-R001 readiness`.

Mandatory metrics: **Requirements structure 100% / G1 SYSTEM FREEZE 47.8% / Backlog DONE 8% / Major gates 0% / U1 component-bearing schematic 0%**.
