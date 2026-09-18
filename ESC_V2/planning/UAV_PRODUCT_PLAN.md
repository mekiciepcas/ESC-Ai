# UAV ESC ürün geliştirme planı

Tarih: 19.09.2026  
Branch: `uav-rebaseline`  
Hedef: 70–100 kg faydalı yük sınıfındaki ağır kaldırma / zirai çok rotorlu UAV için gerçeklenebilir, test edilebilir ve üretime taşınabilir ESC platformu.

> Bu planın amacı hızlıca bir PCB çıkarmak değil; gereksinimden fiziksel doğrulamaya kadar kanıt zinciri kurmaktır. Mevcut A2/B1 çalışmaları korunur ancak yeniden yeterlilik kazanmadan ürün baseline sayılmaz.

## 0. Temel çalışma kuralı

Her kritik karar aşağıdaki zincire bağlı olmalıdır:

`UAV mission -> propulsion operating point -> ESC electrical requirement -> circuit calculation -> component/PCB/firmware decision -> verification evidence`

Aşağıdaki değerler propulsion sizing tamamlanmadan ürün gereksinimi değildir:
- 13S,
- 3 kW,
- 60 A / 80 A / 120 A,
- 20 kHz / 40 kHz,
- 100 V MOSFET,
- iki paralel MOSFET/switch,
- DRV8353,
- STM32G474 veya TMS320F280041C,
- LM5164.

Bunlar yalnız candidate/reference kararlardır.

---

# PHASE A — Sistem ve propulsion tanımı

## A1 — Mission / mass envelope

Girdiler:
- payload min/nom/max,
- airframe tahmini kütlesi,
- batarya kütlesi,
- sıvı/tank/pompa gibi görev ekipmanı,
- hedef uçuş süresi,
- hover oranı,
- kalkış / tırmanma / seyir / iniş profili,
- hedef sıcaklık, rakım ve rüzgâr,
- tek motor/ESC arızasında istenen davranış.

Çıktılar:
- MTOW min/nom/max,
- görev enerji bütçesi,
- çevresel tasarım zarfı.

Kabul kapısı **G0**:
- MTOW ve görev profili sayısal olarak tanımlı,
- 70–100 kg ifadesinin payload olduğu doğrulanmış,
- kritik belirsizlikler açık risk olarak kayıtlı.

## A2 — Rotor mimarisi ve thrust sizing

En az quad / hex / octo ve gerekirse coaxial seçenekler karşılaştırılır.

Hesaplanacak:
- total hover thrust,
- hover thrust / rotor,
- max thrust / rotor,
- thrust-to-weight margin,
- disk loading,
- degraded-mode thrust ihtiyacı,
- rotor çapı / mekanik envelope.

Kabul kapısı **G1A**:
- rotor sayısı ve thrust margin seçilmiş,
- motor başına gerekli hover ve peak thrust belli.

## A3 — Gerçek motor + pervane benchmark

En az iki üretici propulsion seti için doğrulanmış kaynak verisi toplanır:
- thrust vs RPM,
- thrust vs electrical power,
- motor KV,
- prop diameter/pitch,
- nominal/max bus voltage,
- continuous/peak current,
- motor temperature limit,
- motor electrical parameters veya ölçüm planı,
- önerilen ESC rating.

Kabul kapısı **G1B**:
- en az iki aday motor/prop seti,
- hover ve max-thrust çalışma noktaları,
- kaynak linki / datasheet / test data evidence.

## A4 — Battery architecture

Propulsion setinden geriye doğru boyutlandırılır:
- series cell count,
- nominal/min/max bus,
- pack continuous/peak current,
- usable energy,
- voltage sag,
- BMS/contactors/fuse,
- regen/energy acceptance,
- cable/connector current.

Kabul kapısı **G1C**:
- battery voltage architecture ve pack current envelope dondurulmuş.

## A5 — ESC electrical envelope

Her motor/ESC için tanımlanır:
- VBUS min/nom/max/transient,
- electrical input power continuous/peak,
- DC current continuous/peak,
- phase RMS current continuous/overload,
- phase peak current,
- overload duration,
- electrical RPM,
- current ripple target,
- PWM frequency candidate range,
- current sense range,
- ambient/baseplate limits.

Kabul kapısı **G1 — SYSTEM FREEZE**:
- `design_basis.json` içinde hiçbir kritik electrical envelope alanı `null` değil,
- değerler propulsion çalışma noktalarına izlenebilir.

---

# PHASE B — ESC mimari yeterlilik

## B1 — Topology review

Başlangıç adayı: 3-phase 2-level VSI.

Doğrulanacak:
- MOSFET vs alternatif semiconductor technology,
- VDS derating ve transient margin,
- single vs parallel FET/switch,
- switching frequency trade-off,
- dead-time,
- reverse conduction / regen,
- gate drive current,
- SOA ve short-circuit response.

Çıktı:
- semiconductor trade study,
- conduction + switching loss model,
- nominal / hot / worst-case kayıplar.

## B2 — Sensing and protection architecture

Doğrulanacak:
- 3-shunt yaklaşımı,
- shunt value / power / TCR / Kelvin,
- CSA gain / offset / bandwidth,
- bus and phase voltage sensing,
- motor/MOSFET/baseplate temperature,
- hardware OCP,
- desat/VDS protection if applicable,
- PWM inhibit,
- fault latch,
- watchdog,
- over/under-voltage,
- BMS disconnect response.

## B3 — DC-link and input energy management

Hesaplanacak:
- DC-link capacitance,
- RMS ripple current,
- ESR loss,
- life/temperature,
- wiring/bus inductance,
- overshoot,
- precharge requirement,
- fuse/contactor coordination,
- regenerative overvoltage path.

## B4 — Control MCU / gate driver / auxiliary power

Adaylar sıfırdan değil, mevcut Faz 2/3 + B1 havuzundan değerlendirilir:
- STM32G474,
- TMS320F280041C,
- DRV8353 family,
- LM5164 family.

Karar kriterleri:
- ADC/PWM synchronization,
- hardware trip latency,
- FOC execution margin,
- CAN/CAN-FD,
- firmware ecosystem,
- supply voltage compatibility,
- fault coverage,
- availability,
- thermal and layout constraints.

Kabul kapısı **G2 — ARCHITECTURE FREEZE**:
- topology,
- semiconductor class/count,
- gate driver,
- MCU,
- sensing architecture,
- auxiliary rails,
- communication interfaces,
- fault architecture
seçilmiş ve hesaplarla savunulabilir.

---

# PHASE C — Ayrıntılı elektrik tasarımı

## C1 — Schematic revision B2/U1

Mevcut B1 sayfaları tek tek sınıflandırılır:
- `KEEP`: electrical requirement değişmiyor,
- `RECALCULATE`: topology korunuyor, değerler değişiyor,
- `REPLACE`: mimari değişiyor,
- `DELETE`: artık gereksiz.

Her kritik sayfada tasarım notu bulunur:
- requirement ID,
- calculation/evidence,
- selected MPN,
- max ratings / derating,
- test method.

## C2 — BOM closure

Her populated component için:
- exact manufacturer part number,
- active lifecycle,
- datasheet link/evidence,
- exact footprint,
- voltage/current/power/temp rating,
- tolerance/TCR where relevant,
- alternates,
- DNP status.

## C3 — ERC / interface / review

Kabul kapısı **G3 — SCHEMATIC DESIGN REVIEW**:
- ERC clean veya gerekçeli waiver,
- interface audit clean,
- BOM critical-open = 0,
- loss/thermal calculations linked,
- precharge/OV/OCP/fault issues closed,
- no critical TBD in schematic.

---

# PHASE D — Firmware

## D1 — Repository structure

`firmware/` altında gerçek buildable source tree oluşturulur.

Minimum modüller:
- board support / clock,
- PWM,
- ADC/DMA,
- current calibration,
- gate-driver SPI,
- CAN,
- temperature,
- fault manager,
- state machine,
- motor control,
- telemetry/logging,
- unit/SIL tests.

## D2 — Bring-up firmware

Sıra:
1. PWM permanently inhibited at boot,
2. rail/ADC validation,
3. fault input validation,
4. gate-driver configuration,
5. low-voltage open-loop commutation,
6. current sensing validation,
7. closed-loop current control,
8. rotor position / observer validation,
9. FOC/SVPWM,
10. communication/failsafe.

## D3 — Flight-oriented fault policy

Tanımlanacak:
- communication timeout,
- overcurrent,
- overvoltage,
- undervoltage,
- overtemperature,
- sensor invalid,
- gate-driver fault,
- stalled rotor,
- restart policy,
- latched vs recoverable faults.

Kabul kapısı **G4 — FIRMWARE BENCH READY**:
- reproducible build,
- hardware-independent tests,
- fault state machine tests,
- timing budget,
- PWM/ADC synchronization evidence.

---

# PHASE E — PCB / mechanics / thermal

## E1 — Control PCB

Mevcut B1 control PoC yeniden değerlendirilir. Final routing ancak G2/G3 sonrası.

## E2 — Power PCB / bus structure

Kritik konular:
- DC-link loop area,
- half-bridge loop,
- gate loop,
- Kelvin source,
- parallel current sharing,
- shunt Kelvin,
- creepage/clearance,
- copper/busbar current density,
- thermal spreading,
- heatsink/baseplate interface,
- connector mechanical stress.

## E3 — Manufacturability

Çıktılar:
- zero unrouted,
- DRC report,
- Gerber,
- drill,
- IPC-356/netlist where useful,
- pick-and-place,
- BOM,
- assembly drawings,
- stack-up and fab notes.

Kabul kapısı **G5 — PROTOTYPE RELEASE**:
- schematic/PCB cross-check complete,
- critical layout review complete,
- manufacturer DFM review complete,
- no unresolved P0/P1 release issue.

---

# PHASE F — Physical validation

## F1 — Unpowered / low-energy bring-up

1. continuity / short checks,
2. insulation where applicable,
3. current-limited auxiliary power,
4. rail/clock/reset,
5. fault-chain verification,
6. PWM inhibit verification.

## F2 — Switching validation

- low VBUS,
- no propeller,
- guarded motor where required,
- gate VGS,
- switch node,
- dead-time,
- overshoot/ringing,
- current sense timing,
- hardware trip latency.

## F3 — Motor dynamometer / prop stand

- no-load motor,
- stepped load,
- hover operating point,
- continuous thermal soak,
- peak power duration,
- efficiency map,
- phase/DC current correlation,
- motor/ESC thermal limits.

Propeller testing must use a physically guarded and rated propulsion stand; initial electronics bring-up is performed without propellers.

## F4 — Fault injection

- communication loss,
- sensor invalid,
- overcurrent,
- undervoltage,
- overvoltage,
- thermal limit,
- BMS/contact disconnect scenario,
- controlled emergency shutdown.

Kabul kapısı **G6 — PROPULSION VERIFIED**:
- target operating points demonstrated on test stand,
- continuous and peak limits verified,
- thermal equilibrium acceptable,
- protection response recorded.

---

# PHASE G — UAV integration

## G1 — Vehicle integration

- flight controller command interface,
- CAN/telemetry,
- arming/disarming,
- power-up sequencing,
- EMI coexistence,
- harness/fuse architecture,
- cooling airflow,
- motor/ESC pairing.

## G2 — Flight-test readiness review

Flight testing is not used to discover basic power-stage faults. Before flight:
- G0–G6 closed,
- propulsion test evidence complete,
- safe arming/failsafe demonstrated,
- hardware/firmware revision frozen,
- test vehicle and operational risk plan approved by responsible humans.

Kabul kapısı **G7 — FLIGHT TEST READY**.

---

# Release sınıfları

- **R0 — Analysis only:** calculations / simulations.
- **R1 — Bench prototype:** low-energy electronics validation.
- **R2 — Power prototype:** guarded motor/dyno/prop stand.
- **R3 — UAV integration prototype:** vehicle integration, not production release.
- **R4 — Verified engineering prototype:** defined test envelope passed.
- **R5 — Production candidate:** BOM/PCB/firmware/configuration controlled and manufacturing validation complete.

`flight-qualified` veya `production-qualified` ifadeleri ilgili kanıt kapıları tamamlanmadan kullanılmaz.
