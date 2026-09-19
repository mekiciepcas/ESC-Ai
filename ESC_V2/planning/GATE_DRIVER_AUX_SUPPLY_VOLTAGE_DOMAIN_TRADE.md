# Gate-driver and auxiliary-supply voltage-domain trade

Date: 2026-09-19
Branch: `uav-rebaseline`
Status: TRADE INPUT ONLY — no driver or auxiliary-power MPN is selected.

## Purpose
Prepare credible alternatives in case the final G1 VBUS/transient ceiling invalidates the legacy ~100 V DRV8353/LM5164 domain. This document does not select a voltage class. Candidate devices are only architecture anchors supported by current primary manufacturer data.

## Gate-driver candidates

### Legacy reference — DRV8353FSRTAR
Repository status: B1 reference / REVALIDATE.

Reason it remains open:
- legacy architecture already integrates three half-bridge drivers, current-sense amplifiers and SPI configuration;
- its bus-related voltage domain is coupled to the unresolved final transient ceiling;
- if G1 proves that the switch/driver domain can exceed the legacy ~100 V region, the part cannot simply be retained by inertia.

Evidence: B1 repository source, `UAV_TRACEABILITY.md`, previous voltage-domain audit.

### 120 V bootstrap-class anchor — TI UCC27282 / UCC27282-Q1
Primary-source evidence:
- active product family;
- ±3 A peak output class;
- absolute maximum boot voltage 120 V;
- TI product description states maximum HS switch-node rating is 100 V;
- 5.5–16 V driver supply range depending variant/details;
- interlock / enable options and integrated bootstrap diode variants.

Interpretation:
- useful as a modern 120 V bootstrap-family reference;
- **not** a proven solution for a product whose normal/transient switch-node requirement exceeds 100 V, despite the 120 V bootstrap absolute maximum headline;
- therefore it does not eliminate the same fundamental G1 transient dependency as DRV8353.

Primary source: https://www.ti.com/product/UCC27282-Q1 and https://www.ti.com/lit/ds/symlink/ucc27282.pdf

### High-voltage non-isolated half-bridge anchor — TI UCC27712 / UCC27712-Q1
Primary-source evidence:
- active product family;
- fully operational up to 620 V high-side/low-side architecture;
- 700 V absolute maximum on HB pin;
- 1.8 A source / 2.8 A sink;
- recommended VDD 10–20 V, with MOSFET guidance in the lower part of that range;
- 100 ns typical propagation delay, 12 ns typical delay matching;
- 50 V/ns dv/dt immunity; interlock and dead-time features.

Interpretation:
- removes the 100 V bootstrap-domain ceiling as the dominant driver-voltage limitation for a 100–150 V MOSFET study;
- trades away some integration and speed compared with the legacy three-phase smart driver;
- would require three half-bridge driver channels, separate current-sense/protection architecture, and a fresh PWM/dead-time/FOC timing review.

Primary source: https://www.ti.com/product/UCC27712

### Reinforced-isolated dual-channel anchor — TI UCC21540-Q1
Primary-source evidence:
- active automotive dual-channel reinforced isolated driver;
- 5.7 kVrms isolation withstand, 1000 Vrms working isolation specification;
- 4 A source / 6 A sink;
- 125 V/ns minimum CMTI;
- output-side supply 9.2–18 V; input-side supply 3–5.5 V;
- programmable dead time and disable.

Interpretation:
- bus voltage is no longer coupled directly to a monolithic high-side level-shift ceiling in the same way as a bootstrap-only smart driver;
- much stronger architecture change: isolated output bias supplies, propagation-delay/skew budget, creepage/clearance, cost and PCB area all become first-order items;
- retain only as a robustness/high-voltage architecture candidate until G1 proves isolation/CMTI benefit is worth the complexity.

Primary source: https://www.ti.com/product/UCC21540-Q1

## Auxiliary-power candidates

### Legacy reference — LM5164
Repository status: B1 reference / REVALIDATE.

The existing architecture is attractive for low component count but remains coupled to the unresolved ~100 V input-domain ceiling. It cannot be assumed valid if final G1 transient acceptance exceeds its proven input domain.

### 150 V low-power housekeeping anchor — ADI LTC3639
Primary-source evidence:
- recommended for new designs;
- 4–150 V operating input range;
- synchronous step-down with internal switches;
- adjustable 10–100 mA maximum output current;
- 1.8 V / 3.3 V / 5 V or adjustable outputs;
- programmable input overvoltage lockout;
- production orderable variants listed by ADI.

Interpretation:
- credible way to power a low-current always-on/control housekeeping domain directly from a bus up to the 150 V class;
- **not sufficient by itself** for the legacy auxiliary load if the design still requires roughly 0.2 A fan current plus gate-driver/control loads;
- therefore this is a control-housekeeping anchor, not a direct LM5164 replacement for the entire auxiliary-power tree.

Primary source: https://www.analog.com/en/products/ltc3639.html

### 150 V higher-power controller anchor — ADI LTC7801
Primary-source evidence:
- recommended for new designs;
- 4–140 V operating input, 150 V absolute maximum;
- synchronous step-down controller using external MOSFETs;
- 0.8–60 V output range;
- programmable 50–900 kHz operating-frequency range;
- adjustable 5–10 V gate drive; integrated bootstrap diode; programmable input OVLO.

Interpretation:
- credible architecture for a materially higher-current 12 V auxiliary rail while preserving a high-voltage input domain;
- significantly more complex than LM5164 because the power switches, current sensing, inductor and compensation/layout become a full converter design;
- actual output-current capability is design-dependent and shall not be inferred from the controller alone.

Primary source: https://www.analog.com/en/products/ltc7801.html

## Architecture implications

### If final transient ceiling remains comfortably below the proven legacy domain
DRV8353 + LM5164 may remain candidates, subject to normal loss, gate-drive, OCP, aux-load and transient derating proof.

### If final transient ceiling approaches/exceeds the legacy ~100 V domain
The architecture must not merely pair higher-VDS MOSFETs with unchanged 100 V-domain support ICs. At least one of these paths becomes necessary:
1. stronger upstream clamp/protection that guarantees a lower support-IC domain with evidence;
2. higher-voltage non-isolated gate driver + higher-voltage auxiliary converter;
3. isolated gate-driver architecture + appropriately isolated/local bias supplies.

The selected path depends on G1 transient ceiling, PWM/phase-current envelope, gate-charge requirement, fault latency, cost/area and EMI/CMTI evidence.

## What is closed by this trade
- Real active alternatives exist for both gate drive and auxiliary power if the legacy ~100 V support domain is rejected.
- A 120 V bootstrap headline alone is not enough: the UCC27282 family still has a 100 V HS operating ceiling and therefore does not prove >100 V operation.
- UCC27712 provides a credible non-isolated high-voltage half-bridge path; UCC21540-Q1 provides a credible isolated path.
- LTC3639 provides a credible 150 V low-power housekeeping path; LTC7801 provides a credible higher-power 140 V-operating / 150 V-absolute controller path.

## What remains open
- final bus/transient ceiling and required derating;
- gate-driver peak current from selected MOSFET Qg, target transition time and gate resistance;
- PWM/dead-time/propagation-delay budget;
- whether current-sense amplifiers stay integrated or move to separate devices;
- auxiliary load budget split between control, gate drive, fan and external sensors;
- whether isolation is required or merely optional;
- final MPNs, footprints, thermal design and BOM selection.

## Decision rule
Do not select a driver or auxiliary converter from voltage rating alone. First close G1 VBUS/transient and the auxiliary load budget, then normalize gate-drive current, timing, fault coverage, loss, thermal, EMI/CMTI, PCB area and procurement evidence.
