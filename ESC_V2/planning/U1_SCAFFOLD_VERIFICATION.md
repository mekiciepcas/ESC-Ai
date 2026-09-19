# U1 KiCad scaffold verification

Date: 2026-09-19 16:34+03:00  
Branch: `uav-rebaseline`

## Scope

Verify the pre-G2 KiCad architecture scaffold without presenting it as a component-bearing production schematic.

Artifact under test:
- `ESC_V2/hardware_u1_scaffold/ESC_U1_SCAFFOLD.kicad_sch`
- `ESC_V2/hardware_u1_scaffold/U1_PAGE_READINESS.json`
- `ESC_V2/hardware_u1_scaffold/verify_u1_scaffold.py`

Machine-readable CI record:
- `ESC_V2/planning/KICAD_CI_VERIFICATION.json`

## Stage 1 — repository consistency checker

The repository checker was executed locally and again in GitHub Actions.

Observed result:

```text
PASS
blocks=12
component_symbols=0
premature_baseline_tokens=0
s_expression_balance=0
```

This confirms the intended 12 architecture blocks, zero populated component symbols, no guarded legacy/product-baseline tokens and balanced S-expression delimiters.

## Stage 2 — real KiCad CLI parser/netlist/ERC

The first hosted CI attempt installed Ubuntu's base-repository KiCad 7.0.11 and failed to load the newer schematic file. That failure was retained as evidence and was not misreported as a schematic defect.

The workflow was then corrected to use KiCad's official stable Ubuntu PPA:

`ppa:kicad/kicad-10.0-releases`

Observed successful GitHub Actions run:

- Workflow: `KiCad U1 Verify`
- Run ID: `35446125432`
- Head commit: `6fe8638508df7533eb9cb27ac200e77d0915b00b`
- Runner: Ubuntu 24.04.5 LTS
- `kicad-cli --version`: **10.0.6**
- Repository scaffold checker: **PASS**
- KiCad netlist export: **PASS**, non-empty output required by workflow
- KiCad ERC: **PASS**
- ERC violations: **0**
- ERC errors: **0**
- ERC warnings: **0**
- Evidence artifact: `kicad-u1-verification`, artifact ID `10584899264`
- Artifact digest: `sha256:0ed6b0dac1818c79558c0c9429088ab104e5ca71bccec9dd4add1de762113ab3`

The workflow uploads:
- `KICAD_VERSION.txt`
- `ESC_U1_SCAFFOLD.net`
- `ERC.rpt`

## What this proves

- The committed U1 architecture scaffold is accepted by **real KiCad 10.0.6**, not only by a text checker.
- KiCad CLI can export a non-empty netlist from the scaffold.
- KiCad ERC reports zero errors and warnings on this architecture-only artifact.
- The same commit also passes the repository anti-hallucination checker.

## What this does NOT prove

- It does not prove a component-bearing U1 electrical design because the scaffold intentionally contains zero selected component symbols.
- It does not close G1 or G2 requirements.
- It does not qualify MOSFETs, gate drivers, sensing, DC-link, connectors or auxiliary power.
- It does not prove PCB DRC, manufacturability, thermal performance, EMI performance or physical validation.
- It is not a G3 schematic-design-review PASS and is not production readiness evidence.

## Engineering interpretation

The KiCad tooling gap is now closed for the architecture scaffold: the repository has a reproducible CI path using KiCad 10.0.6, parser/netlist export and ERC. The next legitimate KiCad step is not to add guessed parts; it is to promote individual blocks to component-bearing pages only after their parent G1/G2 requirements are frozen and traceable.
