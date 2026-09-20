# PB-08 traction-pack-referred auxiliary-load ledger

Date: 2026-09-20  
Branch: `uav-rebaseline`  
Status: **PARTIAL EVIDENCE LEDGER / NOT A CLOSED AUXILIARY BUDGET**

## Purpose

Provide the evidence boundary required by TR-067 before a whole-pack continuous-current requirement can be frozen. Only loads supported by repository evidence are entered numerically. Regulator current ratings are source capabilities and are not used as load demand.

## Controlled relation

For each auxiliary load `i`, traction-pack input power is

`P_pack,i = P_load,i / eta_path,i`

and the corresponding 36.0 V loaded-floor pack current contribution is

`I_pack,i = P_pack,i / 36.0 V`.

Where converter/path efficiency is not controlled, the actual traction-pack-referred contribution remains **OPEN**. For a positive load, an ideal-lossless (`eta = 1`) calculation may be retained only as a mathematical lower bound; it is not a design budget.

## Evidence-backed rows

| Load/function | Evidence-backed load-side value | Path efficiency | Traction-pack-referred disposition |
|---|---:|---:|---|
| B1 OC_LOW passive reference divider | 91.4 uA at 3.3 V | OPEN | Actual pack contribution OPEN; ideal-lossless lower-bound power is 0.302 mW. |
| B1 OC_HIGH passive reference divider | 91.4 uA at 3.3 V | OPEN | Actual pack contribution OPEN; ideal-lossless lower-bound power is 0.302 mW. |
| B1 OV_REF passive reference divider | 188.6 uA at 3.3 V | OPEN | Actual pack contribution OPEN; ideal-lossless lower-bound power is 0.622 mW. |
| **Known passive-divider subtotal** | **0.3714 mA at 3.3 V** | OPEN | **1.226 mW load-side; ideal-lossless 36 V current lower bound 0.0341 mA. Actual contribution OPEN.** |

Arithmetic uses the resistor-derived currents already controlled in `B1_AUXILIARY_LOAD_DOMAIN_INVENTORY.md`: `3.3/(26.1k+10k)`, `3.3/(10k+26.1k)`, and `3.3/(7.5k+10k)`. Small differences from the earlier rounded 0.371 mA subtotal are rounding only.

## Loads that remain OPEN

The repository does not yet support a defensible simultaneous traction-pack demand for:

- gate-driver quiescent and dynamic gate-charge power;
- fan continuous demand or inrush as a PB-08/U1 requirement;
- Hall sensor/external +5 V load;
- exported board-interface power;
- MCU dynamic current at the final clock/peripheral/FOC workload;
- CAN transceiver demand at the final physical-layer implementation and bus state;
- comparator, CSA/reference, temperature-sense and clamp/fault-state analog currents;
- converter losses and quiescent currents across the final 36.0–50.4 V operating range;
- any vehicle-level avionics/flight-controller/mission-equipment load supplied from the traction pack.

The B1 fan `<=0.2 A` starting budget and LM5164/TPS62160/TLV755 regulator headline ratings are explicitly excluded from the PB-08 demand sum because they are not measured or frozen U1 loads.

## Closure rule

`P_aux,pack` in TR-067 may be frozen only after every simultaneously active traction-pack-fed auxiliary function has either (a) a controlled worst-case demand plus conversion-path loss, or (b) an explicit interface allocation backed by a product decision. Startup/inrush and fault-state loads must be treated separately from continuous demand where their durations differ.

Until that closure occurs, the existing `3000/36 = 83.33 A` propulsion-only value remains only a whole-pack continuous-current lower bound. This ledger does not promote G1, select an auxiliary converter, or qualify B1 for U1 reuse.
