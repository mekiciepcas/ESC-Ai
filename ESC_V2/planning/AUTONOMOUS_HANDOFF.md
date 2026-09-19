# ESC autonomous handoff

Date: 2026-09-19 20:02+03:00  
Branch: `uav-rebaseline`  
Status: `PROGRESS_U1_RATED_HIGH_PERFORMANCE_STRATEGY_LOCKED`

## Progress percentages

- Requirements planned-domain/schema structure: **12/12 = 100%**.
- G1 SYSTEM FREEZE value closure: **22/46 PASS = 47.8%**.
- Backlog tasks explicitly DONE: **2/25 = 8%**.
- Major product gates closed: **0/8 = 0%**.
- U1 KiCad architecture scaffold: **100% structure coverage**.
- U1 component-bearing production-intent schematic: **0%**.

This run did not freeze a new electrical rating; it clarified the product-family strategy and removed a stale metadata inconsistency.

## Product strategy decision

The user approved a high-end-first development path. Initial U1 hardware shall be optimized around the current PB-02 heavy-lift rated baseline rather than compromised to guarantee broad lower-voltage compatibility in revision 1.

`U1_RATED_VARIANT_STRATEGY.md` now records:

- **U1 Rated** = 18S heavy-lift first-release baseline.
- 66.6 V is the 3.7 V/cell nominal convention; 75.6 V is the 4.2 V/cell full-charge target; <=80 V remains the frozen input ceiling.
- Open `dc_bus_min_v` shall be closed from real **18S loaded/sag/cutoff behavior**, not from a future 12S/14S compatibility target.
- The first power stage, auxiliary supply, sensing, current limits, thermal design and firmware shall be optimized for rated 18S performance.
- Lower-series-count operation is not an initial-release promise merely because hardware might power up at that voltage.
- Future 12S/14S/16S lower-power products are allowed as controlled derivatives and may revise MOSFET class/count, gate drive, auxiliary UVLO, sense scaling, current/power limits, DC-link, connectors, propulsion and firmware.
- A derivative that changes frozen values requires a new PB/ECO and exact schematic/BOM/PCB/verification lineage.

PB-02 itself was not modified because no frozen numerical value changed.

## PB-02 rated baseline remains

- X8 coaxial, 4 arms / 8 independent propulsion channels.
- Payload target 70-100 kg; nominal 85 kg.
- <=80 kg operating-empty budget.
- 150 / 165 / 180 kg MTOW targets at 70 / 85 / 100 kg payload.
- 56x20 inch / 45KV / 18S propulsion performance class.
- 18S: 66.6 V nominal convention, 75.6 V full charge target.
- >=70 A continuous DC input capability.
- >=200 A for >=3 s peak DC input capability.
- >=4.8 kW continuous and >=11.5 kW short-duration input capability.
- <=120 V repetitive controlled semiconductor terminal stress.
- >=150 V power-semiconductor class.
- >=60,000 eRPM controller capability.

## Consistency cleanup

`REQUIREMENTS_MASTER.json` still carried the pre-PB-02 historical progress metadata `1/46 = 2.2%` even though the actual controlling G1 matrix and progress authority are `22/46 = 47.8%`. It was revised to `REQ-MASTER-07` and aligned to the current PB-02 authority. This does not change the controlling metric; it removes stale duplicated metadata.

## Current blockers

The next G1 closures remain:

1. phase RMS and peak current,
2. PWM frequency,
3. 18S Ah/Wh, minimum loaded bus, sag, reserve and BMS/disconnect behavior,
4. environmental envelope,
5. detailed <=80 kg operating-empty mass allocation,
6. exact 150 V MOSFET/parallel count and high-voltage half-bridge gate driver,
7. sensing, DC-link, precharge and thermal implementation.

`U1-SCH-R001` remains unallocated because G1/G2 readiness is still incomplete. No component-bearing U1 schematic, PCB, Gerber, production BOM or release package was modified.

## Exact next engineering path

`phase-current model -> PWM freeze -> 18S energy/minimum-loaded-bus closure -> exact 150 V MOSFET/parallel count -> gate driver -> sensing/DC-link/thermal -> U1-SCH-R001 readiness`

Lower-voltage derivative work is intentionally deferred until the rated 18S product baseline is electrically and thermally coherent.

## Next-run briefing

Start from `PRODUCT_BASELINE_PB-02.json`, `BATTERY_VOLTAGE_RATIONALE_PB02.md`, and `U1_RATED_VARIANT_STRATEGY.md`. Do not reopen PB-02 frozen values without PB-03/ECO. Continue with phase-current and PWM evidence; do not equate DC current with phase current.

Mandatory metrics remain: **Requirements structure 100% / G1 SYSTEM FREEZE 47.8% / Backlog DONE 8% / Major gates 0% / U1 component-bearing schematic 0%**.
