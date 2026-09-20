# Run traceability — 2026-09-20 10:18+03:00

Trace ID: **TR-067**  
Branch: `uav-rebaseline`

## Change
Created `PB08_PACK_CONTINUOUS_CURRENT_CLOSURE_CONTRACT.md` to define the evidence and equation required to convert the controlled 83.33 A propulsion-only lower bound into a final whole-pack continuous-current requirement.

## Controlled derivation
Frozen PB-08 parents remain `P_prop = 3000 W` and `V_floor = 36.0 V`, hence `I_prop,lb = 83.33 A`.

Final closure equation is:

`I_pack,cont,req = ((P_prop + P_aux,pack) / V_floor) * (1 + M_cont)`

`P_aux,pack` and `M_cont` remain OPEN. No auxiliary-load value, efficiency, current margin, pack rating, physical result, or product selection was invented.

Parametric sensitivity is exact arithmetic: every additional 36 W of continuous pack-fed auxiliary demand adds 1.00 A at the 36 V floor before margin; 100 W adds 2.78 A.

## Evidence boundary
`B1_AUXILIARY_LOAD_DOMAIN_INVENTORY.md` was reviewed. Legacy regulator source capabilities and the B1 fan starting budget are not promoted to PB-08 load requirements. Final closure requires a simultaneous-load ledger, pack-referred converter losses/efficiency evidence, and an explicit non-double-counted margin policy.

## Gate effect
No G0/G1 row is promoted. Requirements structure remains 12/12; G1 remains 15/48; backlog remains 1/25 DONE. Final continuous pack current, peak current, pack implementation and physical qualification remain OPEN.
