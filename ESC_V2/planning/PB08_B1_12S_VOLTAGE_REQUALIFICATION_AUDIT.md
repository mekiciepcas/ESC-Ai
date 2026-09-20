# PB-08 B1 12S voltage-domain requalification audit

Date: 2026-09-20  
Status: **DESK REQUALIFICATION AUDIT / NOT DESIGN APPROVAL**  
Authority: PB-08 common electrical platform. A2/B1 electrical sources remain immutable historical evidence.

## Purpose

Re-evaluate the legacy B1 VBUS-exposed blocks against the active PB-08 values rather than the superseded 18S heavy-lift envelope. This audit does not select components, allocate `U1-SCH-R001`, or claim physical qualification.

## Controlling PB-08 voltage contract

Frozen values:
- 12S common bus;
- 43.2 V nominal;
- 50.4 V full charge;
- 36.0 V minimum loaded bus for full rated ESC power;
- power-semiconductor class >=100 V;
- repetitive controlled switch-terminal stress target <=75 V;
- normal operation shall not rely on repetitive MOSFET avalanche.

Derived nameplate headroom checks:
- 100 V class vs 50.4 V full charge: **49.6 V** static nameplate headroom;
- 100 V class vs 75 V repetitive stress target: **25 V** nameplate headroom;
- 75 V stress target / 100 V class = **75% of nameplate rating**.

These are arithmetic checks, not derating approval. Exact component SOA, repetitive transient behavior, temperature, lifetime, ripple, DC-bias and layout remain separate obligations.

## B1 block disposition under PB-08

| B1 block / item | Repository evidence | PB-08 disposition | Required evidence before reuse |
|---|---|---|---|
| Q201–Q404 power MOSFETs | CSD19536KTT, 100 V, 2 parallel/switch | **REQUALIFICATION CANDIDATE; NOT SELECTED** | Recompute conduction/switching loss at PB-08 phase current/PWM; demonstrate <=75 V repetitive terminal stress; verify thermal/current sharing and SOA. |
| U501 gate driver | DRV8353FSRTAR, VDRAIN=VBUS | **REQUALIFICATION CANDIDATE; NOT SELECTED** | Verify operating/abs-max margin at 75 V switch-node stress, bootstrap/charge-pump behavior, dv/dt immunity, gate-drive capability for selected MOSFET count and reset/inhibit behavior. |
| C101–C103 bulk DC link | 3 x 470 uF 100 V, exact MPN OPEN | **VOLTAGE CLASS PLAUSIBLE; BOM STILL OPEN** | Exact series/MPN, ripple RMS, ESR/temperature/lifetime, capacitance tolerance and transient validation. |
| C104–C106 local ceramics | 2.2 uF 100 V X7R, exact MPN OPEN | **VOLTAGE CLASS PLAUSIBLE; EFFECTIVE C OPEN** | Exact MPN and DC-bias curve at ~50 V plus switching-ripple/transient verification. |
| LM5164DDAT auxiliary buck | VIN=VBUS, 100 V-class legacy candidate | **REQUALIFICATION CANDIDATE** | Verify PB-08 input/transient domain, startup/RON/current limit, dissipation and external network. Do not credit IC rating alone. |
| Aux HV input capacitors | 2.2 uF 160 V + 100 nF 160 V, MPN OPEN | **LABEL-RATING HEADROOM; NOT QUALIFIED** | Exact MPN, effective capacitance, ripple and temperature. |
| Bus/phase divider upper legs | 2 x 49.9 k, RT0805BRD0749K9L | **RECALCULATE / REQUALIFY** | Recalculate ADC full scale for PB-08 diagnostic range; audit resistor working voltage/pulse rating and divider fault behavior. |
| BAT54H ADC clamps | exact legacy MPN | **ARCHITECTURE REVIEW REQUIRED** | Preserve prior back-power/injection findings; do not reuse merely because bus voltage is lower. |
| External input protection | fused/precharged/reverse-polarity-protected assembly, implementation OPEN | **SYSTEM BLOCKER REMAINS** | Define fuse/precharge/reverse polarity/disconnect/clamp contract and harness inductance before G2. |
| External brake / regen interface | implementation OPEN | **SYSTEM BLOCKER REMAINS** | Define battery acceptance, disconnect event and regenerative/transient energy path. |

## What PB-08 actually improves

The move from the superseded 18S full-charge point (75.6 V) to PB-08 12S full charge (50.4 V) restores **25.2 V** of additional static headroom to a 100 V nameplate device. Therefore the old statement that B1's 100 V class is inherently tight at steady-state no longer applies to PB-08.

However, PB-08 deliberately sets a **75 V repetitive controlled switch-terminal stress target**. A 100 V device at that target still has only 25 V of nameplate headroom, and the target itself must be demonstrated by layout/DC-link/snubber/clamp design and switching tests. Therefore B1 changes from `likely voltage-limited by 18S steady state` to `credible 12S requalification candidate`, not to `qualified` or `approved`.

## Reuse sequence

1. Freeze exact propulsion operating point and derive phase RMS/peak current.
2. Freeze PWM/eRPM only after exact motor inductance/ripple evidence.
3. Re-run B1 MOSFET loss/current-sharing and gate-drive calculations for PB-08.
4. Select exact DC-link bulk/ceramic parts and model loop inductance.
5. Define external input/protection and regen/disconnect contract.
6. Demonstrate by simulation/bench evidence that repetitive switch-terminal stress is <=75 V across required operating cases.
7. Only after the above may B1-derived power-domain blocks be promoted into a component-bearing U1 revision.

## Decision

**B1 is a credible PB-08 12S requalification candidate, but no B1 VBUS-exposed component is automatically approved.** The 18S static-voltage concern is superseded for the active product; the critical path is now phase-current/PWM/loss closure plus proof of the <=75 V repetitive stress contract and exact DC-link/protection implementation.

No physical measurement, thermal qualification, EMI qualification, flight qualification or production readiness is claimed.