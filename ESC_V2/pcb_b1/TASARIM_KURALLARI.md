# ESC-3K B1 — çizim ve PCB kontrol şartnamesi

Belge: ESC-ENG-001 · Revizyon B1 · 14.09.2026 · Durum: mühendislik geliştirme.

**Bu belge uygunluk sertifikası veya üretim onayı değildir.** A2 korunmuştur. B1 şeması kartlar arası motor sıcaklığı bağlantısını düzeltir; B1 pin38 TEMP_MOTOR, A2 pin38 GND'dir. Revizyonlar aynı kabloyla birbirine karıştırılamaz.

## Standart dayanağı ve doğrulama sınırı

- IEC 61082-1: elektroteknik belge, şema ve çizimlerin sunumu için referans. Sayfa başlığı, belge kimliği, revizyon, tarih, işlev grupları ve bağlantı referansları kullanılır. [IEC kapsamı](https://webstore.iec.ch/en/publication/4469).
- IEC 60617: elektriksel grafik semboller için referans. Mevcut özel fonksiyon bloklarının pin numaraları kontrol edilmiş olsa da sembol geometrilerinin tamamı bu veritabanına göre doğrulanmış değildir. MOSFET gövde diyodu, bobin ve polariteli eleman gösterimleri ayrıca gözden geçirilecek. [IEC veritabanı](https://webstore.iec.ch/en/publication/2723).
- IPC-2221 ve IPC-2222: genel ve rijit PCB tasarımı; IPC-2152: iletken akım taşıma değerlendirmesi. PCB geometrisi, bakır kalınlığı, komşu düzlemler ve sıcaklık artışı birlikte değerlendirilir. Bir iz genişliği hesaplayıcısının sonucu tek başına kabul kanıtı değildir. [IPC tasarım standartları](https://www.ipc.org/ipc-design-standards).
- IPC-6012 / IPC-A-600: çıplak kart performansı ve kabulü; IPC-A-610 / J-STD-001: montaj kabulü ve lehimleme için tedarik şartnamesi referansları. Başlangıç satın alma hedefi genel endüstriyel kullanım için Class 2'dir. Üreticiyle sürüm ve uygulanacak maddeler mutabık kalınmadan sipariş şartı kesinleşmez. [IPC DFM kapsamı](https://www.ipc.org/design-manufacturing-confirmed-ipc-standards).

Standartların lisanslı tam metinleri bu çalışmada mevcut değildir. Kamuya açık kapsam bilgileri kullanılmıştır; aşağıdaki sayılar standarttan alınmış zorunlu minimumlar değil, proje başlangıç kurallarıdır. Son uygunluk incelemesinde uygulanacak standardın sürümü, madde numarası ve kanıtı kaydedilmelidir.

## KiCad başlangıç kuralları

Kontrol kartı için 4 katman: F.Cu sinyal, In1.Cu kesintisiz GND, In2.Cu besleme/seyrek sinyal, B.Cu sinyal. 1.6 mm toplam kalınlık ve 35 µm bakır başlangıç hedefidir; gerçek dielektrik dizilim üreticiyle doğrulanır. Güç kartı bakır/katman yapısı akım ve termal hesap kapanmadan sabitlenmez.

- Genel bakır açıklığı 0.20 mm; sinyal iz alt sınırı 0.20 mm.
- Standart sinyal via dış çapı 0.60 mm, delik 0.30 mm; minimum annular ring 0.15 mm.
- Bakır–kart kenarı açıklığı 0.50 mm; mekanik montaj deliklerinde vida/pul zarfı ayrıca keepout olur.
- Baskı yazısı en az 1.0 mm yükseklik, 0.15 mm kalınlık; maske açıklığına en az 0.15 mm uzaklık. Pin1, polarite, konektör adı ve revizyon görünür olmalı.
- VBUS, fazlar ve anahtarlama düğümlerinin farklı potansiyellerle açıklık hedefi 1.00 mm. Entegre pin çıkışındaki zorunlu dar bölgeler genel istisna ile gizlenmez; üretici çizimine ve gerilim stresine göre tek tek incelenir.
- Lehim maskesi veya kaplama var diye açıklık azaltılmaz. Kirlilik, nem, rakım, malzeme CTI ve geçici gerilim koşulları belirlenmeden yalıtım uygunluğu iddia edilmez.
- Kapı sürme döngüleri kısa, dönüş yolu kaynak/Kelvin noktasına yakın; paralel MOSFET kolları simetrik. Şönt ölçüm hatları güç yolundan ayrı çift olarak taşınır.
- 90 A batarya ve 80 A faz RMS hedefi genel sinyal kurallarıyla taşınamaz. Güç yolları düzlem/bara kesiti, bağlantı daralmaları, via paylaşımı ve termal model üzerinden boyutlandırılır. Yalnız toplam bakır alanına bakılarak akım değeri verilmez.

## Şema çizim kabulü

Akış soldan sağa; beslemeler üstte, dönüşler altta. Güç bağlantıları, ölçüm ve lojik işlevler ayrı işlev grupları halinde gösterilir. Global etiketler aynı fiziksel kart içi bağlantıyı açıklayabilir; kartlar arası bağlantılar konektör ve pin tablosuyla ayrıca doğrulanır. Bağlantı noktası olmayan çizgi kesişimleri belirsiz bırakılmaz. NC işaretleri yalnız gerçekten kullanılmayan pinlerde bulunur.

Her sayfada belge/sayfa kimliği, revizyon, tarih ve tasarım durumu bulunur. Değerler birim ve toleransla; kritik kapasitörler gerilim/dielektrik, şöntler güç/Kelvin yönüyle gösterilir. Üretim BOM'unda tam MPN, üretici, footprint, DNP durumu ve muadil onay seviyesi bulunur. Sadece aile kodundan türetilmiş direnç MPN'si satın alma onayı sayılmaz.

## Üretime geçiş kapıları

1. Elektriksel kaynak → KiCad netlist pin eşleşmesi; iki kart arasındaki bütün sinyallerin tekil pin karşılığı; ERC hataları ve devre dışı kontrollerin değerlendirilmesi.
2. Her parçanın tam MPN, veri sayfası ve footprint pad numarası karşılaştırması. Eksik parça veya tahmini land pattern bulunmaması.
3. Tam yerleşim ve routing; sıfır açık bağlantı, kısa devre ve açıklık hatası. DRC istisnası gerekiyorsa konum, gerekçe ve onay kaydı. Hata sayısını azaltmak için kontrol bastırılmaz.
4. Güç döngüsü, gate/Kelvin geometrisi, ADC dönüşleri, konektör akımı, soğutucu izolasyonu ve DC-link kondansatör ripple hesabı incelemesi.
5. Üretici DFM, stackup, stencil, delik ve mekanik doğrulama; Gerber/drill çıktılarının yeniden görüntülenmesi ve şema–PCB–BOM sürüm eşleşmesi.
6. Akım sınırlı ilk enerji, yardımcı beslemeler, reset/fault/PWM kilidi, yüksüz motor, kademeli yük, VGS/VDS taşmaları, termal kararlılık ve BMS açılması/geri sürülme testleri.

İlk beş kapı fiziksel prototip siparişi içindir. Altıncı kapı ve kullanım ortamına özgü EMC/ürün güvenliği incelemesi tamamlanmadan seri üretim/3 kW performans onayı verilmez. Mevcut sistemde giriş koruma/ön şarj ve fren enerjisi yönetimi hâlâ açık tasarım işleridir.
