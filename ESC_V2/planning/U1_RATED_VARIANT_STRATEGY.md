# U1 rated-product and future-variant strategy

Date: 2026-09-19  
Branch: `uav-rebaseline`  
Status: **CONTROLLED PRODUCT STRATEGY — PB-02 VALUES UNCHANGED**

## Decision

The first U1 hardware/release path shall be designed around the current **upper-performance PB-02 baseline**, not compromised to guarantee broad low-voltage compatibility in the first revision.

Rated baseline remains:

- battery architecture: **18S high-rate lithium**,
- nominal-pack convention: **66.6 V** at 3.7 V/cell,
- full-charge target: **75.6 V** at 4.2 V/cell,
- outer full-charge operating ceiling: **<=80 V**,
- repetitive controlled semiconductor-terminal stress ceiling: **<=120 V**,
- power semiconductor class: **>=150 V**,
- ESC DC capability: **>=70 A continuous**, **>=200 A for >=3 s**, **>=4.8 kW continuous input**, **>=11.5 kW short-duration input**.

This strategy does **not** modify the PB-02 frozen values. It clarifies which operating point the first production-intent hardware shall optimize for.

## Initial-release rule

For U1 initial development/release:

1. Optimize switching, conduction, current sensing, DC-link, auxiliary power, connectors, thermal path and firmware limits for the frozen 18S rated baseline.
2. Do not increase cost, size, switching loss or design complexity solely to guarantee operation on lower-series-count packs unless that support is proven to have negligible impact on the rated design.
3. The still-open `dc_bus_min_v` requirement shall be closed from the **18S loaded/sag/cutoff envelope**, not from a future 12S/14S compatibility goal.
4. No lower-S pack shall be advertised as supported merely because the hardware happens to power up at that voltage.

## Future lower-voltage variants

A later lower-voltage/lower-power product is explicitly allowed, for example 12S/14S/16S, but it shall be treated as a **controlled derivative** rather than an assumption of the first U1 release.

A derivative may reuse the U1 control architecture while revising as needed:

- MOSFET voltage class and parallel count,
- gate-drive optimization,
- auxiliary-power UVLO/startup range,
- voltage-sense scaling,
- current limits and derating maps,
- DC-link/precharge,
- connectors/harness,
- motor/propeller operating point,
- firmware voltage/power limits,
- thermal qualification.

If a derivative changes a frozen product decision, it requires a new PB revision / engineering-change record and its own schematic/BOM/PCB/verification lineage.

## Power-scaling principle

Lower bus voltage is acceptable when the product power target is also reduced. For a fixed DC-current capability, available electrical power scales approximately with bus voltage (`P ~= V x I`). Attempting to preserve the same high power at substantially lower voltage increases current and therefore increases conductor, connector, semiconductor and thermal stress.

Therefore the preferred family strategy is:

- **U1 Rated:** 18S, full heavy-lift performance baseline.
- **Future derated derivative:** lower series count with explicitly lower power/thrust/current operating envelope.
- **Future optimized LV derivative:** only if market need justifies a dedicated lower-voltage power stage.

## Verification boundary

This strategy is a product-development decision, not evidence that any lower-voltage pack has been tested or is compatible with the eventual U1 hardware. Compatibility claims require the exact revision to pass electrical, thermal, protection and propulsion verification at the intended voltage/power point.

## Immediate engineering consequence

The critical path remains unchanged:

`phase-current model -> PWM freeze -> 18S energy/minimum-loaded-bus closure -> exact 150 V MOSFET/parallel count -> gate driver -> sensing/DC-link/thermal -> U1-SCH-R001`

Lower-voltage variant work is deferred until the rated U1 baseline is electrically and thermally coherent.
