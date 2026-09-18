# ESC 3 kW — A2 mühendislik inceleme paketi

13 Eylül 2026. Açılacak dosya: `ESC_3kW_A2.kicad_pro`; ana şema: `ESC_3kW_A2.kicad_sch`. KiCad 10.0.6 ile kontrol edildi. A1 klasörü önceki revizyon olarak korunmuştur. A2, üretime verilmiş bir kart değildir.

## Bu revizyonda tamamlanan işler

- İşlevlere göre 29 sayfa; sayfa bazlı referans numaraları, Türkçe tasarım notları, hesap dayanakları ve kabul kriterleri.
- Üç yarım köprüde gerçek güç yolu, ayrı kapı dirençleri, gate-source pull-down bağlantıları ve Kelvin şönt gösterimi.
- Dört gerilim ölçüm kanalında kablolu bölücü, RC filtre ve diyot kelepçe gösterimi.
- Kartlar arası pin39'a eksik olan +5 V Hall beslemesi eklendi. Pin40 GND kaldı.
- Şönt için Bourns CSS4J-4026R-L500F seçildi. Fiziksel dört terminali modellemek için A1'deki yapay 0 ohm parçalar kaldırıldı. Sense ve güç yolları ayrı netler olarak kalır; fiziksel ortaklık şönt içindedir.
- DRV8353FSRTAR için üretici RTA0040B çiziminden yerel footprint oluşturuldu: 40 pin + EP41, 6 × 6 mm, 0.5 mm hatve, 4.15 mm EP. Stencil için dokuz pencere; termal via uygulaması PCB/montaj aşamasındadır.
- BAT54H,115 üretici kodu ve SOD123F footprint eşlemesi yapıldı.
- Standart dirençler YAGEO RC/RT seri kodlama kuralıyla belirtildi; tek tek sipariş edilebilirlikleri ve stokları henüz teyit edilmiş değildir. 100 nF kondansatörlerde üretimde olan TDK C2012X7R2A104K125AA seçildi. NTC'ler TDK NTCG203NH103JT1 olarak seçildi; B25/85 değeri 3650 K olduğundan eski B3435 varsayımı kaldırıldı.
- Beslemeler, arıza zinciri ve akım çıkışlarına 12 test noktası eklendi.
- KiCad'den dışa aktarılan netlist, bağlantı niyetiyle ayrı bir betikte karşılaştırıldı. Sonuçlar `../verification/a2_checks.json` dosyasında; kontrol betiği elektriksel modelin doğru olduğunu veya 3 kW performansı kanıtlamaz.

## Sabit tasarım hedefleri

Motor referansı Golden Motor HPM3000B 48 V, Hall geri beslemeli hava/fan soğutmalı varyanttır. Batarya başlangıç hedefi 13S8P Molicel P45B: 46.8 V nominal, 54.6 V tam dolu, 36 Ah tipik kapasite. Bunlar satın alınmış/doğrulanmış numuneler değildir.

Hedef 3 kW mil gücüdür. %88 motor ve %97 inverter verimi yalnız hesap varsayımıdır; batarya gücü yaklaşık 3.515 kW, 46.8 V'ta yaklaşık 75.1 A olur. Kontrolör batarya akımı hedef sınırı 90 A; faz akımı 80 A RMS boyutlandırma hedefi ve 120 A anlık yazılım sınırıdır. Faz akımı ile batarya akımı birbirine eşit değildir. 1.5 kW aynı kartın sınırlı doğrulama profili olarak tutulur.

## Arıza ve açılış sözleşmesi

1. MCU reset: PWM çıkışları düşük, RUN_REQUEST düşük, ARM_CLK düşük. TIM1 ana çıkış izni kapalıdır.
2. Beslemeler ve reset kararlı olduktan sonra sürücü RUN_REQUEST ile uyandırılır; altı PWM hâlâ düşüktür.
3. SPI üzerinden 6-PWM, CSA gain10 ve koruma kayıtları yazılır ve geri okunur. CSA ofsetleri sıfır akımda ölçülür. Sürücü bekleme süreleri kendi veri sayfasından uygulanır; keyfî gecikme sayısı kabul edilmez.
4. HARD_FAULT_N sağlıklı, komut nötr, Hall sırası geçerli ve ölçümler makul ise tek ARM yükselen kenarı verilir; LATCH_STATE geri okunur.
5. Ardından TIM1 çıkışları devreye alınır. Arıza oluştuğunda hem BKIN hem donanım latch devreye girer. Arıza kalkması otomatik tekrar başlatma nedeni değildir.

Latch sürücü ENABLE hattını kesmez: PWM'yi keser. Böylece sürücü kapandığında CSA çıkışlarının sıfıra inmesinden kaynaklanabilecek açılış kilidi önlenir. Rejenerasyon komutunun yazılımdan kapalı olması motorun dışarıdan döndürülmesiyle oluşan pasif geri beslemeyi engellemez.

## Fiziksel kart ayrımı

Güç kartında köprü, şönt, sürücü, yardımcı kaynaklar, fault karşılaştırıcıları, latch ve altı izin kapısı kalmalıdır. Kontrol kartında MCU, programlama ve haberleşme bulunur. 40 pinli arayüz birleşik sistem modelidir; iki fiziksel kart üretmek için PCB netlistleri ayrıca ayrılmalıdır. Analog sinyallerin konnektörden taşınmasındaki gürültü bütçesi ve toprak dönüşleri yerleşim incelemesinde değerlendirilir.

## Üretim öncesinde hâlâ açık olan işler

`release_register.json` açık işlerin sahibi, kapanış ölçütü ve durumunu içerir. `bom_open_items.json`, üretici kodu veya footprint alanı eksik her parçayı ayrı listeler. Bu alanlar sadece listeyi dolu göstermek için tahmini sipariş kodlarıyla doldurulmadı.

Özellikle giriş sigortası/ön şarj/ters kutup düzeni, fren enerjisi yönetimi, tam BOM, şönt ve yüksek akım terminal geometrisi, PCB, çalışan firmware ve fiziksel testler tamamlanmamıştır. Bunların tümünü “kapandı” diye işaretlemek doğru olmaz. A2 dosyası doğrudan fabrikaya gönderilmemelidir.

## Kontrollerin kapsamı

ERC varsayılan olarak `single_global_label`, `four_way_junction`, `simulation_model_issue`, `footprint_filter` kontrollerini kapalı tutar. Projeye özel ihlal istisnası eklenmedi. KiCad CLI'nin HKCU kayıt anahtarı uyarısı bu ortamda görülür; çıktı dosyaları ayrıca okunarak doğrulandı. ERC sonucu CAD bağlantı kurallarını kapsar; akım taşıma, termal, EMC, mekanik ve koruma gecikmesini kapsamaz.

## Yeniden üretim

Python ile sırasıyla `build_footprints.py`, `build_a2.py` çalıştırılır. Sonra KiCad CLI ile ERC ve netlist `../verification/erc_a2.json` ve `../verification/ESC_3kW_A2.net` yollarına çıkarılır; `verify_a2.py` çalıştırılır. A2 jeneratörü A1'in elektriksel tanımını okur; A1 şemasını yeniden yazmaz. Elle yapılan şema düzenlemeleri yeniden üretimde üzerine yazılabileceğinden elektriksel değişiklikler jeneratöre de işlenmelidir.

## Birincil kaynaklar

- [TI DRV8353F Rev B; RTA0040B mekanik çizimi dahil](https://www.ti.com/lit/ds/symlink/drv8353f.pdf)
- [Bourns CSS4J-4026 şönt veri sayfası](https://www.bourns.com/docs/product-datasheets/css4j-4026.pdf)
- [Nexperia BAT54H pin ve paket bilgisi](https://assets.nexperia.com/documents/data-sheet/BAT54H.pdf)
- [ST STM32G474RE pin/çevre birimi bilgisi](https://www.st.com/resource/en/datasheet/stm32g474re.pdf)
- [TI LM5164 Type-3 ripple ağı](https://www.ti.com/lit/ds/symlink/lm5164.pdf)
- [TI TLV1704](https://www.ti.com/lit/ds/symlink/tlv1704.pdf), [SN74LVC1G74](https://www.ti.com/lit/ds/symlink/sn74lvc1g74.pdf)
- [YAGEO RC seri kodlama ve sınırlar](https://www.yageogroup.com/content/datasheet/asset/file/PYU-RC_GROUP_51_ROHS_L), [RT 49.9k örnek üretici föyü](https://yageogroup.com/component-documentation/download/specsheet/RT0805BRD0749K9L)
- [TDK 100 nF / 100 V kondansatör](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C2012X7R2A104K125AA), [TDK NTC değerleri](https://product.tdk.com/en/search/sensor/ntc/chip-ntc-thermistor/info?part_no=NTCG203NH103JT1)
