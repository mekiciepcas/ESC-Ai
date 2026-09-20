# UAV ESC tasarım izlenebilirlik matrisi

Tarih: 20.09.2026  
Amaç: Faz 2 / Faz 3 dokümanları, B1 ve PB-01..PB-07 tarihsel çalışmaları PB-08 düşük güç ürün yönüne bağlamak.

Durum etiketleri: **KEEP**, **REVALIDATE**, **RECALCULATE**, **REPLACE IF REQUIRED**, **OPEN**, **FROZEN**, **SUPERSEDED**.

> TR-001..TR-046 canonical content is preserved byte-for-byte in commit history through blob `558a79e824d957844766031e357996bc8e0cee01`. The current continuation records TR-047 onward while preserving that history as prior evidence; no historical evidence is deleted.

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
| TR-056 | PB-08 common electrical platform | **FROZEN PARTIAL SYSTEM BASELINE.** 3 kW upper continuous point; 12S at 43.2 V nominal / 50.4 V full / 36.0 V full-rated-power floor; per ESC >=1.0 kW / 30 A continuous and >=1.5 kW / 50 A for >=3 s; >=100 V semiconductor class and <=75 V repetitive controlled terminal-stress target. | `PRODUCT_BASELINE_PB-08.json`; physical evidence later. |
| TR-057 | PB-08 Quad/Hexa architecture mass closure | **CONTROLLED PARAMETRIC DECISION RULE.** Hexa residual-mass advantage is `2.025 - 2*m_axis - delta_structure - delta_common` kg. Rotor count remains OPEN. | `PB08_QUAD_HEXA_MASS_CLOSURE_CONTRACT.md`; exact mass/degraded-mode evidence. |
| TR-058 | PB-08 installed-axis primary mass evidence | **TRADE EVIDENCE.** Hobbywing X8 G2 complete set is 1095 g including cable/propeller, above the 1.0125 kg optimistic added-axis break-even. | Exact custom-axis and structural delta. |
| TR-059 | PB-08 custom-axis partial mass ledger | **SUPERSEDED PARTIAL ANCHOR.** Initial U8 Lite KV85 243 g + HEP-L 29-inch 63 g sum was only a same-class 306 g anchor because exact compatibility was not established. | Replaced by TR-060 exact-pair evidence. |
| TR-060 | PB-08 U8 Lite KV85 + NS28x9.2 exact-pair mass evidence | **TRADE EVIDENCE ADDED / NO PRODUCT SELECTION.** Current T-Motor primary material explicitly pairs U8 Lite KV85 at 12S with NS28x9.2; published masses are 243 g motor incl. cable + 59 g integrated propeller = 302 g exact-pair partial subtotal. Against the 1.0125 kg optimistic axis break-even, 710.5 g/axis remains for custom ESC/cooling/enclosure/harness/connectors/mounts before any Hexa structural/common penalty. | `PB08_U8LITE_KV85_NS28_EXACT_PAIR_EVIDENCE.md`; controlled custom ESC/mechanical mass and structural delta. |
| TR-061 | PB-08 B1 12S voltage-domain requalification | **REQUALIFICATION EVIDENCE / NO COMPONENT APPROVAL.** PB-08 50.4 V full charge restores 49.6 V static nameplate headroom to 100 V-class B1 devices, while the frozen <=75 V repetitive terminal-stress target leaves 25 V nameplate headroom. B1 therefore becomes a credible 12S requalification candidate rather than an 18S-voltage-limited architecture; exact MOSFET/driver/DC-link/protection reuse remains conditional on phase-current/PWM/loss/transient evidence. | `PB08_B1_12S_VOLTAGE_REQUALIFICATION_AUDIT.md`; phase-current/PWM closure and <=75 V switching-stress proof. |

## Canonical PB-08 current state

- `PRODUCT_BASELINE_PB-08.json` is active authority.
- Aggregate propulsion family remains **1.5–3.0 kW total vehicle**, 3.0 kW upper continuous design point.
- Common bus: **12S**, 43.2 V nominal, 50.4 V full, 36.0 V loaded full-rated-power floor.
- 3 kW variant gross pack-energy target: **>=750 Wh**; exact pack OPEN.
- Custom ESC capability: **>=1.0 kW / >=30 A continuous**, **>=1.5 kW / >=50 A for >=3 s**.
- Power semiconductor class **>=100 V**; repetitive controlled switch-terminal stress **<=75 V**; exact MOSFET MPN/count OPEN.
- >=10 min nominal mission target and 20% gross-energy reserve retained.
- Quad and Hexa remain candidates. PB-08 added-axis break-even is **1.0125 kg/axis before extra Hexa structure/common mass**.
- T-Motor U8 Lite KV85 + NS28x9.2 now provides a manufacturer-explicit compatible motor/prop mass anchor of **0.302 kg partial subtotal**, but custom ESC/mechanical installed terms remain OPEN; this is not a motor/prop selection.
- B1's 100 V-class power domain is a **PB-08 requalification candidate only**: 12S resolves the old 18S static-headroom concern, but <=75 V repetitive stress, loss/thermal, exact DC-link and protection evidence remain open.
- Exact payload, MTOW, battery implementation, phase current, PWM/eRPM, protection thresholds and thermal limits remain OPEN.
- CAN-FD/Classic-CAN and power-up/reset DISARMED + hardware-inhibit + no-auto-rearm safety policy retained.
- B1 remains requalification candidate only. A2/B1 electrical source remains immutable.
- No component-bearing U1 schematic allocated; `U1-SCH-R001` remains unused.

## History-preservation note

Historical PB-01..PB-07 calculations are not deleted. PB-08 changes which values are product authority. Reuse decisions must distinguish `historical evidence` from `current requirement` explicitly.
