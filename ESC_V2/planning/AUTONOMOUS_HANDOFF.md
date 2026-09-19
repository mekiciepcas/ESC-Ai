# ESC autonomous handoff

Date: 2026-09-19 18:40+03:00  
Branch: `uav-rebaseline`  
Status: `PROGRESS_MECHANICAL_ELECTRICAL_COTRADE_PRETRADE`

## Progress percentages

- Requirements planned-domain/schema structure: **12/12 = 100%**.
- G1 SYSTEM FREEZE value closure: **1/46 PASS = 2.2%**.
- Backlog tasks explicitly DONE: **1/25 = 4%**.
- Major product gates closed: **0/8 = 0%**.
- U1 component-bearing production-intent schematic: **0%**.
- Mechanical-electrical co-trade framework: **100% defined for concept-stage use**, not product closure.

Product counters remain unchanged because the mechanical design does not yet exist and no benchmark value was promoted into requirements.

## Run summary

The user clarified that no mechanical vehicle design exists yet, so empty mass, battery mass, span, mission duration and related G0 values cannot be provided as real product inputs. Instead of forcing guessed values or blocking all ESC work, the project was switched to a two-layer co-design method: actual G0/G1 fields remain `OPEN/null`, while explicitly labelled market benchmarks and non-binding screening cases are used to explore propulsion and ESC operating regions.

## Work completed

1. Verified the current `uav-rebaseline` branch and previous handoff before changing strategy.
2. Preserved all 14 G0 product-specific fields as `OPEN/null`.
3. Created `CONCEPT_VEHICLE_ENVELOPE_PRETRADE.json`.
4. Added primary-manufacturer commercial benchmark facts for DJI AGRAS T70P and T100 without treating them as requirements.
5. Defined non-binding MTOW screening cases of 130/150/175 kg and rotor-count cases of 4/6/8.
6. Calculated hover load per rotor for each screening case, with no thrust-reserve factor frozen.
7. Created `MECHANICAL_ELECTRICAL_COTRADE_PLAN.md` describing the iterative mass -> rotor -> motor/prop -> battery -> ESC -> mass loop.
8. Updated `autonomy_state.json` to AUTO-STATE-34 and changed the active task to concept vehicle envelope / propulsion co-trade.
9. No B1/U1 KiCad electrical source, PCB, Gerber, production BOM or physical-validation claim was changed.

## Source-backed benchmark context

- DJI AGRAS T70P official specifications: 70 kg spray payload; aircraft 52/56 kg including battery depending on battery option; maximum takeoff weights up to 130 kg depending on configuration; 62-inch propellers; 65 rpm/V motors; 52 V nominal battery. Source: `https://ag.dji.com/t70p/specs`.
- DJI AGRAS T100 official specifications: 100 kg spray payload; 75 kg spraying aircraft weight; 175 kg spraying MTOW; 62-inch propellers; 60 rpm/V motors; 52 V nominal battery. Source: `https://ag.dji.com/t100/specs`.

These remain `BENCHMARK` evidence only.

## Screening hover loads

Before any thrust-reserve factor:

- 130 kg MTOW: 4 rotors = 32.50 kgf/rotor; 6 = 21.67; 8 = 16.25.
- 150 kg MTOW: 4 rotors = 37.50 kgf/rotor; 6 = 25.00; 8 = 18.75.
- 175 kg MTOW: 4 rotors = 43.75 kgf/rotor; 6 = 29.17; 8 = 21.88.

No final MTOW, rotor count, motor-out policy, coaxial permission, vehicle span or thrust margin is frozen.

## Exact next recommended tasks

1. Search primary motor/prop manufacturer data for candidates covering the screening hover-load regions.
2. Build a propulsion operating-region matrix rather than selecting a single motor winner.
3. Derive trade-only voltage/current/power/eRPM ranges for the ESC from feasible candidate operating points.
4. Feed candidate motor/battery masses back into the concept vehicle model and iterate.
5. Compare MOSFET/driver/sensing architecture robustness across the resulting electrical range.
6. Keep G0/G1 product values OPEN until a coherent mechanical/system concept is explicitly accepted or validated.

## Anti-hallucination rules

- Competitor values remain `BENCHMARK`, never `REQUIREMENT`.
- Screening values remain `TRADE_ONLY`.
- No production component is selected solely from these cases.
- No thermal, EMI, endurance, dyno or flight result is claimed without physical evidence.
- B1 and U1 schematic revision history remains immutable; `U1-SCH-R001` is not allocated early.

## Next-run briefing

Start with propulsion candidate data from primary manufacturer sources. Do not wait for unavailable mechanical masses; use the co-trade loop, but never promote the screening cases into G0/G1. Mandatory product metrics remain **100% requirements structure / 2.2% G1 closure / 4% backlog DONE / 0% major gates / 0% component-bearing U1 schematic** until evidence changes them.
