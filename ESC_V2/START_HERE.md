# ESC V2 — UAV yeniden bazlandırma / B1 korunan referans

## 19.09.2026 — P0 yön düzeltmesi

Bu projenin hedef uygulaması **70–100 kg faydalı yük hedefli ağır kaldırma / zirai çok rotorlu UAV için ESC geliştirmesidir**. Önceki B1 tasarım temeli yanlışlıkla `bench_and_general_purpose_ground_drive_not_flight_qualified` varsayımına oturtulmuştur. Bu varsayım artık aktif tasarım temeli değildir.

Aktif gereksinim kaynağı: `design_basis.json` (`B1-UAV-REBASELINE`). UAV hedefi aktiftir; ancak ürün **henüz flight-qualified değildir**. Uçuş yeterliliği ancak propulsion sizing, elektriksel/termal doğrulama, firmware, PCB, prototip ve fiziksel test kapıları tamamlandıktan sonra değerlendirilebilir.

## Aktif çalışma dosyaları

- **Ürün geliştirme planı:** `planning/UAV_PRODUCT_PLAN.md`
- **Aktif UAV backlog:** `planning/uav_backlog.json`
- **Faz 2 / Faz 3 / B1 izlenebilirlik matrisi:** `planning/UAV_TRACEABILITY.md`
- **Rebaseline design authority:** `planning/UAV_REBASELINE.md`
- **Aktif sistem gereksinimleri:** `design_basis.json`

Bu beş dosya `uav-rebaseline` branch'inde yeni ürün geliştirme akışının otoritesidir. Eski 3 kW roadmap ve dashboard tarihsel ilerleme kaydı olarak korunur.

### Tasarım dondurma kararı

Mevcut 3 kW / 13S / Golden Motor HPM3000B / 80 A RMS B1 değerleri artık **UAV baseline değil, yalnız legacy candidate/reference** kabul edilir. Rotor sayısı, toplam kalkış kütlesi, thrust margin, motor/propeller çalışma noktaları, batarya seri sayısı ve gerçek ESC sürekli/tepe güç-akım zarfı yeniden boyutlandırılmadan şu işler nihai tasarım olarak ilerletilmez:

- güç PCB yerleşimi ve routing,
- DC-link ve güç konektörü boyutlandırması,
- MOSFET sayısı / gerilim sınıfı / termal çözümün dondurulması,
- şönt ve akım ölçüm aralığının dondurulması,
- üretim BOM'u ve Gerber release.

Mevcut şema, kontrol PCB PoC'u, doğrulama betikleri ve B1 hata düzeltmeleri korunur; UAV yeniden incelemesinden geçen bölümler yeni revizyona taşınır.

## Mevcut B1 referans durumu

**Kontrol PCB başladı:** [Kontrol kartı KiCad ilk yerleşim](pcb_b1/control/ESC_3kW_CONTROL_B1_PLACEMENT.kicad_pcb) · [Görünüm](pcb_b1/control/placement.png). Kontrol kartı kısmi PoC durumundadır; üretim/enerji verme onayı değildir.

**[HTML proje ve operasyon panosu](dashboard/index.html)** mevcut tarihsel B1 ilerlemesini gösterir. Dashboard ve eski roadmap içindeki 3 kW/13S tamamlanmış çalışma zarfı kayıtları UAV rebaseline tamamlanana kadar güncel design authority olarak kullanılmaz.

14.09.2026 tarihli B1 şema: `hardware_b1/ESC_3kW_B1.kicad_pro`. B1 içinde LM5164 RON bağlantı düzeltmesi, kartlar arası net denetimi ve ERC kontrolleri gibi yeniden kullanılabilir mühendislik çalışmaları vardır; bunlar yeni UAV zarfında yeniden yeterlilik kontrolüne tabi tutulacaktır.

## Geçiş kapıları

1. **G0 — Mission Freeze:** payload/MTOW/görev/çevre zarfı.
2. **G1 — System Electrical Freeze:** rotor + motor/prop + battery + gerçek ESC electrical envelope.
3. **G2 — ESC Architecture Freeze:** semiconductor, topology, PWM, MCU, gate-driver, sensing, fault, thermal architecture.
4. **G3 — Schematic Design Review:** yeni UAV şeması, kritik BOM ve hesaplar kapalı.
5. **G4 — Firmware Bench Ready:** buildable firmware, timing/fault testleri.
6. **G5 — Prototype Release:** control + power PCB, DFM ve üretim paketi.
7. **G6 — Propulsion Verified:** düşük enerji, switching ve guarded dyno/prop testleri geçti.
8. **G7 — Flight Test Ready:** araç entegrasyonu ve failsafe readiness review tamam.

G1 kapanmadan 13S/3 kW/80 A/100 V gibi eski sayılar nihai ürün gereksinimi sayılmaz. G6 kapanmadan uçuş testi temel güç elektroniği doğrulama yöntemi olarak kullanılmaz.

## Korunan tarihsel A2/B1 kayıtları

- A2 KiCad: `hardware_a2/ESC_3kW_A2.kicad_pro`
- B1 KiCad: `hardware_b1/ESC_3kW_B1.kicad_pro`
- A2 PDF: `ESC_3kW_A2_semalar.pdf`
- B1 elektriksel denetimler: `verification/b1_checks.json`
- B1 elektriksel ekip incelemesi: `verification/team_electrical/review.md`
- PCB kuralları: `pcb_b1/TASARIM_KURALLARI.md`

A2/B1 dosyaları silinmez; tarihsel mühendislik kanıtı ve yeniden kullanım kaynağı olarak korunur.
