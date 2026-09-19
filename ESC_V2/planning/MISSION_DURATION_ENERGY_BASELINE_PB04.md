# PB-04 mission duration and energy sizing baseline

Date: 2026-09-19  
Branch: `uav-rebaseline`  
Status: **CONTROLLED PRODUCT TARGET / PACK SELECTION STILL OPEN**

## Frozen product targets

PB-04 freezes the following system targets for the rated heavy-lift product baseline:

- nominal payload reference: **85 kg**;
- nominal MTOW design target: **165 kg**;
- rated total mission-duration target at the nominal reference condition: **>=10 min**;
- first-order hover-equivalent energy-sizing duration at the nominal reference condition: **>=10 min**;
- pack energy sizing reserve: **>=20%** beyond the calculated nominal mission energy.

The 20% value is an engineering sizing reserve. It is **not** yet the firmware low-battery threshold, BMS SOC cutoff or an operational landing-SOC requirement.

## Market sanity check

Current heavy-lift market evidence supports a roughly 10-minute rated target rather than an aggressive 15-20 minute requirement at this mass class.

Primary comparison used:

- DJI FlyCart 100 official specification: at **149.9 kg takeoff weight**, dual-battery maximum hovering endurance is **12 min** and maximum flight time is **14 min**, measured to 0% charge in ideal windless sea-level 25 C conditions.
- Source: https://www.dji.com/flycart-100/specs

Agricultural battery architecture also demonstrates that high-utilization products can prioritize rapid battery turnover rather than very long single-sortie endurance:

- DJI AGRAS T70P DB2160: 52 V, 41 Ah, 14.7 kg; official generator recharge time is about 8-9 min from 30% to 95%.
- Source: https://ag.dji.com/t70p/specs

These competitor figures are market evidence only. They are **not copied as ESC electrical requirements**.

## Current reference propulsion calculation

The current sizing anchor remains Hobbywing X13 G2 / MFP 56x20 at 69 V. The official manufacturer curve includes:

- 24.212 kgf thrust -> 2671.2 W input;
- 26.664 kgf thrust -> 3085.1 W input.

Linear interpolation is used only for first-order system energy sizing between these adjacent published points.

### Nominal 165 kg MTOW

Frozen isolated-equivalent hover thrust per rotor: **24.265 kgf**.

Interpolated input power per rotor:

`P_axis ~= 2680 W`

Eight propulsion channels:

`P_vehicle_hover ~= 8 * 2680 = 21.44 kW`

Ten-minute hover-equivalent mission energy:

`E_mission ~= 21.44 kW * 10/60 h = 3.57 kWh`

With 20% energy reserve interpreted as mission energy occupying no more than 80% of nominal pack energy:

`E_pack_nominal_min ~= 3.57 / 0.80 = 4.47 kWh`

At the current 18S nominal convention of 66.6 V:

`C_equivalent ~= 4.47 kWh / 66.6 V = 67.1 Ah`

### 180 kg maximum-MTOW stress reference

Frozen isolated-equivalent hover thrust per rotor: **26.471 kgf**.

Interpolated input power per rotor:

`P_axis ~= 3053 W`

Vehicle hover input:

`P_vehicle_hover ~= 24.42 kW`

Ten-minute mission energy:

`E_mission ~= 4.07 kWh`

With the same 20% sizing reserve:

`E_pack_nominal ~= 5.09 kWh`

66.6 V nominal-equivalent capacity:

`C_equivalent ~= 76.4 Ah`

The 180 kg result is a **stress/trade reference**, not a PB-04 promise that the vehicle will hover for 10 minutes at maximum payload with the final pack.

## Why the exact pack is still OPEN

The following must close before exact Ah/Wh, cell/pouch and pack mass can freeze:

1. selected cell/pouch discharge curve and temperature behavior;
2. minimum loaded bus voltage and allowed voltage sag;
3. continuous and peak pack-current requirement including eight ESCs and auxiliaries;
4. pack interconnect, fuse/contactor/BMS losses;
5. usable SOC window and actual BMS disconnect behavior;
6. battery mass allocation inside the <=80 kg operating-empty budget;
7. detailed mission power trace and physical propulsion correlation.

Therefore **4.47 kWh / 67.1 Ah is a nominal sizing bound, not the selected battery**.

## Product disposition

- **FROZEN:** >=10 min nominal mission target at 85 kg payload / 165 kg nominal MTOW reference.
- **FROZEN:** >=10 min hover-equivalent first-order energy-sizing duration at the nominal reference.
- **FROZEN:** >=20% energy sizing reserve.
- **DERIVED BOUND:** approximately >=4.47 kWh / 67.1 Ah nominal-equivalent at the current X13 G2 reference curve.
- **TRADE ONLY:** approximately 5.09 kWh / 76.4 Ah for a 10-minute 180 kg stress case.
- **OPEN:** exact battery MPN/cell/pouch, exact Ah/Wh, mass, minimum loaded bus, sag and disconnect thresholds.

No endurance, thermal or flight performance has been physically demonstrated by this document.
