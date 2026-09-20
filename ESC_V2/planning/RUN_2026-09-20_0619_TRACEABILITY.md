# TR-063 — PB-08 P50B 12S4P cell-level mass/energy bound

Date: 2026-09-20 06:19+03:00  
Branch: `uav-rebaseline`

## Task

Advance independent S1R.3B battery closure while S1R.2 custom ESC/structure mass remains evidence-blocked.

## Evidence

Current Molicel INR-21700-P50B Product Data Sheet v1.1: 3.6 V nominal, 4.2 V charge, 5.0 Ah / 18.0 Wh typical, 4.85 Ah / 17.5 Wh minimum, 60 A continuous discharge with 80 degC cut-off condition, 12.8 mOhm typical DC impedance at 50% SOC, 71 g maximum cell weight.

Primary source: https://www.molicel.com/wp-content/uploads/4.TR%E7%B0%A1%E6%98%93%E8%A6%8F%E6%A0%BC_INR21700P50B_1.1_Product-Data-Sheet-of-INR-21700-P50B-80122.pdf

## Controlled derivation

For the existing PB-08 reference-only P50B 12S4P topology: 48 cells; 43.2 V nominal; 50.4 V full; 20.0 Ah typical / 19.4 Ah minimum cell-level capacity; 864 Wh typical / 840 Wh minimum cell-level energy; 3.408 kg maximum-weight cell inventory. Minimum cell-level energy remains 90 Wh above the PB-08 >=750 Wh target; typical cell-level energy is 114 Wh above it.

The 4P arithmetic current ceiling is 240 A from 4 x 60 A, but this is not a pack rating. Complete installed pack mass, sag, thermal/current-sharing behavior, BMS, fuse/disconnect, interconnect and enclosure remain OPEN.

## Disposition

**TRADE EVIDENCE / NO PACK FREEZE.** `battery_mass_kg` remains null because 3.408 kg is cell inventory only. No physical-test claim, production selection or G1 row closure is made.

Artifact: `PB08_P50B_12S4P_CELL_LEVEL_MASS_ENERGY_BOUND.md`.
