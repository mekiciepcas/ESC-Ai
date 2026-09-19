# Battery cell / pack trade — PB-05

Date: 2026-09-19  
Branch: `uav-rebaseline`  
Status: **S1.3 PRODUCTIZATION STUDY / CELL MPN NOT FROZEN**

## Purpose

Convert PB-04's mission-energy bound into a product-level battery architecture that can support the frozen 18S heavy-lift ESC baseline without pretending that an exact cell, BMS, contactor or pack mechanical design has already been qualified.

## Frozen parents

- 18S architecture.
- 85 kg nominal payload / 165 kg nominal MTOW reference.
- 180 kg maximum-MTOW stress reference.
- >=10 min nominal mission target.
- >=10 min hover-equivalent first-order sizing duration.
- 20% gross-pack energy reserve policy.
- Current reference hover input: about 21.441 kW at 165 kg nominal MTOW.
- Current reference hover input: about 24.420 kW at 180 kg maximum-MTOW stress case.
- Full-charge target 75.6 V and outer U1 input ceiling <=80 V.

## Reserve semantics clarification

For S1.3, a **20% reserve** means the nominal mission-energy calculation may consume no more than 80% of gross rated pack energy at the reference condition. Therefore PB-04's 3.574 kWh nominal terminal mission-energy calculation corresponds to 3.574 / 0.80 = 4.467 kWh before battery internal-loss and pack-overhead allowances.

This is a sizing policy. It is not the final BMS SOC cut-off, firmware low-battery threshold or emergency landing threshold.

## Primary-source cell candidates

The following are current manufacturer power-cell references. They are calculation candidates, not selected U1 production cells.

| Cell | Nominal / charge | Typical / minimum energy | Continuous discharge headline | Typical DC impedance @ 50% SOC | Max cell mass | Pack role |
|---|---|---|---:|---:|---:|---|
| Molicel INR-21700-P45B | 3.6 / 4.2 V | 16.2 / 15.5 Wh | 45 A, 80 C cut-off | 15 mOhm | 70 g | mature alternate |
| Molicel INR-21700-P50B | 3.6 / 4.2 V | 18.0 / 17.5 Wh | 60 A, 80 C cut-off | 12.8 mOhm | 71 g | primary qualification candidate |
| Molicel INR-21700-P60B | 3.6 / 4.2 V | 21.6 / 21.3 Wh | 60 A standard; 100 A max under stated limits | 12.8 mOhm | 75 g | mass-optimization candidate |

Manufacturer sources accessed 2026-09-19:
- P45B product data sheet: https://www.molicel.com/wp-content/uploads/INR21700P45B_1.4_Product-Data-Sheet-of-INR-21700-P45B-80109.pdf
- P50B product/data sheet: https://www.molicel.com/product/inr-21700-p50b/ and https://www.molicel.com/wp-content/uploads/Product-Data-Sheet-of-INR-21700-P50B-80122.pdf
- P60B product data sheet: https://www.molicel.com/wp-content/uploads/Product-Data-Sheet-of-INR-21700-P60B_80145.pdf

Molicel explicitly lists drones/eVTOL applications for the P-series power-cell family; P50B is also marketed for heavy-lift drones. This is application relevance, not U1 qualification.

## 5.0 kWh class topology screen

The table below sizes parallel count against **manufacturer minimum cell energy**, not typical capacity.

| Candidate topology | Cells | Minimum cell-only pack energy | Typical cell-only pack energy | Cell-only max mass | Cell-level continuous-current sum |
|---|---:|---:|---:|---:|---:|
| P45B 18S18P | 324 | 5.022 kWh | 5.249 kWh | 22.68 kg | 810 A |
| P50B 18S16P | 288 | 5.040 kWh | 5.184 kWh | 20.45 kg | 960 A |
| P60B 18S14P | 252 | 5.368 kWh | 5.443 kWh | 18.90 kg | 840 A standard-current sum |

These masses are **cells only**. Busbars, welds, conductors, fuses, contactors, BMS electronics, enclosure, insulation, cooling, fire containment and mechanical retention are not included.

## Nominal-hover impedance sanity screen

All three candidate families specify 3.6 V nominal, so their 18S candidate-pack nameplate nominal is 64.8 V. This does not silently supersede the existing PB-04 66.6 V system convention; exact pack nominal labeling remains dependent on the final cell selection and will require controlled baseline reconciliation.

At 21.441 kW / 64.8 V, the simple nominal-bus current screen is about **330.9 A**. Using manufacturer **typical DC impedance at 50% SOC** only as a room-temperature sensitivity term:

| Topology | Current/cell at 330.9 A | Estimated pack R from typical DCR | I*R drop | I^2R loss |
|---|---:|---:|---:|---:|
| P45B 18S18P | 18.4 A | 15.0 mOhm | 5.0 V | 1.64 kW |
| P50B 18S16P | 20.7 A | 14.4 mOhm | 4.8 V | 1.58 kW |
| P60B 18S14P | 23.6 A | 16.46 mOhm | 5.4 V | 1.80 kW |

These are **not minimum-bus predictions**. DC impedance is typical, SOC- and temperature-dependent, and the simple model omits OCV-vs-SOC, interconnect resistance, cell spread, aging and thermal rise. The result is used only to show that PB-04's 4.467 kWh pre-loss bound should not be treated as the final pack rating.

## PB-05 product decisions supported by this study

### 1. Gross rated energy

Adopt **>=5.0 kWh minimum rated pack energy** for the rated 18S U1 vehicle baseline at the nominal mission reference.

Rationale:
- PB-04 pre-loss gross bound is ~4.467 kWh.
- Candidate room-temperature DCR screens add roughly 0.26-0.30 kWh internal-loss energy over a 10-minute hover-equivalent mission at nominal reference power.
- 5.0 kWh provides a clean product target above this first-order result while leaving exact cell chemistry/topology and pack-level validation open.

This does not guarantee 10 minutes at every temperature, altitude, payload or aged-SOH condition.

### 2. Rated-power minimum loaded bus

Adopt **54.0 V loaded bus as the minimum voltage for full rated-power operation**, equivalent to 3.0 V/cell for 18S.

Below 54.0 V, full rated power is not guaranteed and the control system shall enter a power-derating / mission-termination policy to be defined in S1.4. The hard battery cut-off remains cell/BMS-specific and is not frozen here.

This 3.0 V/cell rated-power floor is conservative relative to the P45B/P50B 2.5 V datasheet discharge endpoint and is directly aligned with the P60B maximum-discharge condition that specifies a 3.0 V cut-off.

### 3. Pack continuous-current capability

At the 180 kg maximum-MTOW hover reference, 24.420 kW / 54.0 V = **452.2 A**. Applying about 10% design allowance gives ~497 A, rounded upward to:

**>=500 A continuous pack-current capability at the rated thermal condition.**

This is a battery-system design capability target. It does not mean normal hover current is 500 A, and it does not qualify the cell interconnect/BMS/contactors thermally.

At 500 A, candidate cell current is approximately:
- P45B 18P: 27.8 A/cell,
- P50B 16P: 31.3 A/cell,
- P60B 14P: 35.7 A/cell.

All are below the cited manufacturer continuous cell-current headlines, but pack-level current sharing, thermal rise and conductor losses still require validation.

## Candidate disposition

- **P50B 18S16P**: primary qualification candidate because it combines a mature v1.1 data sheet, explicit heavy-lift/eVTOL application positioning, >=5 kWh minimum cell energy and strong current headroom.
- **P60B 18S14P**: mass-optimization candidate; about 1.55 kg lower cell-only mass than P50B 18S16P, but its current product-data sheet is still version 0.1 and therefore supply/qualification maturity must be checked before selection.
- **P45B 18S18P**: mature fallback/reference; highest cell-only mass among the three for the >=5 kWh target.

No exact cell MPN is FROZEN by PB-05.

## Still OPEN before exact pack freeze

1. Exact cell/pouch MPN and supplier/lot policy.
2. Pack mechanical layout, parallel-group segmentation and serviceability.
3. Cell interconnect / busbar / weld current-sharing and thermal proof.
4. BMS/contactors/fuses/precharge architecture and ratings.
5. Low-SOC/cold/aged voltage-sag model and measured minimum loaded bus correlation.
6. Pack mass including enclosure, cooling, insulation and safety hardware.
7. Peak pack current / duration requirement from vehicle transient-thrust profile.
8. Charging system and turnaround requirement.
9. Environmental / ingress / abuse / transport qualification.

## Engineering boundary

The 5.0 kWh, 54.0 V rated-power floor and 500 A continuous-current values are product-level design requirements. The candidate topology tables and DCR calculations are design evidence only. No physical pack, endurance, thermal or flight verification is claimed.
