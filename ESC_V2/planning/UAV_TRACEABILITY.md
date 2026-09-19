# UAV ESC tasarım izlenebilirlik matrisi

Tarih: 19.09.2026  
Amaç: Faz 2 / Faz 3 dokümanları, B1 ve PB-01..PB-07 tarihsel çalışmaları PB-08 düşük güç ürün yönüne bağlamak.

Durum etiketleri: **KEEP**, **REVALIDATE**, **RECALCULATE**, **REPLACE IF REQUIRED**, **OPEN**, **FROZEN**, **SUPERSEDED**.

> TR-001..TR-046 canonical content is preserved byte-for-byte in commit history through blob `558a79e824d957844766031e357996bc8e0cee01`. The current continuation records TR-047..TR-056 while preserving that history as prior evidence; no historical evidence is deleted.

## Additive continuation

| ID | Fonksiyon / karar | UAV rebaseline kararı | Sonraki kanıt |
|---|---|---|---|
| TR-047 | PB-03 hot MOSFET conduction / thermal sensitivity | **HISTORICAL PREWORK.** IAUTN15S6N025T/G 150 V study remains useful as methodology, but its voltage class is not PB-08 authority. | Re-run with PB-08 100 V class after phase current/PWM close. |
| TR-048 | PB-04 mission duration / energy-sizing policy | **KEEP.** >=10 min nominal mission target and 20% gross-pack reserve remain retained PB-08 targets pending final mass/energy correlation. | `PRODUCT_BASELINE_PB-08.json`; exact pack closure. |
| TR-049 | PB-04 >=90 keRPM / PWM timing | **SUPERSEDED NUMERIC / METHOD KEEP.** 90 keRPM came from old 45KV/42-pole system. PB-08 eRPM and PWM remain open until the new motor is selected. | Exact PB-08 motor pole count/KV/Ld/Lq. |
| TR-050 | PB-05 18S / >=5 kWh / 54 V / >=500 A pack | **SUPERSEDED AS ACTIVE PRODUCT SIZING.** Preserved only as heavy-lift history. | PB-08 12S pack implementation. |
| TR-051 | PB-05 sag/current verification contract | **METHOD KEEP / VALUES SUPERSEDED.** SOC/temperature/SOH/current-sharing verification logic remains useful. | New PB-08 pack thresholds and physical correlation. |
| TR-052 | PB-06 >=1050 A / 3 s whole-pack requirement | **SUPERSEDED AS ACTIVE PRODUCT SIZING.** Heavy-lift stress point is no longer active. | PB-08 vehicle peak pack current after rotor/failure policy. |
| TR-053 | PB-06 high-current current-path component screening | **HISTORICAL ONLY.** EV200/HAX1000/SurLok high-current screening shall not drive the PB-08 BOM. | Re-screen lower-current input path after pack peak current freezes. |
| TR-054 | PB-07 product-family power rebaseline | **FROZEN PRODUCT DIRECTION.** Aggregate propulsion electrical input family range is 1.5–3.0 kW. Former heavy-lift numeric requirements are explicitly superseded as active product authority. | `PRODUCT_BASELINE_PB-07.json`; inherited by PB-08. |
| TR-055 | PB-07 low-power architecture screen | **TRADE ACTIVE / NO ROTOR SELECTION.** At 3 kW aggregate, current manufacturer curves give roughly 16.3 kg Quad vs 18.3 kg Hexa MTOW screen at 1.6 T/W using Hobbywing data, with T-Motor cross-check in a similar range. | Full installed-axis/frame mass roll-up and degraded-mode decision. |
| TR-056 | PB-08 common electrical platform | **FROZEN PARTIAL SYSTEM BASELINE.** 3 kW is the upper continuous family design point; 12S common bus is frozen at 43.2 V nominal / 50.4 V full / 36.0 V full-rated-power floor. Per ESC hardware capability is >=1.0 kW / 30 A continuous and >=1.5 kW / 50 A for >=3 s. Power semiconductor class is >=100 V with <=75 V repetitive controlled terminal-stress target and no repetitive avalanche reliance. 3 kW variant gross pack target is >=750 Wh. Quad/Hexa and exact pack/motor remain OPEN. | `PRODUCT_BASELINE_PB-08.json`; `PB08_COMMON_ELECTRICAL_PLATFORM.md`; switching/thermal/pack physical evidence later. |

## Canonical PB-08 current state

- `PRODUCT_BASELINE_PB-08.json` is the active product authority.
- Aggregate propulsion product family remains **1.5–3.0 kW total vehicle**, with **3.0 kW frozen as the upper continuous design point**.
- Common bus is **12S**, 43.2 V nominal reference, 50.4 V full charge, 36.0 V minimum loaded floor for full rated ESC power.
- The 3 kW variant gross pack-energy target is **>=750 Wh**. P50B 12S4P is a calculation reference, not an exact selected pack.
- Custom ESC hardware capability is **>=1.0 kW / >=30 A continuous** and **>=1.5 kW / >=50 A for >=3 s per channel**. These are hardware capability values, not permission to command every channel to peak simultaneously.
- Power semiconductor class is **>=100 V**; repetitive controlled switch-terminal stress target is **<=75 V** and normal operation may not rely on repetitive avalanche. Exact MOSFET MPN/count remains OPEN.
- Previous heavy-lift 70–100 kg payload / 150–180 kg MTOW / X8 / 18S / 500–1050 A pack / >=150 V semiconductor / 125–375 A phase-current values remain preserved but are **not active PB-08 requirements**.
- >=10 min nominal mission target and 20% gross-energy reserve remain active retained targets.
- Quad and Hexa remain active candidates. PB-08 quantifies the propulsion-axis installed-mass break-even at **1.0125 kg per added axis** before extra Hexa structural mass; rotor count is not frozen.
- Exact payload, MTOW, motor/prop MPN, battery cell/P-count/pack mass/peak current, phase current, PWM/eRPM, protection thresholds and thermal limits remain OPEN.
- CAN-FD/Classic-CAN interface and power-up/reset DISARMED + hardware-inhibit + no-auto-rearm safety policy remain retained.
- B1's historical ~3 kW / ~48 V / 100 V MOSFET domain is now a **requalification candidate**. The old 100 V voltage class is directionally aligned, but no B1 part/count/driver/sensing value is automatically approved.
- A2/B1 electrical source remains immutable; reuse must occur only through a future U1 schematic revision.
- No component-bearing U1 schematic is allocated; `U1-SCH-R001` remains unused.

## History-preservation note

Historical PB-01..PB-07 calculations are not deleted. PB-08 changes which values are product authority. Reuse decisions must distinguish `historical evidence` from `current requirement` explicitly.
