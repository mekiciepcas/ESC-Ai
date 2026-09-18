# ESC-3K B1 — geliştirme revizyonu

Ana dosya `ESC_3kW_B1.kicad_pro`; 29 sayfalık şema `ESC_3kW_B1.kicad_sch`.
14.09.2026 itibarıyla B1 elektriksel geliştirme kaynağıdır. A2 PDF/ZIP eski inceleme kaydı olarak korunmuştur; B1 yerine üretimde kullanılmaz.

## Bu revizyonda yapılanlar

- DR-002: R1301.1 RON direnci VBUS yerine GND; 734 bağlı pinde yalnız bu değişiklik doğrulandı.
- Bobin sargı, MOSFET gövde diyodu ve bulk kondansatör pozitif uç gösterimleri iyileştirildi.

- Her iki kart arayüzünde pin38 motor sıcaklığına ayrıldı. A2'de bu pin GND idi. A2 ve B1 kart/kabloları uyumlu kabul edilmez.
- 32 kartlar arası net, konektör pinleri ve gerçek KiCad netlistiyle denetlendi. Eski sıcaklık eksikliği ve tek uçta yanlış pin ataması enjekte edilerek denetimin ikisini de yakaladığı doğrulandı.
- Şemada 742 kontrol geçti; ERC sıfır ihlal. Bu sonuç sadece belirtilen elektriksel kontrollerin kapsamındadır.
- Projeye KiCad özel tasarım kuralları eklendi. Test kuponundaki dar VBUS açıklığı ve ince sinyal izi KiCad DRC tarafından yakalandı. Kupon ESC kartı değildir.

Çizim ve üretim kabul şartnamesi: `../pcb_b1/TASARIM_KURALLARI.md`.
Denetim kayıtları: `../verification/b1_checks.json`, `../pcb_b1/verification/interface_audit.json`, `../pcb_b1/verification/rule_validation.json`.

## Tamamlanması gerekenler

61 bileşende MPN veya footprint eksikliği sürüyor. Atanmış MPN'lerin tamamı tedarik/onay görmüş değildir. Şemanın bütün özel sembolleri IEC 60617 geometrileriyle karşılaştırılmadı. ERC'nin varsayılan devre dışı kontrolleri `erc_b1.json` içinde ayrıca kayıtlıdır.

**Tam yerleşmiş ve yönlendirilmiş ürün PCB'si henüz yoktur. Gerber üretim paketi oluşturulmamıştır.** Öncelik: güç pasiflerinin ripple/termal seçimi ve pin/pad eşleşmeleri, giriş/enerji yönetimi, sonra iki kartın mekanik yerleşimi ve routing. Güç taşıma yolları 0.20 mm genel sinyal kuralına göre boyutlandırılamaz.

## Tekrarlanabilir denetim

KiCad 10 Python ile `../pcb_b1/tools/prepare_b1.py`, ardından `build_footprints.py` ve `build_b1.py` çalıştırılır. KiCad CLI ile `sch export netlist` sonucu `../verification/ESC_3kW_B1.net`, `sch erc --format json` sonucu `../verification/erc_b1.json` olarak alınır. `verify_b1.py` ve `../pcb_b1/tools/audit_interfaces.py` çalıştırılır. `../pcb_b1/tools/test_rules.py` sadece kural motorunu bağımsız test kuponunda sınar.

Jeneratör A1 elektriksel kaynak tanımını ve B1 düzeltmelerini kullanır; `../hardware` bağımlılığı korunmalıdır. Şema üzerinde elle yapılacak değişiklikler jeneratöre de aktarılmadan yeniden üretim yapılmaz.
