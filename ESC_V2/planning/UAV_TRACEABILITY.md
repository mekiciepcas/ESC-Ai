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
| TR-006 | DC-bus + U/V/W sensing | Var | Divider + BAT54H rail clamps | Divider concept RECALCULATE; B1 rail-clamp/back-power implementation REPLACE IF REQUIRED. Existing divider ideal FS ~102.5 V, but VBUS-present/control-rails-off can back-power +3V3A/+3V3 through BAT54H and TLV75533 output. LT6015/LT6016/LT6017 provide exact primary-source evidence for a power-off-high-impedance input study path. Output sequencing is explicit: LT6017-on / STM32-VDDA-off is prohibited as a normal study state unless separately proven; preferred study rule is shared analog shutdown domain plus a series path sized from ADC settling/fault-current constraints. | `ADC_CLAMP_INJECTION_CLOSURE.md`, `ANALOG_RAIL_BACKPOWER_AUDIT.md`, `NON_BACKPOWER_HV_SENSE_ARCHITECTURES.md`, `POWER_OFF_TOLERANT_SENSE_CANDIDATES.md`, `HV_SENSE_OUTPUT_SEQUENCING.md`, `hv_sense_dynamic_model.py`, final VBUS/transient + sequencing/bench evidence |
| TR-007 | CAN | Var | Var | KEEP | FC protocol/failsafe |
| TR-008 | SPI gate-driver | Var | Var | KEEP if selected architecture still uses serial smart driver; otherwise interface changes with driver topology | final driver/control architecture |
| TR-009 | service/debug | UART/JTAG | SWD/UART | KEEP functionally | MCU pin contract |
| TR-010 | Gate driver | DRV8353 | DRV8353FSRTAR | REVALIDATE; shares unresolved ~100 V-domain ceiling. Primary-source alternatives now exist if G1 disqualifies this domain: UCC27712 non-isolated high-voltage half-bridge anchor and UCC21540-Q1 isolated dual-channel anchor. UCC27282 is only a 120 V bootstrap headline reference because TI still specifies a 100 V HS operating ceiling. No driver selected. | `GATE_DRIVER_AUX_SUPPLY_VOLTAGE_DOMAIN_TRADE.md`, final VBUS transient, MOSFET Qg, PWM/dead-time, fault coverage |
| TR-011 | MCU | TMS320F280041C | STM32G474RET3 | OPEN trade | timing/trip/FOC benchmark |
| TR-012 | Aux buck | LM5164 | LM5164 | REVALIDATE; legacy input domain couples it to final transient ceiling. Source-backed alternatives now exist: LTC3639 (4–150 V, 100 mA housekeeping class) and LTC7801 (4–140 V operating, 150 V abs-max synchronous buck controller) for higher-voltage architectures. No auxiliary topology selected. | `GATE_DRIVER_AUX_SUPPLY_VOLTAGE_DOMAIN_TRADE.md`, final VBUS transient + control/gate/fan load budget |
| TR-013 | MOSFET | CSD19536KTT single/switch | 2 parallel/switch candidate | RECALCULATE / REPLACE | `POWER_STAGE_LOSS_MODEL.md`, `CSD19536KTT_REFERENCE_PARAMETERS.md`, `SEMICONDUCTOR_VOLTAGE_CLASS_CANDIDATES.md`, `power_stage_loss_calculator.py`, VDS/loss/SOA/thermal/sharing |
| TR-014 | MOSFET voltage class | 100 V | 100 V target | OPEN; primary-source trade anchors now exist for 100/120/150 V and include Qgd/Coss/Qrr/RthJC evidence. A mandatory-input normalized screening calculator exists, but class remains blocked by G1 transient/current/PWM/hot-temperature envelope. | `SEMICONDUCTOR_VOLTAGE_CLASS_CANDIDATES.md`, `POWER_STAGE_LOSS_MODEL.md`, `power_stage_loss_calculator.py` + transient ceiling |
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
| TR-031 | G0 trade bounds | none | none | 125/150/175 kg cases allowed only as `ASSUMPTION_FOR_TRADE_ONLY`; never baseline requirements | `G0_TRADE_BOUNDING_CASES.md`, actual G0 vehicle inputs |
| TR-032 | Rotor count | not frozen | not applicable | OPEN; quad conditionally excluded if G0 later requires continued hover after one motor/ESC loss; hex/octo retained | `rotor_trade_study.md`, G0 failure policy + MTOW |
| TR-033 | U1 preliminary BOM evidence map | none | B1 BOM exists | `U1_BOM_CANDIDATES.json` now records legacy references, exact source-backed candidates and G1-blocked/open functions without claiming production release. | G1/G2 closure -> U1 schematic -> `hardware_u1/bom_release.json` |

## Yeni kaynaklı ön-sonuçlar

- XAG P150 official specs provide a current lower heavy-agriculture anchor: 54 kg aircraft weight with spray system and batteries, 70 kg max payload, 125 kg max spraying MTOW, quad, 55 kgf max single-motor thrust, 4.7 kW rated motor power and 120 A continuous ESC.
- XAG P150 Max, 136 kg spraying MTOW sınıfında dört eksenli 4.85 kW rated motor ve 140 A continuous ESC kullanıyor; bu, eski 3 kW B1'in ağır quad için ürün rating'i sayılamayacağını destekliyor.
- DJI T100 official specs provide a 100 kg spraying-payload / 175 kg spraying-MTOW upper benchmark with 60 rpm/V motors and 62-inch propellers. DJI also publishes a Turkey-specific 149.9 kg MTOW operating note for T100; this is recorded as benchmark/regulatory context and is not copied into our product baseline.
- `G0_TRADE_BOUNDING_CASES.md` now governs 125/150/175 kg numerical cases. They are analysis-only and cannot close G0/G1.
- Rotor screening now has an explicit architecture discriminator: if continued hover after complete loss of one motor/ESC becomes a G0 requirement, ordinary quad is eliminated before detailed ESC sizing; otherwise quad remains a candidate.
- Hobbywing X15 G2, 37.5 kg/axis önerilen yükte 18S/69 V, 4.64 kW rated input, 120 A continuous ve 300 A/3 s ESC ile doğrudan ağır-zirai propulsion referansı sağlıyor.
- 18S tam şarj 75.6 V olduğundan 100 V MOSFET sınıfı transient kanıtı olmadan dondurulamaz.
- 100/120/150 V için güncel primary-source MOSFET trade anchors kaydedildi: TI CSD19536KTT 100 V legacy reference; Infineon IPT017N12NM6 120 V; Infineon IAUTN15S6N025 150 V. Dinamik tablo Qgd/Coss/Qrr/RthJC verisini ve farklı test koşullarının normalize edilmesi gerektiğini kaydediyor. `power_stage_loss_calculator.py` bütün çalışma noktası girdilerini zorunlu tutuyor; böylece açık G1 değerleri gizli defaultlarla doldurulmuyor.
- Gate-driver voltage-domain trade artık gerçek alternatifler içeriyor: UCC27282 120 V bootstrap sınıfında olsa da TI HS normal çalışma tavanı 100 V olduğu için >100 V switch-node çözümü sayılmıyor; UCC27712 620 V non-isolated half-bridge ve UCC21540-Q1 reinforced-isolated driver daha yüksek domain alternatifleri olarak kaydedildi. Bu parçalar adaydır, seçim değildir.
- Auxiliary-power trade artık LM5164 dışında iki yüksek-domain anchor içeriyor: LTC3639 4–150 V / 100 mA housekeeping sınıfı ve LTC7801 4–140 V operating / 150 V abs-max controller. Final seçim için toplam gate-drive/control/fan load budget gerekir.
- `U1_BOM_CANDIDATES.json` bu driver/aux alternatiflerini de `CANDIDATE` olarak izliyor; null/Open güç konnektörü, DC-link, precharge, fuse ve clamp satırları olduğu gibi açık kalıyor.
- B1 exact BOM audit: ana DC-link bankı ve local inverter ceramics nominal 100 V ve exact capacitor MPN'leri açık; 160 V etiketli parçalar yalnız LM5164 girişindeki yerel kapasitörlerdir.
- B1 DC input protection ve regen clamp/chopper işlevleri harici modül/interface olarak bırakılmıştır; final transient ceiling bu modüller tanımlanmadan kapanmaz.
- B1 voltage-sense upper BAT54H doğrudan +3V3A rayına clamp eder. +3V3A, 0R ile +3V3'e; +3V3 ise TLV75533 çıkışına bağlıdır. TI TLV755P reverse-current guidance, output input yokken biaslandığında ters akım/reliability riski tanımlar. Bu nedenle mevcut rail-clamp çözümü UAV için power-sequencing kanıtı olmadan korunamaz.
- LT6015/LT6016/LT6017 ailesi için ADI datasheet ve design-note kanıtı, `VS=0` iken canlı girişlerin yüksek empedanslı kalabildiğini ve 0–76 V common-mode giriş davranışının karakterize edildiğini gösteriyor. ST pin tablosu B1 `V_BUS_ADC` bağlantısının STM32G474 LQFP64 pin 8 / PA0 / TT_a olduğunu doğruluyor. `HV_SENSE_OUTPUT_SEQUENCING.md` powered-buffer/unpowered-MCU durumunu normal çalışma için yasaklıyor; shared analog shutdown domain çalışma kuralı ve S1–S4 doğrulama matrisi oluşturuldu.
- `hv_sense_dynamic_model.py` divider RC, op-amp first-order/slew settling ve STM32 ADC acquisition RC etkisini yalnız caller-supplied parametrelerle hesaplıyor; sonuçları SCREENING_ONLY olarak etiketliyor.
- ADA4177 rail-pumping davranışını önleyen OVP açısından güçlü bir robustness referansı, fakat mevcut tek 3.3 V analog domainine drop-in değildir. TI OPAx206 ise OVP akımını supply railine yönlendirdiği için mevcut non-backpower hedefi açısından varsayılan aday olmaktan çıkarılmıştır.
- `G1_REQUIREMENTS_MATRIX.json` G0/G1A/G1B/G1C/G1 kapanışındaki açık alanları makine-okunabilir biçimde takip eder; açık alanlar competitor değerleriyle otomatik doldurulmaz.

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
