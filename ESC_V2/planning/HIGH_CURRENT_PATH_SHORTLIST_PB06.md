# PB-06 high-current path shortlist

Date: 2026-09-19
Status: PRELIMINARY_CANDIDATE_SCREENING_NOT_SELECTION
Authority: PRODUCT_BASELINE_PB-06.json

## Controlled electrical envelope

This screening is bounded by the frozen PB-06 whole-pack requirements: 18S, 75.6 V full charge, <=80 V outer input ceiling, >=500 A continuous pack capability, and >=1050 A for >=3 s. The 1050 A point is a vehicle-level sizing requirement, not a measured pack capability.

No candidate below is released for flight, production, or exact pack design. Continuous ratings are not assumed to imply 1050 A / 3 s interruption capability. Interrupt/break capability, pulse thermal capability, altitude/environment derating, fault-current coordination, terminal temperature and installation conductor requirements remain separate verification items.

## Candidate screening

### Main contactor — TE Connectivity KILOVAC EV200 family

Primary-source screen: TE lists EV200 variants at 500 A contact current rating and 12-900 VDC contact voltage. The EV200 performance data states typical continuous carry current 500 A at 85 C with 400 mcm conductors, typical contact resistance 0.2 mOhm at 200 A, and instructs users to consult the factory for required conductors above 500 A. The same source lists a 2000 A break point at 320 VDC for one cycle; that datum must not be extrapolated into a qualified 1050 A / 3 s carry or interruption result for our 80 V system without the applicable curves/conditions.

Preliminary resistive-loss anchor using 0.2 mOhm typical contact resistance only:
- 500 A: P = I^2 R = 50 W.
- 1050 A: instantaneous arithmetic P = 220.5 W.

These are not guaranteed hot-contact losses; contact resistance versus temperature/life and terminal/conductor losses remain OPEN. EV200 is therefore a CANDIDATE, not selected.

Primary source: https://www.te.com/en/product-1-1618002-1.html and TE EV200 performance-data PDF linked from that product page.

### Pack current sensor — LEM HAX 1000-S

LEM lists HAX 1000-S as 1000 Arms nominal, 3000 A measuring range, AC+DC open-loop Hall measurement, +/-4 V instantaneous output, +/-15 V supply, 1% accuracy, -40 C to +85 C operating range, and DC...25 kHz bandwidth. Its 3000 A measuring range contains the PB-06 1050 A peak requirement with measurement headroom.

This is attractive because the primary conductor passes through the aperture and therefore the sensor itself need not add a series shunt loss. Exact aperture/busbar packaging, supply compatibility, offset/drift, EMC, dynamic accuracy and flight-environment suitability remain OPEN.

Primary source: https://www.lem.com/en/product-list/hax-1000s

Alternative precision/traction candidate: LEM LTC 1000-T is listed as 1000 Arms nominal, 2400 A measuring range, closed-loop Hall, -40 C to +85 C, 0.4% accuracy and integrated-busbar option. Its +/-15 to 24 V bipolar supply and mass/packaging burden require later evaluation.

Primary source: https://www.lem.com/en/product-list/ltc-1000t

### Output/service connector — Amphenol SurLok Plus family

Amphenol's current product page states the SurLok Plus family spans 50 A to 500 A, with IP67 or IP6K9K depending on size/voltage rating and -40 C to 125 C operating temperature. Therefore the family can screen against the 500 A continuous requirement only at the upper-rated configuration; the public family rating does NOT establish >=1050 A / 3 s capability.

Disposition: CANDIDATE_FOR_500A_CONTINUOUS_PATH_ONLY. Exact size/cable cross-section, temperature-rise data, 1050 A pulse evidence, contact resistance, mating-cycle policy and whether a parallel connector architecture is permissible remain OPEN.

Primary source: https://amphenol-industrial.com/products/surlok-plus/

### Main fuse — OPEN

No fuse is selected. The required item must coordinate with >=500 A continuous operation while surviving legitimate >=1050 A / >=3 s propulsion demand and still interrupt the credible pack fault current at <=80 VDC. A current rating alone is insufficient: time-current curve, DC interrupt rating, minimum/maximum clearing I2t, ambient/terminal derating, pre-arcing energy, pack prospective short-circuit current and downstream conductor/contact limits are mandatory evidence.

### Service disconnect — OPEN

No service disconnect is selected. It must not be treated as a load-break device unless its manufacturer explicitly rates it for the required DC interruption conditions. Touch-safe/service isolation, insertion/removal interlock policy, creepage/clearance, continuous temperature rise, pulse current and fault-current withstand remain OPEN.

## First-order current-path loss budget

At these currents milliohms are unacceptable. For the complete pack current path, every 0.1 mOhm produces:
- 25 W at 500 A continuous;
- 110.25 W at 1050 A instantaneous.

A 1.0 mOhm total path would therefore dissipate 250 W at 500 A and 1.1025 kW at 1050 A. This establishes why the next design artifact must budget resistance by element (cell interconnects, series welds/joints, busbars, fuse, contactor, service disconnect, output connector and cable terminations) rather than selecting components independently.

## Selection gates

Before exact current-path release, each series element requires: exact MPN/configuration; guaranteed continuous rating at the intended ambient/terminal temperature; 1050 A / >=3 s thermal/current evidence or controlled test; DC fault/interruption role explicitly classified; resistance or voltage-drop evidence; mass; conductor/terminal geometry; environmental rating; and coordination with BMS/fuse/contactor logic.

## Result

This study reduces S1.3 uncertainty but does not close UAV-005. The contactor and current-sensor categories now have source-backed candidates. Connector screening identifies a likely 500 A boundary but no demonstrated 1050 A pulse capability. Fuse and service disconnect remain OPEN because PB-06 does not yet define credible prospective pack short-circuit current, exact cell topology/current sharing, or environmental envelope.
