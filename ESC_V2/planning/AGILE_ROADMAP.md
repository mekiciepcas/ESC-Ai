# ESC — sprint uygulama yol haritası

PLAN-07 · 2026-09-15 · Şema temeli B1

Asıl durum kaydı `backlog.json`; bu görünüm `render_roadmap.py` ile üretilir. [Sprint 1 uygulama ve karar kaydı](SPRINT_01_UYGULAMA.md).

[HTML proje panosu](../dashboard/index.html) · [Ekip tasarım incelemesi](team_review.json) · [Değişiklik günlüğü](change_log.json).

Hedef: ölçümle doğrulanmış 1.5 kW prototip, ardından marjlar yeterliyse 3 kW ürün adayı. İki haftalık sprintler planlama kutusudur; altı sprint 12 haftalık teslim garantisi değildir. Numune ve laboratuvar süreleri ayrıca izlenir. SP göreli karmaşıklıktır; saat değildir. Kapasite henüz ölçülmedi; yükler sprint taahhüdü sayılmaz. ESC-14 işe alınmadan daha küçük yönlendirme işlerine ayrılır.

Akış: TODO → READY → IN_PROGRESS → REVIEW → DONE; engellenen iş BLOCKED ve gerekçe taşır. WIP: en fazla iki uygulama ve bir inceleme işi. DONE yalnız kabul ölçütü ve kanıtla; donanım için yazılım/DRC sonucu fiziksel test yerine geçmez. Roller ek personel ataması veya bağımsız onay anlamına gelmez.

Sprint başında hazır işler seçilir; sonunda kanıt gösterimi, açık hata incelemesi ve retrospektif yapılır. Ölçümler: tamamlanan iş/SP, açık P0, eksik BOM, açık PCB bağlantısı/DRC ve fiziksel test sonucu. Henüz ölçülmeyen PCB/test verileri sıfır başarı olarak yazılmaz.

Definition of Ready: girdiler, bağımlılıklar, araçlar ve ölçülebilir kabul kriteri hazır. Definition of Done: kriter geçti, kanıt ve revizyon kayıtlı, etkilenmiş şema/PCB/BOM/firmware tutarlı, inceleme tamam.

## Sprint 1 — Çalışma zarfı ve sistem kararları

- [x] **ESC-01 — Çalışma zarfını ve 1.5/3 kW geçiş koşullarını sabitle**
  - DONE · P0 · 3 SP · Codex — sistem
  - Bağımlılıklar: Yok. Risk: R09.
  - Kabul: 13S gerilim aralığı, batarya/faz akımları, ortam sıcaklığı, sürekli/tepe süreleri ve derating eğrisi aynı tasarım temelinde tanımlı; 3 kW mil gücü ile DC giriş gücü ayrılmış.
  - Kanıt: [SPRINT_01_UYGULAMA.md](SPRINT_01_UYGULAMA.md), [envelope_checks.json](envelope_checks.json), [../design_basis.json](../design_basis.json)

- [ ] **ESC-02 — Motor, batarya ve test düzeneği numune planı**
  - TODO · P0 · 3 SP · Codex plan; kullanıcı numune/ölçüm
  - Bağımlılıklar: ESC-01. Risk: R09.
  - Kabul: Motor varyantı, Hall/sıcaklık arayüzü, BMS enerji kabulü ve gerekli ölçüm cihazları listeli; numune temin süresi ve ölçülecek parametreler kayıtlı. Satın alma ayrı kullanıcı kararı.

- [ ] **ESC-03 — Giriş sigorta, ön şarj ve ayırma tasarımını tamamla**
  - IN_PROGRESS · P0 · 8 SP · Codex — güç
  - Bağımlılıklar: ESC-01. Risk: R01.
  - Kabul: Şema, DC kesme kapasitesi, kablo/sigorta I²t koordinasyonu, ön şarj direnç darbe enerjisi ve yardımcı yükle şarj süresi hesapları tamam; ters kutup davranışı tanımlı. DR-002 ELEC-02: MCU kapalıyken MCU komutu beklemeyen ön şarj yük engelleme mimarisini seç.
  - Kalan: Yardımcı beslemenin ön şarjda yükü, direnç pulse/timeout, sigorta/ayırıcı/ters kutup seçimi ve şema açık.
  - Kanıt: [precharge_checks.json](precharge_checks.json)

- [ ] **ESC-04 — Geri sürülme ve BMS açılması için enerji yönetimi seç**
  - TODO · P0 · 8 SP · Codex — sistem/güç
  - Bağımlılıklar: ESC-01. Risk: R02.
  - Kabul: Yük ataleti bilinmeyen alanlar açıkça sınırlandırılmış; geçici enerji zarfına göre fren/enerji kabul yolu, bileşen gerilim marjı ve şema tanımlı. OV trip, gerilim kelepçesi olarak kabul edilmez.

- [ ] **ESC-05 — Standart ve şema çizim incelemesini tamamla**
  - TODO · P1 · 5 SP · Codex — donanım
  - Bağımlılıklar: Yok. Risk: R07.
  - Kabul: IEC/IPC referans sürümleri ve erişim sınırları kayıtlı; özel sembol geometrileri, polarite, birimler, NC, sayfa referansları incelenmiş; uygulanamayan maddeler açık listede. Tam uygunluk iddiası yalnız kanıtla. Bobin/gövde diyodu/polarite ve proje ayarı koruma değişikliklerini kanıtla; kalan özel semboller açık.
  - Kalan: PoC önceliğiyle kapsamlı sembol standardizasyonu ertelendi; kritik elektriksel kontroller devam eder.
  - Kanıt: [SPRINT_01_UYGULAMA.md](SPRINT_01_UYGULAMA.md)

- [x] **ESC-13-P0 — Kontrol kartı ilk yerleşim ve pad-net aktarımı**
  - DONE · P1 · 3 SP · Codex — PCB
  - Bağımlılıklar: ESC-01. Risk: R07.
  - Kabul: İlk mekanik yerleşim dosyası ve pad-net denetimi mevcut; aday kılıflar açık. ESC-13 nihai yerleşim kabulünün yerine geçmez.
  - Kanıt: [../pcb_b1/control/placement_report.json](../pcb_b1/control/placement_report.json), [../pcb_b1/control/ESC_3kW_CONTROL_B1_PLACEMENT.kicad_pcb](../pcb_b1/control/ESC_3kW_CONTROL_B1_PLACEMENT.kicad_pcb)

- [ ] **POC-01 — Kontrol PoC: besleme, programlama ve temel arayüzler**
  - IN_PROGRESS · P0 · 8 SP · Codex tasarım; kullanıcı fiziksel test
  - Bağımlılıklar: ESC-01. Risk: R03, R06, R07.
  - Kabul: Denetlenmiş kontrol şeması/PCB, doğrulanmış düşük gerilim besleme yöntemi, derlenmiş ilk firmware ve gerçek SWD/UART/CAN test kanıtı. İlk izler görevi kapatmaz.
  - Kanıt: [POC_HEDEFI.md](POC_HEDEFI.md), [../pcb_b1/control/first_routes_20260915.json](../pcb_b1/control/first_routes_20260915.json)

## Sprint 2 — BOM, korumalar ve termal tasarım

- [ ] **ESC-06 — DC-link kondansatör bankasını ripple ve ömürle boyutlandır**
  - TODO · P0 · 8 SP · Codex — güç
  - Bağımlılıklar: ESC-01, ESC-04. Risk: R03.
  - Kabul: PWM çalışma zarfında kondansatör RMS akımı, DC bias, ESR kaybı ve ömür hesabı mevcut; tam MPN ve land pattern seçili. 3×470 µF başlangıç varsayımı hesap olmadan korunmaz.

- [ ] **ESC-07 — Yardımcı besleme ve küçük pasif seçimlerini kapat**
  - TODO · P0 · 5 SP · Codex — donanım
  - Bağımlılıklar: ESC-01, ESC-03. Risk: R03.
  - Kabul: 12/5/3.3 V yük bütçeleri, bobin doyma/RMS, kapasitör DC bias ve regülatör ripple/kararlılık hesapları tamam; ilgili BOM alt işleri kanıtla kapanmış. DR-002 ELEC-01 sonrası 100k RON frekans/ripple hesabını ve yardımcı kaynak testini doğrula.

- [ ] **ESC-08 — Şönt, terminal, konektör ve mekanik arayüzleri kesinleştir**
  - TODO · P0 · 5 SP · Codex — PCB/mekanik
  - Bağımlılıklar: ESC-01, ESC-02. Risk: R03, R07.
  - Kabul: Dört uçlu şönt sense/power yönü, konektör akımı/pin1/bakış yönü, terminal montajı ve PCB zarfı ölçülendirilmiş; B1 pin38 uyumsuzluğu montaj belgesinde görünür.

- [ ] **ESC-09 — CAN, Hall, RC ve servis port korumalarını tasarla**
  - TODO · P0 · 5 SP · Codex — donanım
  - Bağımlılıklar: ESC-02. Risk: R05.
  - Kabul: ESD elemanlarının clamp gerilimi IC sınırlarıyla koordineli; Hall çıkış tipi, kablo kopması ve servis besleme geri akışı değerlendirilmiş; şemaya işlenmiş.

- [ ] **ESC-10 — BOM ve footprint çift yönlü denetimini tamamla**
  - TODO · P0 · 8 SP · Codex — donanım/tedarik
  - Bağımlılıklar: ESC-06, ESC-07, ESC-08, ESC-09. Risk: R03, R08.
  - Kabul: 61 başlangıç BOM alt işi ve sonradan eklenen parçalar dahil eksik alan sıfır; tüm MPN/pad numaraları veri sayfasıyla karşılaştırılmış; DNP ve muadil yeterlilik seviyesi kayıtlı. Aile kodu tek başına sipariş kanıtı değil.

- [ ] **ESC-11 — Termal yapı, bakır ve güç bağlantılarını hesapla**
  - TODO · P0 · 8 SP · Codex — güç/mekanik
  - Bağımlılıklar: ESC-06, ESC-08. Risk: R07.
  - Kabul: MOSFET/şönt/kondansatör kayıpları, PCB-via-TIM-soğutucu termal yolu ve bağlantı daralmaları incelenmiş; 1.5 ve 3 kW için sıcaklık bütçeleri ve ölçüm noktaları tanımlı. PCB NTC ile taban plakası sıcaklığı korelasyonu hesap/ölçüm planıyla tanımlı veya ayrı sensör seçili.

- [ ] **ESC-26 — Kritik tedarik ve muadil stratejisini doğrula**
  - TODO · P1 · 3 SP · Codex araştırma; kullanıcı tedarik teyidi
  - Bağımlılıklar: ESC-08. Risk: R08.
  - Kabul: MCU/driver/MOSFET/şönt için adet ve ülke bazlı yetkili kanal kaydı, ömür döngüsü ve muadil doğrulama planı mevcut; stok görüntüsü rezervasyon sayılmaz.

## Sprint 3 — PCB ve firmware temeli

- [ ] **ESC-12 — Güç kartı yerleşimini tamamla**
  - TODO · P0 · 8 SP · Codex — PCB
  - Bağımlılıklar: ESC-03, ESC-04, ESC-05, ESC-10, ESC-11. Risk: R07.
  - Kabul: Gerçek footprintlerle güç döngüsü, paralel kol simetrisi, gate dönüşü ve Kelvin yerleşimi hazır; mekanik/soğutucu keepout ve kritik yerleşim incelemesi kayıtlı.

- [ ] **ESC-13 — Kontrol kartı yerleşimini tamamla**
  - TODO · P1 · 5 SP · Codex — PCB
  - Bağımlılıklar: ESC-05, ESC-10. Risk: R07.
  - Kabul: MCU bypass, analog dönüş, CAN/servis ve konektör yerleşimleri tamam; iki kart zarfı, pin1 ve montaj erişimi doğrulanmış.

- [ ] **ESC-14 — Kartları yönlendir ve elektriksel/mekanik PCB denetimini kapat**
  - TODO · P0 · 13 SP · Codex — PCB
  - Bağımlılıklar: ESC-12, ESC-13. Risk: R07.
  - Kabul: Açık bağlantı ve kısa devre sıfır; açıklık, courtyard, kenar ve delik hataları giderilmiş; bütün istisnalar gerekçeli; şema-PCB pin/net eşleşmesi ve kritik akım yolu incelemesi tamam.

- [ ] **ESC-15 — Firmware pin ve zamanlama temelini kur**
  - TODO · P0 · 8 SP · Codex — gömülü
  - Bağımlılıklar: ESC-09, ESC-10. Risk: R06.
  - Kabul: Pin sözleşmesiyle derleme tutarlı; PWM/ADC tetikleme, dead-time ve örnekleme pencereleri hesaplanmış; kart başlatma iskeleti derleniyor.

## Sprint 4 — Prototip üretim ve numune

- [ ] **ESC-16 — Arıza durum makinesi ve düşük güç test yazılımı**
  - TODO · P0 · 8 SP · Codex — gömülü
  - Bağımlılıklar: ESC-15. Risk: R06, R04.
  - Kabul: Başlatma, CSA kalibrasyonu, fault latch, haberleşme kaybı ve yeniden başlatma durumları uygulanmış; yazılım testleri kayıtlı; donanım testi yapılmamış alanlar ayrı. DR-002 ELEC-03: VOL+VF worst-case düşük seviye marjı, CLR/BKIN ve brownout sıralamasını bütçele.

- [ ] **ESC-17 — DFM incelemesi ve prototip üretim paketini hazırla**
  - TODO · P0 · 5 SP · Codex paket; kullanıcı üretici iletişimi
  - Bağımlılıklar: ESC-14. Risk: R03, R07.
  - Kabul: Gerber/drill yeniden görüntülenmiş; stackup, stencil, BOM, yerleştirme, montaj ve revizyon manifesti tutarlı; üretici DFM bulguları kapanmış. Kullanıcı üretim/sipariş kararı verir.

- [ ] **ESC-18 — Prototip numuneyi üret ve montaj giriş kontrolünü yap**
  - TODO · P0 · 3 SP · Kullanıcı — tedarik/fiziksel kontrol
  - Bağımlılıklar: ESC-17. Risk: R08.
  - Kabul: Gerçek kart/montaj numunesi mevcut; revizyon, parça/polarite, kısa devre ve kritik bağlantı ölçümleri kayıtlı. Süre üretici/teslimata bağlı.

- [ ] **ESC-19 — Motor ve batarya parametrelerini ölç**
  - TODO · P0 · 5 SP · Kullanıcı ölçüm; Codex değerlendirme
  - Bağımlılıklar: ESC-02. Risk: R09.
  - Kabul: Rs, Ld/Lq veya uygun eşdeğerleri, Ke, kutup çifti, Hall sırası, sıcaklık sensörü ve BMS davranışı raporlu; çalışma zarfı saparsa tasarım değişikliği açılmış.

## Sprint 5 — Devreye alma ve 1.5 kW

- [ ] **ESC-20 — Akım sınırlı ilk enerji ve donanım koruma testleri**
  - TODO · P0 · 5 SP · Kullanıcı ölçüm; Codex test planı
  - Bağımlılıklar: ESC-16, ESC-18. Risk: R01, R04, R06.
  - Kabul: Besleme sıralaması, reset, kilitli fault, tüm PWM kapatma ve sensör doğruluğu ölçülmüş; beklenmeyen anahtarlama yok; başarısız kriterler hata kaydıyla giderilmiş. NTC/taban plakası sıcaklık eşlemesi doğrulanmış; yanlış sensör değeriyle termal izin verilmiyor.

- [ ] **ESC-21 — Hall/FOC kontrolünü gerçek motorda devreye al**
  - TODO · P0 · 8 SP · Codex firmware; kullanıcı tezgâh
  - Bağımlılıklar: ESC-19, ESC-20. Risk: R06, R09.
  - Kabul: Hall sırası ve akım polaritesi doğrulanmış; düşük enerji/yüksüz başlatma, kararlı akım kontrolü ve haberleşme kaybı testleri geçilmiş.

- [ ] **ESC-22 — Anahtarlama ve 1.5 kW yük doğrulaması**
  - TODO · P0 · 8 SP · Kullanıcı ölçüm; Codex değerlendirme
  - Bağımlılıklar: ESC-21. Risk: R04, R07.
  - Kabul: VGS/VDS taşması, fault gecikmesi, akım/gerilim sınırları ve tanımlı ortamda termal kararlılık ölçülmüş; 1.5 kW mil gücü doğrulanmış. Yalnız DC giriş wattı yeterli değil.

## Sprint 6 — 3 kW ve ürün doğrulaması

- [ ] **ESC-23 — 3 kW ve enerji yönetimi sınır testleri**
  - TODO · P0 · 8 SP · Kullanıcı ölçüm; Codex değerlendirme
  - Bağımlılıklar: ESC-22, ESC-04. Risk: R02, R04, R07.
  - Kabul: Önceden tanımlı test düzeneğinde 3 kW mil gücü, termal marj, derating ve dolu batarya/BMS ayırma enerji senaryoları geçilmiş; geçmezse 1.5 kW ürün kapsamı veya yeni revizyon kararı kayıtlı.

- [ ] **ESC-24 — EMC ve kullanım ortamına özgü doğrulama**
  - TODO · P1 · 8 SP · Codex plan; kullanıcı/laboratuvar ölçüm
  - Bağımlılıklar: ESC-22. Risk: R05, R07.
  - Kabul: Hedef ürün kullanımına göre uygulanacak testler ve seviyeler kesin; ön uyumluluk/ESD ve çevre test raporları mevcut; kalan resmi uygunluk işleri açıkça ayrılmış.

- [ ] **ESC-25 — Revizyon kapanışı ve ürün teslim dosyası**
  - TODO · P0 · 5 SP · Codex dokümantasyon; kullanıcı kabul
  - Bağımlılıklar: ESC-23, ESC-24, ESC-26. Risk: R01, R02, R03, R04, R05, R06, R07, R08, R09.
  - Kabul: Kritik hata açık değil; doğrulanan güç sınıfı açık; üretim dosyası, firmware etiketi, kalibrasyon, test raporu, montaj ve servis talimatları aynı revizyona ait. Seri tedarik kanıtları tamam.

## Başlangıç — Tamamlanmış başlangıç kontrolleri

- [x] **DONE-01 — B1 şema kontrol tabanı**
  - DONE · P1 · — SP · Codex
  - Bağımlılıklar: Yok. Risk: Başlangıç kanıtı.
  - Kabul: Yalnız belirtilen rapor kapsamındaki kontrol tamam; ürün doğrulaması değildir.
  - Kanıt: [../verification/b1_checks.json](../verification/b1_checks.json)

- [x] **DONE-02 — Motor sıcaklığı arayüz düzeltmesi ve 32 net denetimi**
  - DONE · P1 · — SP · Codex
  - Bağımlılıklar: Yok. Risk: Başlangıç kanıtı.
  - Kabul: Yalnız belirtilen rapor kapsamındaki kontrol tamam; ürün doğrulaması değildir.
  - Kanıt: [../pcb_b1/verification/interface_audit.json](../pcb_b1/verification/interface_audit.json)

- [x] **DONE-03 — KiCad kural motorunun negatif testleri**
  - DONE · P1 · — SP · Codex
  - Bağımlılıklar: Yok. Risk: Başlangıç kanıtı.
  - Kabul: Yalnız belirtilen rapor kapsamındaki kontrol tamam; ürün doğrulaması değildir.
  - Kanıt: [../pcb_b1/verification/rule_validation.json](../pcb_b1/verification/rule_validation.json)

## Gözden geçirme kararları

- **D-01 / F-01** — CLOSED_DOCUMENTATION; ilgili işler: Sprint uygulama kaydı.
- **D-02 / F-02** — OPEN; ilgili işler: ESC-05.
- **D-03 / F-03** — CLOSED_TOOLING; ilgili işler: Sprint uygulama kaydı.
- **D-04 / F-04** — OPEN; ilgili işler: ESC-11, ESC-20.

## Geçiş kapıları

- G1: ESC-01–11 ve ESC-26 tasarım/tedarik kapsamı incelenmiş; kritik seçimler açık değil.
- G2: ESC-14 ve ESC-17 tamam; prototip siparişi kullanıcı kararı.
- G3: ESC-19 ve ESC-20 tamam; gerçek motor/koruma verisiyle enerji verme.
- G4: ESC-22 tamam; yalnız 1.5 kW doğrulaması.
- G5: ESC-23–25 tamam; güç sınıfı ve kalan resmi uygunluk kapsamı açık. Başarısız 3 kW testi kapsam/revizyon kararına döner.

## BOM alt işleri — ESC-10

61 başlangıç bileşen kaydı; farklı MPN sayısı değildir. Yeni parçalar eklenirse yeni alt iş açılır.

- [ ] **BOM-J101** — DC LINK INPUT; TODO; eksik: mpn, footprint.
- [ ] **BOM-J102** — MOTOR U V W; TODO; eksik: mpn, footprint.
- [ ] **BOM-J103** — EXTERNAL BRAKE MODULE; TODO; eksik: mpn, footprint.
- [ ] **BOM-C101** — 470u 100V bulk; TODO; eksik: mpn, footprint.
- [ ] **BOM-C102** — 470u 100V bulk; TODO; eksik: mpn, footprint.
- [ ] **BOM-C103** — 470u 100V bulk; TODO; eksik: mpn, footprint.
- [ ] **BOM-C104** — 2.2u 100V X7R; TODO; eksik: mpn, footprint.
- [ ] **BOM-C105** — 2.2u 100V X7R; TODO; eksik: mpn, footprint.
- [ ] **BOM-C106** — 2.2u 100V X7R; TODO; eksik: mpn, footprint.
- [ ] **BOM-RS201** — 0.5mR 1% Kelvin; TODO; eksik: footprint.
- [ ] **BOM-RS301** — 0.5mR 1% Kelvin; TODO; eksik: footprint.
- [ ] **BOM-RS401** — 0.5mR 1% Kelvin; TODO; eksik: footprint.
- [ ] **BOM-C501** — 47n 100V; TODO; eksik: mpn, footprint.
- [ ] **BOM-C502** — 1u 25V; TODO; eksik: mpn.
- [ ] **BOM-C503** — 1u 25V; TODO; eksik: mpn.
- [ ] **BOM-C504** — 1u 10V; TODO; eksik: mpn.
- [ ] **BOM-C506** — 10u 25V; TODO; eksik: mpn, footprint.
- [ ] **BOM-C701** — 1n C0G; TODO; eksik: mpn.
- [ ] **BOM-C801** — 1n C0G; TODO; eksik: mpn.
- [ ] **BOM-C901** — 1n C0G; TODO; eksik: mpn.
- [ ] **BOM-C1001** — 1n C0G; TODO; eksik: mpn.
- [ ] **BOM-C1101** — 1n C0G; TODO; eksik: mpn.
- [ ] **BOM-C1102** — 1n C0G; TODO; eksik: mpn.
- [ ] **BOM-C1103** — 1n C0G; TODO; eksik: mpn.
- [ ] **BOM-C1201** — 10n; TODO; eksik: mpn.
- [ ] **BOM-C1202** — 10n; TODO; eksik: mpn.
- [ ] **BOM-J1201** — MOTOR TEMP; TODO; eksik: mpn, footprint.
- [ ] **BOM-C1203** — 10n; TODO; eksik: mpn.
- [ ] **BOM-L1301** — 68uH >=1.5A; TODO; eksik: mpn, footprint.
- [ ] **BOM-C1301** — 2.2u 160V; TODO; eksik: mpn, footprint.
- [ ] **BOM-C1302** — 100n 160V; TODO; eksik: mpn, footprint.
- [ ] **BOM-C1303** — 22u 25V; TODO; eksik: mpn, footprint.
- [ ] **BOM-C1304** — 22u 25V; TODO; eksik: mpn, footprint.
- [ ] **BOM-C1305** — 2.2n C0G; TODO; eksik: mpn.
- [ ] **BOM-C1306** — 3.3n; TODO; eksik: mpn.
- [ ] **BOM-C1401** — 56p C0G; TODO; eksik: mpn.
- [ ] **BOM-J1401** — FAN 12V; TODO; eksik: mpn, footprint.
- [ ] **BOM-L1501** — 2.2uH >=1.5A; TODO; eksik: mpn, footprint.
- [ ] **BOM-C1501** — 10u 25V; TODO; eksik: mpn, footprint.
- [ ] **BOM-C1502** — 22u 10V; TODO; eksik: mpn, footprint.
- [ ] **BOM-C1503** — 1u 10V; TODO; eksik: mpn.
- [ ] **BOM-C1504** — 4.7u 10V; TODO; eksik: mpn, footprint.
- [ ] **BOM-C1505** — 4.7u 10V; TODO; eksik: mpn, footprint.
- [ ] **BOM-C1805** — 4.7u; TODO; eksik: mpn, footprint.
- [ ] **BOM-C1807** — 1u VDDA; TODO; eksik: mpn.
- [ ] **BOM-J1901** — SWD; TODO; eksik: mpn, footprint.
- [ ] **BOM-Y1901** — 8MHz 3V3 CMOS oscillator; TODO; eksik: mpn, footprint.
- [ ] **BOM-D1901** — LED GREEN; TODO; eksik: mpn, footprint.
- [ ] **BOM-J2001** — CAN; TODO; eksik: mpn, footprint.
- [ ] **BOM-J2002** — UART 3V3; TODO; eksik: mpn, footprint.
- [ ] **BOM-J2003** — RC PWM 3V3; TODO; eksik: mpn, footprint.
- [ ] **BOM-J2101** — HALL 5V; TODO; eksik: mpn, footprint.
- [ ] **BOM-C2101** — 1n; TODO; eksik: mpn.
- [ ] **BOM-C2102** — 1n; TODO; eksik: mpn.
- [ ] **BOM-C2103** — 1n; TODO; eksik: mpn.
- [ ] **BOM-C2301** — 10n reference; TODO; eksik: mpn.
- [ ] **BOM-C2302** — 10n reference; TODO; eksik: mpn.
- [ ] **BOM-C2303** — 10n reference; TODO; eksik: mpn.
- [ ] **BOM-J2401** — EMERGENCY STOP; TODO; eksik: mpn, footprint.
- [ ] **BOM-J2701** — POWER CARD 2x20; TODO; eksik: mpn, footprint.
- [ ] **BOM-J2702** — CONTROL CARD 2x20; TODO; eksik: mpn, footprint.
