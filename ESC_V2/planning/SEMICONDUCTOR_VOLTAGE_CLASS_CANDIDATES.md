# Semiconductor voltage-class candidate table

Date: 2026-09-19
Branch: `uav-rebaseline`
Status: TRADE INPUT ONLY — no voltage class or production MPN is selected.

## Purpose
Provide primary-source device anchors for the eventual 100/120/150 V power-stage trade while G1 current/transient/PWM requirements remain OPEN. Values below must not be promoted to product ratings without a common operating envelope, hot-loss model, SOA/transient review and thermal design.

## Primary-source candidate anchors

| Class | Candidate | Manufacturer status / technology | VDS | RDS(on) evidence | Qg evidence | Current / thermal evidence | Package | Source |
|---|---|---|---:|---|---|---|---|---|
| 100 V legacy reference | TI CSD19536KTT | ACTIVE, NexFET | 100 V | 2.4 mOhm max @ VGS=10 V, ID=100 A | 118 nC typ; Qgd 17 nC typ @ VDS=50 V, ID=100 A | ID package-limited 200 A; RthJC 0.4 C/W; -55..175 C | TO-263 / D2PAK | TI product page/datasheet: https://www.ti.com/product/CSD19536KTT |
| 120 V candidate | Infineon IPT017N12NM6 | active/preferred, OptiMOS 6 | 120 V | 1.7 mOhm max @ VGS=10 V, ID=150 A | 113 nC typ / 141 nC max; Qgd 25 nC typ / 38 nC max @ VDD=60 V, ID=75 A | ID 331 A @25 C; RthJC 0.38 C/W; Ptot 395 W; -55..175 C | TOLL / PG-HSOF-8 | Infineon product page + Rev 2.0 datasheet: https://www.infineon.com/part/IPT017N12NM6 |
| 150 V candidate | Infineon IAUTN15S6N025 | active/preferred, automotive OptiMOS 6 | 150 V | 2.5 mOhm max @ VGS=10 V | 107 nC typ / 139 nC max; Qgd 27 nC typ @ VDD=75 V, ID=123 A | ID 245 A @25 C; RthJC max 0.42 K/W; -55..175 C | TOLL / PG-HSOF-8 | Infineon product page + Rev 1.0 datasheet: https://www.infineon.com/part/IAUTN15S6N025 |

Alternative 150 V packaging anchor: IAUTN15S6N038T, 150 V, 3.8 mOhm max, Qg 67 nC typ / 88 nC max, ID 170 A @25 C, RthJC 0.6 K/W, TOLT. This is useful if top-side cooling becomes an architecture requirement; it is not selected.

## Dynamic / recovery evidence captured for future normalized loss work

These values are recorded with their test conditions because direct comparison without normalization is misleading.

| Device | Coss evidence | Qoss evidence | Qrr evidence | RthJC | Important test-condition note |
|---|---|---|---|---|---|
| CSD19536KTT | 1820 pF typ / 2370 pF max | 335 nC typ | 548 nC typ | 0.4 C/W | Coss at VDS=50 V, f=1 MHz; Qrr at VDS=50 V, IF=100 A, di/dt=300 A/us |
| IPT017N12NM6 | 2400 pF typ / 3100 pF max | 266 nC typ / 333 nC max | 111 nC typ / 222 nC max @300 A/us; 301 nC typ / 602 nC max @1000 A/us | 0.38 C/W | Coss/Qg at 60 V; reverse recovery at VR=60 V, IF=75 A |
| IAUTN15S6N025 | 2370 pF typ | not yet normalized into trade table | 23 nC typ / 46 nC max | 0.42 K/W max | Coss at VDS=75 V, f=1 MHz; Qrr at VR=75 V, IF=50 A, di/dt=100 A/us |

### Interpretation limit
The low published Qrr of the 150 V part cannot be declared a direct switching-loss win over the 120 V or 100 V devices because the reverse-current and di/dt test conditions differ substantially. Likewise, Coss measured at 50/60/75 V must not be compared as if it represented a complete Eoss curve. The final trade must either use manufacturer Eoss/Qoss curves at the same bus voltage or a measured/simulated common switching condition.

## Hot RDS(on) handling

All three candidates have temperature-dependent RDS(on); the legacy TI datasheet, for example, shows a strong increase from 25 C toward 125–175 C. The final loss model shall use each manufacturer's temperature curve or guaranteed hot limit at the same junction-temperature assumption. A 25 C headline milliohm value is prohibited as the sole conduction-loss input.

Exact normalized hot-RDS multipliers are deliberately not frozen here because the product junction/case/baseplate design temperature remains a G1/G2 dependency.

## What can and cannot be concluded

### Supported now
- Real, currently active devices exist in all three screening classes with low-milliohm RDS(on).
- Moving from the legacy 100 V D2PAK reference to 120 V or 150 V does **not** inherently imply unusable gate charge or resistance; current-generation devices provide plausible trade candidates.
- Package/cooling architecture changes materially across candidates and therefore package current numbers cannot be compared as ESC continuous-current ratings.
- The 100 V legacy CSD19536KTT remains a useful reference point only; its class cannot be accepted until the product transient ceiling and derating rule are closed.
- Enough Qgd/Coss/Qrr/RthJC evidence now exists to build a condition-normalized switching/conduction comparison once the G1 electrical envelope is frozen.

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
