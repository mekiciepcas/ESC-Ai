# Run traceability — 2026-09-19

This additive record preserves new configuration-control and G3 review evidence without overwriting prior canonical history.

- **TR-050 / Schematic revision configuration control:** `SCHEMATIC_VERSIONING_POLICY.md` and `SCHEMATIC_REVISION_REGISTER.json` make `LEGACY-B1` and `U1-SCH-R000` frozen references and reserve `U1-SCH-R001` as the first future component-bearing revision. Superseded revisions are immutable and revision IDs are never reused.
- **TR-051 / Revision evidence manifest:** `SCHEMATIC_REVISION_MANIFEST.template.json` defines the minimum machine-readable binding for requirement references, changed sheets, BOM/PCB impact, exact KiCad/netlist/ERC evidence, waivers, review, physical validation and release state. Unknown/test-not-run values remain null/OPEN/NOT_PERFORMED.
- **TR-052 / Automated immutability guard:** `verify_schematic_revision_policy.py` plus `.github/workflows/schematic-revision-policy.yml` provide CI enforcement for frozen B1/U1-R000 sources and registered U1 revision lineage. Existing registered component-bearing revisions may not have schematic/project electrical files changed in place; a new revision must be allocated first.
- **TR-053 / Future G3 ERC policy:** `U1_G3_ERC_POLICY.json` converts the previously observed KiCad ignored categories into explicit U1 review rules. A clean scaffold or B1 run cannot be reused as a future component-bearing G3 PASS, and project-level ignored categories are not treated as revision-specific waivers.

No product electrical value, MPN selection, G1/G2 architecture selection, bench result or physical qualification was introduced by these records.
