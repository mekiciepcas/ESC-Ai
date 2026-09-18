# Sprint 1 — uygulama kaydı

Revizyon RUN-01 · 14.09.2026 · Kaynak: B1 şema / PLAN-01 backlog.

## ESC-01: çalışma zarfı tasarım kararı

Kapsam, tezgâh ve genel kara tahriki prototipidir; hava aracı veya güvenlik bütünlüğü sertifikasyonu kapsamı değildir. Referans 13S8P batarya, 46.8 V nominal / 54.6 V dolu; referans motor HPM3000B 48 V Hall varyantı. Tam motor parametreleri ESC-19'da ölçülecek. Bunlar mevcut numune veya satın alınmış ürün anlamına gelmez.

İlk doğrulama sınıfı 1.5 kW mil gücü, ikinci sınıf 3 kW mil gücüdür. İkisi de tanımlı çalışma zarfında sürekli çalışma hedefidir; ayrıca bir kısa süreli aşırı yük/boost hakkı tanımlanmamıştır. İlk yük kabul testi, en az 60 dakika VE son 15 dakikada sıcaklık eğimi mutlak 0.2 °C/dakikadan küçük olana kadar sürer. Test akım/gerilim/sıcaklık sınırına ulaşırsa durdurulur; bu kriterin geçmesi ömür veya seri ürün yeterliliği sayılmaz.

Başlangıç sınırları: batarya 90 A, faz boyutlandırma 80 A RMS, anlık yazılım hedefi 120 A, ölçüm aralığı ±150 A. 80 A RMS sinüsün tepesi 113.1 A'dır; PWM ripple ve kontrol taşması için gerçek marj testle doğrulanacak. Donanım trip eşiği ve gecikmesi ayrıca hesaplanıp ölçülür; 120 A yazılım limiti kısa devre koruması değildir.

Referans 4000 rpm'de 3 kW için 7.162 Nm, 1.5 kW için 3.581 Nm tork sınırı başlangıç hedefidir. Daha düşük devirde sabit güç istenmez; tork sınırı gücü azaltır. Bu, kalkış torkunun yeterliliği veya motorun izin verilen azami devri konusunda kanıt değildir. Azami hız ve komütasyon sınırı numune verisiyle ESC-19/ESC-21'de tamamlanmadan yüksek devir denemesi yapılmaz.

Gerilim azaltma katsayısı: 39 V ve altında sıfır; 39–44 V arasında (V−39)/5; 44–54.6 V arasında bir. 54.6 V üstünde tork komutu sıfır. Düşük gerilim sonrası yeniden izin eşiği 40 V; yeniden başlatma mevcut arıza durum makinesinin izin akışına tabidir. Bu eşikler ölçüm toleransı incelemesi sonrası firmware'e aktarılır.

Nominal ortam 40 °C. Kalibre edilmiş taban plakası sıcaklığı 70 °C'ye kadar tam termal katsayı; 70–80 °C arası (80−T)/10; 80 °C ve üzerinde sıfır tork komutu. MOSFET/PCB NTC okuması doğrudan taban plakası sıcaklığı kabul edilmez: ilişki ESC-11/ESC-20'de ölçülmeli veya ayrı sensör eklenmeli. Eklem ve diğer eleman sıcaklık sınırları yine bağımsızdır. Daha yüksek ortam için tam güç iddiası yoktur.

Komut tavanı: seçili güç sınıfı × gerilim katsayısı × termal katsayı, DC güç bütçesi ve tork×açısal hız sınırlarının en küçüğü. Verim bütçeleri motor 0.88, inverter 0.97 varsayımıdır; 3 kW için yaklaşık 3515 W batarya gücü gerekir. Aktif rejenerasyon ilk devreye almada kapalıdır; pasif geri sürülme enerjisi ESC-04 kapanmadan güvenli kabul edilmez.

`sprint1_envelope.py` bu mühendislik modelini hesaplar; firmware değildir. `envelope_checks.json` 128 çalışma noktası ve 9 kontrol içerir. Sensör geçersizliği, düşük gerilim, termal azaltma ve düşük devir sınırı kapsanmıştır. Histerezis/zamanlama kontrolü firmware durum makinesinde ayrıca uygulanacak.

## Gözden geçirme DR-001 — iyileştirme kararları

Tür: Codex tarafından yapılan masa başı tasarım incelemesi. Kullanıcı/üretici katılımlı toplantı yapılmadı; katılımcı veya onay uydurulmadı. Proje yöneticisi ve uygulama bakış açıları aynı ajan tarafından değerlendirildi; bağımsız teknik onay yerine geçmez.

- **F-01 — revizyon tutarsızlığı:** güncel şema B1 iken ana tasarım temeli A2 idi. Karar D-01: önceki dosyayı koruyup B1 çalışma zarfını ana temele ekle; izlenebilirliği sağla. Kapanış: arşiv ve güncel JSON karşılaştırması.
- **F-02 — tamamlanmamış standart incelemesi:** özel şema sembollerinin tümü normatif grafiklerle karşılaştırılmadı. Bu bir kesin madde ihlali tespiti değil, uygunluk kanıtı açığıdır. Karar D-02: ESC-05 açık kalır; sembol bazlı geometri/polarite kontrolü ve erişilemeyen standart maddeleri kaydedilmeden kapanmaz.
- **F-03 — plan ilerlemesinin iki dosyada tutulması:** Markdown görünümü elle güncellenirse JSON ile ayrışabilir. Karar D-03: backlog tek kaynak, yol haritası güncel durumlardan üretilir. Tamamlandı işaretleri kanıt yollarıyla oluşturulur.
- **F-04 — sıcaklık ölçüm yeri belirsizliği:** termal taban plakası hedefi, PCB NTC ile doğrudan aynı sayı değildir. Karar D-04: ESC-11'e sensör/termal korelasyon veya ek taban sensörü işi; ESC-20'ye doğrulama ekle. Fiziksel kanıt gelene kadar bulgu açık.

Toplantı gerektiren karar eşiği: doğrulanmış güç sınıfını düşürme, motor/batarya kapsam değişikliği, üretim siparişi veya çözülmemiş teknik çelişki. Bu durumda ilgili hesap/çizim ve seçenekler kullanıcıya sunulur, karar kaydı yanıtla tamamlanır. Rutin belge ve tasarım düzeltmeleri mevcut yetkiyle ilerler. Otomatik toplantı veya dış iletişim oluşturulmadı.

## Sonraki uygulama sırası

ESC-01 tasarım tanımı tamam; fiziksel performans onayı değil. ESC-05 standart incelemesi sürüyor. ESC-03 giriş koruma/ön şarj hesabı sıradaki uygulama işi. ESC-04 enerji yönetimi, ESC-02 numune planı ve tedarik belirsizliği görünür tutulur. Satın alma/ölçüm yapılmadan teslim süresi veya gerçek numune parametresi varsayılmaz.
