# PoC önceliği — 15.09.2026

Kullanıcının güncel hedefi: önce çalışabilir bir kavram kanıtı. 3 kW ürün hedefi korunur; ilk PoC tam güç veya seri üretim yeterliliği değildir.

1. **Kontrol PoC:** eksiksiz ve denetlenmiş kontrol kartı bağlantıları; doğrulanmış harici düşük gerilim besleme yöntemi; SWD ile programlama, saat/reset, UART ve CAN loopback/iki düğüm testi. Gerçek numune ölçümü kullanıcıya ait. Mevcut kartta regülatör yok; besleme arayüzü ve geri besleme davranışı çözülmeden enerji verme talimatı yayımlanmaz.
2. **Düşük enerjili motor PoC:** güç kartı/koruma tasarımı sonrası akım sınırlı düzenek, Hall sırası, akım sensörü kalibrasyonu ve yüksüz motor kontrolü. Ön şarj ve fault marjı işleri burada kapı koşuludur.
3. **Yük doğrulaması:** önce 1.5 kW, sonra yeterli marj varsa 3 kW. Numune ve ölçüm olmadan tamamlandı sayılmaz.

PoC için ertelenebilir: nihai kasa estetiği, seri tedarik optimizasyonu, bütün özel sembollerin görsel standardizasyonu. Ertelenemez: pin/pad doğruluğu, gerilim sınırları, kısa devre/PWM kapatma, temel DRC ve enerji kontrolü. Tam uygunluk/sertifikasyon kapsamı ürün aşamasında ayrıca izlenir.

Somut bu tur: üç konnektörün montaj katmanı yazıları düzeltildi; C1801 MCU 64/63 besleme/GND pinlerine yaklaştırıldı; dört iz segmentiyle ilk iki bağlantı çizildi. 192 pad-net eşleşmesi korunuyor; DRC 0 ihlal, 126 açık bağlantı. Bu sonuç çalışır kart değildir.

Sonraki paket: MCU diğer bypass bağlantıları ve GND düzlemi stratejisi; ardından reset/SWD/clock hatları. Aday kılıflar kesinleşmeden üretim çıktısı oluşturulmaz. Kontrol kartına harici beslemenin nasıl verileceği ayrı şema ve bağlantı belgesinde çözülür. Gerekli yazılımlar için mevcut KiCad yeterli; Java/Freerouting başlatma doğrulaması daha sonra yapılabilir.
