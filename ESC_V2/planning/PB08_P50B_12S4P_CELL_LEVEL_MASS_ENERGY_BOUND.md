# PB-08 P50B 12S4P cell-level mass / energy bound

Date: 2026-09-20  
Status: **TRADE EVIDENCE — NOT PACK FREEZE / NOT PHYSICAL VERIFICATION**

## Purpose

Reduce the open PB-08 battery-mass uncertainty without inventing pack hardware. This note evaluates only the repository's existing reference topology `Molicel P50B 12S4P` against current manufacturer cell data. It does **not** select the production cell, P-count, BMS, fuse, disconnect, enclosure, interconnect, cooling, harness, or pack architecture.

## Primary-source cell data

Current Molicel INR-21700-P50B Product Data Sheet v1.1 lists:

- nominal voltage: 3.6 V,
- charge voltage: 4.2 V,
- typical capacity: 5.0 Ah / 18.0 Wh,
- minimum capacity: 4.85 Ah / 17.5 Wh,
- continuous discharge current: 60 A with 80 degC cut-off condition,
- typical DC impedance at 50% SOC: 12.8 mOhm,
- maximum cell weight: 71 g,
- maximum dimensions: 21.55 mm diameter x 70.15 mm height.

Primary source: Molicel, `INR-21700-P50B Product Data Sheet`, Version 1.1, accessed 2026-09-20: https://www.molicel.com/wp-content/uploads/4.TR%E7%B0%A1%E6%98%93%E8%A6%8F%E6%A0%BC_INR21700P50B_1.1_Product-Data-Sheet-of-INR-21700-P50B-80122.pdf

## Deterministic 12S4P cell-only roll-up

Cell count:

`12 series * 4 parallel = 48 cells`

Voltage:

- nominal = `12 * 3.6 = 43.2 V`, matching PB-08 nominal convention,
- full charge = `12 * 4.2 = 50.4 V`, matching PB-08 full-charge bus.

Capacity and energy:

- typical pack capacity at cell level = `4 * 5.0 = 20.0 Ah`,
- minimum pack capacity from datasheet minimum cell capacity = `4 * 4.85 = 19.4 Ah`,
- typical cell-level energy = `48 * 18.0 = 864 Wh`,
- minimum cell-level energy = `48 * 17.5 = 840 Wh`.

Therefore the existing PB-08 >=750 Wh gross-rated-energy target has **90 Wh typical** and **90 Wh minimum-datasheet-cell-energy** margin? Correction: minimum cell-level margin is `840 - 750 = 90 Wh`; typical margin is `864 - 750 = 114 Wh`.

Cell-only mass upper bound using manufacturer maximum cell weight:

`48 * 71 g = 3408 g = 3.408 kg`

This is a **cell-only maximum-weight roll-up**, not a complete-pack mass. Complete pack mass must add, at minimum, cell interconnects/welds, insulation/holders, BMS and sensing harness, fuse, contactor/disconnect/precharge if allocated to the pack, terminals/connectors, power conductors, enclosure, sealing, cooling/thermal materials, mounting hardware and manufacturing tolerances.

## Current capability boundary

Four cells in parallel have a simple datasheet-current arithmetic ceiling of:

`4 * 60 A = 240 A`

This is **not** a frozen pack continuous-current rating. The cell's published 60 A value is temperature-conditioned, and real pack capability additionally depends on cell temperature distribution, SOC, SOH, parallel current sharing, interconnect/contact resistance, BMS/fuse/disconnect limits, enclosure/cooling and voltage-sag acceptance. No PB-08 pack current requirement is closed by this arithmetic.

At the datasheet typical 50%-SOC DC impedance, an ideal equal-sharing 4P group would have a cell-only equivalent resistance of `12.8 / 4 = 3.2 mOhm`; 12 such series groups would give `38.4 mOhm` as a **typical cell-only arithmetic reference at the stated datasheet condition**. This value shall not be used as a guaranteed pack resistance or as proof of the 36.0 V loaded-floor requirement.

## Mass-budget consequence

PB-08 previously had `battery_mass_kg = null`. This study establishes only a rigorous lower-completeness boundary:

- 12S4P P50B cell inventory: 48 cells,
- cell-only maximum-weight roll-up: **3.408 kg**,
- complete installed pack mass: **OPEN and necessarily greater than the cell-only inventory once pack hardware is included**.

The result is useful for the Quad/Hexa vehicle mass ledger because any vehicle concept using this reference topology must reserve at least the cell inventory mass plus all pack hardware. It is not sufficient to close MTOW or rotor architecture.

## Disposition

- Keep P50B 12S4P as **REFERENCE_ONLY**, consistent with PB-08.
- Do not populate `mission_requirements.json:battery_mass_kg` from the 3.408 kg cell-only value.
- Do not freeze pack current from 4 x 60 A arithmetic.
- Next safe battery task: source or allocate real interconnect/BMS/protection/enclosure/cooling hardware and build a complete installed-pack mass ledger; then evaluate sag over SOC/temperature/SOH with controlled evidence.
