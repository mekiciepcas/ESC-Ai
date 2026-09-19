# Run traceability — 2026-09-19 16:19+03

This additive record preserves new evidence without risking destructive overwrite of the large canonical matrix.

- **TR-043 / G0 product-input closure:** `G0_INPUT_CLOSURE_PACKET.json` defines the minimal missing vehicle inputs. Product values remain null; no competitor/B1 values are promoted.
- **TR-044 / CAN physical/timing verification:** `CAN_BUS_VERIFICATION_CONTRACT.json` defines CANV-01..10 and keeps protocol, bitrate, topology, harness, grounding, transient/EMC and acceptance limits null until frozen.
- **TR-045 / KiCad CLI reproducibility:** `.github/workflows/kicad-u1-verify.yml` now uses the official `ppa:kicad/kicad-10.0-releases` path. GitHub Actions run `35446125432` at head `6fe8638508df7533eb9cb27ac200e77d0915b00b` completed successfully with KiCad CLI `10.0.6`: repository scaffold checker PASS, non-empty KiCad netlist export PASS, and ERC PASS with 0 violations / 0 errors / 0 warnings. Machine-readable evidence: `KICAD_CI_VERIFICATION.json`.
- **TR-046 / KiCad evidence scope:** the observed ERC PASS applies only to the component-free U1 architecture scaffold. It does not close G1/G2, does not qualify a component-bearing schematic, and shall not be interpreted as G3 or production readiness.

Canonical `UAV_TRACEABILITY.md` TR-001..TR-042 remains authoritative for prior decisions. This run-local record is additive evidence until the next safe canonical matrix consolidation.
