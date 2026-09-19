# ESC schematic versioning policy

Date: 2026-09-19  
Branch policy: `uav-rebaseline`  
Status: **ACTIVE / REQUIRED BEFORE ANY FUTURE SCHEMATIC EDIT**

## Purpose

All future KiCad schematic changes shall be revision-controlled as engineering document revisions, not performed as silent in-place edits. This policy is additional to Git commit history: Git preserves source history, while the revision system preserves explicit electrical-design baselines that can be referenced by BOM, PCB, ERC/netlist evidence, reviews and physical tests.

## Core rule

**Any change to a `.kicad_sch` file that can alter, add, remove or reconnect electrical content requires a new schematic revision before the change is made.**

A superseded schematic revision is immutable. It shall not be edited to “clean up” history. Corrections are made in the next revision.

## Revision identifier

U1 schematic revisions use monotonically increasing identifiers:

- `U1-SCH-R000` — architecture/scaffold baseline only; not a component-bearing product schematic.
- `U1-SCH-R001` — first component-bearing U1 revision when G1/G2 parents permit it.
- `U1-SCH-R002`, `R003`, ... — subsequent electrical changes.

Revision numbers are never reused, even if a revision is abandoned.

Legacy B1 is not renumbered into the U1 sequence. It remains an immutable migration/reference baseline.

## Storage rule

When component-bearing U1 work begins, every revision shall be stored as a complete project snapshot under a revision-specific directory, for example:

`ESC_V2/hardware_u1/revisions/U1-SCH-R001/`

A revision snapshot must contain the complete KiCad hierarchy required to open and reproduce that revision, including referenced hierarchical sheets and project-local symbol/footprint tables where applicable. Do not version only one child sheet while leaving it dependent on mutable sheets from another revision.

## Required revision manifest

Each revision shall contain a machine-readable manifest recording at minimum:

- `revision_id`
- `parent_revision_id`
- date/time
- creating Git commit SHA once known
- reason for revision
- requirement / decision references that authorize the change
- list of changed schematic sheets
- electrical-change summary
- component/BOM impact summary
- PCB impact summary
- KiCad version used for verification
- netlist export result
- ERC result and explicit waiver/ignored-check list
- review status
- physical-validation status
- release status

Unknown or not-yet-tested fields remain `null`, `OPEN` or `NOT_PERFORMED`.

## Revision creation sequence

Before changing a schematic:

1. Read the current revision register and identify the latest revision.
2. Allocate the next unused `U1-SCH-Rxxx` number.
3. Copy the complete parent project into the new revision directory.
4. Create/update that revision's manifest with status `DRAFT`.
5. Make schematic changes only inside the new revision.
6. Run repository checks plus real KiCad parser/netlist/ERC verification.
7. Record the exact results; do not convert warnings or ignored checks into a PASS by interpretation alone.
8. Update `SCHEMATIC_REVISION_REGISTER.json` and traceability.
9. Update `AUTONOMOUS_HANDOFF.md` and `autonomy_state.json`.

## What does not require a new electrical schematic revision

Changes confined to planning documents, calculation scripts, source-evidence files, CI scripts or other files that do not modify a `.kicad_sch` electrical design do not increment the schematic revision.

A purely graphical/title-block edit inside a `.kicad_sch` still receives a new revision if the schematic file itself is changed. This deliberately favors auditability over revision-number economy.

## Legacy B1 rule

`ESC_V2/hardware_b1/` is a frozen legacy reference for migration analysis. Autonomous work shall not modify its electrical source. If B1 circuitry is reused, it must be copied into a new U1 revision and requalified against current G1/G2 requirements.

## BOM and PCB binding

A BOM or PCB revision may not be described as belonging to “U1” generically. It must reference an exact schematic revision.

Recommended binding:

- schematic: `U1-SCH-Rxxx`
- PCB: `U1-PCB-Rxxx`
- BOM: `U1-BOM-Rxxx`

The three counters do not need to advance together, but every PCB/BOM manifest must identify the exact parent schematic revision.

## Release rule

`DRAFT`, `REVIEW`, `BENCH`, and `RELEASED` are distinct states.

No revision is promoted to `RELEASED`, no Gerbers/manufacturing package is released, and no main-branch merge is performed without explicit user approval. A clean ERC/netlist result is not release approval.

## Autonomous-work enforcement

For future autonomous runs:

- do not edit an existing U1 schematic revision in place;
- allocate a new revision first;
- preserve all previous revisions;
- keep legacy B1 immutable;
- tie every electrical change to requirement/decision evidence;
- tie every ERC/netlist/bench result to the exact revision tested;
- if a revision cannot be created safely, record a blocker rather than bypassing version control.
