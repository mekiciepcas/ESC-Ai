# ESC autonomous handoff

Date: 2026-09-19 17:16+03:00  
Branch: `uav-rebaseline`  
Status: `PROGRESS_REVISION_POLICY_CI_AND_G3_ERC_CONTRACT`  
Repository HEAD immediately before this handoff update: `7b759df5877af73d30f076723a75f9f4148dd7d1`.

## Progress percentages

- Requirements planned-domain/schema structure: **12/12 = 100%**.
- G1 SYSTEM FREEZE value closure: **1/46 PASS = 2.2%**.
- Backlog tasks explicitly DONE: **1/25 = 4%**.
- Major product gates closed: **0/8 = 0%**.
- U1 KiCad architecture scaffold: **100% structure coverage**.
- U1 KiCad scaffold parser/netlist/ERC validation: **100% for the current zero-component scaffold only**.
- Legacy B1 reproducible KiCad baseline audit: **100% for the recorded software-baseline scope only**.
- Schematic revision-control policy definition: **100%**.
- Schematic revision-control CI enforcement: **100% for the current policy/checker baseline**.
- Future U1 G3 ERC-policy definition: **100% structure defined, not yet exercised on a component-bearing U1 revision**.
- U1 component-bearing production-intent schematic: **0%**, still blocked by G1/G2.

The conservative product counters remain unchanged because this run strengthened configuration control and review evidence without inventing product values or prematurely allocating a schematic revision.

## Run summary

The run re-read the current plan, traceability, backlog, mission requirements, requirements master/progress, handoff/state and the newly mandatory schematic-versioning authorities against the actual `uav-rebaseline` branch. It then converted the versioning rule from documentation into an enforceable CI control, defined the future G3 ERC acceptance contract, added a revision evidence manifest template, and produced a compact G0 input form for the remaining product-specific critical path. No `.kicad_sch` file was changed and `U1-SCH-R001` was not allocated because G1/G2 parents remain open.

## Tasks completed

1. Created `U1_G3_ERC_POLICY.json` with explicit rules for ERC errors/warnings, single-use global labels, four-way junctions, SPICE-model issues, footprint-filter mismatches, power-drive semantics, unconnected required pins, pin-type conflicts, hierarchical interfaces and library reproducibility.
2. Defined that project-level ignored ERC categories are not revision-specific waivers and cannot be carried automatically into G3.
3. Created `SCHEMATIC_REVISION_MANIFEST.template.json` with requirement/decision refs, changed sheets, BOM/PCB impact, exact KiCad/netlist/ERC results, waiver list, review state, physical evidence and release state.
4. Created `verify_schematic_revision_policy.py` to validate the revision register, revision directory/manifest consistency, immutable legacy B1 and frozen `U1-SCH-R000`, and no in-place electrical changes to an already allocated component-bearing revision.
5. Created `.github/workflows/schematic-revision-policy.yml` as a lightweight full-history diff guard independent of the heavier KiCad install workflow.
6. Observed GitHub Actions run `35448141446`, job `105910551415`, complete successfully. Checker output was `PASS`, `registered_component_bearing_revisions=0`, `next_component_bearing_revision=U1-SCH-R001`, `changed_files_checked=1`.
7. Created `G0_USER_INPUT_FORM.md` from the existing null-only closure packet. It exposes the 14 missing product inputs without defaults or competitor substitutions.
8. Added additive traceability TR-050 through TR-054 in `RUN_2026-09-19_1715_TRACEABILITY.md`.
9. Updated `autonomy_state.json` to AUTO-STATE-29.
10. Preserved all product-specific G0/G1/G2 values as OPEN/null and made no U1 component selection.

## Files added / changed

- `planning/U1_G3_ERC_POLICY.json`
- `planning/SCHEMATIC_REVISION_MANIFEST.template.json`
- `planning/verify_schematic_revision_policy.py`
- `.github/workflows/schematic-revision-policy.yml`
- `planning/G0_USER_INPUT_FORM.md`
- `planning/RUN_2026-09-19_1715_TRACEABILITY.md`
- `planning/autonomy_state.json`
- `planning/AUTONOMOUS_HANDOFF.md`

## Engineering / configuration-control findings

- The user-requested versioning rule is now enforceable rather than advisory.
- `LEGACY-B1` and `U1-SCH-R000` remain frozen references.
- The revision register currently contains **zero** allocated component-bearing U1 revisions; the next valid ID remains `U1-SCH-R001`.
- An existing allocated U1 revision is not an editable working folder. If an electrical/project change is needed after that revision exists in the base history, the checker requires a new revision allocation.
- A clean legacy/scaffold ERC cannot be used as a future G3 pass. Future component-bearing revisions require their own exact parser/netlist/ERC/waiver/interface/BOM-footprint evidence.
- No component-bearing revision was created merely to show progress; that would violate the current gate logic.

## Assumptions / evidence level

- 70–100 kg remains USER TARGET payload, not MTOW.
- Remaining G0 vehicle/mission/environment values remain OPEN/null.
- Revision-policy workflow result is OBSERVED CI SOFTWARE EVIDENCE for run `35448141446` only.
- G3 ERC policy is a DEFINED ACCEPTANCE CONTRACT, not verification evidence of a future U1 schematic.
- Physical bench, thermal, EMC, dyno and flight evidence remain NOT PERFORMED.

## Unresolved blockers

- 14 G0 product-specific inputs: nominal payload, airframe/battery/equipment mass, mission/hover duration, ambient range, altitude, wind, ingress target, single-motor-failure policy, coaxial allowance and max vehicle span.
- MTOW and final rotor architecture.
- Propulsion operating point and battery architecture.
- ESC VBUS/current/eRPM/PWM/transient envelope.
- Semiconductor, driver, MCU, sensing, DC-link, auxiliary-power, CAN and fault architecture freeze.
- First component-bearing U1 schematic revision and production BOM.

## Exact next recommended tasks

1. Obtain/approve the real product values in `G0_USER_INPUT_FORM.md`; write back only user-supplied values into `mission_requirements.json` and `G0_INPUT_CLOSURE_PACKET.json`.
2. Once G0 inputs are available, calculate MTOW cases and close the rotor architecture/thrust requirement chain before selecting motor/prop operating points.
3. In parallel, consolidate TR-043..TR-054 into canonical `UAV_TRACEABILITY.md` without dropping prior history and continue requirement-independent exact support-part audits.
4. Prepare a revision-creation helper that can instantiate `U1-SCH-R001` from a frozen parent when G1/G2 page readiness is achieved, but **do not allocate R001 yet**.
5. When parent requirements truly freeze, allocate `U1-SCH-R001` before the first component-bearing KiCad edit, then run exact KiCad parser/netlist/ERC evidence against that revision.

## Dependency chain

`G0 real vehicle inputs -> MTOW -> G1A rotor architecture/thrust -> G1B propulsion operating point -> G1C battery/transient -> G1 SYSTEM FREEZE -> G2 architecture freeze -> allocate U1-SCH-R001 -> component-bearing schematic -> G3 schematic/BOM review`

## Next-run briefing

Do not edit B1, R000 or any future existing revision in place. The versioning guard is now live and observed PASS. The product critical path is no longer KiCad tooling; it is the unresolved G0 vehicle inputs. Continue safe independent audits where possible, but prioritize converting actual G0 inputs into MTOW/rotor/propulsion requirements as soon as those values are supplied. Progress counters remain **100% requirements structure / 2.2% G1 value closure / 4% backlog DONE / 0% major gates / 0% component-bearing U1** until controlling evidence genuinely changes.
