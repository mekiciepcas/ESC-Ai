# G0 controlled trade-only bounding cases

Date: 2026-09-19
Status: ANALYSIS ONLY / NOT PRODUCT REQUIREMENTS
Branch: `uav-rebaseline`
Purpose: permit useful rotor/propulsion screening while vehicle-specific G0 inputs remain OPEN, without silently converting competitor data into our product baseline.

## Governance

These cases are `ASSUMPTION_FOR_TRADE_ONLY`. They may be used for sensitivity calculations, architecture elimination and test-planning only. They MUST NOT populate `mission_requirements.json`, close G0/G1, freeze a rotor count, battery architecture, ESC rating, semiconductor class, or release hardware.

Promotion rule: a trade-only value can become a product requirement only after it is independently supplied/approved as our vehicle target and entered into the normal G0/G1 evidence chain.

## Primary-source anchors

- XAG P150 official specs: 54 kg aircraft weight with RevoSpray 4 and batteries; 70 kg maximum payload; 125 kg maximum spraying takeoff weight; four-motor platform; 55 kgf maximum single-motor thrust; 4.7 kW rated power per motor; XESC-F360 120 A continuous / 360 A 30 s.
- XAG P150 Max official specs: 56 kg empty weight with RevoSpray and batteries; 80 kg maximum payload; 136 kg maximum spraying takeoff weight; 4 motors; 56 kgf maximum single-motor thrust; 4.85 kW rated power per motor; 140 A continuous / 380 A 30 s ESC.
- DJI Agras T100 official specs: 75 kg spraying weight; 100 kg spraying payload; 175 kg maximum spraying takeoff weight; 60 rpm/V motors; 62 inch propellers; published propulsion layout uses 8 propeller pairs. DJI's published page also states that in Turkey the maximum takeoff weight should be kept at 149.9 kg; this is a regulatory/use constraint on that product, not automatically our design requirement.

Source URLs:
- https://www.xa.com/en/p150/p150specs
- https://xa.com/en/p150max/p150maxspecs
- https://ag.dji.com/t100/specs

## Controlled bounding cases

| Case | Analysis MTOW | Why retained | Baseline authority |
|---|---:|---|---|
| T125 | 125 kg | lower current heavy-agriculture benchmark; XAG P150 class | TRADE ONLY |
| T150 | 150 kg | interpolation/sensitivity point and close to four X15-class axes at 37.5 kg recommended load/axis | TRADE ONLY |
| T175 | 175 kg | upper current 100 kg-payload spraying benchmark; DJI T100 class | TRADE ONLY |

No nominal payload, airframe mass, battery mass, endurance, reserve, altitude, temperature or failure-survival target is inferred for our product from these cases.

## Rotor-load screening

For mass M and N lifting axes, static hover load per axis is M/N kgf. The 1.6 and 1.8 multipliers below are sensitivity cases already used by `rotor_trade_study.md`; they are not requirements.

| Case | Axes | Hover kgf/axis | 1.6x kgf/axis | 1.8x kgf/axis |
|---|---:|---:|---:|---:|
| T125 | 4 | 31.25 | 50.00 | 56.25 |
| T125 | 6 | 20.83 | 33.33 | 37.50 |
| T125 | 8 | 15.63 | 25.00 | 28.13 |
| T150 | 4 | 37.50 | 60.00 | 67.50 |
| T150 | 6 | 25.00 | 40.00 | 45.00 |
| T150 | 8 | 18.75 | 30.00 | 33.75 |
| T175 | 4 | 43.75 | 70.00 | 78.75 |
| T175 | 6 | 29.17 | 46.67 | 52.50 |
| T175 | 8 | 21.88 | 35.00 | 39.38 |

## Architecture elimination logic that is valid before G0 freeze

- Ordinary quad cannot satisfy a requirement to continue controlled hover after complete loss of one motor/ESC using only the remaining three fixed-pitch lifting axes; therefore if `single_motor_failure_requirement` is later set to continued-hover, ordinary quad is excluded by architecture before detailed ESC sizing.
- If single-motor-out continued hover is explicitly waived, quad remains a valid candidate and has direct commercial precedent in the T125/T136 region.
- T175 quad requires 43.75 kgf per axis merely to hover and 70-78.75 kgf/axis in the two sensitivity-margin cases. It is therefore the highest per-axis electrical-stress branch and should not be treated as the default architecture.
- Hex and octo reduce per-axis thrust but increase motor/ESC/harness count. Whether the redundancy benefit is required is a vehicle-level G0 decision.

## What this closes and what it does not

Closed for analysis:
- a controlled MTOW sensitivity envelope of 125/150/175 kg is now available for rotor and propulsion trade calculations;
- trade-only versus product-baseline semantics are explicit;
- the single-motor-failure policy is identified as an architecture discriminator rather than an afterthought.

Still OPEN for G0:
- nominal payload;
- our airframe, battery and mission-equipment masses;
- our MTOW min/nom/max;
- endurance/hover/reserve mission profile;
- environmental envelope;
- span/coaxial constraints;
- degraded/single-motor-failure policy.

Therefore G0 remains OPEN and no G1 requirement row changes to PASS from this document alone.
