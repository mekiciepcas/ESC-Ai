# UAV ESC tasarım izlenebilirlik matrisi

Tarih: 19.09.2026  
Amaç: Faz 2 / Faz 3 dokümanları ile mevcut B1 tasarımını yeni UAV ürün gereksinimine bağlamak.

Durum etiketleri: **KEEP**, **REVALIDATE**, **RECALCULATE**, **REPLACE IF REQUIRED**, **OPEN**, **FROZEN**.

> TR-001..TR-046 canonical content is preserved byte-for-byte in commit history through blob `558a79e824d957844766031e357996bc8e0cee01`. The current continuation records TR-047..TR-050 while preserving that history as controlling prior evidence; no prior classification is revoked.

## Additive continuation

| ID | Fonksiyon / karar | UAV rebaseline kararı | Sonraki kanıt |
|---|---|---|---|
| TR-047 | PB-03 hot MOSFET conduction / thermal sensitivity | **PREWORK / exact selection OPEN.** IAUTN15S6N025T/G remains a 150 V calculation anchor. Khot=1.6/2.0/2.3 are sensitivity points only, not guaranteed hot RDS(on) values. N=2 and N=3 remain detailed-study branches; no count, MPN or thermal stack is frozen. | `POWER_STAGE_HOT_THERMAL_SENSITIVITY_PB03.md`; guaranteed hot-resistance policy, switching waveform/energy, transient ZthJC, TIM/baseplate model, current sharing. |
| TR-048 | PB-04 mission duration / energy-sizing policy | **FROZEN PRODUCT TARGET.** >=10 min total mission target and >=10 min hover-equivalent first-order energy-sizing target at 85 kg nominal payload / 165 kg nominal MTOW reference; 20% of gross pack energy is reserved. | `PRODUCT_BASELINE_PB-04.json`; `MISSION_DURATION_ENERGY_BASELINE_PB04.md`; exact cell/pouch, pack mass, sag, minimum loaded bus, usable SOC and mission-power correlation. |
| TR-049 | Controller electrical-speed capability and PWM timing | **eRPM FROZEN / PWM OPEN.** Previous >=60 keRPM capability is superseded by >=90 keRPM because the frozen 80 V / 45 KV / 42-pole envelope screens to 75.6 keRPM no-load linear speed. Preferred PWM analysis window is 24-32 kHz; 20/40 kHz remain boundary sensitivity points. | `PRODUCT_BASELINE_PB-04.json`; `ERPM_PWM_TIMING_CORRECTION_PB04.md`; exact production-motor Ld/Lq or impedance measurement before PWM freeze. |
| TR-050 | PB-05 rated battery architecture | **PARTIAL FROZEN.** Rated 18S pack energy >=5.0 kWh, minimum loaded bus for full rated power 54.0 V, and continuous whole-pack capability >=500 A are product requirements. P50B 18S16P is the primary qualification candidate, P60B 18S14P the mass-optimization candidate and P45B 18S18P the mature alternate; exact cell MPN/topology is OPEN. | `PRODUCT_BASELINE_PB-05.json`; `BATTERY_CELL_PACK_TRADE_PB05.md`; low-SOC/cold/aged sag, pack mass, interconnect/BMS/contactors, peak pack current and physical thermal validation. |

## Canonical current state inherited from TR-001..TR-050

- `PRODUCT_BASELINE_PB-05.json` is current product authority.
- X8 / eight independent propulsion channels, 18S, 75.6 V full charge, <=80 V outer full-charge ceiling, >=150 V semiconductor class, >=125 A RMS continuous phase current, >=265 A RMS for >=3 s, >=375 A phase peak and +/-400 A minimum measurement range remain frozen.
- Nominal mission target >=10 min at 85 kg payload / 165 kg MTOW reference, hover-equivalent sizing duration >=10 min and 20% gross-pack reserve are frozen.
- Rated battery architecture now additionally freezes >=5.0 kWh gross rated energy, 54.0 V minimum loaded bus for full rated power and >=500 A continuous whole-pack capability.
- Controller electrical-speed capability is >=90 keRPM. This is capability headroom, not expected loaded propeller speed.
- PWM exact value, exact production motor winding inductance, exact battery cell/topology/mass/peak current, exact MOSFET MPN/count, thermal stack, environment and protection thresholds remain OPEN.
- A2/B1 are preserved as historical/reference evidence; no A2/B1 source was changed.
- No component-bearing U1 schematic is allocated.

## History-preservation note

The preceding full matrix blob `558a79e824d957844766031e357996bc8e0cee01` remains the canonical detailed text for TR-001..TR-046. This continuation intentionally does not paraphrase or overwrite those rows. Future consolidation should reconstruct the full matrix from that blob plus TR-047..TR-050 rather than treating this compact continuation as deletion of history.
