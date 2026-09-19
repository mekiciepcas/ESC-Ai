# ESC autonomous handoff

Date: 2026-09-19 18:58+03:00  
Branch: `uav-rebaseline`  
Status: `PROGRESS_ESC_ELECTRICAL_PRETRADE_VERIFIED`

## Progress percentages

- Requirements planned-domain/schema structure: **12/12 = 100%**.
- G1 SYSTEM FREEZE value closure: **1/46 PASS = 2.2%**.
- Backlog tasks explicitly DONE: **1/25 = 4%**.
- Major product gates closed: **0/8 = 0%**.
- U1 KiCad architecture scaffold: **100% structure coverage**.
- U1 component-bearing production-intent schematic: **0%**.
- ESC electrical-envelope pretrade: **100% for the current benchmark-derived stress-screen scope**.
- ESC pretrade source/arithmetic CI consistency check: **100% / observed PASS**.

Product counters remain unchanged because no benchmark value has been promoted into G0/G1.

## Run summary

The project continued from the source-backed heavy-lift propulsion screening into a concrete electrical architecture stress screen. `ESC_ELECTRICAL_ENVELOPE_PRETRADE.json` now converts the current commercial benchmark set into a machine-readable trade-only electrical envelope. The calculations are executable and were verified by GitHub Actions run `35453244140` with PASS.

## Verified trade-only electrical reference results

- Highest observed commercial input-voltage reference in the current benchmark set: **81 V**.
- Highest observed continuous DC-bus current example: **120 A**.
- Highest observed peak/short DC-bus current example: **300 A**.
- Highest observed rated input-power example: **4640 W**.
- `4640 W / 69 V = 67.246 A` is retained only as arithmetic scale, not a custom ESC current requirement.
- 45 rpm/V x 81 V = 3645 rpm is retained only as a no-load linear speed screen; eRPM remains OPEN because motor pole-pair count and loaded RPM are not frozen.

## Power-stage voltage-class narrowing

Static headroom to the 81 V benchmark, before any switching/transient allowance:

- **100 V class -> 19 V headroom (19% of device rating)**: deprioritized as the primary 80 V-class design path. It remains a legacy/reference option only if the final bus/transient envelope later proves materially lower.
- **120 V class -> 39 V headroom (32.5%)**: carried forward.
- **150 V class -> 69 V headroom (46%)**: carried forward.

This is not a final MOSFET selection. 120 V and 150 V must still be compared at common current, PWM, junction temperature, package/cooling, switching energy and transient assumptions.

## Current-domain boundary

Commercial DC-bus current is not treated as motor phase current. The following remain OPEN/null:

- phase RMS current,
- phase peak current,
- switch RMS/peak current,
- MOSFET parallel count,
- PWM frequency,
- exact semiconductor MPN selection.

## Concrete files added

- `planning/ESC_ELECTRICAL_ENVELOPE_PRETRADE.json`
- `planning/POWER_STAGE_VOLTAGE_CLASS_SCREENING.md`
- `planning/verify_esc_electrical_pretrade.py`
- `.github/workflows/esc-pretrade-check.yml`
- `planning/RUN_2026-09-19_1855_TRACEABILITY.md`
- `planning/autonomy_state.json` -> AUTO-STATE-36

## Executed verification

GitHub Actions run `35453244140` completed SUCCESS. Executed output:

```text
PASS
reference_voltage_v=81
reference_continuous_bus_current_a=120
reference_peak_bus_current_a=300
reference_power_w=4640
class_100V_headroom=19V
class_120V_headroom=39V
class_150V_headroom=69V
phase_current_frozen=false
product_baseline_frozen=false
```

This proves source-to-derived-value consistency only; it is not bench, thermal, EMC, dyno or flight validation.

## Exact next recommended tasks

1. Run a normalized **120 V vs 150 V MOSFET loss comparison** using explicit trade-only current/PWM/junction-temperature sweep points.
2. Screen gate-driver voltage-domain compatibility for both carried-forward classes.
3. Build a trade-only DC-link transient/precharge bounding model around the current 80 V-class benchmark.
4. Extract manufacturer motor load-curve points so phase/bus current estimates can be tied to thrust operating points rather than broad published maxima.
5. Calculate total propulsion-system mass sensitivity for 4/6/8 rotor concepts and feed that mass back into the vehicle co-design loop.

## Anti-hallucination rules

- Competitor/benchmark values stay `BENCHMARK` or `TRADE_ONLY`.
- 81 V / 120 A / 300 A are not custom ESC requirements.
- No phase current is inferred directly from DC bus current.
- No product MOSFET, driver, parallel count, capacitor or PWM value is frozen before G1/G2 closure.
- No B1/U1 schematic is edited in place; `U1-SCH-R001` remains unallocated until readiness closes.

## Next-run briefing

Start with the normalized 120 V versus 150 V power-stage loss trade. Prefer executable calculations with explicit assumptions and keep all trade sweep points visibly non-binding. Dashboard should refresh from `autonomy_state.json` automatically. Mandatory product metrics remain **100% requirements structure / 2.2% G1 closure / 4% backlog DONE / 0% major gates / 0% component-bearing U1 schematic** until evidence changes them.
