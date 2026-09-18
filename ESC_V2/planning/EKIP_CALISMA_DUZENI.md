# ESC — mühendislik ekip çalışma düzeni

14.09.2026. Kullanıcı agent ekiplerini ve proje dosyalarında uygulama yapmalarını açıkça yetkilendirdi. Ekipler yazılım agentlarıdır; fiziksel tezgâh işlemleri kullanıcıya aittir. Bu yapı bağımsız yetkili mühendis imzası veya sertifikasyon yerine geçmez.

- **Entegrasyon / proje yönetimi:** ana agent; backlog, kabul kapıları, karar kaydı, değişiklik manifesti ve teslim durumu.
- **Şema uygulama:** B1 jeneratörü ve üretilen KiCad şema/sembolleri; netlist ve ERC karşılaştırmasıyla değişiklik.
- **Elektriksel inceleme:** şema/pin/net ve üretici verisinden bulgu; uygulayıcı dosyalarını eşzamanlı değiştirmez.
- **Proje görünürlüğü:** backlog ve kanıtlardan yerel HTML panosu; tamamlanan görev oranını ürün yeterliliği gibi sunmaz.

Her ekip somut dosya kapsamına sahiptir. Aynı jeneratör üzerinde iki yazar çalışmaz. İnceleme bulguları entegrasyon agentına gider; gerekli düzeltme uygulama ekibine atanır. Görüş ayrılığı olursa alternatif, kanıt ve karar gerekçesi `team_review.json` içinde kayıt edilir. Gerçekleşmeyen insan toplantısı veya ölçüm yazılmaz.

## Güncelleme akışı

1. Değişiklikten önce güncel CHECKPOINT ve backlog okunur; değiştirilecek dosyaların sahipliği belirlenir.
2. Kaynak değişikliği uygulanır. B1'i A2'den yeniden türeten `prepare_b1.py` tek seferliktir; mevcut geliştirmeyi ezmesi engellenmiştir.
3. Şema değiştiyse KiCad Python ile `planning/publish_progress.py --verify-schematic` çalıştırılır. Şema değişmediyse `planning/publish_progress.py` yeterlidir.
4. Bulgu, karar, kanıt ve kapsam `planning/team_review.json` ve `planning/change_log.json` içinde güncellenir; HTML bu kayıtları yeniden üretimde okur. Bu nedenle kayıt değiştikten sonra yayınlama komutu çalıştırılır.
5. CHECKPOINT sonraki somut işi ve engelleri taşır. Otomatik çalıştırmalar aynı süreci izler.

HTML kendi kendine mühendislik işi yapmaz: agent turunda kaynaklardan yeniden üretilir. Tarayıcıda açık eski görünüm yenilenmelidir. Satın alma, üretim siparişi ve fiziksel test onayları mevcut kullanıcı kapsamına göre yürütülür.
