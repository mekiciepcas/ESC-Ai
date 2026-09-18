# Otonom yürütme ve anti-halüsinasyon politikası

Tarih: 19.09.2026
Branch: `uav-rebaseline`
Amaç: ESC geliştirmesinin kullanıcıdan sürekli komut beklemeden, ancak kanıt zincirini bozmadan ilerlemesini sağlamak.

## 1. Çalışma döngüsü

Her otonom çalıştırmada sırayla:

1. `START_HERE.md`, `design_basis.json`, `planning/UAV_PRODUCT_PLAN.md`, `planning/uav_backlog.json`, `planning/UAV_TRACEABILITY.md` ve bu dosya okunur.
2. En yüksek öncelikli **UNBLOCKED** iş seçilir.
3. İşin gerektirdiği girdilerin kaynağı doğrulanır.
4. Hesap / araştırma / kod / şema incelemesi yapılır.
5. Çıktı bir kanıt dosyasına bağlanır.
6. Backlog durumu ve varsa karar kaydı güncellenir.
7. Değişiklik yalnız `uav-rebaseline` branch'ine commit edilir.
8. Bir sonraki iş, dependency ve gate durumuna göre seçilir.

## 2. İlerleme tetikleyicileri

Aşağıdaki koşullarda otonom olarak ilerlenebilir:

- gerekli girdi repo içinde veya doğrulanabilir kamu kaynağında mevcutsa,
- hesap deterministik olarak yapılabiliyorsa,
- simülasyon/model sonucu fiziksel test sonucu gibi sunulmuyorsa,
- değişiklik geri alınabilir ve izlenebilir ise,
- sonraki gate'in kabul kriterleri açıkça tanımlıysa.

Öncelik sırası:

`P0 safety/system > P0 electrical > P0 verification > P1 architecture > P1 implementation > documentation/cleanup`

Aynı öncelikte önce dependency zincirini açan iş yapılır.

## 3. Zorunlu durma tetikleyicileri

Aşağıdaki durumlarda sayı veya sonuç uydurulmaz; ilgili iş **BLOCKED** yapılır:

- kullanıcının ürün tercihi gerekli ise,
- fiziksel ölçüm/test sonucu gerekli ise,
- motor/propeller datasheet veya güvenilir test verisi bulunamıyorsa,
- mekanik kütle/MTOW gibi sistem girdisi bilinmiyorsa ve makul aralık dahi kaynağa bağlanamıyorsa,
- güvenlik açısından kritik bir sınır yalnız varsayımla belirlenebiliyorsa,
- gerçek komponent footprint/pinout doğrulanamıyorsa,
- fiziksel termal/EMI performansı ancak prototip ölçümüyle kapanabilecek durumdaysa,
- üretim release / uçuş yeterliliği / sertifikasyon sonucu isteniyorsa fakat kanıt yoksa.

## 4. Anti-halüsinasyon kuralları

- Kaynaksız spesifik sayı ürün gereksinimi yapılamaz.
- Bilinmeyen değer `null`, `OPEN`, `TBD` veya açık varsayım olarak tutulur.
- Tahmin ile ölçüm aynı statüde gösterilmez.
- Simülasyon sonucu `SIMULATED`; fiziksel test sonucu `MEASURED`; datasheet sonucu `DATASHEET`; mühendislik varsayımı `ASSUMPTION` etiketi taşır.
- Eski B1/A2 değeri yalnız tarihsel referans olduğu açıkça belirtilmeden yeni UAV baseline'a taşınmaz.
- ERC/DRC sıfır olması fonksiyonel doğrulama sayılmaz.
- Datasheet maksimum rating tasarım çalışma noktası kabul edilmez.
- Web stok bilgisi tedarik garantisi sayılmaz.
- Bir hesapta giriş değeri değişirse bağımlı sonuçlar yeniden üretilir.
- Çelişen iki kaynak varsa daha yeni olan otomatik kazanmaz; üretici verisi, revizyon, test koşulu ve applicability karşılaştırılır.

## 5. Kanıt sınıfları

Her kapanan kritik iş en az bir kanıta bağlanır:

- `REQ` — gereksinim kaydı
- `SRC` — üretici/datasheet/kaynak veri
- `CALC` — hesap
- `SIM` — simülasyon
- `ERC/DRC` — statik elektrik/PCB kontrolü
- `CODE` — derlenen/test edilen yazılım
- `MEAS` — fiziksel ölçüm
- `TEST` — tanımlı kabul kriterli test sonucu

Bir iş yalnız gerekli kanıt sınıfı mevcutsa `DONE` olabilir.

## 6. Gate davranışı

- **G0:** mission/mass zarfı kapanmadan thrust sizing freeze edilmez.
- **G1:** propulsion + battery + ESC electrical envelope kapanmadan power-stage/BOM freeze edilmez.
- **G2:** semiconductor/protection/thermal hesapları kapanmadan güç şeması release edilmez.
- **G3:** firmware timing/fault mimarisi kapanmadan güç verme testine geçilmez.
- **G4:** footprint/pin/BOM doğrulanmadan nihai PCB routing kabul edilmez.
- **G5:** sıfır unrouted + kritik DRC/DFM kapanmadan üretim paketi oluşturulmaz.
- **G6:** bench ve propulsion standı testleri geçmeden uçuş denemesi doğrulama adımı sayılmaz.
- **G7:** kullanıcı açıkça istemeden `main` merge, üretim release veya flight-qualified iddiası yapılmaz.

## 7. GitHub yazma politikası

Otonom çalışma sırasında:

- `main` branch'e yazılmaz.
- A2/B1 tarihsel kanıtları silinmez.
- Binary üretim çıktıları gereksiz yere yenilenmez.
- Aynı dosya eşzamanlı iki iş tarafından değiştirilmez.
- Her commit tek bir anlamlı değişiklik grubunu temsil eder.
- Backlog/evidence güncellemesi teknik değişiklikle aynı veya takip eden committe yapılır.

## 8. Kullanıcıya raporlama

Her otonom koşuda yalnız anlamlı ilerleme veya blokaj raporlanır.

Rapor formatı:

- `YAPILDI`: tamamlanan iş ve commit/evidence
- `DOĞRULANDI`: hangi hesap/kaynak/test ile
- `AÇIK`: sıradaki iş
- `BLOCKED`: gerekiyorsa kullanıcıdan/gerçek dünyadan ihtiyaç duyulan tekil girdi

İlerleme yoksa sahte aktivite üretilmez.

## 9. Fiziksel güvenlik sınırı

Masaüstü analiz; üretim, uçuş veya insan yakınında çalışma onayı değildir. İlk enerjilendirme düşük gerilim ve akım sınırlı yapılmalı; pervane ilk elektronik bring-up sırasında takılı olmamalı; yüksek güçlü motor/prop testleri fiziksel muhafaza ve uygun test düzeneğiyle gerçekleştirilmelidir.
