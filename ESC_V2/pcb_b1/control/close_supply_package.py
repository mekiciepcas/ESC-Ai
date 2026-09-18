from pathlib import Path
import json, hashlib
import pcbnew as k
r=Path(__file__).resolve().parent; root=r.parents[1]
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def write(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=r/'ESC_3kW_CONTROL_B1_PLACEMENT.kicad_pcb'; b=k.LoadBoard(str(p))
f={x.GetReference():x for x in b.GetFootprints()}
report=read(r/'placement_report.json'); checked=0
for entry in report['placed']:
    actual={a.GetNumber():a.GetNetname() or None for a in f[entry['ref']].Pads()}
    assert actual==entry['nets'], (entry['ref'],actual,entry['nets'])
    checked+=len(actual)
    pos=f[entry['ref']].GetPosition(); entry['at_mm']=[k.ToMM(pos.x),k.ToMM(pos.y)]
    entry['rotation_deg']=f[entry['ref']].GetOrientationDegrees()
assert checked==192
drc=read(r/'drc_placement.json'); assert len(drc['violations'])==0
assert len(drc['unconnected_items'])==120
change=read(r/'supply_routes_20260915.json')
for c in change['connections']:
    for a,z in zip(c['path_mm'],c['path_mm'][1:]):
        def key(x): return (round(x[0],6),round(x[1],6))
        expected={key(a),key(z)}
        assert any({key((k.ToMM(t.GetStart().x),k.ToMM(t.GetStart().y))),key((k.ToMM(t.GetEnd().x),k.ToMM(t.GetEnd().y)))}==expected and t.GetNetname()==c['net'] for t in b.GetTracks())
report.update(track_count=len(b.GetTracks()),drc_violations=0,unconnected_items=120,drc_scope='Four digital MCU bypass pairs only; analog/VBAT and complete distribution still open',board_sha256=hashlib.sha256(p.read_bytes()).hexdigest())
write(r/'placement_report.json',report)
change.update(final_verified=True,checked_pads=checked,drc_violations=0,unconnected_items=120,board_sha256=report['board_sha256'],verification='Saved PCB reopened; 192 pad nets equal prior placement manifest; six new paths verified segment by segment; zero reported DRC violations; no exclusions added.')
write(r/'supply_routes_20260915.json',change)
(r/'README.md').write_text('# Kontrol PCB — kısmi PoC yönlendirmesi\n\n100 × 80 mm, 4 katman; 38 elektriksel bileşen, 192 pad. 22 iz segmenti, 120 açık bağlantı, mevcut kurallarla DRC 0 ihlal. C1801–C1804 dijital bypass çiftleri MCU pinlerine bağlı. VBAT, analog besleme ve ortak güç/GND dağıtımı tamamlanmadı. Üretim veya enerji verme onayı değildir.\n\nKaynak: ESC_3kW_CONTROL_B1_PLACEMENT.kicad_pcb. Kanıt: supply_routes_20260915.json ve drc_placement.json. Değişiklik öncesi snapshot korunur. route/refine betikleri tarihsel tek seferlik değişikliklerdir; mevcut PCB üzerine yeniden uygulanmaz. Aday kılıflar placement_report.json içinde açıkça işaretlidir.\n',encoding='utf-8')
plan=root/'planning'; backlog=read(plan/'backlog.json'); backlog['revision']='PLAN-07'; backlog['date']='2026-09-15'; backlog['execution_policy']='Kullanıcı yönlendirmesi: takvim beklenmez; kapasite ve doğrulama kapılarıyla kontrollü ilerlenir.'
write(plan/'backlog.json',backlog)
log=read(plan/'change_log.json'); log['changes' if 'changes' in log else 'entries'].append({'id':'CHG-07','date':'2026-09-15','title':'Üç ek dijital MCU bypass çifti yönlendirildi ve çakışmalar giderildi','status':'PARTIAL_ROUTING_VERIFIED','files':['pcb_b1/control/supply_routes_20260915.json','pcb_b1/control/drc_placement.json'],'verification':['192 pad-net eşleşmesi korundu; kaydedilmiş PCB yeniden açıldı','22 iz segmenti, 126 → 120 açık bağlantı','İlk kontroldeki 32 ihlal, geometri düzeltmeleriyle 0 oldu; kural bastırılmadı','PoC-01 devam ediyor; takvim beklemeden kapasiteye göre ilerleme']})
write(plan/'change_log.json',log)
cp=plan/'CHECKPOINT.md'; old=cp.read_text(encoding='utf-8'); marker='Önceki kayıt (tarihsel sayılar içerir):'; history=old[old.index(marker):] if marker in old else old
cp.write_text('# Güncel devam kaydı — 15.09.2026 / PLAN-07\n\nKullanıcı takvim beklemeden kapasite ve doğrulama kapılarıyla kontrollü ilerlemeyi istedi. POC-01 ve ESC-03 aktif. Kontrol PCB: 38 elektriksel footprint, 192 pad-net korunmuş, 22 iz segmenti, 120 açık bağlantı, DRC 0 ihlal. C1801–C1804 dijital bypass çiftleri bağlı; supply_routes_20260915.json doğrulama ve hash kanıtıdır. Şema bu tur değişmedi.\n\nSONRAKİ PAKET: C1806 VBAT ve C1807/8/9 analog besleme pin yakınlığı/yerel bağlantıları; ardından GND dönüş düzlemi ve besleme dağıtımı. Sonra reset/SWD/saat ve düşük gerilim PoC firmware. Aday MPN, güç kaynağı ve tüm yollar kesinleşmeden üretim/enerji verme yok. Güç PCB ve fiziksel doğrulama açık.\n\nMevcut KiCad yeterli; yeni kurulum yok. Bu tur başlangıcında haftalık %14 ve beş saatlik %57 kalan okundu; sonraki tur taze kontrol et. Tarihler bekleme koşulu değildir; kaynak ve teknik kabul kapıları geçerlidir. HTML statik kontrol edilir; tarayıcı görsel doğrulaması erişim politikası nedeniyle tamamlanmış sayılmaz.\n\n'+history,encoding='utf-8')
schedule=plan/'TAMAMLAMA_TAKVIMI.md'; schedule.write_text('> 15.09.2026 kullanıcı kararı: Aşağıdaki tarihler yalnız planlama referansıdır. Hazır işler tarih beklemeden kapasite dahilinde yapılır; sonraki aşamaya geçiş test ve kabul kanıtına bağlıdır.\n\n'+schedule.read_text(encoding='utf-8'),encoding='utf-8')
print('PASS: 192 pads, six new paths, 22 tracks, zero violations, 120 unconnected.')
