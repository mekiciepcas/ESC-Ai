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
| TR-062 | PB-08 U8 Lite KV85 operating-curve eRPM evidence | **TRADE EVIDENCE / NO PRODUCT SELECTION.** T-Motor publishes U8 Lite KV85 as 12S, 36N42P; its 48 V G28x9.2 CF curve reaches 3200 rpm, 16.5 A, 792 W and 6352 g thrust. 42 poles = 21 pole pairs gives 67,200 eRPM / 1,120 Hz electrical fundamental at that published point. G28x9.2 CF is not merged with the NS28x9.2 mass evidence. | `PB08_U8LITE_KV85_OPERATING_CURVE_ERPM_EVIDENCE.md`; exact selected prop/winding data before PWM freeze. |
| TR-063 | PB-08 P50B 12S4P cell-level mass/energy bound | **TRADE EVIDENCE / NO PACK FREEZE.** P50B datasheet arithmetic gives 48 cells, 840 Wh minimum / 864 Wh typical cell-level energy and 3.408 kg maximum-weight cell inventory. The 4P `4 x 60 A = 240 A` arithmetic is not a qualified pack rating. | `PB08_P50B_12S4P_CELL_LEVEL_MASS_ENERGY_BOUND.md`; complete pack hardware mass, sag, thermal/current-sharing and protection evidence. |
| TR-064 | PB-08 P50B 12S4P cell geometric packaging bound | **TRADE EVIDENCE / NO PACK SELECTION.** Current Molicel maximum cell dimensions 21.55 mm diameter x 70.15 mm height imply 25.5866 cm3 cylindrical envelope per cell and 1.228 L for 48 cell cylinders. This excludes packing voids, clearances and all non-cell hardware and is not a realizable complete-pack envelope. | `PB08_P50B_12S4P_GEOMETRIC_PACKAGING_BOUND.md`; sourced pack hardware/layout and installed mass. |
| TR-065 | PB-08 whole-pack continuous-current mathematical lower bound | **DERIVED LOWER BOUND / NO PACK FREEZE.** Frozen 3000 W upper continuous propulsion input and 36.0 V full-rated-power loaded floor imply `3000/36 = 83.33 A` propulsion-only continuous terminal current. Final requirement must additionally include controlled auxiliary load and margin/derating; vehicle peak current remains OPEN. | `PB08_PACK_CONTINUOUS_CURRENT_LOWER_BOUND.md`; auxiliary-load/margin closure plus physical sag/current-path evidence. |
| TR-066 | Canonical traceability continuity audit | **REPOSITORY CONSISTENCY REPAIR.** Run records for TR-062, TR-063 and TR-065 were verified against committed evidence and restored to the canonical continuation after an omission was detected; no engineering value or gate was promoted. | Canonical `UAV_TRACEABILITY.md`; run records remain preserved in history. |
| TR-067 | PB-08 continuous pack-current closure contract | **CONTROLLED METHOD / NO PACK FREEZE.** Final continuous pack current is defined as `((3000 W + P_aux,pack)/36.0 V)*(1+M_cont)`; `P_aux,pack` and `M_cont` remain OPEN and legacy regulator capability values cannot be substituted for load demand. | `PB08_PACK_CONTINUOUS_CURRENT_CLOSURE_CONTRACT.md`; evidence-backed auxiliary ledger and approved margin policy. |
| TR-068 | Canonical trace continuity repair run | **REPOSITORY CONSISTENCY RECORD.** Previous handoff documented restoration of TR-066/TR-067; current canonical file is verified to contain those records. No engineering value or gate promoted. | `RUN_2026-09-20_1123_TRACEABILITY.md`; commit history. |
| TR-069 | PB-08 traction-pack auxiliary-load ledger | **PARTIAL EVIDENCE / NO CURRENT FREEZE.** Only repository-proven B1 passive trip-reference dividers are numeric: 0.3714 mA at 3.3 V = 1.226 mW load-side, equivalent to 0.0341 mA at 36 V only under ideal lossless conversion. Actual traction-pack contribution remains OPEN because conversion efficiency and all major dynamic/external loads are unclosed. | `PB08_TRACTION_PACK_AUXILIARY_LOAD_LEDGER.md`; close simultaneous U1 loads and conversion-path losses before evaluating TR-067. |
| TR-070 | PB-08 continuous-current margin / derating policy | **CONTROLLED METHOD / NUMERIC MARGIN OPEN.** Defines anti-double-counting taxonomy: 3 kW propulsion and 36 V loaded floor are already embedded in the base current equation; simultaneous auxiliary demand/losses belong in `P_aux,pack`; SOC/temperature/SOH, sag/current-sharing and component thermal derating remain separate qualification checks. `M_cont` may cover only residual evidenced uncertainty not represented elsewhere. | `PB08_CONTINUOUS_CURRENT_MARGIN_POLICY.md`; close simultaneous auxiliary demand and residual uncertainty allocation before numeric current freeze. |

## Canonical PB-08 current state

- `PRODUCT_BASELINE_PB-08.json` is active authority.
- Aggregate propulsion family remains **1.5–3.0 kW total vehicle**, 3.0 kW upper continuous design point.
- Common bus: **12S**, 43.2 V nominal, 50.4 V full, 36.0 V loaded full-rated-power floor.
- 3 kW variant gross pack-energy target: **>=750 Wh**; exact pack OPEN.
- Custom ESC capability: **>=1.0 kW / >=30 A continuous**, **>=1.5 kW / >=50 A for >=3 s**.
- Power semiconductor class **>=100 V**; repetitive controlled switch-terminal stress **<=75 V**; exact MOSFET MPN/count OPEN.
- >=10 min nominal mission target and 20% gross-energy reserve retained.
- Quad and Hexa remain candidates. PB-08 added-axis break-even is **1.0125 kg/axis before extra Hexa structure/common mass**.
- T-Motor U8 Lite KV85 + NS28x9.2 provides a manufacturer-explicit compatible motor/prop mass anchor of **0.302 kg partial subtotal**, but custom ESC/mechanical installed terms remain OPEN; this is not a motor/prop selection.
- U8 Lite KV85 controller-timing trade evidence includes a **67.2 keRPM / 1.12 kHz electrical** published-curve-derived anchor using the separately identified G28x9.2 CF curve; it is not an exact selected-prop operating point.
- P50B 12S4P reference has controlled cell-only anchors of **840–864 Wh**, **3.408 kg maximum-weight inventory** and **1.228 L** maximum-dimension cylindrical material-envelope arithmetic; none is a complete installed-pack value.
- The 3 kW/36 V frozen parents impose an **83.33 A propulsion-only continuous pack-current lower bound**; final continuous current follows TR-067. TR-069 inventories the only presently numeric repository-backed passive auxiliary subtotal; TR-070 now controls how residual continuous-current margin may be added without double counting. Neither closes `P_aux,pack` or `M_cont`.
- B1's 100 V-class power domain is a **PB-08 requalification candidate only**; exact reuse remains conditional.
- Exact payload, MTOW, battery implementation, phase current, PWM/eRPM final requirement, protection thresholds and thermal limits remain OPEN.
- CAN-FD/Classic-CAN and power-up/reset DISARMED + hardware-inhibit + no-auto-rearm safety policy retained.
- B1 remains requalification candidate only. A2/B1 electrical source remains immutable.
- No component-bearing U1 schematic allocated; `U1-SCH-R001` remains unused.

## History-preservation note

Historical PB-01..PB-07 calculations are not deleted. PB-08 changes which values are product authority. Reuse decisions must distinguish `historical evidence` from `current requirement` explicitly.
