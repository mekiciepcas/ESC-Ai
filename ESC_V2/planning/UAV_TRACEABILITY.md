# UAV ESC tasarım izlenebilirlik matrisi

Tarih: 19.09.2026  
Amaç: Faz 2 / Faz 3 dokümanları, B1 ve PB-01..PB-06 tarihsel çalışmaları PB-07 düşük güç ürün yönüne bağlamak.

Durum etiketleri: **KEEP**, **REVALIDATE**, **RECALCULATE**, **REPLACE IF REQUIRED**, **OPEN**, **FROZEN**, **SUPERSEDED**.

> TR-001..TR-046 canonical content is preserved byte-for-byte in commit history through blob `558a79e824d957844766031e357996bc8e0cee01`. The current continuation records TR-047..TR-055 while preserving that history as prior evidence; no historical evidence is deleted.

## Additive continuation

| ID | Fonksiyon / karar | UAV rebaseline kararı | Sonraki kanıt |
|---|---|---|---|
| TR-047 | PB-03 hot MOSFET conduction / thermal sensitivity | **HISTORICAL PREWORK.** IAUTN15S6N025T/G 150 V study remains useful as methodology, but its voltage class is not PB-07 authority. | Re-run after PB-07 bus/transient class freezes. |
| TR-048 | PB-04 mission duration / energy-sizing policy | **KEEP.** >=10 min nominal mission target and 20% gross-pack reserve remain retained PB-07 targets pending new mass/energy correlation. | `PRODUCT_BASELINE_PB-07.json`; PB-07 battery closure. |
| TR-049 | PB-04 >=90 keRPM / PWM timing | **SUPERSEDED NUMERIC / METHOD KEEP.** 90 keRPM came from old 45KV/42-pole system. PB-07 eRPM and PWM reopen until the new motor is selected. | Exact PB-07 motor pole count/KV/Ld/Lq. |
| TR-050 | PB-05 18S / >=5 kWh / 54 V / >=500 A pack | **SUPERSEDED AS ACTIVE PRODUCT SIZING.** Preserved only as heavy-lift history. | PB-07 12S/14S battery trade. |
| TR-051 | PB-05 sag/current verification contract | **METHOD KEEP / VALUES SUPERSEDED.** SOC/temperature/SOH/current-sharing verification logic remains useful, but 54 V/500 A values do not carry into PB-07. | New PB-07 pack thresholds. |
| TR-052 | PB-06 >=1050 A / 3 s whole-pack requirement | **SUPERSEDED AS ACTIVE PRODUCT SIZING.** Heavy-lift stress point is no longer active. | PB-07 pack peak current derived from selected rotor/bus. |
| TR-053 | PB-06 high-current current-path component screening | **HISTORICAL ONLY.** EV200/HAX1000/SurLok high-current screening is not the expected PB-07 path and shall not drive the new BOM. | Re-screen lower-current contactor/fuse/sensor/connector after PB-07 pack envelope. |
| TR-054 | PB-07 product-family power rebaseline | **FROZEN PRODUCT DIRECTION.** Aggregate propulsion electrical input family range is 1.5–3.0 kW. The former 70–100 kg payload, 150/165/180 kg MTOW, X8/18S and high-current heavy-lift numeric requirements are explicitly superseded as active product authority. | `PRODUCT_BASELINE_PB-07.json`; `LOW_POWER_PROPULSION_REBASELINE_PB07.md`; `G1_REQUIREMENTS_MATRIX.json`. |
| TR-055 | PB-07 low-power architecture screen | **TRADE ACTIVE / NO SELECTION.** Current 12S manufacturer curves show at 3 kW aggregate roughly 16.3 kg MTOW screen for Quad and 18.3 kg for Hexa at 1.6 T/W using Hobbywing X8 G2 data; T-Motor U8 Lite independently gives ~15.3 / 17.7 kg. Hexa is leading candidate, Quad alternate. 12S is leading battery candidate, 14S alternate. | Freeze rotor count/MTOW/payload, then 12S/14S energy/current and exact motor/prop MPN. |

## Canonical PB-07 current state

- `PRODUCT_BASELINE_PB-07.json` is the active product authority.
- Aggregate propulsion input product-family range is **1.5–3.0 kW total vehicle**, not per ESC.
- Previous heavy-lift 70–100 kg payload / 150–180 kg MTOW / X8 / 18S / 500–1050 A pack / >=150 V semiconductor / 125–375 A phase-current values remain preserved but are **not active PB-07 requirements**.
- >=10 min nominal mission target and 20% gross-energy reserve remain active retained targets.
- Hexa non-coaxial is the leading rotor candidate and Quad the alternate; neither is frozen.
- 12S is the leading battery candidate and 14S the alternate; neither is frozen.
- Exact payload, MTOW, rotor count, motor/prop MPN, battery topology, per-ESC power/current, phase current, PWM, eRPM, semiconductor class, protection thresholds and thermal limits are OPEN.
- CAN-FD/Classic-CAN interface and the power-up/reset DISARMED + hardware-inhibit + no-auto-rearm safety policy remain retained.
- B1's historical ~3 kW / ~48 V power stage is now a **requalification candidate** because PB-07 returns to the same broad power/voltage class. It is not automatically accepted.
- A2/B1 electrical source remains immutable; reuse must occur only through a future U1 schematic revision.
- No component-bearing U1 schematic is allocated; `U1-SCH-R001` remains unused.

## History-preservation note

Historical PB-01..PB-06 calculations are not deleted. PB-07 changes which values are product authority. Reuse decisions must distinguish `historical evidence` from `current requirement` explicitly.
