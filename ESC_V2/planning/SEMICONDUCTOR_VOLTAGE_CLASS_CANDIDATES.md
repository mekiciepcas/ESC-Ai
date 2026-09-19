# Semiconductor voltage-class candidate table

Date: 2026-09-19
Branch: `uav-rebaseline`
Status: TRADE INPUT ONLY — no voltage class or production MPN is selected.

## Purpose
Provide primary-source device anchors for the eventual 100/120/150 V power-stage trade while G1 current/transient/PWM requirements remain OPEN. Values below must not be promoted to product ratings without a common operating envelope, hot-loss model, SOA/transient review and thermal design.

## Primary-source candidate anchors

| Class | Candidate | Manufacturer status / technology | VDS | RDS(on) evidence | Qg evidence | Current / thermal evidence | Package | Source |
|---|---|---|---:|---|---|---|---|---|
| 100 V legacy reference | TI CSD19536KTT | ACTIVE, NexFET | 100 V | 2.4 mOhm max @ VGS=10 V | 118 nC typ; Qgd 17 nC typ | ID package-limited 200 A; -55..175 C | TO-263 / D2PAK | TI product page/datasheet: https://www.ti.com/product/CSD19536KTT |
| 120 V candidate | Infineon IPT017N12NM6 | active/preferred, OptiMOS 6 | 120 V | 1.7 mOhm max @ VGS=10 V | 113 nC typ @10 V | ID 331 A @25 C; Ptot 395 W; -55..175 C | TOLL / PG-HSOF-8 | Infineon product page + Rev 2.0 datasheet: https://www.infineon.com/part/IPT017N12NM6 |
| 150 V candidate | Infineon IAUTN15S6N025 | active/preferred, automotive OptiMOS 6 | 150 V | 2.5 mOhm max @ VGS=10 V | 107 nC typ @10 V; manufacturer page also lists 139 nC max | ID 245 A @25 C; RthJC max 0.42 K/W; -55..175 C | TOLL / PG-HSOF-8 | Infineon product page: https://www.infineon.com/part/IAUTN15S6N025 |

Alternative 150 V packaging anchor: IAUTN15S6N038T, 150 V, 3.8 mOhm max, Qg 67 nC typ / 88 nC max, ID 170 A @25 C, RthJC 0.6 K/W, TOLT. This is useful if top-side cooling becomes an architecture requirement; it is not selected.

## What can and cannot be concluded

### Supported now
- Real, currently active devices exist in all three screening classes with low-milliohm RDS(on).
- Moving from the legacy 100 V D2PAK reference to 120 V or 150 V does **not** inherently imply unusable gate charge or resistance; current-generation devices provide plausible trade candidates.
- Package/cooling architecture changes materially across candidates and therefore package current numbers cannot be compared as ESC continuous-current ratings.
- The 100 V legacy CSD19536KTT remains a useful reference point only; its class cannot be accepted until the product transient ceiling and derating rule are closed.

### Not supported yet
- No candidate is proven lower-loss at the UAV operating point because phase RMS/peak current, PWM, junction/case temperature and switching waveform are not frozen.
- Manufacturer ID ratings are not ESC current ratings and shall not be copied into `design_basis.json`.
- No SOA, avalanche, repetitive transient, parallel-sharing or PCB thermal qualification has been completed.
- No final 100/120/150 V choice is made.

## Required normalization before G2 semiconductor freeze
For every surviving candidate, evaluate at the same evidenced envelope:
1. VBUS min/nom/full-charge/transient and explicit VDS derating margin.
2. Phase RMS/peak current and overload duration.
3. PWM frequency and gate-drive voltage/resistance.
4. RDS(on) at the relevant hot junction temperature using manufacturer curves/limits.
5. Conduction loss including parallel count and current-sharing tolerance.
6. Switching loss using datasheet/test-condition-aware Qgd/Coss/Qrr or measured Eon/Eoff where available.
7. Package RthJC plus actual PCB/baseplate thermal path.
8. SOA, avalanche/repetitive transient policy and short-circuit/fault-clearing interaction.
9. Layout implications: Kelvin source, loop inductance, top-side vs bottom-side cooling, manufacturability.
10. Lifecycle/availability check at selection time.

## Decision rule
Voltage class is governed first by the verified G1 transient envelope and derating policy, then by loss/thermal/package trade. A lower-voltage device cannot win solely on RDS(on) if transient margin is inadequate; a higher-voltage device cannot win solely on VDS if its loss/thermal implementation fails the common operating point.
