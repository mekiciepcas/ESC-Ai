# UAV ESC ürün geliştirme planı — PB-07 rebaseline

Tarih: 19.09.2026  
Branch: `uav-rebaseline`  
Aktif ürün yönü: **1.5–3.0 kW toplam propulsion giriş gücü sınıfında utility multirotor UAV + custom ESC platformu**.

> PB-01..PB-06 ağır-yük çalışmaları silinmez; tarihsel kanıt olarak korunur. PB-07, 70–100 kg payload / 150–180 kg MTOW / X8 / 18S / 500–1050 A yüksek-akım sayısal kapsamını aktif ürün otoritesi olmaktan çıkarmıştır.

## 0. Temel çalışma kuralları

Her kritik karar şu zincire bağlıdır:

`mission -> rotor/mass operating point -> battery -> per-ESC electrical requirement -> circuit calculation -> component/PCB/firmware -> verification evidence`

Kurallar:
- Bilinmeyen değerler `OPEN`, `null` veya `TBD` kalır.
- Üretici eğrisi sizing kanıtıdır; fiziksel doğrulama değildir.
- B1/Faz2/Faz3 değerleri otomatik product baseline değildir.
- G1/G2 kapanmadan komponentli U1 şema allocate edilmez.
- Her `.kicad_sch` değişikliği yeni şema revizyonu ister.
- Gerber/manufacturing release/main merge explicit user approval olmadan yapılmaz.

## PHASE A — PB-07 system / propulsion freeze

### A1 — Mission + mass envelope

Kontrollü mevcut değerler:
- toplam propulsion elektriksel güç ailesi: **1.5–3.0 kW**,
- nominal mission target: **>=10 min**,
- gross-pack reserve sizing policy: **>=20%**.

Kapanacak:
- payload min/nom/max,
- airframe + battery + mission equipment mass,
- MTOW min/nom/max,
- environment,
- degraded/failure behavior.

### A2 — Rotor architecture

Aktif trade:
- **Hexa non-coaxial — leading candidate**,
- **Quad non-coaxial — alternate**.

Current manufacturer curves show the 3 kW study point is roughly a 15–18 kg MTOW exploration band when screened at 1.6 static T/W. This is not yet a frozen MTOW.

Kapanış G1A:
- rotor count,
- thrust margin,
- hover/max thrust per rotor,
- single-motor failure/degraded policy.

### A3 — Motor / propeller operating point

Current primary-source anchors:
- Hobbywing X8 G2 12S + MFP 30x11S,
- T-Motor U8 Lite 12S.

Reference class only: roughly 28–30 inch propeller / 85–110 KV / 12S-class. Exact MPN remains OPEN.

Kapanış G1B:
- exact motor/propeller,
- hover/max-thrust power/current/RPM,
- pole count/eRPM,
- winding electrical parameters or controlled measurement.

### A4 — Battery architecture

Active candidates:
- **12S — leading**,
- **14S — alternate**.

Energy sensitivity for 10 min + 20% gross reserve before pack losses:
- 1.5 kW constant: 312.5 Wh,
- 2.0 kW: 416.7 Wh,
- 2.5 kW: 520.8 Wh,
- 3.0 kW: 625 Wh.

P50B 12S3P/12S4P are calculation candidates only.

Kapanış G1C:
- S/P count,
- min/nom/full bus,
- current/peak duration,
- energy/mass/sag,
- BMS/fuse/disconnect/precharge behavior.

### A5 — Per-ESC electrical envelope

Old PB-06 per-ESC >=4.8 kW / >=11.5 kW and 125–375 A phase-current values are retired.

New values will be derived after rotor architecture and battery freeze. Current first-order 3 kW study split:
- Hexa: ~500 W/axis,
- Quad: ~750 W/axis.

Kapanış G1:
- continuous/peak DC power/current,
- phase RMS/peak current,
- current-sense range,
- eRPM,
- PWM candidate/final value,
- bus/transient class,
- environment/protection/thermal limits.

## Active execution sprint — S1R

Authority: `SPRINT_PB07_LOW_POWER_REBASELINE.md`

1. **S1R.1 Product power rebaseline — DONE**
2. **S1R.2 Quad/Hexa + MTOW/payload — IN PROGRESS**
3. S1R.3 12S/14S + energy/current/mass
4. S1R.4 per-ESC envelope + B1/Faz2/Faz3 reuse audit
5. S1R.5 PWM/semiconductor/protection/thermal pre-freeze
6. S1R.6 G1 closeout

A reduction in G1 completion percentage after PB-07 is expected: incompatible heavy-lift values were intentionally reopened.

## PHASE B — ESC architecture freeze

After G1:
- 3-phase 2-level VSI topology review,
- exact semiconductor voltage class / MPN / parallel count,
- gate driver,
- MCU,
- phase-current sensing,
- bus sensing,
- DC-link/precharge/regen,
- auxiliary rails,
- CAN interface,
- fault architecture,
- thermal path.

Special PB-07 action: re-audit B1 because its historical ~3 kW / ~48 V / 100 V device class is now close to the active product power/voltage region. Reuse requires recalculation, not copy/paste.

Kabul kapısı: **G2 — ARCHITECTURE FREEZE**.

## PHASE C — Revision-controlled schematic + BOM

- Allocate `U1-SCH-R001` only when G1 and required G2 architecture conditions are PASS.
- Migrate only qualified B1 blocks.
- Exact MPN/footprint/derating evidence for every critical component.
- Real KiCad netlist/ERC/interface review.

Kabul kapısı: **G3 — SCHEMATIC DESIGN REVIEW**.

## PHASE D — Firmware

Minimum:
- safe boot with PWM inhibited,
- PWM/ADC synchronization,
- current calibration,
- gate-driver control,
- CAN-FD/Classic CAN,
- fault manager/state machine,
- motor-control bring-up,
- FOC/SVPWM,
- telemetry/logging,
- unit/SIL tests.

Kabul kapısı: **G4 — FIRMWARE BENCH READY**.

## PHASE E — PCB / thermal / manufacturability

- control PCB,
- power PCB/bus structure,
- Kelvin/gate/DC-link loops,
- creepage/clearance,
- thermal spreading/baseplate,
- DFM.

No Gerber release before explicit approval.

Kabul kapısı: **G5 — PROTOTYPE RELEASE**.

## PHASE F — Physical validation

Order:
1. unpowered/low-energy checks,
2. current-limited rails + PWM inhibit,
3. low-VBUS switching without propeller,
4. guarded motor test,
5. dyno/guarded prop stand,
6. thermal soak,
7. protection/fault injection.

Kabul kapısı: **G6 — PROPULSION VERIFIED**.

## PHASE G — UAV integration

- FC/CAN integration,
- harness/fuse architecture,
- arming/failsafe,
- EMI coexistence,
- cooling,
- configuration freeze,
- flight readiness review.

Flight is not used to discover basic power-stage faults.

Kabul kapısı: **G7 — FLIGHT TEST READY**.

## Major gates

- G0 Mission freeze — OPEN PB-07
- G1 System electrical freeze — OPEN PB-07
- G2 Architecture freeze — blocked by G1
- G3 Schematic review — blocked by G2
- G4 Firmware bench ready — blocked by G2
- G5 Prototype release — blocked by G3/G4
- G6 Propulsion verified — blocked by G5
- G7 Flight-test ready — blocked by G6

## Immediate dependency chain

`PB-07 -> Quad/Hexa + MTOW/payload -> 12S/14S + energy -> per-ESC envelope + B1 reuse -> PWM/protection/thermal -> G1 -> G2 -> U1-SCH-R001`
