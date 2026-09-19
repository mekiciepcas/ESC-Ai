# UAV ESC tasarım izlenebilirlik matrisi

Tarih: 19.09.2026  
Amaç: Faz 2 / Faz 3 dokümanları ile mevcut B1 tasarımını yeni UAV ürün gereksinimine bağlamak.

> Canonical matrix history through TR-046 is preserved in prior revisions. This additive continuation avoids reinterpreting earlier A2/B1 evidence while recording current PB-03 work.

## Additive traceability continuation

| ID | Function / decision | Current disposition | Evidence / next proof |
|---|---|---|---|
| TR-047 | PB-03 hot MOSFET conduction/thermal sensitivity | **PREWORK / OPEN selection.** IAUTN15S6N025T/G remains a 150 V calculation anchor. Khot=1.6/2.0/2.3 are sensitivity points only, not guaranteed hot RDS(on) values. N=2 and N=3 remain detailed-study branches; no count or MPN is frozen. | `POWER_STAGE_HOT_THERMAL_SENSITIVITY_PB03.md`; next: guaranteed hot-resistance policy, switching waveform/energy, transient ZthJC, TIM/baseplate model, current sharing. |

## Current controlled baseline summary

- PB-03 remains the product-baseline authority.
- X8 / eight independent propulsion channels, 18S / 75.6 V full-charge, <=80 V outer full-charge ceiling, >=150 V MOSFET class, >=125 A RMS continuous phase current, >=265 A RMS for >=3 s, >=375 A phase peak, +/-400 A minimum measurement range remain frozen.
- PWM, exact motor winding inductance, exact MOSFET MPN/count, thermal stack, pack Ah/Wh/min-loaded-bus, environment and protection thresholds remain OPEN.
- A2/B1 remain historical/reference evidence and were not modified by TR-047.
- No component-bearing U1 schematic has been allocated.

## Historical authority

The full TR-001..TR-046 matrix remains available in repository history immediately preceding this revision and in the linked controlled evidence files. This continuation does not revoke or supersede those entries; it adds TR-047 only.
