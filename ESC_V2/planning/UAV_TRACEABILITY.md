# UAV ESC tasarım izlenebilirlik matrisi

Tarih: 19.09.2026  
Amaç: Faz 2 / Faz 3 dokümanları ile mevcut B1 tasarımını yeni UAV ürün gereksinimine bağlamak.

Durum etiketleri: **KEEP**, **REVALIDATE**, **RECALCULATE**, **REPLACE IF REQUIRED**, **OPEN**.

| ID | Fonksiyon / karar | Faz 2/3 | B1 | UAV rebaseline kararı | Sonraki kanıt |
|---|---|---|---|---|---|
| TR-001 | 3 faz 2-level VSI | Ana topoloji | Aynı | KEEP + REVALIDATE | G1 envelope, loss/SOA |
| TR-002 | BLDC/PMSM | Evet | Uyumlu aday | KEEP | Motor/eRPM |
| TR-003 | FOC + SVPWM | Hedef | Firmware yok | KEEP target | SIL + bench |
| TR-004 | Sensorless | Hedef/opsiyon | Firmware yok | REVALIDATE | startup/observer tests |
| TR-005 | 3 low-side shunt | Seçili | Mevcut | REVALIDATE | phase current + PWM windows |
| TR-006 | DC-bus + U/V/W sensing | Var | Divider + BAT54H rail clamps | Divider concept RECALCULATE; B1 rail-clamp/back-power implementation REPLACE IF REQUIRED. Existing divider ideal FS ~102.5 V, but VBUS-present/control-rails-off can back-power +3V3A/+3V3 through BAT54H and TLV75533 output. | `ADC_CLAMP_INJECTION_CLOSURE.md`, `ANALOG_RAIL_BACKPOWER_AUDIT.md`, final VBUS/transient + sequencing/bench evidence |
| TR-007 | CAN | Var | Var | KEEP | FC protocol/failsafe |
| TR-008 | SPI gate-driver | Var | Var | KEEP | final driver |
| TR-009 | service/debug | UART/JTAG | SWD/UART | KEEP functionally | MCU pin contract |
| TR-010 | Gate driver | DRV8353 | DRV8353FSRTAR | REVALIDATE; shares unresolved 100 V-domain ceiling | VBUS transient, Qg, PWM, OCP |
| TR-011 | MCU | TMS320F280041C | STM32G474RET3 | OPEN trade | timing/trip/FOC benchmark |
| TR-012 | Aux buck | LM5164 | LM5164 | REVALIDATE; 100 V input domain couples it to bus transient requirement | final VBUS transient/load/precharge |
| TR-013 | MOSFET | CSD19536KTT single/switch | 2 parallel/switch candidate | RECALCULATE / REPLACE | `POWER_STAGE_LOSS_MODEL.md`, `CSD19536KTT_REFERENCE_PARAMETERS.md`, VDS/loss/SOA/thermal/sharing |
| TR-014 | MOSFET voltage class | 100 V | 100 V target | OPEN; compare 100/120/150 V only at common verified envelope | `POWER_STAGE_LOSS_MODEL.md` + transient ceiling |
| TR-015 | PWM | 40 kHz | 20 kHz | RECALCULATE | motor L + switching loss |
| TR-016 | continuous phase current | 60 A RMS | 80 A RMS target | OPEN | motor operating points |
| TR-017 | overload/peak phase current | ~80/~100 A | 120 A SW/150 A sense | OPEN | motor operating points + duration |
| TR-018 | power target | 1.5/3 kW | 3 kW candidate | RECALCULATE; commercial quad references ~4.64–4.85 kW rated/axis | `propulsion_benchmark.md`, `esc_envelope_parametric.md` |
| TR-019 | Battery | 12–60 V generic | 13S | OPEN; carry ~50–53 V and 18S/69 V families | `battery_architecture_pretrade.md` |
| TR-020 | Hardware trip | CMPSS/Trip Zone + driver | dedicated trip logic | KEEP principle + REVALIDATE | latency/threshold/reset |
| TR-021 | Motor temp | desired | TEMP_MOTOR | KEEP | sensor/fault policy |
| TR-022 | DC-link | open | 3x470uF 100V bulk + 3x2.2uF 100V local, exact cap MPNs open | RECALCULATE / NOT 18S QUALIFIED | `B1_EXACT_VBUS_BOM_AUDIT.md`, ripple/ESR/life/transient |
| TR-023 | Precharge | open | external assembly required, exact design open | OPEN P0 | input-module electrical contract + `precharge_energy_model.py` with evidenced inputs |
| TR-024 | Regen/BMS disconnect | conceptual | external brake interface, clamp sizing open | OPEN P0 | energy acceptance/OV path |
| TR-025 | Parallel FET sharing | not primary | candidate | OPEN | symmetry/thermal/gate loops |
| TR-026 | Control PCB | concept | partial PoC | REUSE selectively | G2/G3 review |
| TR-027 | Power PCB | concept | incomplete | NEW DESIGN after freeze | power/thermal/mechanical review |
| TR-028 | Firmware | goals | no complete tree | NEW IMPLEMENTATION | build + SIL + bench |
| TR-029 | Production package | intended | incomplete | OPEN | after G5 |
| TR-030 | Physical validation | target | incomplete | REQUIRED | staged G6 |

## Yeni kaynaklı ön-sonuçlar

- XAG P150 Max, 136 kg spraying MTOW sınıfında dört eksenli 4.85 kW rated motor ve 140 A continuous ESC kullanıyor; bu, eski 3 kW B1'in ağır quad için ürün rating'i sayılamayacağını destekliyor.
- Hobbywing X15 G2, 37.5 kg/axis önerilen yükte 18S/69 V, 4.64 kW rated input, 120 A continuous ve 300 A/3 s ESC ile doğrudan ağır-zirai propulsion referansı sağlıyor.
- 18S tam şarj 75.6 V olduğundan 100 V MOSFET sınıfı transient kanıtı olmadan dondurulamaz.
- B1 exact BOM audit: ana DC-link bankı ve local inverter ceramics nominal 100 V ve exact capacitor MPN'leri açık; 160 V etiketli parçalar yalnız LM5164 girişindeki yerel kapasitörlerdir. Bu nedenle 'B1 has 160 V capacitors' ifadesi 18S power-stage qualification kanıtı değildir.
- B1 DC input protection ve regen clamp/chopper işlevleri harici modül/interface olarak bırakılmıştır; final transient ceiling bu modüller tanımlanmadan kapanmaz.
- Aynı güçte 69 V bus, 52.5 V bus'a göre ideal DC akımı yaklaşık %24 azaltır; iletken I²R kaybı ilk mertebede yaklaşık %42 azalır. Bu yalnız bus-level trade'dir.
- B1 voltage-sense upper BAT54H doğrudan +3V3A rayına clamp eder. +3V3A, 0R ile +3V3'e; +3V3 ise TLV75533 çıkışına bağlıdır. TI TLV755P reverse-current guidance, output input yokken biaslandığında ters akım/reliability riski tanımlar. Bu nedenle mevcut rail-clamp çözümü UAV için power-sequencing kanıtı olmadan korunamaz.
- `G1_REQUIREMENTS_MATRIX.json` artık G0/G1A/G1B/G1C/G1 kapanışındaki açık alanları makine-okunabilir biçimde takip eder; açık alanlar competitor değerleriyle otomatik doldurulmaz.

## Korunacak çekirdek

Üç faz VSI, PWM-senkron akım ölçümü, FOC/SVPWM hedefi, CAN, hızlı donanımsal kapatma, sıcaklık/gerilim telemetrisi, modüler kontrol/güç kartı ve otomatik ERC/netlist/interface kontrolleri korunur.

## Yeniden hesaplanacak çekirdek

UAV-001…006 kapanmadan 13S, 3 kW, 60/80/100/120/150 A, 20/40 kHz, 100 V semiconductor class, FET sayısı, shunt/gain, DC-link, connector/fuse/cable ve thermal budget taşınmaz.

## Çelişki çözme sırası

1. güncel UAV requirement,
2. doğrulanmış motor/prop operating point,
3. electrical/thermal calculation,
4. datasheet/source evidence,
5. prototype measurement.

Eski doküman geçmiş tasarım gerekçesidir; otomatik design authority değildir.
