"""Read-only electrical review evidence; does not modify design files."""
from pathlib import Path
import sys, json, hashlib
root=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(root/'hardware'))
from sexpr import parse, child, children
out=Path(__file__).resolve().parent
mp=root/'hardware_b1/connection_manifest.json'
np=root/'verification/ESC_3kW_B1.net'
parts={p['ref']:p for p in json.loads(mp.read_text(encoding='utf-8'))}
tree=parse(np.read_text(encoding='utf-8'))
nets={}
for net in children(child(tree,'nets'),'net'):
    name=child(net,'name')[1]
    for node in children(net,'node'):
        nets[(child(node,'ref')[1],child(node,'pin')[1])]=name
def evidence(refs):
    return [dict(ref=r,page=parts[r]['page'],value=parts[r]['value'],manifest_nets=parts[r]['nets'],exported_nets={p:nets.get((r,p)) for p in parts[r]['nets']}) for r in refs]
findings=[
dict(id='ELEC-01',priority='P0',classification='CONFIRMED_CONNECTION_ERROR',title='LM5164 RON direnci yanlış besleme hattına bağlı',
 evidence=evidence(['U1301','R1301']),
 observation='R1301.1=VBUS, R1301.2=BUCK_RON ve U1301.4=BUCK_RON; hem manifest hem KiCad netlist aynı bağlantıyı içeriyor.',
 consequence='Zamanlama girişinin üretici bağlantı şartı sağlanmıyor; yardımcı kaynağın çalıştığı kabul edilemez. ERC geçişi bu işlevsel hatayı saptamaz.',
 correction='R1301 pin1 bağlantısını GND yap; jeneratör kaynağını da düzelt. Gerçek netlistten RON-GND bağlantısını denetleyen regresyon ekle. 100k değerinin frekans/ripple hesabını tekrar çalıştır.',
 acceptance='Üretici pin tablosuyla eşleşen yeni netlist ve ERC; düşük enerjili yardımcı kaynak testi ayrıca bekler.',
 sources=[dict(url='https://www.ti.com/lit/ds/symlink/lm5164.pdf',section='Rev D, Table 4-1 pin4; Figure7-1')]),
dict(id='ELEC-02',priority='P1',classification='CONFIRMED_DESIGN_GAP_CONDITIONAL_FAILURE',title='Ön şarj sırasında yardımcı yükün engellenmesi tanımlı değil',
 evidence=evidence(['U1301','R1401','R1402','U1501','J1401','J101']),
 observation='BUCK_UVLO yalnız VBUS 1M/100k bölücüsünden sürülüyor. FAN sürekli +12V bağlı; TPS62160 EN de +12V. Ön şarj tamamlandı sinyali veya yük engelleme elemanı yok.',
 consequence='22 ohm aday ve 39V kaynakta yüzde95 hedefi sabit giriş yükü 88.6mA altında gerektiriyor. Bu sınır üzerindeki gerçek yardımcı yük şarjı engelleyebilir; gerçek yük akımı henüz ölçülmedi.',
 correction='Ön şarj tamamlanana kadar fan/yardımcı yükleri engelleyen ya da ayrı kontrol beslemesi sağlayan mimariyi seç. MCU kapalıyken MCU komutu bekleyen başlangıç kilitlenmesi oluşturma. Gerilime bağlı yük, histerezis ve zaman aşımı modeli ekle.',
 acceptance='39–54.6V aralığında en kötü yük/tolerans hesabı, enerji ve tekrar deneme sınırı; ardından ön şarj test kaydı.',
 sources=[dict(path='planning/precharge_checks.json'),dict(url='https://www.ti.com/lit/ds/symlink/lm5164.pdf',section='RevD Table4-1 and6.3.9')]),
dict(id='ELEC-03',priority='P1',classification='CONFIRMED_VERIFICATION_GAP_NOT_PROVEN_FAILURE',title='Diyotlu fault/reset zincirinin düşük seviye marjı kapanmamış',
 evidence=evidence(['D2401','D2402','D2403','D2404','R2401','R1801','U2401','U1701']),
 observation='D2401–4 anotları HARD_FAULT_N; katotları DRV_FAULT_N, NRST, PG_12V, PG_5V. HARD_FAULT_N, U2401.6 CLR ve U1701.34 BKIN girişlerini sürüyor. R2401 2.2k ek sink yükü getiriyor.',
 consequence='Düşük seviye, kaynak VOL + diyot VF toplamıdır. SN74LVC1G74 3–3.6V beslemede VIL üst sınırı 0.8V. BAT54H 25C tablosu tek başına soğuk/sıcak çalışma marjını ve güç geçişlerini kanıtlamaz. Kesin arıza iddiası yok.',
 correction='Her kaynak için toplam pull-up akımı, garantili VOL, sıcaklıkta VF, CLR/BKIN eşikleri ve minimum reset darbesini bütçele. Marj kanıtlanamazsa diyot ağı yerine uygun aktif mantık/supervisor kullan. NRST sürücü akımı ve BOR/option-byte davranışını ayrıca doğrula.',
 acceptance='Tüm kaynaklar için pozitif worst-case gürültü marjı ve açılış/brownout/reset sırasında PWM inhibit kanıtı; MCU reseti tek başına dış latch başlangıcının kanıtı sayılmaz.',
 sources=[dict(url='https://www.ti.com/lit/ds/symlink/sn74lvc1g74.pdf',section='6.3 Recommended Operating Conditions'),dict(url='https://assets.nexperia.com/documents/data-sheet/BAT54H.pdf',section='Pinning and Table7'),dict(url='https://www.st.com/resource/en/datasheet/stm32g474re.pdf',section='5.3.15 NRST')])]
result=dict(review_date='2026-09-14',reviewer='Electrical review AI agent',scope='B1 exported connectivity and selected datasheets; no laboratory measurement or human approval',inputs={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (mp,np,root/'planning/precharge_checks.json')},findings=findings)
(out/'review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# B1 elektriksel ekip incelemesi','', 'Tarih: 14 Eylül 2026. İnceleyen: elektriksel inceleme AI agentı. Bu kayıt masa başı incelemedir; insan onayı veya fiziksel ölçüm değildir. Kaynak dosyaların SHA-256 değerleri review.json içindedir.','']
for f in findings:
    lines += [f"## {f['id']} — {f['priority']} — {f['title']}",'',f"Sınıf: `{f['classification']}`.",'',f['observation'],'',f['consequence'],'',f"Düzeltme: {f['correction']}",'',f"Kapanış: {f['acceptance']}",'']
    for s in f['sources']:
        lines.append(f"- [{s.get('section','Proje hesabı')}]({s.get('url','../../'+s.get('path',''))})")
    lines.append('')
lines += ['İnceleme sonucu: ELEC-01 giderilmeden yardımcı kaynak doğru kabul edilemez. Diğer iki kayıt, kapanmamış mühendislik doğrulamalarını gösterir; arıza oluştuğunu iddia etmez. Şema veya üretim dosyaları bu ekip tarafından değiştirilmedi.']
(out/'review.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('Three findings saved; manifest/export evidence captured.')
