# UAV ESC tasarım izlenebilirlik matrisi

Tarih: 19.09.2026  
Amaç: Faz 2 / Faz 3 dokümanları ile mevcut B1 tasarımını yeni UAV ürün gereksinimine bağlamak.

Durum etiketleri: **KEEP**, **REVALIDATE**, **RECALCULATE**, **REPLACE IF REQUIRED**, **OPEN**, **FROZEN**.

> TR-001..TR-046 canonical content is preserved byte-for-byte in commit history through blob `558a79e824d957844766031e357996bc8e0cee01`. The current continuation records TR-047..TR-053 while preserving that history as controlling prior evidence; no prior classification is revoked.

## Additive continuation

| ID | Fonksiyon / karar | UAV rebaseline kararı | Sonraki kanıt |
|---|---|---|---|
| TR-047 | PB-03 hot MOSFET conduction / thermal sensitivity | **PREWORK / exact selection OPEN.** IAUTN15S6N025T/G remains a 150 V calculation anchor. Khot=1.6/2.0/2.3 are sensitivity points only, not guaranteed hot RDS(on) values. N=2 and N=3 remain detailed-study branches; no count, MPN or thermal stack is frozen. | `POWER_STAGE_HOT_THERMAL_SENSITIVITY_PB03.md`; guaranteed hot-resistance policy, switching waveform/energy, transient ZthJC, TIM/baseplate model, current sharing. |
| TR-048 | PB-04 mission duration / energy-sizing policy | **FROZEN PRODUCT TARGET.** >=10 min total mission target and >=10 min hover-equivalent first-order energy-sizing target at 85 kg nominal payload / 165 kg nominal MTOW reference; 20% of gross pack energy is reserved. | `PRODUCT_BASELINE_PB-04.json`; `MISSION_DURATION_ENERGY_BASELINE_PB04.md`; exact cell/pouch, pack mass, sag, usable SOC and mission-power correlation. |
| TR-049 | Controller electrical-speed capability and PWM timing | **eRPM FROZEN / PWM OPEN.** >=90 keRPM controller capability; preferred PWM analysis window 24-32 kHz; 20/40 kHz remain boundary sensitivity points. | `PRODUCT_BASELINE_PB-04.json`; `ERPM_PWM_TIMING_CORRECTION_PB04.md`; exact production-motor Ld/Lq or impedance measurement before PWM freeze. |
| TR-050 | PB-05 rated battery architecture | **PARTIAL FROZEN.** Rated 18S pack energy >=5.0 kWh, minimum loaded bus for full rated power 54.0 V, and continuous whole-pack capability >=500 A are product requirements. Exact cell MPN/topology remains OPEN. | `PRODUCT_BASELINE_PB-05.json`; `BATTERY_CELL_PACK_TRADE_PB05.md`; low-SOC/cold/aged sag, pack mass, interconnect/BMS/contactors and physical thermal validation. |
| TR-051 | PB-05 battery sag / continuous-current verification | **VERIFICATION CONTRACT DEFINED / PHYSICAL EVIDENCE OPEN.** BV-01..BV-05 cover SOC, temperature, SOH, terminal sag, BMS state, current-path drops and parallel-group sharing. Typical cell DCR alone is not qualification evidence. | `BATTERY_SAG_VERIFICATION_CONTRACT_PB05.md`; exact-pack cold/low-SOC/EOL measurements or physically correlated pack model. |
| TR-052 | PB-06 whole-pack short-duration current and pack-architecture framework | **PEAK CURRENT FROZEN / EXACT PACK OPEN.** Frozen normal 1.6 T/W point maps through current X13 G2 69 V + MFP56x20 manufacturer data to about 50.11 kW aggregate input. At 54 V this is about 928 A; with 10% design allowance the product requirement is >=1050 A for >=3 s. Prototype study direction is one electrical 18S pack with internal service segmentation; exact cell/P-count/mechanical module/BMS/current path remains OPEN. | `PRODUCT_BASELINE_PB-06.json`; `BATTERY_PEAK_CURRENT_DERIVATION_PB06.md`; `BATTERY_PACK_ARCHITECTURE_MASS_FRAMEWORK_PB06.md`; physical peak-current/sag/current-sharing/thermal evidence. |
| TR-053 | PB-06 high-current pack path component screening | **SOURCE-BACKED CANDIDATES / NO SELECTION.** TE EV200 is screened at its published 500 A continuous class; LEM HAX 1000-S/LTC 1000-T provide >=1050 A measurement-range candidates; Amphenol SurLok Plus reaches a published 500 A family boundary. Fuse and service disconnect remain OPEN. A 0.1 mOhm series-path increment costs 25 W at 500 A and 110.25 W at 1050 A, making element-by-element resistance/thermal budgeting mandatory. | `HIGH_CURRENT_PATH_SHORTLIST_PB06.md`; exact MPN/configuration, hot resistance/temperature rise, 1050 A pulse evidence, prospective pack fault current, fuse I2t/interrupt coordination, service-disconnect/load-break classification. |

## Canonical current state inherited from TR-001..TR-053

- `PRODUCT_BASELINE_PB-06.json` is current product authority.
- X8 / eight independent propulsion channels, 18S, 75.6 V full charge, <=80 V outer full-charge ceiling, >=150 V semiconductor class, >=125 A RMS continuous phase current, >=265 A RMS for >=3 s, >=375 A phase peak and +/-400 A minimum measurement range remain frozen.
- Nominal mission target >=10 min at 85 kg payload / 165 kg MTOW reference, hover-equivalent sizing duration >=10 min and 20% gross-pack reserve are frozen.
- Rated battery architecture freezes >=5.0 kWh gross rated energy, 54.0 V minimum loaded bus for full rated power, >=500 A continuous and >=1050 A for >=3 s whole-pack capability.
- Controller electrical-speed capability is >=90 keRPM. This is capability headroom, not expected loaded propeller speed.
- PWM exact value, exact production motor winding inductance, exact battery cell/P-count/pack mass/peak-capable SOC-temperature-SOH envelope, exact MOSFET MPN/count, thermal stack, environment and protection thresholds remain OPEN.
- PB-06 current-path screening has source-backed candidates but no contactor/sensor/connector/fuse/service-disconnect selection is frozen.
- A2/B1 are preserved as historical/reference evidence; no A2/B1 source was changed.
- No component-bearing U1 schematic is allocated.
