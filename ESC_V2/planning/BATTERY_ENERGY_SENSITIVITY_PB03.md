# S1.3 battery-energy sensitivity — PB-03

Date: 2026-09-19  
Branch: `uav-rebaseline`  
Status: **TRADE / NO FLIGHT-TIME OR PACK-CAPACITY VALUE FROZEN**

## Purpose

Continue safe S1.3 work while S1.2 PWM is blocked by exact motor inductance. This file quantifies how the current PB-03 max-payload hover reference drives pack energy and mass, without inventing a mission duration or reserve requirement.

## Frozen / source-backed parents

PB-03 inherits:

- maximum design MTOW: 180 kg,
- X8 / eight propulsion channels,
- max-MTOW hover isolated-equivalent point: 26.471 kgf per rotor,
- manufacturer-curve reference at that point: approximately 3.0525 kW electrical input per propulsion channel at the 69 V X13 G2 reference condition,
- 18S battery architecture,
- <=80 kg vehicle operating-empty mass budget,
- eight reference propulsion units at 4.185 kg each = 33.48 kg reference propulsion mass.

Therefore the source-backed max-MTOW hover electrical reference is:

`8 * 3.05252 kW = 24.420 kW total propulsion input`

This is still a manufacturer isolated-rotor/coaxial sizing reference, not a measured custom-vehicle hover power.

## Hover-energy sensitivity before reserve

`E_hover = P_hover * time`

| Max-payload hover-equivalent time | Raw propulsion energy |
|---:|---:|
| 8 min | 3.256 kWh |
| 10 min | 4.070 kWh |
| 12 min | 4.884 kWh |
| 15 min | 6.105 kWh |

This table excludes avionics/pump/fan/auxiliary energy, battery inefficiency, voltage sag, ageing, cold-temperature derating and reserve.

## Reserve sensitivity

Reserve fraction is still OPEN. To show the consequence without selecting one, the required *usable-plus-reserve* energy is:

| Hover-equivalent time | +15% sensitivity | +20% sensitivity | +25% sensitivity |
|---:|---:|---:|---:|
| 8 min | 3.744 kWh | 3.907 kWh | 4.070 kWh |
| 10 min | 4.681 kWh | 4.884 kWh | 5.088 kWh |
| 12 min | 5.617 kWh | 5.861 kWh | 6.105 kWh |
| 15 min | 7.021 kWh | 7.326 kWh | 7.631 kWh |

These percentages are trade points only. No reserve requirement is frozen by this table.

## Pack-mass sensitivity against current <=80 kg operating-empty budget

The PB-02/PB-03 reference propulsion mass is 33.48 kg, leaving only:

`80 - 33.48 = 46.52 kg`

for **battery + airframe/arms + tank/pump/fixed mission hardware + avionics + landing gear + wiring**.

The following table uses the **+20% reserve sensitivity only as an illustration** and divides required energy by assumed complete-pack specific energy. Complete-pack specific energy is not yet frozen.

### Estimated battery mass sensitivity

| Hover-equivalent | 160 Wh/kg pack | 180 Wh/kg pack | 200 Wh/kg pack | 220 Wh/kg pack |
|---:|---:|---:|---:|---:|
| 10 min | 30.5 kg | 27.1 kg | 24.4 kg | 22.2 kg |
| 12 min | 36.6 kg | 32.6 kg | 29.3 kg | 26.6 kg |
| 15 min | 45.8 kg | 40.7 kg | 36.6 kg | 33.3 kg |

Remaining mass after propulsion + battery, before frame/fixed equipment, under the same illustration:

| Hover-equivalent | 160 Wh/kg pack | 180 Wh/kg pack | 200 Wh/kg pack | 220 Wh/kg pack |
|---:|---:|---:|---:|---:|
| 10 min | 16.0 kg | 19.4 kg | 22.1 kg | 24.3 kg |
| 12 min | 9.9 kg | 14.0 kg | 17.2 kg | 19.9 kg |
| 15 min | 0.7 kg | 5.8 kg | 9.9 kg | 13.2 kg |

## Engineering interpretation

The current 80 kg operating-empty budget makes **battery endurance a first-order mechanical constraint**, not merely an electrical choice.

In particular, a 15-minute max-payload hover-equivalent target would consume most of the remaining non-payload mass budget over a broad 160–220 Wh/kg pack sensitivity range. That does not prove 15 minutes is impossible, but it makes it difficult to reconcile with the frozen 80 kg empty-mass target once frame, tank/pump, avionics, landing gear, wiring and structural margin are included.

A 10-minute max-payload hover-equivalent point is materially easier to package, but it is **not frozen** because actual frame/fixed-equipment mass, complete-pack specific energy, mission profile and reserve policy are still open.

## Required closure inputs before PB-04 battery freeze

S1.3 still needs:

1. target total mission time,
2. target max-payload hover-equivalent time,
3. reserve-energy policy,
4. airframe/arm mass allocation,
5. fixed mission-equipment mass allocation,
6. exact battery cell/pouch candidate and complete-pack specific-energy/current capability,
7. minimum loaded bus / sag model,
8. BMS/contactors/fuse/disconnect behavior,
9. auxiliary and mission-equipment electrical loads.

Only after these are coherent should Ah/Wh, battery mass, minimum loaded bus and UV thresholds be frozen.

## Anti-hallucination boundary

All 160/180/200/220 Wh/kg values and 15/20/25% reserve columns are explicit sensitivity cases, not product requirements or claims about a selected battery. The 24.420 kW parent is a source-backed sizing reference from the current propulsion benchmark, not physical hover-power evidence for the custom X8 vehicle.
