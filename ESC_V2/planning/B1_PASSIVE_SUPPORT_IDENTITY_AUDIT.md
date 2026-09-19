# B1 passive support-part identity audit

Date: 2026-09-19
Branch: `uav-rebaseline`
Status: `LEGACY_IDENTITY_AUDIT_ONLY`

## Purpose

This is requirement-independent prework for UAV-007. It records which B1 passive support parts already have exact MPN/package identities in the repository and separates that fact from U1 qualification. It does not select any part for U1 and does not close G1/G2/G3.

Repository authority inspected: `ESC_V2/hardware_b1/bom_review.json`.

## Exact identities already present in B1

| Function | B1 MPN | B1 footprint | Disposition |
|---|---|---|---|
| 100 kOhm bleed | `RC1206FR-07100KL` | `Resistor_SMD:R_1206_3216Metric` | LEGACY_REFERENCE / REVALIDATE |
| 4.7 Ohm gate resistor | `RC0805FR-074R7L` | `Resistor_SMD:R_0805_2012Metric` | LEGACY_REFERENCE / RECALCULATE |
| 47 kOhm gate-source / pull-down | `RC0805FR-0747KL` | `Resistor_SMD:R_0805_2012Metric` | LEGACY_REFERENCE / REVALIDATE |
| 4.7 kOhm pull-up | `RC0805FR-074K7L` | `Resistor_SMD:R_0805_2012Metric` | LEGACY_REFERENCE / REVALIDATE |
| 10 kOhm pull-up/down | `RC0805FR-0710KL` | `Resistor_SMD:R_0805_2012Metric` | LEGACY_REFERENCE / REVALIDATE |
| 49.9 kOhm 0.1% sense-divider resistor | `RT0805BRD0749K9L` | `Resistor_SMD:R_0805_2012Metric` | LEGACY_REFERENCE / RECALCULATE |
| 3.32 kOhm 0.1% sense-divider resistor | `RT0805BRD073K32L` | `Resistor_SMD:R_0805_2012Metric` | LEGACY_REFERENCE / RECALCULATE |
| 1 kOhm ADC series resistor | `RC0805FR-071KL` | `Resistor_SMD:R_0805_2012Metric` | LEGACY_REFERENCE / RECALCULATE |
| 100 Ohm ADC series resistor | `RC0805FR-07100RL` | `Resistor_SMD:R_0805_2012Metric` | LEGACY_REFERENCE / RECALCULATE |
| 1 nF C0G ADC filter capacitor | `C0805C102J5GACTU` | `Capacitor_SMD:C_0805_2012Metric` | LEGACY_REFERENCE / RECALCULATE |
| 100 nF 100 V X7R local capacitor | `C2012X7R2A104K125AA` | `Capacitor_SMD:C_0805_2012Metric` | LEGACY_REFERENCE / REVALIDATE |
| BAT54H clamp diode | `BAT54H,115` | `Diode_SMD:D_SOD-123F` | LEGACY_REFERENCE / REPLACE_IF_REQUIRED |

## Engineering classification

1. Exact MPN text existing in B1 is evidence of **legacy identity only**. It is not evidence of current lifecycle, procurement availability, exact manufacturer land-pattern compliance, UAV derating, or production qualification.
2. Gate resistance is operating-point dependent. `4.7 Ohm` remains only a B1 starting value until selected switch Qg, driver source/sink impedance, loop inductance, PWM/dead-time and measured VGS/VDS behavior are known.
3. Voltage-divider and ADC-filter values are tied to the sensing architecture. The B1 divider/clamp network is not copied automatically because the existing traceability audit identifies a partial-power/backfeed risk through the BAT54H rail clamps.
4. The 100 kOhm bleed resistor cannot be qualified until final DC-link capacitance, maximum bus voltage, required discharge time and resistor working-voltage/pulse/thermal limits are known.
5. Package-family matches in the B1 BOM are not proof that the generic KiCad footprints meet manufacturer recommended land patterns or U1 assembly rules.

## Explicit unresolved evidence

The following must remain OPEN before any of these parts can become U1 production selections:

- current manufacturer lifecycle/orderability evidence for each exact MPN;
- manufacturer package drawing versus exact KiCad pad geometry;
- voltage/current/power/temperature derating from frozen G1/G2 requirements;
- tolerance/TCR/noise requirements where functionally relevant;
- DC-bias behavior for MLCCs where relevant;
- failure-mode and partial-power behavior for clamp networks;
- alternates and procurement risk;
- assembly/DFM review.

## Result

This audit reduces ambiguity in the B1-to-U1 migration: the listed components have traceable legacy identities, but none is promoted to U1. Values whose function depends on the final electrical envelope remain `RECALCULATE`; the BAT54H rail-clamp implementation remains `REPLACE_IF_REQUIRED` because the canonical traceability record already documents the back-power concern.
