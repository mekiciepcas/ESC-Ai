# PB-08 traction-pack auxiliary demand closure contract

Date: 2026-09-21
Status: **CLOSURE CONTRACT / NO AUXILIARY POWER FREEZE / NO PACK-CURRENT FREEZE**

## Purpose

Define the minimum evidence needed to close the traction-pack auxiliary demand term used in PB-08 pack-current and loaded-floor calculations without inventing loads or conversion efficiencies.

The controlled 3 kW propulsion study point and 36.0 V loaded floor are not sufficient by themselves to freeze pack current. Any load powered directly or indirectly from the traction pack and simultaneous with propulsion must be included before a total continuous/peak pack-current requirement can be frozen.

## Controlled arithmetic

For a simultaneous operating condition:

`P_pack,total = P_propulsion,pack + sum(P_aux,input,i)`

`I_pack,total = P_pack,total / V_pack_loaded`

For an auxiliary load behind a converter:

`P_aux,input,i = P_aux,load,i / eta_i`

where `eta_i` must be supported at the applicable input voltage, output load, temperature and operating mode. If efficiency is unknown, the real traction-pack contribution remains **OPEN**; ideal-lossless arithmetic may only be reported as a lower-bound sensitivity and must be labeled as such.

TR-086's 7.867 mA and 14.161 mA values are therefore only ideal-lossless 36 V translations of legacy-B1 gate-charge power endpoints. They are not entries in a frozen PB-08 auxiliary budget.

## Required auxiliary-load ledger

Every traction-pack-derived load must have a controlled row before closure. At minimum assess:

| Load class | Exact hardware / configuration | Load-side demand | Converter / path | Applicable efficiency | Simultaneity with propulsion | Evidence | Status |
|---|---|---:|---|---:|---|---|---|
| ESC gate-drive supply, all simultaneously active ESCs | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN |
| ESC MCU / logic / sensing rails, all active ESCs | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN |
| Flight controller and required avionics if traction-pack supplied | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN |
| CAN / communications / telemetry if traction-pack supplied | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN |
| BMS / contactor / precharge-control steady demand | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN |
| Cooling pumps / fans if fitted and traction-pack supplied | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN |
| Payload / mission equipment if included in propulsion-pack energy/current scope | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN |
| Other traction-pack-derived load | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN | OPEN |

Rows that are not applicable require explicit configuration evidence; they may not be silently treated as zero.

## Evidence acceptance

A numeric auxiliary contribution may be promoted only when all of the following are known for the applicable configuration:

1. exact load hardware or bounded configuration;
2. operating mode and load-side voltage/current or power;
3. exact conversion path from traction pack;
4. efficiency or input-power evidence at the relevant operating point;
5. simultaneity/duty relationship with propulsion continuous and peak cases;
6. temperature/voltage applicability where material;
7. primary-source calculation basis or controlled measurement reference.

Catalog maximums may be used as conservative bounds only when their applicability and simultaneity are explicit. Typical values are not worst-case requirements unless separately justified.

## Closure outputs

Only after the ledger is complete may PB-08 derive:

- `P_aux,pack,continuous`;
- `P_aux,pack,peak` and peak duration/duty basis;
- total continuous traction-pack current at the controlled loaded-voltage condition;
- total simultaneous peak traction-pack current;
- the current used by installed-pack sag / 36.0 V loaded-floor verification;
- auxiliary energy contribution to the mission energy budget.

Until then these values remain **OPEN**. The existing 83.33 A value (`3000 W / 36.0 V`) remains only a propulsion-power lower bound and must not be relabeled as total pack current.

## Non-claims

This contract does not select a converter, BMS, avionics set, cooling architecture, payload power source, exact ESC MOSFET/count/PWM, or pack. It does not establish physical efficiency, thermal performance, battery compliance, G1 closure, flight qualification, or production readiness.
