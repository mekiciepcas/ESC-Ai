# Geliştirme araçları — durum ve sıradaki kurulum

Kullanıcı gerekli geliştirme/test programlarının indirilmesini yetkilendirdi. Yalnız gereken araçlar resmî kaynaklarından alınacak; fiziksel test cihazları yazılım kurulumu ile sağlanmış sayılmayacak.

- **KiCad 10.0.6 ve pcbnew Python:** mevcut, PCB dosyası üretimi ve ERC/DRC ile çalıştığı doğrulandı. Yeniden indirme gerekmiyor. PATH'te görünmese de `C:/Program Files/KiCad/10.0/bin` üzerinden kullanılıyor.
- **Python, Node ve SVG→PNG dönüştürme:** mevcut ve proje kontrollerinde çalışıyor.
- **Freerouting 2.4.1:** resmî sürümden daha önce alınan JAR `pcb_b1/tools` içinde. Henüz çalıştırma/yönlendirme doğrulaması yapılmadı.
- **Java 25 çalışma ortamı:** daha önce alınan `jre25.zip` mevcut; henüz çıkarılmadı. Sonraki tur arşiv kaynağı/bütünlüğü ve giriş yolları doğrulanıp proje içine çıkarılacak, sürüm ve Freerouting açılışı sınanacak. Tasarım dosyaları dış servise yüklenmeyecek; telemetri ayarları incelenecek.
- **STM32 derleyici/programlayıcı:** mevcut PATH kontrolünde ARM derleyicisi görünmedi; sistemde hiç kurulmadığı anlamına gelmez. Firmware ESC-15 öncesi kurulu dizinler kontrol edilecek; eksikse resmî STM32/Arm dağıtımından uygun araç alınacak. Bu tur indirilmedi.
- **SPICE:** simülasyon aşamasında KiCad ile mevcut motorun kullanılabilirliği ve üretici model uyumluluğu test edilecek. Test edilmeden simülasyon hazır kabul edilmeyecek.

Donanım devreye alma için ST-Link, akım sınırlı kaynak, uygun diferansiyel prob/osiloskop, akım ölçümü, yük/fren düzeneği ve sıcaklık ölçüm erişimi ayrıca ESC-02 numune/test planında doğrulanacak. Bu liste satın alma emri değildir.

Bu tur ana beş saatlik kullanımın %99'u tüketilmiş olduğundan yeni ağır kurulum ve PCB düzenlemesi başlatılmadı. Mevcut PCB korunuyor. Sonraki somut iş: araç açılış doğrulaması, kalan 6 serigrafi çakışması ve MCU bypass yerleşimi; ardından kontrollü yerel bağlantı yönlendirmesi.
