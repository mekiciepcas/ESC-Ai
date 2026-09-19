# Sprint S1 — PB-02 -> G1 SYSTEM FREEZE

Date: 2026-09-19  
Branch: `uav-rebaseline`  
Status: **ACTIVE**  
Parent phase: **PHASE A — System and propulsion definition**  
Gate target: **G1 — SYSTEM ELECTRICAL FREEZE**  
Baseline authority: `PRODUCT_BASELINE_PB-02.json`

## Why this sprint exists

The project has moved beyond architecture-only screening: PB-02 already freezes the X8 vehicle direction, MTOW targets, 56x20 / 45KV / 18S propulsion class, DC-side ESC capability, >=150 V semiconductor class and >=60 keRPM controller capability. However G1 is only 22/46 PASS because phase-current, PWM, battery-energy/minimum-bus, environment, protection and thermal-domain values are still open.

This sprint converts the remaining system-level electrical unknowns into a closed, traceable G1 envelope before exact component-bearing U1 schematic work begins. It is an execution sprint, **not a new approval gate**.

## Sprint rule

- Do not reopen PB-02 frozen decisions without PB-03/ECO.
- Do not copy DC current into phase-current requirements.
- Do not freeze values from competitor headline ratings alone.
- Use primary-source motor/device data, explicit calculations and bounded product decisions.
- Keep `U1-SCH-R001` unallocated until the allocation guard is READY.
- No Gerber, manufacturing release or `main` merge is authorized by this sprint.

## S1.1 — Phase-current model closure

Goal: close `G1-03`, `G1-04` and provide the parent value for `G1-08`/`G1-15`.

Required work:
- obtain or source-back the 56x20 / 45KV / 18S reference motor electrical parameters needed for a phase-current model,
- correlate torque / mechanical output power / electrical input power from published operating points,
- derive continuous phase RMS current at rated continuous operating points,
- derive short-duration phase peak requirement and duration,
- state model uncertainty and required bench-correlation method.

Outputs:
- `PHASE_CURRENT_MODEL_PB02.md`
- machine-readable calculation/evidence record
- updated G1 matrix only when values are defensible.

Exit condition: phase RMS and peak-current requirements are numeric, bounded and traceable; DC current is not reused as phase current.

## S1.2 — PWM / ripple / switching-loss closure

Goal: close `G1-07` and create the quantitative parent for G2 power-stage optimization.

Required work:
- motor inductance / electrical time-constant evidence or conservative measured-plan bounds,
- >=60 keRPM control timing constraint,
- 150 V MOSFET candidate switching-energy data,
- current-ripple sweep across candidate PWM frequencies,
- switching + conduction loss comparison at nominal and hot conditions,
- dead-time and current-sampling-window constraints.

Outputs:
- `PWM_RIPPLE_LOSS_STUDY_PB02.md`
- selected PWM frequency or bounded operating range.

Exit condition: PWM is frozen from control + ripple + loss evidence, not inherited from B1/Faz2/Faz3.

## S1.3 — 18S energy / minimum-loaded-bus closure

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
- `BATTERY_ENERGY_BASELINE_PB03_CANDIDATE.md`
- battery architecture update / PB-03 only if frozen values change or new product values are added.

Exit condition: `G1C-02` and the energy/mass parents needed by G0/G1 are numeric and traceable.

## S1.4 — Environment, derating and protection envelope

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

## S1.5 — G2 pre-freeze: exact power-stage short list

Goal: avoid a dead stop immediately after G1 while not pretending G2 is already closed.

Required work:
- exact 150 V MOSFET candidates and hot `RDS(on)` / `Qg` / switching-energy / SOA comparison,
- required MOSFET parallel count per switch,
- gate-driver current requirement and exact high-voltage half-bridge driver shortlist,
- preliminary current-sense range / shunt / CSA shortlist,
- DC-link capacitance / ripple-current / precharge / regen screening,
- thermal-loss budget.

Outputs:
- `POWER_STAGE_TRADE_PB02_G2_PREWORK.md`
- exact evidence-backed shortlist, no production-selection claim before G2.

Exit condition: G2 can start from a quantified shortlist immediately after G1 closure.

## S1.6 — Configuration-control closeout

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

## Current sprint metrics at activation

- Requirements structure: **12/12 = 100%**
- G1 SYSTEM FREEZE: **22/46 = 47.8%**
- Backlog DONE: **2/25 = 8%**
- Major gates closed: **0/8 = 0%**
- Component-bearing U1 schematic: **0%**

These controlling metrics change only when their source authorities change with evidence.

## Execution order

`S1.1 phase current -> S1.2 PWM/ripple/loss -> S1.3 18S energy/min bus -> S1.4 environment/protection -> S1.5 exact power-stage prefreeze -> S1.6 configuration closeout -> G1 -> G2`
