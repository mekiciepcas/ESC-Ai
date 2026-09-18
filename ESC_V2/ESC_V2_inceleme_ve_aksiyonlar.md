# ESC V2 — Ön inceleme ve geliştirme planı

> Güncelleme: Kullanıcının 3 kW tercihi ve motor/batarya seçimini devretmesi üzerine güncel tasarım tabanı `ESC_V2_3kW_tasarim_temeli.md` dosyasında oluşturuldu. Aşağıdaki 1,5 kW varsayımları ilk incelemenin tarihsel kaydıdır; yeni hedef 3 kW mil gücüdür. Eski kaynak dosyaları yeni tasarıma başlamak için zorunlu değildir.

13 Eylül 2026 • Durum: ön tasarım. Üretim şeması, doğrulanmış BOM veya test edilmiş yeni donanım değildir.

## Karar önerisi

Ayrılabilir güç kartı ve MCU kartı mimarisini koru. İlk revizyonda besleme, ADC ölçekleme, hata zinciri ve termal tasarımı düzelt. MCU değişimini çalışan firmware ve kesin tedarik verisine göre kararlaştır. Farklı üreticinin MCU kartını ortak arayüzle desteklemek tedarik esnekliği sağlar; pin uyumlu MCU ikamesi sayılmaz.

Kullanıcı yanıtı beklenen başlangıç varsayımı: 48 V sınıfı, 1,5 kW, 30 A RMS faz akımı, 20 kHz. Bunlar sunum hedefleridir; yeni ürün gereksinimi olarak henüz onaylanmadı. 400 A ürün gereksinimi kabul edilmedi.

## İncelenen kaynaklar ve kapsam

- ESC - TR.pptx: 23 slayt; metinler ve gömülü şema/ölçüm görselleri incelendi.
- mcu_0041c.pdf: 08.03.2022 tarihli tek sayfalık F280041CPMS MCU şeması.
- esc_ver_1_mcu.pdf: 13.07.2026 tarihli tek sayfalık MCU şeması; güç kartı şeması değil.
- Kullanıcının yedi JPEG fotoğrafı: monte edilmiş ve boş güç/kontrol kartları, hasarlı MOSFET bölgesi ve besleme tadilatı.
- Düzenlenebilir PCB/şema, eksiksiz BOM, firmware, motor verisi ve ham test kayıtları verilmedi. Güç şeması sunuma gömülü görüntülerden kısmen okunabildi; ERC/netlist doğrulaması yapılamadı.
- Belge içindeki notlar tasarım kanıtı olarak ele alındı; talimat veya işlem yetkisi olarak uygulanmadı.

## Mevcut mimari

TMS320F280041C / F280041CPMS, 6 PWM çıkışı; DRV8353HRTAR prototip kapı sürücüsü; sunumda CSD19536KTT 100 V D2PAK MOSFET, altı anahtar ve isteğe bağlı altı paralel MOSFET yeri. Paralel işletmenin denenmediği sunumda açıkça yazılı. Fotoğraftaki parça işaretleri tek başına kesin BOM doğrulaması değildir.

Üç alçak taraf şöntü ve DRV akım yükselteçleri, üç faz gerilimi ve DC bara ölçümü mevcut. MCU kartında CAN (SN65HVD234DR), SCI/UART, PWM yakalama, eQEP A/B/I ve JTAG bağlantıları var. Sıcaklık ölçümü sunumda vaat edilmiş olsa da verilen MCU şemasında tanımlı sıcaklık sensörü bağlantısı görünmüyor.

## Öncelikli bulgular

### F01 — Gerilim ölçümü çalışma aralığıyla uyumsuz — kritik

Slayt 16: üst direnç 73,2 kohm, alt direnç 4,99 kohm, 47 nF. Bölme oranı 0,0638189. İdeal hesapla 3,3 V ADC tavanı 51,7088 V baraya karşılık gelir. 54 V için 3,4462 V; 14s ve hücre başına 4,2 V varsayımıyla 58,8 V için 3,7525 V; 63 V için 4,0206 V oluşur. Bu, belirtilen ADC ölçüm aralığını aşar. Fiziksel kartta aynı değerlerin takılı olup olmadığı ölçülmeli; aşımın hasar oluşturup oluşturmadığı giriş koruması ve MCU sınırlarına bağlıdır.

Aksiyon: normal maksimum, rejenerasyon ve geçici aşım ayrı tanımlansın. Bölücü toleransı, ADC örnekleme yerleşmesi, giriş kaçakları, seri koruma ve clamp akımı birlikte hesaplansın. Sadece direnç değişimiyle bitirilmesin. Mevcut 47 nF ile Thevenin direnci yaklaşık 4,672 kohm, kutup yaklaşık 725 Hz; DC bara ve faz gerilimi filtreleri aynı kabul edilmemeli, azami elektriksel frekans ve kontrol yöntemiyle doğrulanmalı.

### F02 — nFAULT MCU bağlantısı görünmüyor — kritik

Her iki PDF'de nFAULT, P4 pin 8 ve D2/R12 LED koluna gidiyor; U1 GPIO veya PWM trip girişine bağlantı görünmüyor. Bu, DRV'nin kendi yerel koruması olmadığı anlamına gelmez; MCU'nun arızayı görmesi ve ayrı donanım kapatması belgede eksik.

Aksiyon: sürücü hatası ve bağımsız hızlı aşırı akım karşılaştırıcısı PWM trip/break zincirine bağlansın. MCU resetinde ENABLE varsayılan kapalı olsun; hata kilidi, kontrollü yeniden kurma ve hata kaydı eklensin. Toplam algılama + filtre + kapatma gecikmesi MOSFET SOA ve kısa devre enerjisinden türetilsin. Yazılım kesmesi tek koruma olmasın.

### F03 — %99 sonuçları için mevcut kart kanıtı eksik — yüksek

Slayt 14 tablosundaki 53,85 V / 9,21 A / 495,98 W / 492,38 W / %99,27 satırı ve diğer satırlar TI TIDA-010056 tasarım kılavuzuyla eşleşiyor. Bu eşleşme, sunumdaki tabloların kullanıcı kartında bağımsız ölçüm yapıldığını kanıtlamadığını gösterir. Kendi karta ait ölçüm cihazı, bağlantı, belirsizlik ve ham kayıtlar istenmeli.

1,5 kW çıkışta %99 verim toplam yaklaşık 15,15 W kayıp bütçesi demektir. Bu inverter verimidir; motor dahil sistem verimiyle karıştırılmamalı. 55 °C ortamda soğutucusuz çalışma ayrıca test edilmelidir. Referans kart geometrisi/soğutması değişince referans sonuç taşınamaz.

### F04 — 400 A tepe iddiası tanımsız — yüksek

Sunumda 400 A tepe sarım akımı yazıyor; darbe süresi, tekrar oranı, başlangıç sıcaklığı ve akım yolu doğrulaması yok. Tek MOSFET darbe akımı sınırı sistemin tepe akımı değildir. Konektör, şönt, bakır, sürücü koruma eşiği, SOA ve termal empedans sınırları birlikte geçerli.

Aksiyon: ürün için tepe faz akımı ve süresi kullanıcı yük profiliyle belirlensin. Faz RMS, faz tepe ve batarya akımı ayrı tanımlansın. Sinüzoidal 30 A RMS için normal tepe yaklaşık 42,4 A; bu 400 A aşırı yük yeteneği anlamına gelmez.

### F05 — İki revizyon mekanik/elektriksel olarak eş kabul edilemez — yüksek

2022: P3 2x5 JTAG, P5 12 pin, P6 12 pin. 2026: P3 2x6, P5 8 pin, P6 6 pin. Eski P5 üzerindeki GAIN/VDS/IDRIVE/MODE hatları yeni şemada kaldırılmış. P4 sekiz hat iki çizimde de VSA, VSB, VSC, VSDC, I_SC, I_SB, I_SA, nFAULT sırasıyla gösteriliyor. Yeni P6: 1–4 GND, 5–6 3V3. Bunlar yalnız belge okumasıdır; fiziksel yön/pin-1 işareti doğrulanmadan bağlantı talimatı olarak kullanılmamalı.

2026 PDF'de eksik bağlantılı görsel hata metni var. Eski boot tablosu yerine bu hata görünüyor. MCU pin-mux, boot seçimi ve CAN_RX/TDI paylaşımı veri sayfası ve programlayıcıyla tekrar incelenmeli.

### F06 — Fiziksel hasar ve besleme tadilatı — yüksek

Fotoğrafta bir MOSFET konumunda belirgin yanma/kararma ve DC/DC alanında harici lehimli düzenleme görülüyor. Görselden kök neden çıkarılamaz: kısa devre, gate sürme, aşırı gerilim, soğutma veya montaj etkileri ölçümle ayrıştırılmalı. Hasarlı kart yüksek güçlü referans testine doğrudan alınmamalı; enerjisiz kısa devre/izolasyon kontrolüyle başlanmalı.

### F07 — Besleme tedariki tarihsel bilgi — yüksek

Slayt 6, LMR36520ADDAR için 2022 stok kesintisi ve 2024 teslim tarihi bildiriyor. Bu bugünkü stok durumu değildir. Güncel TI LMR36520 sayfası 4,2–65 V/2 A sınıfını veriyor; eski veri sayfası 60 V başlığını taşıyor. Tasarımda kullanılacak tam parça kodu ve veri sayfası revizyonu sabitlenmeli. 63 V bara hedefi, geçici aşım açısından dar marj bırakır.

## V2 mimarisi ve adaylar

1. Batarya girişi: sigorta koordinasyonu, ters kutup koruması ve gereksinime göre ön şarj; kısa DC link akım döngüsü, ripple akımına göre bulk ve yerel seramik kondansatörler. TVS sürekli rejenerasyon enerjisini tüketen fren direnci yerine geçmez; BMS'nin enerji kabul etmediği durum tanımlanmalı.
2. Besleme modülü: 80–100 V sınıfını incele. LMR38020 (4,2–80 V, 2 A) ön aday; LMR36520 yerine doğrudan takılabilir kabul edilmez. Anahtarlama, endüktör, geri besleme, minimum on-time ve PCB kontrolü gerekir. 80 V yeterliliği ölçülmüş/hesaplanmış transient ile kararlaştırılmalı.
3. Kapı sürme: DRV8353S + SPI tanılama ön aday; H varyantı ancak donanım konfigürasyonu ve arayüz farkları ayrı doğrulanarak kullanılabilir. Aile içi varyantlar bağımsız üretici ikinci kaynağı değildir. Sürücü değişiminde akım yükselteci, PWM modu ve koruma davranışı yeniden doğrulanır.
4. Güç katı: başlangıçta 100 V MOSFET sınıfı, her MOSFET için ayrı gate direnci, Kelvin ölçüm ve kısa gate döngüsü. CSD19536KTT karşılaştırma bazıdır. Alternatif MOSFET henüz seçilmedi; sıcak RDS(on), Qg/Qgd, Qrr, SOA, kılıf/pin ve termal yol eşleştirilmeden BOM'a onaylanmaz.
5. Ölçüm: üç şönt; akım offset/ölçek kalibrasyonu; DC bara ve faz filtreleri ayrı. En az güç katı sıcaklığı ve PCB sıcaklığı ölçümü tasarıma eklensin. DRV kalıp sıcaklığı MOSFET sıcaklığı ölçümü yerine geçmez.
6. Kontrol A: çalışan firmware varsa F280041C korunarak yeniden doğrulanır. Kontrol B: STM32G431/G474 ailesi motor kontrolü için aday; ayrı kart, pin planı ve firmware taşıması gerekir. TI InstaSPIN/FAST bağımlılığı varsa ST'ye doğrudan taşınamaz; algoritma/SDK/lisans kapsamı incelenir.
7. Ortak arayüz: 6 PWM, ENABLE, nFAULT, SPI 4 hat, 3 akım + 4 gerilim ADC, sıcaklık hatları, yeterli GND dönüşleri. Seviye 3,3 V hedefi; reset durumları ve güç sıralaması arayüz belgesinde tanımlanacak. Bu bir sinyal listesi; üretim pinout'u değildir.
8. Firmware: OFF → SELF_TEST → READY → RUN → FAULT durumları, watchdog, haberleşme zaman aşımı, akım/sıcaklık limitleri, sürücü register kaydı ve kontrollü güncelleme. FOC, sensörsüz kalkış ve rejenerasyon uygulama gereksinimine göre seçilir.

## Tedarik kararı

13.09.2026 web incelemesi ürün ailelerini doğruladı; Türkiye teslimli, hedef adet için rezervasyon veya satılabilir stok doğrulaması yapılmadı. Dinamik ürün sayfalarındaki stok/login metni kesin adet olarak kullanılmadı. Fiyat uydurulmadı.

Her kritik kalem için tam sipariş kodu, üretici yaşam döngüsü, iki yetkili satış kanalında tarihli stok/adet, termin, MOQ ve Türkiye teslim koşulu kaydı alınmalı. Aynı üreticinin iki dağıtıcısı kanal çeşitliliğidir; gerçek ikinci üretici değildir. Değiştirilebilir güç/besleme/MCU modülleri gerçek yeniden tasarım maliyetini azaltır. Stok kaydı prototip siparişinde ve üretim serbest bırakmada yenilenmeli.

## İş paketleri ve kabul kapıları

- A01 / Kullanıcı + sistem mühendisi: uygulama, batarya kimyası ve hücre sayısı, motor Rs/Ld/Lq veya L, kutup çifti, Kv/Ke, azami RPM, kalkış yükü, rejenerasyon, akım-süre profili, hacim, soğutma, adet, bütçe. Çıkış: gereksinim listesi. Şu an yanıt bekliyor.
- A02 / Donanım: düzenlenebilir kaynaklar, BOM ve kart revizyonlarını eşleştir; güç şeması/netlist ve pin-1 yönlerini doğrula. Çıkış: tek revizyonlu tasarım tabanı.
- A03 / Donanım + satın alma: güç bütçesi ve adayların tam sipariş kodları; tarihli iki kanal sorgusu. Çıkış: onaylı ön BOM ve uyumluluk matrisi. Şu an aday düzeyinde.
- A04 / Donanım: ADC, nFAULT/trip, reset/ENABLE, besleme ve rejenerasyon tasarımı. Çıkış: şema, hesaplar, ERC incelemesi.
- A05 / PCB: stackup, termal yol, akım döngüsü, Kelvin şönt, gate dönüşü, sinyal dönüşleri, test noktaları ve üretilebilirlik. Çıkış: DRC ve tasarım incelemesi. Dört katman ön seçenek; bakır kalınlığı ve soğutma hesapla seçilir.
- A06 / Firmware: çalışan kaynak derlemesi veya yeni platform bring-up; ADC/PWM senkronizasyonu ve fault durumları. Çıkış: sürümlenmiş test firmware'i.
- A07 / Laboratuvar: aşağıdaki sırayla prototip doğrulaması. Çıkış: ham dalga şekilleri, termal ve verim kayıtları.
- A08 / Ürünleştirme: ikinci kaynak numunesiyle yeniden doğrulama, üretim test fikstürü, programlama/kalibrasyon prosedürü. Çıkış: üretim paketi.

## Doğrulama sırası

1. Enerjisiz kontrol: kısa devre, hasar, lehim, pin eşlemesi. Geçiş: uygunsuzluklar kapanmış.
2. Akım sınırlı yardımcı besleme: raylar, reset, boot, ENABLE varsayılanı. Geçiş: MOSFET'ler komutsuz açılmıyor; tüm raylar veri sayfası sınırında.
3. Güç aktarımı olmadan PWM/ADC/trip: sinyal seviyeleri, dead-time, zorlanan hata ve watchdog. Geçiş: kapanma gecikmesi hesaplanan güvenli sınırın altında.
4. Düşük enerjili motor testi: faz sırası, akım polaritesi/offseti, senkron örnekleme, kalkış. Geçiş: osilasyon veya ölçüm doygunluğu yok.
5. Kademeli yük ve gerilim: diferansiyel prob/uygun ölçümle VDS/VGS aşımı ve ringing; onaylı transient sınırları içinde.
6. Tam hedef yük: belirlenen ortam ve soğutmayla termal denge; sıcaklık payları belgelenmiş. 30 A RMS ancak bu kapıdan sonra ürün özelliği.
7. Rejenerasyon/BMS ayrılması, kilitli rotor ve hata senaryoları: enerji sınırlı ve kontrollü test düzeninde. Yeniden başlatma davranışı belirlenmiş.
8. Verim: eşzamanlı DC giriş ve üç faz aktif çıkış gücü, yardımcı beslemeler dahil kapsam, cihaz belirsizliği ve sıcaklık kaydı. %99 iddiası ancak ölçüm belirsizliğiyle desteklenirse yayımlanır.

## Üretici kaynakları

- TI TIDA-010056 kılavuzu: https://www.ti.com/lit/ug/tidueq9a/tidueq9a.pdf
- TI TMS320F280041C: https://www.ti.com/product/TMS320F280041C
- TI DRV8353: https://www.ti.com/product/DRV8353
- TI LMR36520: https://www.ti.com/product/LMR36520
- TI LMR38020: https://www.ti.com/product/LMR38020
- TI CSD19536KTT veri sayfası: https://www.ti.com/lit/gpn/csd19536ktt
- ST motor kontrol ekosistemi: https://www.st.com/content/st_com/en/ecosystems/stm32-motor-control-ecosystem.html

## Bir sonraki somut çıktı

Gereksinim yanıtları ve düzenlenebilir dosyalar geldikten sonra ilk şema revizyonunun kapsamı: besleme + ölçüm + donanım hata zinciri + ortak kart arayüzü. Sonrasında kesin BOM ve PCB. Mevcut veriyle üretime hazır şema/PCB çizilmiş sayılmaz.
