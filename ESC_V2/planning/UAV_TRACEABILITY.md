# UAV ESC tasarım izlenebilirlik matrisi

Tarih: 20.09.2026

> TR-001..TR-046 canonical content is preserved byte-for-byte in commit history through blob `558a79e824d957844766031e357996bc8e0cee01`. TR-047..TR-070 remain preserved in the immediately preceding canonical blob `2456bb4b0915ffd5104f99a594e94f594a4bb4a4`; this compact continuation repair does not supersede or delete that engineering history.

## Additive continuation repair

| ID | Fonksiyon / karar | UAV rebaseline kararı | Sonraki kanıt |
|---|---|---|---|
| TR-071 | PB-08 B1 gate-drive auxiliary-power screen | **PARAMETRIC REQUALIFICATION PREWORK / NO U1 FREEZE.** Legacy B1 has 12 physical CSD19536KTT gates and controlled typical Qg = 118 nC. First-order ideal gate-charge dependency is `P_gate,ideal = N_gate * Qg * V_gate * f_pwm`; sensitivity points span 0.2832 W at 10 V/20 kHz to 0.5098 W at 12 V/30 kHz. These are legacy screening values, not U1 requirements or measurements. | `PB08_B1_GATE_DRIVE_AUXILIARY_POWER_SCREEN.md`; exact U1 MOSFET/count, PWM, gate amplitude, driver/converter loss before promotion into `P_aux,pack`. |
| TR-072 | Canonical traceability continuity audit after TR-071 | **REPOSITORY CONSISTENCY REPAIR.** AUTO-STATE-69 and the 14:23 run trace/handoff recorded TR-071, but the canonical matrix stopped at TR-070. TR-071 is restored here without promoting any engineering value or gate. | `RUN_2026-09-20_1520_TRACEABILITY.md`; repository history. |

## Canonical PB-08 current state

PB-08 remains active authority. Requirements structure is 12/12 = 100%; G1 value closure remains 15/48 = 31.3%; backlog DONE remains 1/25 = 4.0%; major gates remain 0/8. S1R.2 remains blocked by controlled custom-axis/structural mass and degraded-mode evidence. `P_aux,pack`, `M_cont`, exact pack, exact motor/prop, phase current and PWM remain OPEN. The 83.33 A value remains propulsion-only continuous pack-current lower bound. B1 remains a requalification candidate only; A2/B1 electrical source is immutable. No component-bearing U1 schematic is allocated and `U1-SCH-R001` remains unused.

## History-preservation note

Historical PB-01..PB-07 calculations and TR-001..TR-070 are not deleted or reinterpreted by this compact repair. The previous canonical blob above is the continuity anchor for TR-047..TR-070; commit history remains authoritative for earlier rows.