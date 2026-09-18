# B1 elektriksel ekip incelemesi

Tarih: 14 Eylül 2026. İnceleyen: elektriksel inceleme AI agentı. Bu kayıt masa başı incelemedir; insan onayı veya fiziksel ölçüm değildir. Kaynak dosyaların SHA-256 değerleri review.json içindedir.

## ELEC-01 — P0 — LM5164 RON direnci yanlış besleme hattına bağlı

Sınıf: `CONFIRMED_CONNECTION_ERROR`.

R1301.1=VBUS, R1301.2=BUCK_RON ve U1301.4=BUCK_RON; hem manifest hem KiCad netlist aynı bağlantıyı içeriyor.

Zamanlama girişinin üretici bağlantı şartı sağlanmıyor; yardımcı kaynağın çalıştığı kabul edilemez. ERC geçişi bu işlevsel hatayı saptamaz.

Düzeltme: R1301 pin1 bağlantısını GND yap; jeneratör kaynağını da düzelt. Gerçek netlistten RON-GND bağlantısını denetleyen regresyon ekle. 100k değerinin frekans/ripple hesabını tekrar çalıştır.

Kapanış: Üretici pin tablosuyla eşleşen yeni netlist ve ERC; düşük enerjili yardımcı kaynak testi ayrıca bekler.

- [Rev D, Table 4-1 pin4; Figure7-1](https://www.ti.com/lit/ds/symlink/lm5164.pdf)

## ELEC-02 — P1 — Ön şarj sırasında yardımcı yükün engellenmesi tanımlı değil

Sınıf: `CONFIRMED_DESIGN_GAP_CONDITIONAL_FAILURE`.

BUCK_UVLO yalnız VBUS 1M/100k bölücüsünden sürülüyor. FAN sürekli +12V bağlı; TPS62160 EN de +12V. Ön şarj tamamlandı sinyali veya yük engelleme elemanı yok.

22 ohm aday ve 39V kaynakta yüzde95 hedefi sabit giriş yükü 88.6mA altında gerektiriyor. Bu sınır üzerindeki gerçek yardımcı yük şarjı engelleyebilir; gerçek yük akımı henüz ölçülmedi.

Düzeltme: Ön şarj tamamlanana kadar fan/yardımcı yükleri engelleyen ya da ayrı kontrol beslemesi sağlayan mimariyi seç. MCU kapalıyken MCU komutu bekleyen başlangıç kilitlenmesi oluşturma. Gerilime bağlı yük, histerezis ve zaman aşımı modeli ekle.

Kapanış: 39–54.6V aralığında en kötü yük/tolerans hesabı, enerji ve tekrar deneme sınırı; ardından ön şarj test kaydı.

- [Proje hesabı](../../planning/precharge_checks.json)
- [RevD Table4-1 and6.3.9](https://www.ti.com/lit/ds/symlink/lm5164.pdf)

## ELEC-03 — P1 — Diyotlu fault/reset zincirinin düşük seviye marjı kapanmamış

Sınıf: `CONFIRMED_VERIFICATION_GAP_NOT_PROVEN_FAILURE`.

D2401–4 anotları HARD_FAULT_N; katotları DRV_FAULT_N, NRST, PG_12V, PG_5V. HARD_FAULT_N, U2401.6 CLR ve U1701.34 BKIN girişlerini sürüyor. R2401 2.2k ek sink yükü getiriyor.

Düşük seviye, kaynak VOL + diyot VF toplamıdır. SN74LVC1G74 3–3.6V beslemede VIL üst sınırı 0.8V. BAT54H 25C tablosu tek başına soğuk/sıcak çalışma marjını ve güç geçişlerini kanıtlamaz. Kesin arıza iddiası yok.

Düzeltme: Her kaynak için toplam pull-up akımı, garantili VOL, sıcaklıkta VF, CLR/BKIN eşikleri ve minimum reset darbesini bütçele. Marj kanıtlanamazsa diyot ağı yerine uygun aktif mantık/supervisor kullan. NRST sürücü akımı ve BOR/option-byte davranışını ayrıca doğrula.

Kapanış: Tüm kaynaklar için pozitif worst-case gürültü marjı ve açılış/brownout/reset sırasında PWM inhibit kanıtı; MCU reseti tek başına dış latch başlangıcının kanıtı sayılmaz.

- [6.3 Recommended Operating Conditions](https://www.ti.com/lit/ds/symlink/sn74lvc1g74.pdf)
- [Pinning and Table7](https://assets.nexperia.com/documents/data-sheet/BAT54H.pdf)
- [5.3.15 NRST](https://www.st.com/resource/en/datasheet/stm32g474re.pdf)

İnceleme sonucu: ELEC-01 giderilmeden yardımcı kaynak doğru kabul edilemez. Diğer iki kayıt, kapanmamış mühendislik doğrulamalarını gösterir; arıza oluştuğunu iddia etmez. Şema veya üretim dosyaları bu ekip tarafından değiştirilmedi.
