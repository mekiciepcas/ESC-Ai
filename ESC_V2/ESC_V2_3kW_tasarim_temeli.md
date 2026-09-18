# ESC V2 — 3 kW tasarım temeli, A0

**A2 güncellemesi:** Bu dosya başlangıç kararlarının tarihçesidir. Güncel şema `hardware_a2/ESC_3kW_A2.kicad_pro` ve karar kaydı `hardware_a2/README.md` dosyasındadır. A2'de MCU STM32G474RET3, sürücü DRV8353FSRTAR, yardımcı kaynak LM5164DDAT; bölücü üst kolu 2 × 49.9k olmuştur. Güncel sayısal temel `design_basis.json` dosyasındadır.

13 Eylül 2026. Kullanıcı 3 kW hedefini ve motor/batarya seçiminin tarafımızdan yapılmasını yetkilendirdi. Bu belge ön tasarım kararlarını sabitler; şema, üretim BOM'u, firmware veya doğrulanmış ürün değildir. Önceki inceleme raporundaki 1,5 kW başlangıç varsayımının yerini alır.

## Seçilen yön

3 kW **motor mil gücü** hedefiyle devam ediyoruz. ESC elektriksel çıkışı için yaklaşık 3,4 kW bütçe ayırıyoruz. 1,5 kW çalışmayı aynı kartın sınırlanmış çalışma profili olarak tutuyoruz. Yeni bir düşük maliyetli 1,5 kW kart varyantı şu anda tasarlanmıyor.

Uygulama belirtilmediğinden geliştirme tabanını test tezgâhı ve genel amaçlı yer tipi tahrik olarak seçtik. Hafif uçuş ESC'si, pervane uygulaması veya araçta kullanım onayı anlamına gelmez. Seçilen motorun ağırlığı ve batarya kapasitesi bu başlangıç kullanımına göredir.

## Motor seçimi

Referans motor: **Golden Motor HPM3000B, 48 V sargı, hava/fan soğutmalı 3 kW sınıfı**. Üretici 48/72 V seçenekleri, 2–3 kW nominal sınıf ve 3000–5000 rpm aralığı yayımlıyor. 48 V performans eğrisi 4000 rpm nominal ve 85 A nominal akım etiketi taşıyor. Bu 85 A değeri doğrulanmış faz RMS akımı olarak kullanılmadı. Referans hesap noktası 4000 rpm; 3 kW mil gücünde tork yaklaşık 7,16 Nm.

Hall geri beslemeli varyant satın alma şartına alınacak; Hall bağlantısı, gerilim seviyesi ve sırası üretici/numuneyle doğrulanacak. İlk kontrol yöntemi Hall destekli FOC; sensörsüz çalışma sonraki yazılım özelliği. Mil hızı tüm batarya gerilimlerinde aynı kalmayacak. 3 kW sürekli çalışma, motorun nominal hız/soğutma bölgesinde hedefleniyor; düşük devirde aynı gücü zorlamayacağız.

Motorun faz direnci, Ld/Lq veya faz endüktansı, kutup çifti, Ke ve Hall açısı henüz bilinmiyor. Başka sargı varyantının verileri kopyalanmayacak. Bu değerler numune tanımlama testinde ölçülecek; FOC kazançları, elektriksel hız limiti ve nihai faz akımı buna göre ayarlanacak. Satıcıdaki stok ve tam varyant henüz doğrulanmadı.

Kaynaklar: [Üretici ürün ve çizim sayfası](https://www.goldenmotor.com/eCar/frame-eCar.htm), [48 V motor performans eğrisi](https://www.goldenmotor.com/hubmotors/hubmotor-imgs/HPM3000-48V3KW%20Curve.pdf). Eğri 2014 tarihli; güncel satın alınan motorun aynı özellikte olduğu teyit edilmeli.

## Batarya seçimi

Referans paket: **13S8P Molicel INR21700-P45B**, paket üreticisi tarafından tamamlanmış ve test edilmiş olarak tedarik edilecek.

- 104 hücre; 46,8 V nominal, 54,6 V tam dolu.
- Tipik 36 Ah ve 1,685 kWh. Hücre minimum kapasitesi kullanılırsa 34,4 Ah; kullanılabilir enerji bunlardan daha düşüktür.
- Paket sürekli deşarj yeteneği hedefi 100 A; ESC normal batarya akımı tavanı 90 A.
- 13S BMS için 120 A sürekli sınıf başlangıç satın alma şartı. Bu değer tek başına uygunluk kanıtı değil; kapalı muhafazada termal test, kablolar, bağlantılar, sigorta ve kesme davranışı birlikte doğrulanacak.
- Şarj cihazı: 54,6 V CC/CV, başlangıçta 5 A. BMS/hücre sıcaklığına bağlı şarj izni gerekli.
- ESC tasarım işletme aralığı 39–54,6 V. 44 V altında güç azaltımı; 39 V nominal yazılım durdurma eşiği taslak. BMS ayrıca hücre bazında sınırlar; paket toplam gerilimi tek hücre koruması yerine geçmez.
- İlk prototipte komutlu rejeneratif frenleme kapalı. BMS'nin ters enerji kabulü ve dolu batarya durumu çözüldükten sonra açılacak. Kapalı PWM'de dahi dönen motorun diyotlar üzerinden barayı yükseltmesi mümkün; aşırı gerilim/enerji yönetimi donanım incelemesinde kalıyor.

P45B veri sayfası hücre başına 3,6 V, 4,5 Ah tipik, 4,2 V şarj bilgisi veriyor. 45 A deşarj değeri 80 °C kesme koşuluna bağlı; paket akımını 8 × 45 A kabul etmiyoruz. 90 A paket akımında hücre başına 11,25 A düşer.

Isı ön kontrolü: veri sayfasındaki 15 milliohm tipik DC dirençle hücrelerin eşdeğer paket direnci yaklaşık 24,4 milliohm. 75 A'da yaklaşık 137 W; 90 A'da yaklaşık 197 W hücre kaybı çıkıyor. Bu kaba, SOC/sıcaklık/yaşlanmaya bağlı hesap bağlantı ve BMS kayıplarını içermez. Paket termal yönetimi ve güç azaltımı tasarım gereksinimidir. 100 A sürekli kabiliyeti bu hesapla kanıtlanmış değildir.

Kaynak: [Molicel P45B veri sayfası, v1.4](https://www.molicel.com/wp-content/uploads/INR21700P45B_1.4_Product-Data-Sheet-of-INR-21700-P45B-80109.pdf). Bu seçim paket mimarisidir; hücre montaj talimatı veya belirli bir hazır paketin uygunluk onayı değildir.

## Güç ve akım hesabı

Boyutlandırma varsayımları: motor verimi %88, inverter verimi %97. Bunlar ölçüm sonucu veya garanti değildir. Nominal gerilim yerine yük altında ESC terminal gerilimi kullanılmalıdır.

- 3 kW mil çıkışı → yaklaşık 3409 W motor elektrik girişi → 3515 W batarya terminal gücü.
- 54,6 V: yaklaşık 64,4 A; 46,8 V: 75,1 A; 44 V: 79,9 A; 39 V: 90,1 A.
- İnverter kayıp tahmini: yaklaşık 105 W. Motor ve batarya kayıpları bu sayıya dahil değil.
- Tipik paket enerjisiyle teorik tam yük süresi yaklaşık 29 dakika. Gerilim düşümü, kullanılabilir SOC, sıcaklık ve paket kayıpları nedeniyle gerçek süre daha kısa; menzil vaadi değildir.
- 1,5 kW mil hedefi aynı varsayımlarla yaklaşık 1757 W batarya gücü, 46,8 V'ta 37,5 A gerektirir. Düşük yükte gerçek verimler değişir.

Batarya akımı faz akımına eşit değildir. Güç katı ön boyutlandırması 80 A RMS faz akımına göre; normal sinüs tepesi 113 A. Başlangıç anlık faz yazılım tavanı 120 A hedefi, ripple ve kontrol taşması nedeniyle 80 A RMS'e çok az pay bırakır: gerçek ripple görüldüğünde RMS sınırı düşürülecek veya donanım yeniden boyutlandırılacak. Bu hedef motorun o akımı sürekli kabul ettiğini göstermez. İlk test akımları çok daha düşük tutulur. 400 A hedefi kaldırılmıştır.

## Elektronik mimari

**Kontrol kartı:** STM32G474RET6 ön seçimi; yeni geliştirmede mevcut C2000 firmware'ine bağımlılık olmayacak. Motor kontrol PWM/ADC kaynakları, fault/break, Hall timer, CAN, UART ve SWD pinleri şema aşamasında doğrulanacak. FOC için ST motor kontrol ekosistemi kullanılabilir; özel güç kartı uyarlaması ve sürüm/lisans kontrolü gerekir. Ortak arayüz ikinci MCU kartına açık kalacak.

**Kapı sürücü:** DRV8353SRTAR ön seçimi, SPI tanılama. Üç şönt yükselteci ve 6 PWM kontrol. Eski H sürümüyle yazılım/pin fonksiyonları aynı sayılmayacak. nFAULT MCU fault/break yoluna, ENABLE varsayılan kapalı donanımına bağlanacak. VDS koruması yanında hızlı akım kesme yolu bulunacak; eşikler ve gecikmeler MOSFET SOA ile hesaplanacak, henüz sayısal donanım trip eşiği serbest bırakılmadı.

**Güç katı:** üç yarım köprü, anahtar başına iki paralel 100 V MOSFET, toplam 12 adet başlangıç mimarisi. Her MOSFET'e ayrı gate direnci ve dengeli güç/gate dönüş yolu. İlk aday karşılaştırma bazı CSD19536KTT; kesin MOSFET kodu stok, sıcak RDS(on), Qg/Qgd, Qrr, SOA ve soğutma karşılaştırmasından sonra seçilecek. 12 MOSFET zorunlu nihai adet değil; kayıp ve tedarik sonucu altı daha güçlü MOSFET de değerlendirilebilir.

**PCB ve mekanik:** güç kartında ilk yerleşim zarfı yaklaşık 120 × 90 mm; dört katman ve yüksek akım için bakır güç bağlantıları/bara imkânı. Boyut, bakır kalınlığı ve akım taşıma henüz doğrulanmadı. Alüminyum soğutucu, elektriksel izolasyon ve zorlanmış hava başlangıç gereksinimi. Farklı elektriksel düğümlerdeki MOSFET tabları ortak soğutucuya doğrudan kısa devre edilmemeli.

**Besleme:** LM5164 ailesi, 100 V giriş sınıfı, 12 V ara ray için ön seçim; 12→5 V buck ve 5→3,3 V analog/dijital raylar. Fan akımı yardımcı güç bütçesine dahil edilecek; 1 A ray kapasitesi yetmezse ayrı fan beslemesi seçilecek. DRV VM/VDRAIN besleme düzeni kendi veri sayfasına göre kurulacak. LMR38020 alternatif besleme modülü olabilir; pin uyumlu ikame kabul edilmez.

**Giriş:** DC kesme kapasitesi uygun sigorta, ön şarj, bağlantı/kontaktör seçimi, ters kutup ve transient koruması. 100 V kondansatör sınıfı başlangıç tercihi; kapasite/ripple, kablo endüktansı ve rejenerasyon hesabıyla seçilecek. Fren direnci/chopper ihtiyacı mekanik atalet ve geri sürme enerjisi görülmeden iptal edilmeyecek. TVS sürekli fren enerjisi tüketmez.

Kaynaklar: [STM32G474RE](https://www.st.com/en/microcontrollers-microprocessors/stm32g474re.html), [DRV8353](https://www.ti.com/product/DRV8353), [LM5164](https://www.ti.com/product/LM5164). Bu ürün aileleri doğrulandı; hedef adet ve Türkiye teslimli stok henüz doğrulanmadı.

## Ön analog boyutlandırma

DC bara bölücü: üst toplam 100 kohm (seri iki 49,9 kohm veya tolerans hesabıyla uygun toplam), alt 3,32 kohm ön değer. Hesapta ideal üst 100 kohm kullanıldı. 54,6 V → 1,754 V, 80 V → 2,571 V. ADC tam ölçeği yaklaşık 102,7 V; bu kartın 102,7 V çalışma onayı değildir. Direnç toleransı, gerilim katsayısı, seri koruma, ADC örnekleme süresi, clamp ve açık-devre arızası analiz edilecek. Faz gerilimi ve DC filtreleri ayrı boyutlandırılacak.

Üç alçak taraf şöntü: kanal başına 0,5 milliohm Kelvin tip ön değer. Kazanç 10 V/V ve 1,65 V merkez varsayımıyla ±150 A → 0,90–2,40 V; 12-bit/3,3 V ADC'de ideal yaklaşık 0,161 A/LSB. Gerçek referans, sürücü yükselteci çıkış aralığı, offset ve bant genişliği doğrulanacak. Şönt kaybı low-side iletim penceresine bağlı; 80 A sürekli akımın şöntte bulunduğu üst sınır hesabı 3,2 W/şönt. Sürekli ve pulse güç için ayrı pay bırakılacak. Üç şönt akım yeniden oluşturması, yüksek modülasyonda örnekleme penceresiyle doğrulanacak.

En az MOSFET/soğutucu, PCB ve motor sıcaklık kanalları ayrılacak. Motor sensör tipi NTC varsayılmayacak; teslim edilen motorun sensörüyle eşleştirilecek. CAN/UART/PWM ve Hall hatları için ESD, filtre ve doğru seviye dönüşümü planlanacak.

## 3 kW ek iş değerlendirmesi

MCU, temel FOC ve haberleşme geliştirmesi 1,5 kW ile büyük ölçüde aynı. Ek iş; paralel MOSFET akım paylaşımı, gate sürme, bakır/kablo/konnektör boyutlandırması, şönt ve kondansatör ripple, soğutucu ve yük testidir. Aynı dirençte akım iki katına çıktığında iletim kaybı dört katına çıkar; yalnız yazılım gücünü artırmak yeterli değil.

Örnek: sıcak MOSFET direnci 4 milliohm/adet varsayılırsa, anahtar başına iki paralel MOSFET ile üç faz toplam iletim kaybı 3 × 80² × 0,004 / 2 = 38,4 W. Bu; anahtarlama, diyot, gate, şönt, PCB ve yardımcı besleme kayıplarını içermez.

Soğutma ön bütçesi 120 W. 40 °C ortamda soğutucu tabanını 80 °C altında tutmak için soğutucu-ortam termal direnci en fazla yaklaşık 0,33 K/W. MOSFET birleşiminden soğutucuya ve izolasyon padine ek sıcaklık artışı ayrıca hesaplanacak. Bu, soğutucusuz 3 kW hedefinden vazgeçmek için yeterli gerekçedir. 55 °C ortamda güç azaltımı beklenir; kesin eğri testle çıkarılır.

Sonuç: 3 kW hedefini korumak uygun. 1,5 kW'a dönmek temel yazılım işini ortadan kaldırmaz; güç katı ve test maliyetini azaltır. Fiyat teklifi/iş programı olmadan yüzde maliyet veya süre artışı verilmiyor.

## Gerçekleştirilen işler ve sıradaki mühendislik kapısı

- Motor/batarya sınıfı, güç tanımı, çalışma aralığı, soğutma yaklaşımı ve kontrol MCU adayı seçildi.
- design_basis.json makine tarafından okunabilir tasarım girdilerini, calculate_design.py tekrar hesaplamayı, calculated_budget.json sonuçları içerir.
- Üç tutarlılık kontrolü çalıştırıldı: ADC ön aralığı, 44 V'ta batarya akımı bütçesi, sinüs tepe/RMS ilişkisinin yazılım sınırıyla uyumu. Bunlar devre simülasyonu veya laboratuvar testi değildir.
- Sonraki kapı: tam parça kodları ve tedarik matrisi, motor pin/sensör teyidi, net bağlantılı şema, MCU pin-mux ve yardımcı besleme bütçesi. Sonra ERC, PCB/DRC, firmware ve prototip testleri.
- Eski Altium dosyaları yeniden tasarımın başlaması için zorunlu değil. Geldiğinde eski kartla uyumluluk analizi yapılabilir; yeni kart eski konnektörlere doğrudan takılabilir ilan edilmiyor.
- Nihai üretim onayı motor tanımlama, gerilim aşımı/kısa devre koruması, termal denge, EMC ve ikinci kaynak testlerini bekler.
