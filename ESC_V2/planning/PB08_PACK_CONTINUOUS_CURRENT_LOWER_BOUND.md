# PB-08 pack continuous-current lower bound

Date: 2026-09-20  
Authority: `PRODUCT_BASELINE_PB-08.json`, `mission_requirements.json`  
Status: **DERIVED LOWER BOUND — NOT PACK QUALIFICATION**

## Purpose

Convert already-frozen PB-08 system values into a minimum whole-pack continuous-current sizing bound without inventing pack losses, auxiliary load, peak policy, cell sag, or current-sharing performance.

## Frozen parent values

- Upper aggregate continuous propulsion electrical-input design point: **3000 W**.
- Minimum loaded DC bus for full rated ESC power: **36.0 V**.
- Common battery architecture: **12S**.
- Exact pack implementation remains OPEN.

## Deterministic lower-bound derivation

At the lowest bus voltage at which PB-08 still requires full rated propulsion power:

`I_pack,propulsion,min = P_propulsion / V_bus = 3000 / 36.0 = 83.333 A`

Therefore a pack intended to support the PB-08 3 kW upper continuous variant must have a demonstrated continuous terminal-current capability **strictly greater than or equal to 83.33 A for propulsion alone**.

This is a mathematical lower bound, not a final pack-current requirement. The final required continuous pack current must additionally cover any loads not already included in the 3000 W propulsion-input definition, including vehicle auxiliaries supplied from the traction pack, and must include the selected engineering margin/derating policy. Those terms remain OPEN and shall not be guessed.

## Voltage sensitivity

For the same 3000 W propulsion-input requirement:

| Bus voltage | Propulsion-only DC current |
|---:|---:|
| 50.4 V | 59.52 A |
| 43.2 V | 69.44 A |
| 36.0 V | 83.33 A |

The 36.0 V row controls the minimum continuous-current sizing bound because PB-08 explicitly requires full rated ESC power down to that loaded voltage.

## Relationship to the P50B 12S4P reference topology

The repository's P50B 12S4P topology remains reference-only. Prior primary-source evidence records a 60 A continuous-discharge cell rating. Four ideal parallel cells would give `4 x 60 = 240 A` by arithmetic, but **240 A is not a qualified pack rating**. Real pack capability depends on temperature, SOC, SOH, cell matching/current sharing, interconnect resistance, welds, BMS/protection, terminals, harness, cooling and manufacturer application limits.

Accordingly:

- **83.33 A** = controlled propulsion-only system lower bound derived from frozen PB-08 requirements.
- **240 A** = cell-rating arithmetic for a reference topology only.
- exact continuous pack-current requirement = **OPEN** pending auxiliary-load and margin closure.
- demonstrated pack capability = **OPEN** pending physical/supplier-qualified pack evidence.
- vehicle aggregate peak current and duration = **OPEN** pending rotor/degraded-mode policy.

## Verification contract impact

Any eventual pack candidate for the 3 kW variant must demonstrate, at minimum, continuous delivery at the final requirement (which cannot be below 83.33 A propulsion-only) while respecting the PB-08 36.0 V full-power loaded floor over the controlled SOC/temperature/SOH envelope. A room-temperature short pulse or multiplication of cell datasheet current is insufficient evidence.

## Decision

This artifact closes only the **continuous-current mathematical lower bound**. It does not freeze cell MPN, P-count, BMS, fuse, disconnect, precharge, pack mass, pack peak current, sag, thermal capability, or vehicle architecture. No G1 row is promoted to PASS solely from this derivation.
