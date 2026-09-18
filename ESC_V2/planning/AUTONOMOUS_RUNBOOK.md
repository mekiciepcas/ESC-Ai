# Autonomous runbook

Bu dosya saatlik otonom çalışma döngüsünün kısa giriş noktasıdır.

Her çalıştırmada:
1. `AUTONOMOUS_EXECUTION_POLICY.md` okunur.
2. `autonomy_state.json` okunur.
3. `UAV_PRODUCT_PLAN.md` ve `uav_backlog.json` üzerinden en yüksek öncelikli unblocked iş seçilir.
4. Teknik kanıt üretilir ve branch'e commit edilir.
5. Gate kapanmadan alt bağımlılık freeze edilmez.
6. Kullanıcı kararı, fiziksel ölçüm veya güvenlik-kritik bilinmeyen gerekiyorsa iş BLOCKED olarak bırakılır.

Ana hedef: gerçeklenebilir ve izlenebilir UAV ESC ürünü; sahte ilerleme veya kaynaksız mühendislik kararı yok.
