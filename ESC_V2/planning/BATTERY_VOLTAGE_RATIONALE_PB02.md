# PB-02 battery voltage rationale

Date: 2026-09-19
Branch: `uav-rebaseline`
Status: CONTROLLED_RATIONALE — does not change PB-02 frozen values

## Short answer

The PB-02 value `66.6 V nominal` is **not an industry standard voltage**. It is the arithmetic nominal voltage of the frozen 18S lithium architecture when the selected cell-class convention is 3.7 V nominal per cell:

- nominal: `18 × 3.7 V = 66.6 V`
- full charge: `18 × 4.2 V = 75.6 V`
- inherited U1 full-charge operating ceiling: `<= 80 V`

The series count (18S) is the architectural decision. The exact nominal number depends on the final cell/pouch chemistry and manufacturer convention. A 3.6 V-nominal 18S cell family would be described as 64.8 V nominal while still being 18S and, if charged to 4.2 V/cell, still reaching 75.6 V at full charge.

## Why 18S is used in PB-02

PB-02 chose 18S because it coherently matches the frozen heavy-lift propulsion performance class and voltage-domain decisions:

1. The 56x20 / 45 KV propulsion class is anchored to current heavy-lift systems that explicitly support 18S lithium operation.
2. Hobbywing X13 G2 publishes `18S LiPo`, a `69 V` rated system voltage, and a `25–80 V` input range. Its manufacturer load curve is published at 69 V. PB-02 uses this as a source-backed operating reference, not as proof that the custom vehicle will behave identically.
3. The inherited PB-01 outer full-charge ceiling is `<=80 V`; 18S with 4.2 V/cell reaches 75.6 V and therefore fits inside that frozen envelope.
4. For a given mechanical power, moving from lower-series-count packs toward 18S reduces DC current relative to a lower-voltage architecture, which helps cable, connector, copper and semiconductor conduction-loss budgets. This is a system-level trade; higher voltage also increases switching/transient and insulation/protection demands.

## It is not a universal agricultural-drone standard

Commercial agricultural UAVs use different battery voltages. Examples include systems around the 48–52 V nominal region as well as 18S-class propulsion systems. Therefore the project must not describe 66.6 V or 18S as a universal drone standard.

## Required terminology in project documents

Use the following wording:

- `18S` = frozen battery series architecture.
- `66.6 V nominal` = PB-02 nominal-pack convention for 3.7 V/cell; this is a descriptive nominal value, not a hard bus operating point.
- `75.6 V full charge` = frozen target for 4.2 V/cell class.
- `<=80 V full-charge operating ceiling` = frozen ESC/U1 input-domain limit.
- `69 V manufacturer reference curve` = external propulsion test/reference voltage; do not relabel it as our nominal bus voltage.

## Engineering consequence

The next battery closure must define exact cell/pouch MPN, minimum loaded bus voltage, sag, Ah/Wh, reserve and BMS/disconnect behavior. If the final selected cell family uses a nominal-voltage convention other than 3.7 V/cell, the descriptive nominal voltage may require a controlled PB revision, while the frozen 18S series architecture and 75.6 V 4.2 V/cell full-charge target remain the governing architecture unless separately changed.
