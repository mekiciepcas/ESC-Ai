# ESC V2 — UAV yeniden bazlandırma / B1 korunan referans

## 19.09.2026 — P0 yön düzeltmesi

Bu projenin hedef uygulaması **70–100 kg faydalı yük hedefli ağır kaldırma / zirai çok rotorlu UAV için ESC geliştirmesidir**. Önceki B1 tasarım temeli yanlışlıkla `bench_and_general_purpose_ground_drive_not_flight_qualified` varsayımına oturtulmuştur. Bu varsayım artık aktif tasarım temeli değildir.

Aktif gereksinim kaynağı: `design_basis.json` (`B1-UAV-REBASELINE`). UAV hedefi aktiftir; ancak ürün **henüz flight-qualified değildir**. Uçuş yeterliliği ancak propulsion sizing, elektriksel/termal doğrulama, firmware, PCB, prototip ve fiziksel test kapıları tamamlandıktan sonra değerlendirilebilir.

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

## UAV yeniden bazlandırma sırası

1. Görev profili ve toplam kalkış kütlesi zarfı.
2. Rotor sayısı ve emniyet/thrust marjı.
3. Motor + pervane seçim/benchmark ve hover/max-thrust çalışma noktaları.
4. Batarya gerilimi ve akım mimarisi.
5. ESC sürekli/tepe gerilim, faz akımı, DC akımı ve güç zarfı.
6. MOSFET/topoloji/gate-driver kayıp-SOA değerlendirmesi.
7. DC-link, koruma, sensing ve termal tasarım.
8. Firmware kontrol/fault mimarisi.
9. Güç + kontrol PCB tasarımı, DRC/DFM ve üretim paketi.
10. Kademeli bench + motor/propulsion doğrulaması.

Bu maddeler kapanmadan mevcut B1'in 3 kW/13S değerleri nihai ürün gereksinimi olarak kabul edilmez.

## Korunan tarihsel A2/B1 kayıtları

- A2 KiCad: `hardware_a2/ESC_3kW_A2.kicad_pro`
- B1 KiCad: `hardware_b1/ESC_3kW_B1.kicad_pro`
- A2 PDF: `ESC_3kW_A2_semalar.pdf`
- B1 elektriksel denetimler: `verification/b1_checks.json`
- B1 elektriksel ekip incelemesi: `verification/team_electrical/review.md`
- PCB kuralları: `pcb_b1/TASARIM_KURALLARI.md`

A2/B1 dosyaları silinmez; tarihsel mühendislik kanıtı ve yeniden kullanım kaynağı olarak korunur.
