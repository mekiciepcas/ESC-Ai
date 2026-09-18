# ESC 3 kW — güncel B1 geliştirme / A2 arşiv

**PCB başladı:** [Kontrol kartı KiCad ilk yerleşim](pcb_b1/control/ESC_3kW_CONTROL_B1_PLACEMENT.kicad_pcb) · [Görünüm](pcb_b1/control/placement.png). PLAN-05: 38 bileşen / 192 pad kontrolü; yönlendirme henüz yok. 128 açık bağlantı ve 6 serigrafi ihlali kaldı; üretim paketi değildir.

**[HTML proje ve operasyon panosu](dashboard/index.html)** — PLAN-04, ekip bulguları, yapılan değişiklikler, sprintler ve gerçek kanıt dosyaları. DR-002: LM5164 RON düzeltmesi; 742 kontrol / ERC 0. [Ekip çalışma düzeni](planning/EKIP_CALISMA_DUZENI.md).

**Agile yol haritası ve yapılacaklar:** [PLAN-03](planning/AGILE_ROADMAP.md). Asıl takip kaydı: `planning/backlog.json`. Sprint 1: ESC-01 tasarım zarfı tamamlandı; ESC-05 ve ESC-03 uygulamada. 25 açık ana iş, 4 tamamlanmış kayıt ve 61 BOM alt işi. [Uygulama ve iyileştirme kararları](planning/SPRINT_01_UYGULAMA.md).

[Tamamlama takvimi](planning/TAMAMLAMA_TAKVIMI.md) · [Otomatik devam kaydı](planning/CHECKPOINT.md). Altı saatte bir kullanım limiti kontrolüyle devam otomasyonu oluşturuldu.

14.09.2026: Güncel şema `hardware_b1/ESC_3kW_B1.kicad_pro`; açıklamalar `hardware_b1/README.md`.
Çizim ve üretim kuralları `pcb_b1/TASARIM_KURALLARI.md`; uygulanabilir KiCad kuralları `hardware_b1/ESC_3kW_B1.kicad_dru`.
B1 pin38 TEMP_MOTOR'dur; A2 pin38 GND olduğundan kart/kablo revizyonları karıştırılmaz.
B1: 741 şema kontrolü, sıfır ERC ihlali, 32 kartlar arası netin denetimi. Ürün PCB routing ve üretim onayı henüz tamamlanmadı.

## Korunan A2 inceleme paketi

- **KiCad:** `hardware_a2/ESC_3kW_A2.kicad_pro`
- **PDF şemalar:** `ESC_3kW_A2_semalar.pdf`
- **Tarayıcıda inceleme:** `hardware_a2/inceleme.html`
- **Tasarım açıklamaları:** `hardware_a2/README.md`
- **Açık işler ve kabul kriterleri:** `hardware_a2/release_register.json`
- **Kontrol sonuçları:** `verification/a2_checks.json`

A2 önceki inceleme revizyonudur. `hardware` klasörü A1 referansını ve jeneratörlerin okuduğu elektriksel kaynak tanımını içerir; bağımlılık nedeniyle korunmuştur.

A2 bir mühendislik inceleme revizyonudur. Üretim BOM'u, PCB, firmware ve fiziksel güç doğrulaması tamamlanmamıştır. Web stok kayıtları sipariş veya rezervasyon anlamına gelmez.
