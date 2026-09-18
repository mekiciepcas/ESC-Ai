# UAV ESC yeniden bazlandırma — design authority

Tarih: 19.09.2026  
Durum: **P0 / aktif**  
Hedef: 70–100 kg faydalı yük hedefli ağır kaldırma / zirai çok rotorlu UAV için ESC sistemi.

## Neden yeniden bazlandırma yapılıyor?

Önceki B1 çalışma zarfı 3 kW, 13S ve Golden Motor HPM3000B varsayımlarını sabitlemiş; ayrıca uygulamayı tezgâh/genel kara tahriki olarak tanımlamıştır. Bu, gerçek UAV ürün hedefiyle uyumlu değildir. B1'deki devre, doğrulama ve PCB çalışmaları korunur ancak UAV sistem gereksinimi üzerinden yeniden yeterlilik kazanmadıkça ürün baseline sayılmaz.

## Tasarım otoritesi

1. `design_basis.json` — aktif sistem gereksinimleri ve freeze kapıları.
2. Bu dosya — yeniden bazlandırma sırası ve karar kuralları.
3. A2/B1 dosyaları — tarihsel referans / candidate design.
4. Eski roadmap, dashboard ve 3 kW çalışma zarfı — UAV rebaseline tamamlanana kadar tarihsel ilerleme kaydıdır; ürün gereksinimi değildir.

## P0 — önce çözülmesi gereken sistem soruları

### UAV-01 — Kütle ve görev zarfı

Kesinleştirilecekler:
- 70–100 kg ifadesinin payload olduğu kabulü,
- boş araç kütlesi,
- batarya kütlesi,
- maksimum kalkış kütlesi (MTOW),
- hover süresi ve görev süresi,
- hedef ortam sıcaklığı/rakım/rüzgâr,
- motor kaybında veya degraded-mode durumda beklenen davranış.

Çıkış: min/nominal/max MTOW ve görev profili.

### UAV-02 — Rotor mimarisi ve thrust margin

Karşılaştırılacak mimariler en az quad/hex/octo veya uygun coaxial varyantlardır. Rotor sayısı yalnız motor sayısını azaltmak için seçilmez; tek motor/ESC arızası, disk loading, mekanik çap, verim ve maliyet birlikte değerlendirilir.

Çıkış:
- rotor sayısı,
- hover thrust / rotor,
- max thrust / rotor,
- thrust-to-weight hedefi,
- gerekli kontrol marjı.

### UAV-03 — Motor + pervane

Piyasadaki ağır yük / zirai UAV propulsion sistemlerinden güncel üretici verisi toplanacak. Seçim için en az:
- thrust–RPM–power eğrisi,
- prop çap/pitch,
- motor KV,
- nominal/max gerilim,
- continuous/peak current,
- motor sıcaklık limiti,
- motor R/L ve pole-pair verisi veya ölçüm planı,
- ESC önerilen rating
karşılaştırılacak.

Çıkış: en az iki gerçek aday propulsion seti ve doğrulanmış çalışma noktaları.

### UAV-04 — Batarya mimarisi

Motor/prop çalışma noktalarından sonra seri hücre sayısı ve pack mimarisi seçilecek. 13S varsayımı korunmak zorunda değildir. Daha yüksek bus gerilimi; kablo/ESC akımı, semiconductor gerilim stresi, izolasyon, güvenlik ve batarya kullanılabilirliği ile birlikte değerlendirilecek.

Çıkış: min/nom/max DC bus, pack continuous/peak current, BMS davranışı ve regen/OV senaryosu.

### UAV-05 — ESC elektriksel zarfı

Her ESC için ayrı tanımlanacak:
- continuous mechanical/electrical power,
- peak power ve izin verilen süre,
- battery/DC current,
- phase RMS / phase peak current,
- electrical RPM,
- PWM frekansı,
- motor inductance kaynaklı ripple,
- current-sense range,
- bus transient/regen voltage,
- ambient/baseplate limitleri.

Bundan önce 3 kW, 80 A RMS, 120 A peak veya 100 V MOSFET sınıfı ürün gereksinimi değildir.

## P1 — ESC mimarisini tekrar yeterlendir

### UAV-06 — Power stage

Mevcut iki paralel MOSFET/switch yaklaşımı; gerçek UAV zarfında conduction, switching, diode/reverse-recovery, gate drive, current sharing, SOA ve transient açısından tekrar hesaplanacak. Si MOSFET, GaN veya başka aday teknoloji yalnız sistem gerilim/güç zarfı çıktıktan sonra kıyaslanacak.

### UAV-07 — DC-link / koruma / sensing / termal

- DC-link ripple/ESR/ömür,
- input connector/cable/fuse,
- precharge ihtiyacı ve mimarisi,
- BMS disconnect / regen overvoltage,
- phase current sensing,
- bus/phase voltage sensing,
- hardware overcurrent trip,
- gate fault chain,
- MOSFET/baseplate/motor temperature sensing,
- thermal path ve airflow
birlikte kapanacak.

### UAV-08 — Kontrol ve firmware

Gerçek firmware repo ağacı oluşturulacak. Asgari kapsam:
- clock/pin initialization,
- synchronized PWM + ADC,
- current offset calibration,
- commutation/FOC strategy,
- startup,
- current/voltage/temperature limits,
- hardware trip integration,
- watchdog,
- communications timeout,
- fault latch/restart policy,
- logging/telemetry,
- bench test modes.

## P2 — PCB / üretim

### UAV-09 — PCB

Mevcut kontrol PoC yerleşimi yeniden kullanılabilir; fakat sistem zarfı kapanmadan nihai routing yapılmaz. Güç kartında gate loop, Kelvin source, shunt sense, DC-link loop, phase paths, bus bars/planes, thermal spreading, connector stress ve creepage/clearance birlikte doğrulanır.

Çıkış: sıfır unrouted, gerekçeli sıfır kritik DRC, tam BOM, üretici doğrulanmış footprints, Gerber/drill/PnP/assembly çıktıları.

## P3 — doğrulama

### UAV-10 — Kademeli test

Sıra:
1. enerjisiz continuity/short/insulation,
2. current-limited auxiliary power,
3. MCU/reset/fault/PWM inhibit,
4. gate-driver test ve düşük VBUS double-pulse / switching gözlemi,
5. yüksüz motor,
6. düşük yük,
7. kademeli motor/prop test standı,
8. continuous thermal soak,
9. peak transient,
10. BMS disconnect / overvoltage/fault cases.

Uçuş denemesi, masa üstü ve propulsion standı kabul kriterleri geçilmeden doğrulama aracı olarak kullanılmaz.

## Mevcut B1'den korunacak değer

- STM32G474 tabanlı kontrol mimarisi aday olarak güçlü kalabilir.
- DRV8353 mimarisi adaydır; bus/power envelope sonrasında tekrar kontrol edilir.
- Donanımsal PWM inhibit/fault latch yaklaşımı korunmaya değerdir.
- CAN, Hall, sıcaklık ve test point ayrımı faydalıdır.
- ERC/netlist/interface audit betikleri korunur.
- LM5164 RON düzeltmesi ve diğer kanıtlı bağlantı düzeltmeleri kaybedilmez.

## Şu anda durdurulan işler

Aşağıdaki çalışmalar UAV-01…UAV-05 kapanana kadar nihai ürün işi sayılmaz:
- güç PCB routing,
- final control PCB routing,
- production BOM freeze,
- 13S'e özel konektör/şönt/DC-link freeze,
- 100 V MOSFET sınıfını nihai seçim kabul etme,
- Gerber release.

Araştırma, hesap, simülasyon, candidate schematic review ve test otomasyonu devam edebilir.
