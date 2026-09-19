# ESC autonomous handoff

Date: 2026-09-19 19:06+03:00  
Branch: `uav-rebaseline`  
Status: `PROGRESS_PRELIMINARY_DATASHEET_PDS00_CREATED`

## Progress percentages

- Requirements planned-domain/schema structure: **12/12 = 100%**.
- G1 SYSTEM FREEZE value closure: **1/46 PASS = 2.2%**.
- Backlog tasks explicitly DONE: **1/25 = 4%**.
- Major product gates closed: **0/8 = 0%**.
- U1 KiCad architecture scaffold: **100% structure coverage**.
- U1 component-bearing production-intent schematic: **0%**.
- Preliminary engineering datasheet: **100% for the current PDS-00 concept snapshot only**.

Product counters remain unchanged because PDS-00 documents the current evidence state; it does not freeze new product ratings.

## Run summary

The user requested a datasheet while continuing the ESC design. A versioned preliminary engineering datasheet, `ESC_U1_PRELIMINARY_DATASHEET_PDS-00.md`, was created as a controlled concept-stage snapshot. The document explicitly separates user targets, planned architecture, candidates, OPEN requirements and TRADE_ONLY benchmark stress references so the datasheet cannot accidentally be read as a production rating sheet.

A four-page PDF derivative was also generated for user delivery and visually inspected page-by-page after rendering. No clipping, overlap or missing-glyph issue was observed.

## Datasheet contents

PDS-00 records:

- 70-100 kg as **payload target**, not MTOW.
- DC operating voltage, phase current, power, PWM and eRPM as **OPEN** product requirements.
- 81 V, 120 A continuous, 300 A / 3 s and 4.64 kW only as **TRADE_ONLY architecture stress references** from the current benchmark set.
- 120 V and 150 V MOSFET classes as carried-forward trade candidates; no winner selected.
- 100 V as legacy/reference comparison, not the preferred primary path for the current ~80 V benchmark screen.
- Planned 3-phase VSI, FOC/SVPWM-capable control, current/voltage/temperature sensing, hardware trip, PWM inhibit and CAN-family interface direction.
- Candidate MCU, gate-driver and CAN parts without promoting them to production selection.
- Mechanical dimensions, mass, cooling, environmental and connector requirements as OPEN.
- Verification state: scaffold/software-baseline evidence exists, but component-bearing U1 schematic, PCB, physical switching, thermal, EMI, dyno and flight qualification remain NOT RUN / NOT STARTED.

## Files changed

- `planning/ESC_U1_PRELIMINARY_DATASHEET_PDS-00.md` - new versioned preliminary datasheet source.
- `planning/autonomy_state.json` - AUTO-STATE-37.
- `planning/AUTONOMOUS_HANDOFF.md` - this handoff.

No B1/U1 KiCad electrical source, PCB, Gerber, production BOM or release package was modified.

## Engineering boundary

PDS-00 is explicitly **not a production datasheet**. `OPEN`, `TRADE_ONLY`, `PLANNED`, `CANDIDATE` and `REVALIDATE` fields are not guaranteed product ratings. The document is intended to align the mechanical, propulsion, battery and ESC co-design while G0/G1 remain open.

## Exact next recommended tasks

1. Run the normalized **120 V vs 150 V MOSFET loss comparison** using explicit trade-only sweep points for current, PWM and junction temperature.
2. Screen gate-driver voltage-domain and gate-current compatibility for both classes.
3. Build trade-only DC-link/precharge/transient bounding calculations around the current 80 V-class benchmark.
4. Extract source-backed motor load-curve operating points to begin replacing broad bus-current references with propulsion-linked estimates.
5. Keep `U1-SCH-R001` unallocated until G1/G2 page readiness closes.

## Next-run briefing

Start with the 120 V versus 150 V loss trade. PDS-00 is now the human-readable concept snapshot and should be revised as PDS-01, PDS-02, etc. rather than silently rewriting released snapshots when major design status changes. Mandatory product metrics remain **100% requirements structure / 2.2% G1 closure / 4% backlog DONE / 0% major gates / 0% component-bearing U1 schematic** until evidence changes them.
