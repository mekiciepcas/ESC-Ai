# CSD19536KTT reference parameters

Date: 2026-09-19
Role: LEGACY/B1 REFERENCE ONLY — not a UAV part selection

TI currently lists CSD19536KTT as an active 100 V N-channel NexFET in D2PAK/TO-263.

## Primary-source headline parameters
From TI product/datasheet data:

- VDS: 100 V
- VGS: +/-20 V class (product page lists 20 V)
- RDS(on), max at VGS=10 V: 2.4 mOhm
- Qg, typical: 118 nC
- Qgd, typical: 17 nC
- Qgs, typical: 37 nC
- ID silicon-limited at TC=25 C: 272 A
- ID package-limited: 200 A
- operating junction-temperature range: -55 to +175 C
- package: TO-263 / D2PAK
- avalanche rated per TI feature list

Primary evidence: TI CSD19536KTT product page and Rev. C datasheet.

## Use in the UAV loss framework
These values are sufficient to populate a **reference-only** row in the semiconductor trade, but not to calculate a release loss number. Required numeric loss inputs still include:

- RDS(on) versus junction temperature / selected VGS,
- actual phase RMS and peak current,
- switching frequency,
- VBUS at the operating point,
- measured/validated switching transition behavior with the selected gate driver and gate network,
- reverse-recovery/body-diode behavior relevant to commutation,
- parallel-current sharing,
- PCB/package thermal impedance and cooling boundary condition.

A simplistic screening conduction term for N identical, perfectly sharing parallel devices is:

`Pcond_switch ~= I_rms_switch^2 * RDSon_hot / N`

A first-order switching-energy screen may use datasheet charge/transition information only for ranking; final switching loss requires representative double-pulse or equivalent switching evidence.

## Voltage-class finding
At the current 18S candidate full-charge value of 75.6 V, a 100 V MOSFET has only 24.4 V static headroom before any wiring/PCB inductive overshoot, regen, or disconnect event. Therefore CSD19536KTT remains useful as a B1 loss/reference anchor but **100 V is not frozen for the UAV design**.

No current rating, parallel count, thermal rating, or production MPN is frozen by this note.