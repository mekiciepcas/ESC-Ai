# ESC autonomous handoff

Date: 2026-09-19 16:58+03:00  
Branch: `uav-rebaseline`  
Status: `PROGRESS_SCHEMATIC_VERSIONING_POLICY_ENFORCED`  
Repository HEAD immediately before this handoff update: `5223e92b7ce1312aac1cbeb005368b5993c561a6`.

## Product/gate status

- Requirements planned-domain/schema structure: **12/12 = 100%**.
- G1 SYSTEM FREEZE value closure: **1/46 PASS = 2.2%**.
- Backlog tasks explicitly DONE: **1/25 = 4%**.
- Major product gates closed: **0/8 = 0%**.
- U1 KiCad architecture scaffold: **100% structure coverage**.
- U1 component-bearing production-intent schematic: **0%**, still blocked by G1/G2.
- Legacy B1 reproducible KiCad software-baseline audit: complete for recorded scope only.
- Schematic revision-control policy: **ACTIVE / mandatory**.

## New user-directed rule

All future schematic updates must use explicit engineering revisioning in addition to normal Git history. No superseded U1 schematic revision may be silently edited in place.

The policy is now recorded in:

- `planning/SCHEMATIC_VERSIONING_POLICY.md`
- `planning/SCHEMATIC_REVISION_REGISTER.json`

## Revision scheme

- `LEGACY-B1` — frozen migration/reference source. Do not edit `hardware_b1` electrical source in place.
- `U1-SCH-R000` — existing zero-component architecture scaffold reference only. It is not a product schematic and does not close G3.
- `U1-SCH-R001` — reserved as the first future component-bearing U1 revision once parent G1/G2 requirements permit it.
- Subsequent electrical changes use monotonically increasing `U1-SCH-R002`, `R003`, ... identifiers. Revision numbers are never reused.

Every future component-bearing revision must be a complete hierarchical KiCad project snapshot under a revision-specific directory rather than a single mutable child-sheet copy.

## Mandatory revision workflow

Before any `.kicad_sch` change:

1. Read `SCHEMATIC_REVISION_REGISTER.json`.
2. Allocate the next unused revision ID.
3. Copy the complete parent hierarchy into the new revision directory.
4. Create the revision manifest as `DRAFT` with requirement/decision references.
5. Make schematic changes only in the new revision.
6. Run repository checks plus real KiCad parser/netlist/ERC verification.
7. Record exact ERC result, ignored/waived checks and KiCad version against that revision.
8. Update revision register, traceability, state and handoff.

If this sequence cannot be completed safely, record a blocker; do not bypass versioning.

## BOM / PCB / validation binding

Future outputs must reference exact design revisions, e.g. `U1-SCH-Rxxx`, `U1-PCB-Rxxx`, `U1-BOM-Rxxx`. PCB/BOM counters do not have to match the schematic counter, but their manifests must identify the exact parent schematic revision.

ERC/netlist/bench/thermal/EMC evidence must also identify the exact revision actually tested. A PASS on one revision cannot be carried forward automatically to a later revision.

## Release guard

Revision status and production release remain separate. `DRAFT`, `REVIEW`, `BENCH` and `RELEASED` are distinct. No Gerbers/manufacturing package, no `RELEASED` status and no merge to `main` without explicit user approval.

## Previous engineering evidence retained

The prior B1 KiCad baseline remains valid as migration evidence: KiCad 10.0.6 parses the complete legacy hierarchy, exports a non-empty netlist and reports zero messages from enabled ERC checks after CI footprint-library resolution. This does not qualify B1 for U1 and ignored ERC categories remain explicit review scope.

Legacy TPS62160DGKR and TLV75533PDBVR remain REVALIDATE references only. No U1 selection was made.

## Current blockers

G0/G1 product-specific mass, mission, environment, rotor/failure policy, propulsion operating point, battery/transient envelope, phase current/PWM and related architecture inputs remain open. Therefore the first component-bearing U1 revision is not yet authorized by its parent requirements.

## Exact next tasks

1. Continue G0 input closure and requirement-independent migration evidence.
2. Define the future U1 G3 ERC policy for currently ignored KiCad check categories.
3. Continue exact lifecycle/package/source audit for support parts without promoting product selections.
4. Consolidate additive traceability safely.
5. When parent requirements genuinely freeze, allocate `U1-SCH-R001` **before** making the first component-bearing schematic edit.

## Next-run briefing

Do not edit `hardware_b1` source and do not edit an existing U1 schematic revision in place. Treat `SCHEMATIC_VERSIONING_POLICY.md` and `SCHEMATIC_REVISION_REGISTER.json` as mandatory planning authorities at run start. Keep product values OPEN/null until controlling evidence closes them. Schematic versioning is now a hard project rule, not an optional documentation step.
