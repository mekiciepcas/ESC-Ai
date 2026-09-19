# Run traceability — 2026-09-19 16:19+03

This additive record avoids rewriting the large canonical matrix while preserving traceable new evidence.

- **TR-043 / G0 product-input closure:** `G0_INPUT_CLOSURE_PACKET.json` defines the minimal missing vehicle inputs. Product values remain null; no competitor/B1 values are promoted.
- **TR-044 / CAN physical/timing verification:** `CAN_BUS_VERIFICATION_CONTRACT.json` defines CANV-01..10 and keeps protocol, bitrate, topology, harness, grounding, transient/EMC and acceptance limits null until frozen.
- **TR-045 / KiCad CLI reproducibility:** `.github/workflows/kicad-u1-verify.yml` installs KiCad on a hosted runner, executes the repository scaffold checker, asks KiCad CLI to export a netlist, runs ERC, and retains the report as an artifact. Workflow existence is not a PASS claim; a completed run must be observed first.

Canonical `UAV_TRACEABILITY.md` TR-001..TR-042 remains authoritative for prior decisions. This file is the run-local additive trace until the next safe canonical matrix consolidation.
