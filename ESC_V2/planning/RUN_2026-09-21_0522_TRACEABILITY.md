# Run traceability — 2026-09-21 05:22+03:00

Branch: `uav-rebaseline`
Run-start HEAD: `c3acc6e2cfe21efbf1643c3f7b8765b71c1a4dd7`

## TR-087 — PB-08 traction-pack auxiliary-demand closure contract

S1R.2 was rechecked and remains blocked by controlled installed-axis/Quad-Hexa structural mass evidence plus degraded-mode/single-motor-failure policy. Independent S1R.3B work therefore defined the evidence boundary required before auxiliary loads may be added to total traction-pack current or mission energy.

Artifact: `PB08_TRACTION_PACK_AUXILIARY_DEMAND_CLOSURE_CONTRACT.md`.

Decision: every traction-pack-derived load must identify exact hardware/configuration, load-side demand, conversion path, applicable efficiency, simultaneity/duty, condition applicability and evidence. A load may not be silently assigned zero merely because it is not yet selected. Unknown conversion efficiency leaves real input power/current OPEN. Ideal-lossless calculations remain lower-bound sensitivities only.

The controlled `3000 W / 36.0 V = 83.33 A` value remains propulsion-only lower-bound arithmetic and is not total continuous pack current. TR-086's 7.867–14.161 mA values remain legacy-B1 ideal-lossless gate-charge sensitivities and are not promoted into `P_aux,pack`.

Canonical `UAV_TRACEABILITY.md` was also repaired/advanced to include both TR-086 and TR-087. No G1 row, backlog task, gate, product selection, physical result, A2/B1 electrical source, KiCad schematic, PCB, Gerber or release artifact was changed.
