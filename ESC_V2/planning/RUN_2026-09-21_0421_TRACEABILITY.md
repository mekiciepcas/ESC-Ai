# Run traceability — 2026-09-21 04:21+03:00

Branch: `uav-rebaseline`  
Run-start HEAD: `acaacc73dca1259a9d6501ff7dbc2642b7232b98`

## TR-086 — PB-08 legacy B1 gate-drive traction-pack current sensitivity

**Disposition:** REQUALIFICATION PREWORK / NO U1 AUXILIARY-BUDGET OR GATE ADVANCE.

Using only the already-controlled TR-071 legacy B1 sensitivity endpoints and the frozen PB-08 36.0 V loaded floor, the ideal-lossless traction-pack current lower bounds are:

- 0.2832 W / 36.0 V = **7.867 mA** for the legacy 10 V / 20 kHz endpoint.
- 0.5098 W / 36.0 V = **14.161 mA** for the legacy 12 V / 30 kHz endpoint.
- Endpoint span = **6.294 mA**.

These values are arithmetic translations of legacy B1 screening points only. They are not U1 allocations, measurements, or a closed `P_aux,pack` budget. Exact U1 MOSFET/count, Qg basis, gate amplitude, PWM, driver demand and auxiliary conversion efficiency remain OPEN. Quiescent and other auxiliary loads are excluded.

Evidence: `PB08_B1_GATE_DRIVE_PACK_CURRENT_SENSITIVITY.md`, parent TR-071, `PB08_TRACTION_PACK_AUXILIARY_LOAD_LEDGER.md`.

Canonical counters remain unchanged: requirements structure 12/12 = 100%; G1 value closure 15/48 = 31.3%; backlog DONE 1/25 = 4.0%; major gates 0/8.
