# UAV ESC tasarım izlenebilirlik matrisi

Tarih: 19.09.2026  
Amaç: Faz 2 / Faz 3 dokümanları ile mevcut B1 tasarımını yeni UAV ürün gereksinimine bağlamak.

Durum etiketleri:
- **KEEP** — prensip doğrudan korunabilir.
- **REVALIDATE** — mimari aday olarak korunur fakat gerçek UAV zarfında yeniden kanıt gerekir.
- **RECALCULATE** — aynı fonksiyon korunur fakat sayısal değerler yeniden hesaplanır.
- **REPLACE IF REQUIRED** — propulsion/system sonucu mevcut çözümü yetersiz bırakırsa değişir.
- **OPEN** — henüz ürün kararı yok.

| ID | Fonksiyon / karar | Faz 2/3 | B1 | UAV rebaseline kararı | Sonraki kanıt |
|---|---|---|---|---|---|
| TR-001 | 3 faz 2-level VSI | Ana topoloji | Aynı temel topoloji | KEEP + REVALIDATE | G1 electrical envelope, loss/SOA |
| TR-002 | BLDC/PMSM desteği | Evet | Aday mimari uyumlu | KEEP | Motor adayları / eRPM |
| TR-003 | FOC + SVPWM | Ana hedef | Firmware yok | KEEP as target | SIL + motor bench |
| TR-004 | Sensorless | Ana hedef, sensör geliştirme opsiyonu | Firmware yok | REVALIDATE | Motor saliency/BEMF, startup tests |
| TR-005 | 3 low-side shunt | Seçili | Mevcut | REVALIDATE | PWM windows, common-mode, current range |
| TR-006 | DC-bus + U/V/W ölçümü | 4 kanal | Mevcut | KEEP + RECALCULATE | Final VBUS max, ADC input model |
| TR-007 | CAN | Ana dış haberleşme | Mevcut | KEEP | UAV FC protocol/failsafe |
| TR-008 | SPI gate-driver | Evet | Evet | KEEP | Driver final selection |
| TR-009 | UART/JTAG/SWD service | Var | Var / farklı MCU debug yapısı | KEEP functionally | Final MCU pin contract |
| TR-010 | Gate driver | DRV8353 | DRV8353FSRTAR | REVALIDATE | Final VBUS, FET Qg, PWM, OCP architecture |
| TR-011 | MCU | TMS320F280041C seçilmiş | STM32G474RET3 | OPEN trade study | ADC/PWM/trip/FOC timing benchmark |
| TR-012 | Aux buck | LM5164 | LM5164 | REVALIDATE | Final VBUS transient + load budget + precharge behavior |
| TR-013 | MOSFET | CSD19536KTT, one/switch prototype | parallel FET candidate | RECALCULATE / REPLACE IF REQUIRED | VDS margin, loss, SOA, thermal, current sharing |
| TR-014 | MOSFET voltage class | 100 V | 100 V target | OPEN | Final battery max + switching overshoot |
| TR-015 | PWM frequency | 40 kHz | 20 kHz | RECALCULATE | loss/ripple/acoustic/control-loop trade |
| TR-016 | Continuous phase current | 60 A RMS | 80 A RMS target | OPEN | propulsion operating points |
| TR-017 | Overload / peak current | ~80 A short / ~100 A peak | 120 A SW / 150 A sense target | OPEN | thrust transient + motor/ESC thermal limits |
| TR-018 | Power target | 1.5 kW cont / 3 kW short reference | 3 kW shaft candidate | OPEN | motor/prop hover and max-thrust power |
| TR-019 | Battery | 12–60 V generic | 13S candidate | OPEN | battery architecture study |
| TR-020 | Hardware trip | CMPSS/Trip Zone + driver fault | dedicated fault/trip logic | KEEP principle + REVALIDATE implementation | latency + threshold + reset policy |
| TR-021 | Motor temperature | Desired telemetry/protection | TEMP_MOTOR added | KEEP | Sensor type / range / fault handling |
| TR-022 | DC-link | Required but not fully closed | candidate bank | RECALCULATE | ripple RMS, ESR, life, transient |
| TR-023 | Precharge | Not product-closed | B1 open issue | OPEN P0 | Aux-load behavior, timeout, resistor pulse |
| TR-024 | Regen / BMS disconnect | Mentioned conceptually | initial regen disabled; open energy path | OPEN P0 | System energy acceptance and OV path |
| TR-025 | Parallel FET current sharing | Not primary Faz 2/3 architecture | B1 candidate | OPEN | layout symmetry, thermal sharing, gate loops |
| TR-026 | Control PCB | Concept | partial PoC | REUSE selectively | G2/G3 then placement/routing review |
| TR-027 | Power PCB | Concept | Not complete | NEW DESIGN after freeze | power loop / thermal / mechanical review |
| TR-028 | Firmware | Control goals | No completed source tree | NEW IMPLEMENTATION | Build + SIL + HIL/bench evidence |
| TR-029 | Production package | Intended | Not complete | OPEN | Gerber/BOM/PnP/DFM after G5 |
| TR-030 | Physical validation | Prototype/test target | Not completed | REQUIRED | staged G6 propulsion validation |

## Tasarımın korunacak çekirdeği

Şimdilik aşağıdaki mimari kararlar iyi başlangıç noktalarıdır ve ürün hedefiyle çelişmez:
- üç fazlı VSI,
- PWM senkron akım ölçümü,
- FOC/SVPWM hedefi,
- CAN tabanlı üst seviye haberleşme,
- donanımsal hızlı kapatma katmanı,
- sıcaklık ve gerilim telemetrisi,
- modüler kontrol/güç kartı yaklaşımı,
- otomatik ERC/netlist/interface kontrolleri.

## Tasarımın yeniden hesaplanacak çekirdeği

UAV-01…UAV-05 tamamlanmadan şu değerler taşınmaz:
- 12–60 V / 13S,
- 1.5/3 kW,
- 60/80/100/120/150 A akım seviyeleri,
- 20/40 kHz PWM,
- 100 V semiconductor class,
- CSD19536KTT,
- iki paralel FET/switch,
- shunt değeri ve CSA gain,
- DC-link kapasitesi,
- connector/fuse/cable ratings,
- heatsink/baseplate loss budget.

## Çelişki çözme kuralı

Bir Faz 2/3 kararı ile B1 kararı çelişirse hiçbirisi otomatik olarak üstün değildir. Karar sırası:

1. güncel UAV system requirement,
2. doğrulanmış motor/prop çalışma noktası,
3. electrical/thermal calculation,
4. component datasheet/source evidence,
5. prototype measurement.

Eski doküman yalnız geçmiş tasarım gerekçesi olarak kullanılır.
