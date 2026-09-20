# PB-08 P50B 12S4P geometric packaging bound

Date: 2026-09-20
Status: TRADE / PACKAGING PREWORK ONLY
Authority: PB-08 common 12S platform; P50B 12S4P remains REFERENCE_ONLY.

## Purpose

Extend the existing P50B 12S4P cell-level mass/energy bound with a source-backed geometric lower-bound input for mechanical packaging. This is not a complete pack CAD layout, enclosure allocation, thermal design, crash/impact design, or production cell selection.

## Primary-source cell geometry

Molicel's current INR-21700-P50B product page and product data sheet give:

- cylindrical 21700 format,
- maximum diameter: **21.55 mm**,
- maximum height: **70.15 mm**,
- maximum mass: **71 g**,
- nominal voltage: 3.6 V,
- typical capacity: 5.0 Ah.

Primary sources accessed 2026-09-20:
- https://www.molicel.com/product/inr-21700-p50b/
- https://www.molicel.com/wp-content/uploads/Product-Data-Sheet-of-INR-21700-P50B-80122.pdf

## Deterministic geometry arithmetic

Existing reference topology: 12S4P = **48 cells**.

Using the manufacturer's maximum cylindrical dimensions only:

`V_cell,cylinder = pi * (21.55 mm / 2)^2 * 70.15 mm = 25.5866 cm^3`

`V_48,cylinders = 48 * 25.5866 = 1228.16 cm^3 = 1.228 L`

This **1.228 L is cell-cylinder geometric volume only**. It is not an achievable complete-pack external volume because real packaging also requires cell-to-cell spacing/tolerance, holders/insulation, interconnects, sense wiring, BMS, fuse/disconnect/precharge hardware, enclosure, thermal paths, harness/connectors and mounting features.

For a simple orthogonal 12-by-4 cell pitch thought experiment at zero clearance:

- 12-cell pitch = `12 * 21.55 = 258.6 mm`,
- 4-cell pitch = `4 * 21.55 = 86.2 mm`,
- cell height = `70.15 mm`.

Therefore **258.6 x 86.2 x 70.15 mm** is only a zero-clearance bounding brick for one orientation, not a pack envelope or recommended layout. Electrical series/parallel interconnect topology, cooling and service isolation may require a different arrangement.

## Relation to existing mass/energy evidence

The previous controlled bound remains:

- 48 cells,
- 840 Wh minimum / 864 Wh typical cell-level energy,
- 3.408 kg maximum-weight cell inventory.

This run adds only the maximum-dimension geometric input. It does not populate `battery_mass_kg` or any vehicle envelope field.

## Engineering consequence

The complete 12S pack mass/volume closure now has hard cell-only anchors of **3.408 kg maximum-weight inventory** and **1.228 L maximum-dimension cylindrical material envelope arithmetic**. Any complete-pack proposal below either underlying cell inventory mass or without explicit allowance for non-cell hardware is invalid. The 1.228 L value shall not be treated as a realizable rectangular pack volume because cylinder packing voids and required clearances/hardware are excluded.

## Still OPEN

- exact production cell and P-count,
- cell orientation and mechanical retention,
- cell spacing and tolerance stack,
- holder/insulation/fire-barrier strategy,
- interconnect/weld geometry and mass,
- BMS identity and mass,
- fuse/disconnect/precharge identity and mass,
- enclosure/cooling mass and external dimensions,
- harness/connectors/mounting mass,
- pack sag/current qualification over SOC/temperature/SOH,
- vibration/shock/ingress/environmental qualification.

No physical verification or flight/production qualification is claimed.
