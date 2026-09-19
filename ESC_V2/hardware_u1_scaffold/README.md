# ESC U1 KiCad architecture scaffold

This directory is a **concrete KiCad pre-G2 artifact**, not the production U1 schematic.

`ESC_U1_SCAFFOLD.kicad_sch` is intentionally component-free. It gives the real U1 electrical architecture a stable KiCad surface now, while preventing open G0/G1/G2 values from being silently converted into component selections.

## What is concrete

- a KiCad schematic file with 12 architecture blocks;
- a machine-readable page/block readiness matrix;
- an executable consistency checker;
- explicit gating for when each block may receive real components.

## What is deliberately not claimed

No MOSFET, gate driver, shunt, DC-link capacitor, MCU, CAN transceiver, connector, PWM frequency, current rating or bus-voltage class is selected by this scaffold.

## Verification

Run:

```bash
python verify_u1_scaffold.py
```

A PASS proves internal scaffold consistency only. It is **not** KiCad ERC, electrical validation, thermal validation or hardware verification. `kicad-cli` must later be run when available and after component-bearing pages exist.
