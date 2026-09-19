# Power-domain voltage-class trade — 18S candidate

Date: 2026-09-19
Status: REQUIREMENTS TRADE / NO PART FREEZE

## Known source-backed boundaries

- Candidate 18S LiPo full charge: 75.6 V (18 × 4.2 V).
- Hobbywing X15 G2: 18S compatible, rated 69 V, published input range 25–80 V.
- TI DRV8353: 9–100 V recommended operating range, 102 V absolute maximum supply rating (TI product/datasheet information).
- Legacy B1 MOSFET target: 100 V class; this is not frozen for the UAV product.

## Static headroom only

| Nominal device/domain class | Headroom above 75.6 V full charge | Ratio Vclass/Vfull | Interpretation |
|---:|---:|---:|---|
| 100 V | 24.4 V | 1.323 | narrow transient budget; not qualified |
| 120 V | 44.4 V | 1.587 | more transient room; device ecosystem/loss trade required |
| 150 V | 74.4 V | 1.984 | strong voltage room; likely Rds/Qg/cost penalty versus lower class |

These numbers are only arithmetic static headroom. They are not sufficient to select a semiconductor class.

## Required ceiling equation

The design voltage requirement must be treated as:

`V_required >= V_battery_max + V_switching_overshoot + V_harness_event + V_regen_or_disconnect + design_margin`

where correlated events must not be blindly added if they cannot physically coincide. Clamp action may replace part of the uncontrolled transient term only after clamp dynamic voltage and absorbed-energy capability are demonstrated.

## DRV8353 consequence

DRV8353 cannot be considered automatically safe merely because 75.6 V is below 100 V. Its supply domain shares the transient problem: TI lists 100 V operating and 102 V absolute maximum. Therefore a design that permits the DC bus to approach/exceed 100 V during switching, regen or disconnect has essentially no acceptable margin for this driver domain. If the final bus transient ceiling cannot be constrained well below the driver limit, either the driver supply must be protected/decoupled by a proven architecture or a higher-voltage gate-driver family must be selected.

## Selection gates

Before choosing 100/120/150 V power silicon:
1. Freeze battery max voltage and credible BMS/contact-disconnect behavior.
2. Establish harness + PCB commutation-loop inductance target and later measurement.
3. Establish DC-link effective capacitance at voltage/temperature.
4. Define regen policy and energy destination.
5. Define clamp/snubber architecture and dynamic clamp ceiling if used.
6. Measure representative-layout switching overshoot at staged voltage/current.
7. Compare candidate silicon at the resulting VDS requirement for conduction loss, switching loss, Qg/Qgd, reverse recovery, SOA, package thermal path, parallel sharing, availability and cost.

## Current decision

- 100 V MOSFETs: `NOT_QUALIFIED / HIGH_RISK_CANDIDATE` for 18S until transient closure.
- DRV8353: `REVALIDATE / VOLTAGE_MARGIN_CRITICAL` for 18S.
- 120 V and 150 V silicon: `TRADE_CANDIDATES`, not recommendations yet.
- No production part number is selected by this document.
