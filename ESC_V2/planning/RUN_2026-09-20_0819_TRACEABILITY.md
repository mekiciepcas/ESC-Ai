# RUN 2026-09-20 08:19+03:00 — traceability

## TR-065 — PB-08 whole-pack continuous-current mathematical lower bound

**Parents:** PB-035 aggregate upper continuous propulsion input = 3000 W; PB-039 full-rated-power loaded bus floor = 36.0 V.  
**Derivation:** `3000 W / 36.0 V = 83.333 A`.  
**Disposition:** **DERIVED LOWER BOUND / NO PACK FREEZE.** Any 3 kW PB-08 pack must ultimately demonstrate at least 83.33 A continuous propulsion-only terminal current at the 36 V full-power floor. Final continuous-current requirement must be >= this value and additionally account for traction-pack auxiliary loads and controlled design margin.  
**Evidence:** `PB08_PACK_CONTINUOUS_CURRENT_LOWER_BOUND.md`, `PRODUCT_BASELINE_PB-08.json`, `mission_requirements.json`.  
**Explicit non-claims:** P50B 12S4P remains reference-only; 4 x 60 A cell-rating arithmetic is not a 240 A qualified pack rating. Peak pack current/duration remains OPEN. No physical sag, thermal, current-sharing or pack qualification is claimed.  
**Gate impact:** no G1 row promoted; current counters remain unchanged.

Preservation: PB-01..PB-07/A2/B1 history is unchanged. No component-bearing U1 schematic, PCB, Gerber or manufacturing release was modified.
