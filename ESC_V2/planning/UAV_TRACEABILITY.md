# UAV ESC tasarım izlenebilirlik matrisi

Tarih: 19.09.2026  
Amaç: Faz 2 / Faz 3 dokümanları ile mevcut B1 tasarımını yeni UAV ürün gereksinimine bağlamak.

Durum etiketleri: **KEEP**, **REVALIDATE**, **RECALCULATE**, **REPLACE IF REQUIRED**, **OPEN**, **FROZEN**.

> TR-001..TR-046 canonical content is preserved byte-for-byte in commit history through blob `558a79e824d957844766031e357996bc8e0cee01`. The current continuation records TR-047 while preserving that history as controlling prior evidence; no prior classification is revoked.

## Additive continuation

| ID | Fonksiyon / karar | UAV rebaseline kararı | Sonraki kanıt |
|---|---|---|---|
| TR-047 | PB-03 hot MOSFET conduction / thermal sensitivity | **PREWORK / exact selection OPEN.** IAUTN15S6N025T/G remains a 150 V calculation anchor. Khot=1.6/2.0/2.3 are sensitivity points only, not guaranteed hot RDS(on) values. N=2 and N=3 remain detailed-study branches; no count, MPN or thermal stack is frozen. | `POWER_STAGE_HOT_THERMAL_SENSITIVITY_PB03.md`; guaranteed hot-resistance policy, switching waveform/energy, transient ZthJC, TIM/baseplate model, current sharing. |

## Canonical current state inherited from TR-001..TR-046

- `PRODUCT_BASELINE_PB-03.json` remains product authority.
- X8 / eight independent propulsion channels, 18S, 75.6 V full charge, <=80 V outer full-charge ceiling, >=150 V semiconductor class, >=125 A RMS continuous phase current, >=265 A RMS for >=3 s, >=375 A phase peak and +/-400 A minimum measurement range remain frozen.
- PWM, exact production motor winding inductance, exact MOSFET MPN/count, thermal stack, pack Ah/Wh/minimum-loaded-bus, environment and protection thresholds remain OPEN.
- A2/B1 are preserved as historical/reference evidence; no A2/B1 source was changed by TR-047.
- No component-bearing U1 schematic is allocated.

## History-preservation note

The immediately preceding full matrix blob `558a79e824d957844766031e357996bc8e0cee01` is the canonical detailed text for TR-001..TR-046. This continuation intentionally does not paraphrase or overwrite those rows. Future consolidation should reconstruct the full matrix from that blob plus TR-047 rather than treating this compact continuation as deletion of history.
