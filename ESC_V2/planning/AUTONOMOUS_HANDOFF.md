# ESC autonomous handoff

Date: 2026-09-19 18:40+03:00  
Branch: `uav-rebaseline`  
Status: `PROGRESS_PROPULSION_SCREENING_PRETRADE`

## Progress percentages

- Requirements planned-domain/schema structure: **12/12 = 100%**.
- G1 SYSTEM FREEZE value closure: **1/46 PASS = 2.2%**.
- Backlog tasks explicitly DONE: **1/25 = 4%**.
- Major product gates closed: **0/8 = 0%**.
- U1 component-bearing production-intent schematic: **0%**.
- Mechanical-electrical co-trade framework: **100% defined for concept-stage use**.
- Source-backed propulsion screening pretrade: **100% for the current screening scope**.

Product counters remain unchanged because the mechanical design does not yet exist and no benchmark value was promoted into requirements.

## Run summary

The user clarified that no mechanical vehicle design exists yet, so empty mass, battery mass, span, mission duration and related G0 values cannot be provided as real product inputs. Instead of forcing guessed values or blocking all ESC work, the project now uses a two-layer co-design method: actual G0/G1 fields remain `OPEN/null`, while explicitly labelled market benchmarks and non-binding screening cases are used to explore propulsion and ESC operating regions.

## Work completed

1. Preserved all 14 product-specific G0 fields as `OPEN/null`.
2. Created `CONCEPT_VEHICLE_ENVELOPE_PRETRADE.json` using primary DJI AGRAS T70P/T100 manufacturer data only as `BENCHMARK` anchors.
3. Created `MECHANICAL_ELECTRICAL_COTRADE_PLAN.md` defining the iterative vehicle-mass -> rotor -> motor/prop -> battery -> ESC -> vehicle-mass loop.
4. Defined non-binding MTOW screening cases `130 / 150 / 175 kg` and rotor counts `4 / 6 / 8`.
5. Calculated hover load per rotor for each case with no thrust-reserve multiplier frozen.
6. Created `PROPULSION_SCREENING_PRETRADE.json` from primary Hobbywing sources for X11 Plus, X11 Max, X13, X13 G2, X15 and X15 G2.
7. Mapped all nine MTOW/rotor screening points into manufacturer reference thrust regions without selecting a motor winner.
8. Recorded trade-only electrical reference classes: 12–14S and 18S propulsion families, high-end input-voltage examples around 78.3–81 V, and short/peak-current examples around 200–300 A. These are architecture stress-test references only, not custom ESC requirements.
9. Updated `autonomy_state.json` to AUTO-STATE-35.
10. No B1/U1 KiCad electrical source, PCB, Gerber, production BOM or physical-validation claim was changed.

## Primary-source benchmark context

- DJI AGRAS T70P: 70 kg spray payload; aircraft 52/56 kg including battery depending on battery option; maximum takeoff weights up to 130 kg depending on configuration; 62-inch propellers; 65 rpm/V motors; 52 V nominal battery. Source: `https://ag.dji.com/t70p/specs`.
- DJI AGRAS T100: 100 kg spray payload; 75 kg spraying aircraft weight; 175 kg spraying MTOW; 62-inch propellers; 60 rpm/V motors; 52 V nominal battery. Source: `https://ag.dji.com/t100/specs`.
- Hobbywing X11/X13/X15 family provides primary-source integrated propulsion reference regions from roughly 15–18 kg/axis through 37.5 kg/axis recommended load, with X15/X15 G2 maximum-thrust figures much higher than the recommended hover-load points. Sources are recorded in `PROPULSION_SCREENING_PRETRADE.json`.

## Screening hover loads

Before any thrust-reserve factor:

- 130 kg MTOW: 4 rotors = 32.50 kgf/rotor; 6 = 21.67; 8 = 16.25.
- 150 kg MTOW: 4 rotors = 37.50 kgf/rotor; 6 = 25.00; 8 = 18.75.
- 175 kg MTOW: 4 rotors = 43.75 kgf/rotor; 6 = 29.17; 8 = 21.88.

The 4-rotor / 175 kg case exceeds X15's recommended per-axis loading even though it remains below published maximum thrust, so reserve margin is not proven and this case cannot be treated as acceptable without further criteria.

## Exact next recommended tasks

1. Extract manufacturer load-curve points for the most relevant X11/X13/X15 regions.
2. Calculate trade-only per-motor power, current and rpm/eRPM ranges for each feasible screening point.
3. Calculate total propulsion-system mass sensitivity for 4/6/8-rotor concepts using source-backed system weights.
4. Feed propulsion mass back into the concept vehicle mass loop.
5. Derive a provisional custom-ESC architecture stress range and test 100/120/150 V semiconductor/driver/sensing concepts against it without selecting a winner.
6. Keep actual G0/G1 values OPEN until a coherent mechanical/system concept is explicitly accepted or validated.

## Anti-hallucination rules

- Competitor values remain `BENCHMARK`, never `REQUIREMENT`.
- Screening values remain `TRADE_ONLY`.
- No production component is selected solely from these cases.
- No thermal, EMI, endurance, dyno or flight result is claimed without physical evidence.
- B1 and U1 schematic revision history remains immutable; `U1-SCH-R001` is not allocated early.

## Next-run briefing

Start with manufacturer load-curve extraction and propulsion-mass/electrical-range sensitivity. Do not wait for unavailable mechanical masses, but never promote the screening cases into G0/G1. Mandatory product metrics remain **100% requirements structure / 2.2% G1 closure / 4% backlog DONE / 0% major gates / 0% component-bearing U1 schematic** until evidence changes them.
