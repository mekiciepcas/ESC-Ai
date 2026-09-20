# PB-08 P50B OCV / DC-resistance envelope evidence contract

Date: 2026-09-20  
Branch: `uav-rebaseline`  
Status: **EVIDENCE CONTRACT / NO PACK FREEZE / NO PHYSICAL VERIFICATION**

## Purpose

Define the minimum evidence needed to replace the present condition-specific P50B sag screen with a controlled SOC-temperature-SOH envelope suitable for PB-08 36.0 V loaded-floor analysis. This document does not assign missing cell data and does not select P50B as the production cell.

## Controlled parents

- PB-08 common bus: 12S, 43.2 V nominal convention, 50.4 V full charge, 36.0 V loaded floor for full rated ESC power.
- P50B 12S4P remains reference-only.
- Existing condition-specific screen uses the already-controlled typical 12.8 mOhm/cell DC-impedance datum at 50% SOC, yielding 38.4 mOhm ideal cell-only 12S4P resistance.
- 83.33 A remains propulsion-only continuous pack-current lower bound, not final simultaneous pack current.

## Required evidence grid

No numeric envelope row may be populated unless its source or measurement identifies the applicable condition. Required independent variables are:

| Variable | Required treatment | Current state |
|---|---|---|
| SOC | Multiple points spanning the intended usable window, including the intended low-SOC full-power boundary | OPEN |
| Cell temperature | Minimum/nominal/maximum operating conditions relevant to full-power use | OPEN |
| SOH / ageing state | New-cell reference plus an explicit end-of-life or degraded resistance/capacity criterion | OPEN |
| OCV | Rested/open-circuit voltage at the same SOC/temperature/SOH condition used for the sag calculation | OPEN |
| DC resistance | Pulse-derived or manufacturer-defined DC resistance with pulse duration/current/method stated | OPEN except existing condition-specific typical datum |
| Capacity / usable-energy relation | Applicable capacity at the same temperature/SOH boundary where required | OPEN |

A resistance value measured or published under one condition shall not be silently combined with OCV from another condition to claim compliance.

## Accepted evidence classes

1. Exact manufacturer primary-source table/curve with test conditions stated.
2. Controlled cell test with calibrated voltage/current/temperature acquisition and recorded cell identity, SOC preparation, rest period, pulse magnitude/duration and calculation method.
3. A conservative derived bound only when every parent value is controlled and the derivation is explicit.

Distributor summaries, generic 21700 assumptions, marketing current ratings, unrelated-cell curves, and unsourced forum data are not closure evidence.

## Measurement contract when primary data are insufficient

For each tested condition record at minimum:

- cell lot / serial or traceable sample identifier,
- cycle count or SOH definition,
- stabilized cell temperature,
- SOC preparation method and capacity reference,
- rest time before OCV sample,
- pre-pulse OCV,
- pulse current and direction,
- pulse duration and the exact voltage sample time used,
- voltage immediately before and at the defined pulse sample,
- derived `Rdc = (V_pre - V_pulse) / I_pulse`,
- post-pulse recovery observation,
- instrumentation IDs and calibration status,
- raw-data file reference.

Repeatability shall be demonstrated before promoting a measured point into the controlled envelope. Exact repeat count/tolerance remains OPEN until the verification plan is frozen.

## Pack-level transformation

For an ideal `Ns x Np` reference topology, a cell-level condition may be transformed only as:

`V_OCV,pack = Ns * V_OCV,cell`

`R_cell,pack = Ns / Np * Rdc,cell`

For the reference-only 12S4P topology:

`R_cell,pack = 3 * Rdc,cell`

The installed loaded-voltage closure remains:

`V_loaded = V_OCV,pack - I_pack * (R_cell,pack + R_noncell,installed)`

Acceptance for the full-rated-power floor requires:

`V_loaded >= 36.0 V`

at one jointly applicable evidenced condition, with simultaneous `I_pack`, installed non-cell resistance and thermal state. Cell-current sharing must also be justified; ideal 4P sharing alone is not physical proof.

## Promotion rule

The PB-08 pack sag/loaded-floor requirement may move from OPEN only when:

1. intended usable SOC window and cutoff/derating policy are controlled;
2. OCV and Rdc envelopes are controlled across the relevant SOC-temperature-SOH boundary;
3. exact pack topology is selected;
4. simultaneous pack current is controlled;
5. installed non-cell resistance is controlled at applicable temperature;
6. parallel current-sharing and thermal limits are addressed; and
7. the worst jointly applicable condition satisfies the loaded-floor criterion or produces a documented derating/mission-termination boundary.

Until then, the existing 39.20 V conditional OCV threshold and all resistance-allowance sensitivities remain arithmetic screens only.

## Result

This contract closes an evidence-definition gap, not a product-value gap. No G1 row, backlog task, physical-verification claim, cell selection or U1 allocation is advanced by this document.