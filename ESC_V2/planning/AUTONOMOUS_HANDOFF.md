# ESC autonomous handoff

Tarih: 2026-09-19  
Branch: `uav-rebaseline`  
Durum: `READY_FOR_NEXT_RUN`

Bu dosya her otonom çalışma koşusunun sonunda güncellenecek ve bir sonraki koşunun ilk okuduğu süreklilik kaydı olacaktır. Bu kayıt tek başına design authority değildir; her koşuda gerçek repository durumu ile doğrulanacaktır.

## Son doğrulanmış proje yönü

- Ürün hedefi: 70–100 kg payload sınıfında heavy-lift / agricultural multirotor UAV ESC.
- Eski 3 kW / 13S / Golden Motor B1: tarihsel candidate/reference; UAV ürün baseline değildir.
- Aktif design authority: `../design_basis.json`, `UAV_PRODUCT_PLAN.md`, `UAV_REBASELINE.md`, `UAV_TRACEABILITY.md`, `mission_requirements.json`.
- A2/B1 geçmişi korunacak; `main` otomatik olarak değiştirilmeyecek.
- Final Gerber/production release ve flight-qualified iddiası kullanıcı onayı + fiziksel kanıt olmadan yapılmayacak.

## Çalışma zinciri

`mission -> MTOW -> rotor/thrust -> motor/prop -> battery -> ESC electrical envelope -> power stage -> protection/sensing/thermal -> firmware -> PCB -> staged validation`

## Başlangıç durumu

### Tamamlanan yön düzeltmeleri

- UAV uygulama hedefi aktif tasarım temeline alındı.
- Eski ground-drive assumption ürün otoritesinden çıkarıldı.
- Ürün geliştirme gate planı oluşturuldu.
- Faz 2/Faz 3/B1 için traceability yaklaşımı oluşturuldu.
- Bilinmeyen görev parametreleri `null/TBD/OPEN` politikasıyla ayrıldı.

### Kritik açık işler

1. G0 mission / mass envelope kapatma.
2. Rotor mimarisi ve thrust sizing.
3. Gerçek ağır UAV motor/propulsion benchmark kanıtlarının repository içinde kalıcılaştırılması.
4. Battery architecture.
5. ESC continuous/peak voltage-current-power envelope.
6. Mevcut B1/Faz2/Faz3 tasarımının yeni envelope'a göre requalification'ı.

### Bilinen blokajlar

- Airframe empty mass bilinmiyor.
- Battery mass bilinmiyor.
- Nominal payload henüz dondurulmadı.
- Hedef hover / flight duration bilinmiyor.
- Çevresel zarf ve single-motor failure beklentisi henüz dondurulmadı.

Bu blokajlar bütün işi durdurmaz. Güvenilir kaynaklarla yapılabilecek propulsion benchmark, rotor trade study, mimari analiz, hesap altyapısı, firmware/verification scaffolding ve B1 requalification hazırlıkları bağımsız olarak ilerletilebilir.

## Sonraki koşu için çalışma kuralı

1. Önce bu dosyayı ve machine-readable `autonomy_state.json` dosyasını oku.
2. Repository HEAD ve ilgili plan/backlog dosyalarıyla tutarlılığı kontrol et.
3. En yüksek öncelikli unblocked işi seç.
4. Bir iş tamamlanınca aynı koşu içinde sıradaki unblocked işe geç.
5. Bir iş bloklanırsa blocker kaydet ve başka bağımsız işe geç.
6. Salt görünür aktivite için filler commit yapma.
7. Koşu sonunda bu dosyayı gerçek değişiklikler, kanıtlar, riskler ve sonraki görevlerle güncelle.

## Next-run briefing

İlk hedef, mevcut planın sadece metin olarak kalmamasını sağlamak: G0/G1'e hizmet eden kaynaklı propulsion benchmark ve hesap artefaktlarını repository'ye bağla; ardından bunlardan rotor/motor/battery/ESC sizing kararlarını türet. Bilinmeyen kullanıcı parametrelerini uydurma; parametrik aralıklarla çalış ve hangi kararın hangi girdiye duyarlı olduğunu göster. Eğer G0 tamamen kapanamıyorsa, G1 için güvenilir aralık analizi üret ve kritik kullanıcı girdilerini net biçimde ayır.
