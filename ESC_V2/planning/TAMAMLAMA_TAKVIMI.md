> 15.09.2026 kullanıcı kararı: Aşağıdaki tarihler yalnız planlama referansıdır. Hazır işler tarih beklemeden kapasite dahilinde yapılır; sonraki aşamaya geçiş test ve kabul kanıtına bağlıdır.

## 15 Eylül PoC öncelik güncellemesi

İlk teslim hedefi kontrol PoC: besleme/programlama/temel arayüzler. Sonraki iki uygulama paketi MCU besleme yolları ve reset/SWD/clock bağlantılarıdır. Tamamlanma; kalan routing, aday kılıflar ve numune testine bağlıdır. Eski 3 kW tarihleri garantiye dönüşmez; 21 Eylül değerlendirmesinde PoC gerçekleşmesine göre yeniden planlanacak.

# ESC tamamlama takvimi — CAL-01

Başlangıç 14 Eylül 2026; saat dilimi Europe/Istanbul. Tarihler ilk plan hedefidir, teslim garantisi değildir. Kullanım limitlerinden kesin mühendislik kapasitesi çıkarılamaz; ilk haftanın gerçekleşen işleriyle 21 Eylül'de bu dosya yeniden değerlendirilecek. Dış test/tedarik gecikmeleri sonraki kapıları kaydırır.

- **14–27 Eylül / Sprint 1:** ESC-01–05; çalışma zarfı, giriş/enerji yönetimi ve çizim incelemesi. Hedef kapanış 27 Eylül.
- **28 Eylül–11 Ekim / Sprint 2:** ESC-06–11 ve ESC-26; BOM, korumalar, mekanik/termal kararlar. Hedef tasarım sabitleme 11 Ekim.
- **12–25 Ekim / Sprint 3:** ESC-12–15; iki kart yerleşimi, routing ve firmware temeli. Hedef PCB inceleme adayı 25 Ekim.
- **26 Ekim–8 Kasım / Sprint 4:** ESC-16–19; test firmware'i, DFM ve prototip paketi. Dijital üretim paketi hedefi 8 Kasım. Numune teslim tarihi henüz bilinmiyor; aynı tarihte fiziksel kart var sayılmaz.
- **9–22 Kasım / Sprint 5, koşullu:** Numune ve test düzeneği hazırsa ilk enerji, motor devreye alma ve 1.5 kW doğrulaması. Numune geç gelirse pencere kayar.
- **23 Kasım–6 Aralık / Sprint 6, koşullu:** 1.5 kW kapısı geçmişse 3 kW/enerji/EMC değerlendirmesi ve ürün adayı dosyası. İlk ürün adayı hedefi 6 Aralık; sertifikalı seri ürün teslim tarihi değildir.

## Kullanım limitiyle çalışma

14 Eylül 2026 yaklaşık 18:02 İstanbul anlık kaydı: ana beş saatlik hak %56, haftalık hak %46 kalan. Beş saatlik yenileme 14 Eylül 22:17; haftalık yenileme 20 Eylül 00:46. Bunlar hesap genelindeki kullanım oranlarıdır, proje token adedi veya sabit günlük bütçe değildir; diğer görevler de tüketebilir.

Bu göreve bağlı otomasyon altı saatte bir devam etmeyi dener. Her çalışmada güncel limit okunur; iki ana pencereden herhangi biri %10 veya altındaysa ağır iş ertelenir. Bu bir prompt tabanlı çalışma politikasıdır; kesin token tavanı veya kesinti önleme garantisi değildir. Limit bitmişse çalıştırma başlayamayabilir; sonraki zamanlanmış denemede yeniden başlanması amaçlanır. Tam yenilenme anında tetiklenme garantisi yoktur.

Her tur tek somut iş paketi, gerekli doğrulama ve checkpoint ile tamamlanır. Gereksiz tam dosya okumaları ve değişmeyen test tekrarları yapılmaz. Yeni görev yaratılmaz; mevcut görev ve model ayarı korunur. Reset kredisi/ek kullanım satın alınmaz. Fiziksel testler kullanıcıya aittir.

Yerel dosyalara erişim için bilgisayar ve masaüstü uygulaması çalışır durumda olmalı. Kaynak: [resmî zamanlanmış görevler açıklaması](https://learn.chatgpt.com/docs/automations?surface=app).

Otomasyon kimliği: `esc-sprintlerini-kald-yerden-s-rd-r`. Dijital kapsam bittiğinde veya yalnız dış bağımlılıklar kaldığında duraklatma ve devir listesi beklenir. Önemli ilerleme, hata veya kullanıcı aksiyonu dışında bildirim istenmez.

## Takvim değiştirme kuralı

Bir sprint sonunda kabul kriteri geçmeyen iş taşınır; neden, etkilediği bağımlılıklar ve yeni hedef yazılır. Güç sınıfı değişikliği, üretim siparişi veya çözülemeyen teknik tercih kullanıcıyla karar kaydına alınır. Takvim baskısı nedeniyle standart kontrolü, fiziksel test veya DFM atlanmaz.
