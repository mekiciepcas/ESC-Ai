# Sprint S1 — PB-02/PB-03 -> G1 SYSTEM FREEZE

Date: 2026-09-19  
Branch: `uav-rebaseline`  
Status: **ACTIVE — S1.1 DONE / S1.2 ACTIVE**  
Parent phase: **PHASE A — System and propulsion definition**  
Gate target: **G1 — SYSTEM ELECTRICAL FREEZE**  
Current baseline authority: `PRODUCT_BASELINE_PB-03.json`

## Why this sprint exists

PB-02 froze the X8 vehicle direction, MTOW targets, 56x20 / 45KV / 18S propulsion class, DC-side ESC capability, >=150 V semiconductor class and >=60 keRPM controller capability. Sprint S1.1 then created PB-03 and closed the phase-current design envelope. G1 is still open because PWM, battery-energy/minimum-bus, environment, protection and thermal-domain values remain unresolved.

This sprint converts the remaining system-level electrical unknowns into a closed, traceable G1 envelope before exact component-bearing U1 schematic work begins. It is an execution sprint, **not a new approval gate**.

## Sprint rule

- Do not reopen PB-03 frozen decisions without PB-04/ECO.
- Do not copy DC current into phase-current requirements.
- Do not freeze values from competitor headline ratings alone.
- Use primary-source motor/device data, explicit calculations and bounded product decisions.
- Keep `U1-SCH-R001` unallocated until the allocation guard is READY.
- No Gerber, manufacturing release or `main` merge is authorized by this sprint.

## S1.1 — Phase-current model closure — **DONE**

Closed outputs:

- `PHASE_CURRENT_MODEL_PB02.md`
- `PHASE_CURRENT_MODEL_PB02.json`
- `PRODUCT_BASELINE_PB-03.json`
- `verify_phase_current_pb03.py`
- `.github/workflows/phase-current-pb03.yml`

Frozen design-capability requirements:

- continuous phase current: **>=125 A RMS**,
- short-duration phase overload: **>=265 A RMS for >=3 s**,
- instantaneous phase-current design peak: **>=375 A**,
- phase-current measurement range: **at least -400 A to +400 A**.

Evidence method:

- current X13 G2 69 V / MFP56x20 manufacturer torque/load curve,
- source-backed previous X13 18S / 45 KV back-EMF constants used as a bounded electrical proxy because public G2 winding constants are not published,
- two independent torque-constant interpretations form a conservative current band,
- explicit 15% rated-point and 10% maximum-curve design/model allowances.

Physical production-motor correlation remains mandatory; S1.1 closes design requirements, not bench verification.

## S1.2 — PWM / ripple / switching-loss closure — **ACTIVE**

Goal: close `G1-07` and create the quantitative parent for G2 power-stage optimization.

Required work:
- resolve whether the published X13 18S `R/L/M` values can be converted into a defensible phase/line inductance model for the G2-class motor,
- retain uncertainty if exact G2 inductance is unavailable and define the required bench measurement,
- use the now-frozen 125 A RMS continuous / 265 A RMS 3 s / 375 A peak phase-current envelope,
- enforce the >=60 keRPM control requirement,
- compare exact >=150 V MOSFET candidate switching-energy / Qg / hot RDS(on) data,
- sweep current ripple across candidate PWM frequencies,
- compare switching + conduction loss at nominal/hot conditions,
- check dead-time and current-sampling windows.

Outputs:
- `PWM_RIPPLE_LOSS_STUDY_PB03.md`
- machine-readable PWM/loss evidence record,
- selected PWM frequency or bounded operating range,
- next PB revision only when a new frozen product value is added.

Exit condition: PWM is frozen from control + ripple + loss evidence, not inherited from B1/Faz2/Faz3.

## S1.3 — 18S energy / minimum-loaded-bus closure — **QUEUED**

Goal: finish the open battery-side G1C values and make the rated 18S product self-consistent.

Required work:
- mission energy model for 150 / 165 / 180 kg cases,
- target flight-time / hover-equivalent design point,
- reserve-energy policy,
- pack Ah / usable Wh target,
- minimum loaded bus including cell sag and cutoff,
- continuous / peak pack current,
- BMS / contactor / fuse / disconnect behavior,
- battery-mass allocation inside the <=80 kg operating-empty budget.

Outputs:
- `BATTERY_ENERGY_BASELINE_PB04_CANDIDATE.md`
- battery architecture update / new PB revision only when new frozen product values are added or existing frozen values change.

Exit condition: `G1C-02` and the energy/mass parents needed by G0/G1 are numeric and traceable.

## S1.4 — Environment, derating and protection envelope — **QUEUED**

Goal: close the remaining system-level operating boundaries that directly affect the ESC architecture.

Required work:
- minimum/maximum ambient product targets,
- altitude and cooling derating basis,
- ingress/cooling concept boundary,
- baseplate-temperature design limit,
- OV/UV response thresholds below the existing <=120 V repetitive stress ceiling,
- OCP / OTP strategy and latency targets,
- watchdog and command-timeout numerical requirements.

Outputs:
- `ENVIRONMENT_DERATING_BASELINE.md`
- `PROTECTION_THRESHOLD_REQUIREMENTS.md`

Exit condition: G1 environmental/protection rows are frozen as product requirements while later bench verification remains explicitly pending.

## S1.5 — G2 pre-freeze: exact power-stage short list — **QUEUED / BOUNDED PREWORK ALLOWED**

Goal: avoid a dead stop immediately after G1 while not pretending G2 is already closed.

Required work:
- exact 150 V MOSFET candidates and hot `RDS(on)` / `Qg` / switching-energy / SOA comparison,
- required MOSFET parallel count per switch using PB-03 phase-current requirements,
- gate-driver current requirement and exact high-voltage half-bridge driver shortlist,
- preliminary current-sense shunt / CSA shortlist consistent with +/-400 A range,
- DC-link capacitance / ripple-current / precharge / regen screening,
- thermal-loss budget.

Outputs:
- `POWER_STAGE_TRADE_PB03_G2_PREWORK.md`
- exact evidence-backed shortlist, no production-selection claim before G2.

Exit condition: G2 can start from a quantified shortlist immediately after G1 closure.

## S1.6 — Configuration-control closeout — **QUEUED**

Required work:
- synchronize `G1_REQUIREMENTS_MATRIX.json`, `REQUIREMENTS_PROGRESS.json`, `UAV_TRACEABILITY.md`, backlog, dashboard and handoff,
- issue next preliminary datasheet revision with all newly frozen values visibly marked,
- rerun PB consistency / dashboard validation,
- re-evaluate `U1_SCHEMATIC_ALLOCATION_READINESS.json`.

Sprint completion requires:
- G1 matrix has no unresolved critical electrical-envelope row required by the G1 completion rule,
- G0/G1A/G1B/G1C parent conditions needed by G1 are closed,
- G2 architecture work is unblocked,
- `U1-SCH-R001` remains unallocated until both AR-001 and AR-002 are PASS.

## Current sprint metrics after S1.1

- Requirements structure: **12/12 = 100%**
- G1 SYSTEM FREEZE: **25/46 = 54.3%**
- Backlog DONE: **2/25 = 8%**
- Major gates closed: **0/8 = 0%**
- Component-bearing U1 schematic: **0%**

These controlling metrics change only when their source authorities change with evidence.

## Execution order

`S1.1 DONE -> S1.2 PWM/ripple/loss ACTIVE -> S1.3 18S energy/min bus -> S1.4 environment/protection -> S1.5 exact power-stage prefreeze -> S1.6 configuration closeout -> G1 -> G2`
