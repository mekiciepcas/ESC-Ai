# Autonomous run trace — 2026-09-20 14:23+03:00

Trace ID: **TR-071**
Branch: `uav-rebaseline`
Status: **PB08_B1_GATE_DRIVE_AUXILIARY_SCREEN_ADDED**

## Change
Added `PB08_B1_GATE_DRIVE_AUXILIARY_POWER_SCREEN.md` to convert the legacy B1 12-gate / CSD19536KTT 118 nC typical-Qg evidence into a controlled parametric gate-drive power dependency.

First-order screen: `P_gate,ideal = N_gate * Qg * V_gate * f_pwm`.

Legacy B1 arithmetic examples span 0.2832 W at 10 V/20 kHz to 0.5098 W at 12 V/30 kHz. These are screening points only, not U1 requirements or measurements.

## Evidence boundary
Exact U1 MOSFET/parallel count, PWM, gate amplitude, driver loss and converter loss remain OPEN. No G1 row, backlog task, physical qualification or component approval is promoted.

## Dependency reduction
The gate-drive contribution to `P_aux,pack` is no longer an unstructured unknown: it has a controlled equation and explicit closure inputs. Numeric `P_aux,pack` remains OPEN until exact power-stage/PWM selections exist.

## Preserved history
A2/B1 electrical source, KiCad, PCB/Gerber and manufacturing artifacts were not modified. `U1-SCH-R001` remains unallocated.