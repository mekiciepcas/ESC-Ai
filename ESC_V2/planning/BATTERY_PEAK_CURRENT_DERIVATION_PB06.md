# Battery peak-current derivation — PB-06

Date: 2026-09-19  
Branch: `uav-rebaseline`  
Status: **S1.3 CONTROLLED SYSTEM REQUIREMENT DERIVATION / PHYSICAL PACK VALIDATION OPEN**

## Purpose

Derive a whole-pack short-duration current requirement from already-frozen vehicle thrust requirements instead of multiplying the per-ESC 200 A capability by eight.

## Frozen parents

- X8 coaxial / eight independent propulsion channels.
- Maximum design MTOW: 180 kg.
- Normal static thrust-to-weight requirement: >=1.6.
- Coaxial sizing factor: 0.85.
- Isolated-equivalent thrust required per rotor at the 1.6 T/W point: 42.353 kgf.
- 18S battery architecture.
- Minimum loaded bus for full rated power: 54.0 V.
- Per-ESC short-duration electrical capability: >=11.5 kW and >=200 A for >=3 s.

## Propulsion source anchor

Current Hobbywing X13 G2 manufacturer data for 69 V + MFP 56x20 gives adjacent measured points around the required 42.353 kgf isolated-equivalent thrust:

- 40.351 kgf: 84.0 A, 5795.8 W input.
- 43.409 kgf: 94.4 A, 6511.1 W input.

Primary source:
`https://www.hobbywing.com/en/products/x13-g2`

The source curve is a benchmark anchor, not final U1 flight validation.

## Interpolation at the frozen 42.353 kgf sizing point

Linear interpolation between the two manufacturer points gives approximately:

- current at 69 V reference: **90.81 A per propulsion channel**;
- input power: **6.264 kW per propulsion channel**.

For eight propulsion channels operating simultaneously at the frozen normal 1.6 T/W static point:

- aggregate electrical input power = 8 x 6.264 kW = **50.11 kW**.

At the frozen 54.0 V minimum loaded bus for full rated-power operation:

- ideal pack current = 50.11 kW / 54.0 V = **928 A**.

Applying a 10% system design allowance for interpolation/model spread and current-path overhead gives about **1021 A**. The controlled product requirement is rounded upward to:

**>=1050 A whole-pack peak current for >=3 s.**

## Why this is not 8 x 200 A

Eight ESCs each being capable of 200 A for 3 s does not imply the battery must supply 1600 A simultaneously. The per-ESC limit is an inverter electrical capability envelope. The vehicle battery requirement is instead tied to the simultaneous propulsion operating point required by the frozen vehicle thrust target.

The 1050 A pack requirement therefore reflects the current vehicle-level 1.6 T/W design point plus margin. If later vehicle control or propulsion evidence requires a higher simultaneous transient, PB-06 must be revised under change control.

## Candidate-cell impact screen — not qualification

At 1050 A pack current:

- P45B 18S18P: 58.3 A/cell.
- P50B 18S16P: 65.6 A/cell.
- P60B 18S14P: 75.0 A/cell.

These arithmetic values do not prove a topology is acceptable. P50B's published continuous rating is 60 A/cell; P60B publishes a higher conditional maximum discharge rating. Pack-level current sharing, temperature, SOC, SOH, busbar/weld losses and BMS/contactors remain mandatory verification items.

## Requirement disposition

Freeze:

- `battery_pack_peak_current_a_min = 1050 A`
- `battery_pack_peak_current_duration_s_min = 3 s`

Keep OPEN:

- exact cell MPN and P-count;
- allowable SOC/temperature/SOH envelope for peak current;
- pack terminal sag at 1050 A;
- cell-group current-sharing acceptance;
- contactor/fuse/busbar/weld ratings;
- exact BMS peak-current logic;
- measured thermal rise and physical qualification.

## Evidence boundary

This is a controlled sizing derivation from frozen vehicle requirements and manufacturer propulsion data. It is not a physical battery-pack, dyno, thermal or flight result.
