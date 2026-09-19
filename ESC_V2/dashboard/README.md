# ESC UAV proje dashboard

`index.html` proje durumunu basit dille gösteren çevrimdışı dashboard'dur. Şu bilgileri doğrudan güncel planlama kayıtlarından alır:

- requirement yapısı yüzdesi,
- G1 gerçek değer kapanış yüzdesi,
- backlog DONE yüzdesi,
- U1 KiCad iskelet / gerçek komponentli şema durumu,
- son çalışma state'i,
- aktif blocker'lar,
- sıradaki işler,
- eksik G0 araç/görev girdileri,
- sıradaki şema revizyon numarası,
- KiCad ve revision-control kanıt kayıtları.

## Otomatik güncelleme

`.github/workflows/dashboard-refresh.yml`, `uav-rebaseline` branch'inde planning veya U1 donanım kayıtları değiştiğinde otomatik olarak:

1. `python3 ESC_V2/dashboard/build_dashboard.py`
2. `python3 ESC_V2/dashboard/validate_static.py`
3. değişiklik varsa `index.html`, `snapshot.json`, `validation.json` dosyalarını tekrar commit eder.

Generated dashboard commit'i yalnız dashboard çıktılarını değiştirir ve workflow path filtresi nedeniyle yeniden kendi kendini tetiklemez.

## Manuel güncelleme

Repo checkout'u üzerinde:

```bash
python3 ESC_V2/dashboard/build_dashboard.py
python3 ESC_V2/dashboard/validate_static.py
```

Dashboard bilinmeyen mühendislik değerlerini tahmin etmez. `OPEN/null/TBD` alanlar açık kalır. Dashboard yüzdeleri ürün yeterliliği veya fiziksel test sonucu değildir; her kartın açıklaması kendi kapsamını belirtir.
