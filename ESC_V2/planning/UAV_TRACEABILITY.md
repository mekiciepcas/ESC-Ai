# UAV ESC tasarım izlenebilirlik matrisi

Tarih: 21.09.2026

> TR-001..TR-046 canonical content is preserved byte-for-byte in commit history through blob `558a79e824d957844766031e357996bc8e0cee01`. TR-047..TR-070 remain preserved in canonical blob `2456bb4b0915ffd5104f99a594e94f594a4bb4a4`; TR-071..TR-090 remain preserved in canonical blob `fae32f3ba0832c550ce9469e41703dc15e68a6ea`. This compact continuation does not supersede or delete that engineering history.

## Additive continuation

| ID | Fonksiyon / karar | UAV rebaseline kararı | Sonraki kanıt |
|---|---|---|---|
| TR-091 | PB-08 degraded-mode decision evidence contract | **EVIDENCE CONTRACT / NO SAFETY DECISION / NO ARCHITECTURE FREEZE.** Defines explicit controlled decision classes for single propulsion-axis loss and requires authority, normative requirement, failure boundary, required response, prohibited unsafe responses, acceptance criteria, evidence and architecture-independence. No class is selected and no requirement is inferred from Quad/Hexa topology. | `PB08_DEGRADED_MODE_DECISION_CONTRACT.md`; explicit controlled user/system-safety decision or approved requirement. |
| TR-092 | PB-08 degraded-mode decision result schema | **VERIFICATION ARTIFACT / UNPOPULATED / NO GATE ADVANCE.** Machine-readable result record holds authority, decision class, one-axis-loss boundary, required/prohibited responses, acceptance criteria, evidence and review. Decision fields remain null/open until controlled evidence exists; architecture/G0/G1 advancement flags remain false. | `PB08_DEGRADED_MODE_DECISION_RESULT.template.json`; populate only from an explicit controlled safety decision/requirement. |
| TR-093 | PB-08 degraded-mode decision fail-closed verifier | **FAIL-CLOSED VERIFICATION TOOL / NO PHYSICAL OR SAFETY QUALIFICATION.** Rejects absent authority, decision class, normative requirement, one-axis-loss boundary, required/prohibited responses, evidence, architecture-independence, review and class-specific acceptance criteria. PASS means record completeness only and explicitly leaves architecture/G0/G1 advancement false. | `verify_pb08_degraded_mode_decision.py`; run only against a populated TR-092 record backed by controlled safety authority. |
| TR-094 | Canonical traceability synchronization after TR-093 | **REPOSITORY CONSISTENCY REPAIR / NO GATE ADVANCE.** Prior handoff and AUTO-STATE-87 correctly recorded TR-091..TR-093 while canonical `UAV_TRACEABILITY.md` ended at TR-090. TR-091..TR-093 are folded into the canonical continuity chain here without changing any engineering value, physical claim, backlog state or G1 row. | `RUN_2026-09-21_0922_TRACEABILITY.md`; repository history. |

## Canonical PB-08 current state

PB-08 remains active authority. Requirements structure is 12/12 = 100%; G1 value closure remains 15/48 = 31.3%; backlog DONE remains 1/25 = 4.0%; major gates remain 0/8. S1R.2 remains blocked by controlled custom-axis/structural mass and degraded-mode evidence. `P_aux,pack`, total continuous/peak traction-pack current, exact pack, exact motor/prop, phase current and PWM remain OPEN. The 83.33 A value remains propulsion-only continuous pack-current lower bound. P50B 12S4P remains reference-only; the cell-only sag, conditional non-cell-resistance screen, installed-path ledger, OCV/Rdc evidence contract, cell-mass screen, physical-evidence templates and fail-closed verifiers do not establish installed-pack compliance. B1 remains a requalification candidate only; A2/B1 electrical source is immutable. No component-bearing U1 schematic is allocated and `U1-SCH-R001` remains unused.

## History-preservation note

Historical PB-01..PB-07 calculations and TR-001..TR-090 are not deleted or reinterpreted by this compact continuation. The previous canonical blobs above remain continuity anchors; commit history remains authoritative for earlier rows.