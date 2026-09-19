# UAV ESC ürün geliştirme planı — PB-08 common-platform baseline

Tarih: 19.09.2026  
Branch: `uav-rebaseline`  
Aktif ürün yönü: **1.5–3.0 kW toplam propulsion giriş gücü sınıfında utility multirotor UAV + custom ESC platformu**.

> PB-01..PB-06 ağır-yük çalışmaları silinmez; tarihsel kanıt olarak korunur. PB-07 ürünü düşük-güç sınıfına rebaseline etti. PB-08 bu yeni ürün için ortak 12S elektrik platformunu ve ESC donanım kapasitesini dondurur.

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

## PHASE A — PB-08 system / propulsion freeze

### A1 — Mission + mass envelope

Kontrollü mevcut değerler:
- toplam propulsion elektriksel güç ailesi: **1.5–3.0 kW**,
- üst continuous ürün tasarım noktası: **3.0 kW**,
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

Current manufacturer curves show the 3 kW study point is roughly a 15–18 kg MTOW exploration band when screened at 1.6 static T/W. PB-08 mass roll-up adds a hard decision rule: the Hexa MTOW screen gains 2.025 kg over Quad, therefore the break-even installed mass for each of the two extra propulsion axes is **1.0125 kg/axis** before extra arm/frame mass. Exact custom propulsion-axis and structural mass still decide the winner.

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

PB-08 frozen common bus:
- **12S**,
- **43.2 V nominal** system convention,
- **50.4 V full charge**,
- **36.0 V loaded floor for full rated ESC power**,
- below 36 V: controlled derating / mission-termination policy required,
- **>=750 Wh gross rated pack-energy target for the 3 kW upper variant**.

Calculation references only:
- P50B 12S4P preferred 3 kW energy topology,
- P50B 12S3P lower-power/lightweight reference.

Exact cell/P-count/pack mass/sag/BMS/fuse/disconnect remain OPEN.

Kapanış G1C:
- exact pack implementation and current/peak duration,
- mass/sag/SOC-temperature-SOH envelope,
- BMS/fuse/disconnect/precharge behavior.

### A5 — Per-ESC electrical envelope

PB-08 frozen hardware capability:
- **>=1.0 kW continuous input per ESC**,
- **>=1.5 kW for >=3 s per ESC**,
- **>=30 A continuous DC per ESC**,
- **>=50 A for >=3 s per ESC**,
- **>=100 V power-semiconductor class**,
- **<=75 V repetitive controlled switch-terminal stress target**,
- no normal repetitive avalanche reliance.

These are hardware capability values. Vehicle-level normal aggregate propulsion remains 1.5–3.0 kW; vehicle simultaneous peak policy remains OPEN until rotor/degraded-mode closure.

Still required for G1:
- phase RMS/peak current,
- current-sense range,
- eRPM,
- PWM candidate/final value,
- pack peak current,
- environment/protection/thermal limits,
- DC-link ripple/transient-energy requirements.

## Active execution sprint — S1R

Authority: `SPRINT_PB07_LOW_POWER_REBASELINE.md`

1. **S1R.1 Product power rebaseline — DONE**
2. **S1R.2 Quad/Hexa + MTOW/payload — IN PROGRESS**
3. **S1R.3A common 12S bus + common ESC hardware envelope — DONE in parallel via PB-08**
4. S1R.3B exact pack energy/current/mass/sag/BMS closure
5. S1R.4 exact motor/prop + per-ESC phase-current/eRPM + B1/Faz2/Faz3 reuse audit
6. S1R.5 PWM/semiconductor exact MPN/count/protection/thermal pre-freeze
7. S1R.6 G1 closeout

The PB-07 rebaseline intentionally reopened incompatible heavy-lift values; PB-08 now restores only those values that can be closed safely without inventing vehicle mass or motor data.

## PHASE B — ESC architecture freeze

After G1:
- 3-phase 2-level VSI topology review,
- exact >=100 V semiconductor MPN / parallel count,
- gate driver,
- MCU,
- phase-current sensing,
- bus sensing,
- DC-link/precharge/regen,
- auxiliary rails,
- CAN interface,
- fault architecture,
- thermal path.

Special PB-08 action: re-audit B1 because its historical ~3 kW / ~48 V / 100 V device class is now close to the active platform. Reuse requires recalculation and exact rating checks, not copy/paste.

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

- G0 Mission freeze — OPEN PB-08
- G1 System electrical freeze — OPEN PB-08 partial
- G2 Architecture freeze — blocked by G1
- G3 Schematic review — blocked by G2
- G4 Firmware bench ready — blocked by G2
- G5 Prototype release — blocked by G3/G4
- G6 Propulsion verified — blocked by G5
- G7 Flight-test ready — blocked by G6

## Immediate dependency chain

`PB-08 common 12S/ESC platform -> Quad/Hexa + installed-axis/frame mass -> payload/MTOW -> exact motor/prop + pack implementation -> phase current/eRPM/PWM -> exact MOSFET/driver/sensing/DC-link/protection/thermal -> G1 -> G2 -> U1-SCH-R001`
