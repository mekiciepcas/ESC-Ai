# PB-08 pack continuous-current closure contract

Date: 2026-09-20  
Branch: `uav-rebaseline`  
Status: **CONTROLLED CLOSURE METHOD / FINAL CURRENT STILL OPEN**

## Purpose

Convert the already-controlled propulsion-only lower bound into a final whole-pack continuous-current requirement without inventing auxiliary demand, converter efficiency, or design margin.

## Frozen parent inputs

From PB-08 authority:
- aggregate upper continuous propulsion input: `P_prop = 3000 W`;
- full-rated-power loaded bus floor: `V_floor = 36.0 V`;
- therefore propulsion-only lower bound: `I_prop,lb = 3000 / 36 = 83.33 A`.

This 83.33 A value is a mathematical lower bound, not a pack rating.

## Required closure equation

At the 36.0 V loaded floor, the final whole-pack continuous requirement shall be calculated only after auxiliary input power and an explicit engineering margin policy are controlled:

`I_pack,cont,req = ((P_prop + P_aux,pack) / V_floor) * (1 + M_cont)`

where:
- `P_aux,pack` = total continuous power drawn from the traction pack by all non-propulsion loads at the same worst-case operating state;
- `M_cont` = explicitly approved continuous-current sizing/derating margin, dimensionless and >= 0;
- `V_floor = 36.0 V` remains the frozen PB-08 full-rated-power floor.

Equivalent incremental-current form:

`I_pack,cont,req = 83.33 A + P_aux,pack/36 V`, followed by the approved margin convention.

No numerical value is assigned to `P_aux,pack` or `M_cont` in this record.

## Auxiliary-load boundary

`P_aux,pack` must include every continuous traction-pack-fed non-propulsion load that can coexist with the 3 kW propulsion state, including as applicable:
- ESC gate-drive/control auxiliary conversion losses across all active channels;
- flight controller / avionics if powered from the traction pack;
- CAN/interface electronics;
- cooling fans/pumps;
- BMS and contactor/disconnect hold power;
- payload/mission electronics only if the product power architecture assigns them to this pack;
- converter losses needed to translate downstream rail loads back to traction-pack input power.

Loads powered by a physically independent source shall not be included, but that independence must be documented.

The legacy B1 auxiliary inventory is decomposition evidence only. LM5164/TPS62160/TLV755 source ratings and the B1 `fan <=0.2 A` starting budget are not U1/PB-08 load requirements.

## Evidence required before closure

For each auxiliary load, record:
1. load/function identity and operating mode;
2. rail voltage and continuous current or direct input power;
3. source of the value: exact datasheet operating point, controlled calculation from selected parts, interface contract, or measurement;
4. converter path and efficiency evidence when translating to pack input;
5. simultaneous-operation rule relative to the 3 kW propulsion state;
6. temperature/voltage derating where relevant.

The continuous-current margin policy must separately state what uncertainty it covers. It must not double-count already worst-cased load or efficiency values.

## Sensitivity relation for future trade work

Before values are frozen, the exact effect of auxiliary power is safely expressible parametrically:

- each additional `36 W` of pack-fed continuous auxiliary power adds `1.00 A` at the 36.0 V floor before margin;
- each additional `100 W` adds `2.78 A` before margin.

These are arithmetic sensitivities only, not assumed auxiliary budgets.

## What remains OPEN

- `P_aux,pack` total;
- `M_cont` policy/value;
- final `I_pack,cont,req`;
- simultaneous vehicle peak-current policy and peak duration;
- exact cell/P-count freeze;
- BMS, fuse, disconnect, connector and conductor ratings;
- SOC/temperature/SOH sag and current-sharing qualification.

## Acceptance rule

PB-08 continuous pack current may move from OPEN only when the load ledger and margin policy are controlled and the equation above can be evaluated without placeholders. Pack hardware qualification remains a separate step: satisfying the calculated current numerically does not prove thermal, sag, protection, life, or flight performance.
