"""Build the offline project dashboard from engineering records; no network required."""
from pathlib import Path
from datetime import datetime
from html import escape
from urllib.parse import quote
import json
import base64
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
def read(path, fallback=None):
    p = ROOT / path
    return json.loads(p.read_text(encoding='utf-8-sig')) if p.exists() else fallback
def esc(value):
    return escape(str(value), quote=True)
def link(path, label=None, base=None):
    p = ((base or ROOT) / path).resolve()
    if not p.is_relative_to(ROOT.resolve()) or not p.is_file():
        return '<span class="missing">' + esc(label or path) + ' · kanıt dosyası yok</span>'
    href = '../' + quote(p.relative_to(ROOT.resolve()).as_posix(), safe='/')
    return '<a href="' + href + '">' + esc(label or p.name) + ' ↗</a>'
def human(value):
    if isinstance(value, dict):
        return '<dl>' + ''.join('<dt>'+esc(k)+'</dt><dd>'+human(v)+'</dd>' for k,v in value.items()) + '</dl>'
    if isinstance(value, list):
        return '<ul>'+''.join('<li>'+human(v)+'</li>' for v in value)+'</ul>'
    return esc(value if value is not None else '—')

plan = read('planning/backlog.json', {})
tasks = plan.get('tasks', [])
bom = read('hardware_b1/bom_open_items.json', [])
checks = read('verification/b1_checks.json', {})
envelope = read('planning/envelope_checks.json', {})
status_names = {'DONE':'Tamamlandı','IN_PROGRESS':'Sürüyor','TODO':'Sırada','BLOCKED':'Engelli','READY':'Hazır'}
done = sum(t.get('status') == 'DONE' for t in tasks)
active = sum(t.get('status') == 'IN_PROGRESS' for t in tasks)
boards = [p for p in (ROOT/'pcb_b1').rglob('*.kicad_pcb') if 'verification' not in p.parts and 'tools' not in p.parts]
cards=[]
for t in tasks:
    s=t.get('status','TODO')
    evidence=' · '.join(link(p,base=ROOT/'planning') for p in t.get('evidence',[]))
    extra=''.join('<p class="detail"><strong>'+label+'</strong> '+esc(t[key])+'</p>' for key,label in [('remaining','Kalan iş:'),('blocked_reason','Engel:'),('completion_scope','Tamamlama kapsamı:')] if t.get(key))
    cards.append(f'''<article class="task" data-status="{esc(s)}" data-sprint="{esc(t.get('sprint',''))}">
    <div class="task-top"><span class="mono">{esc(t['id'])} · {esc(t.get('priority',''))}</span><span class="badge {esc(s)}">{esc(status_names.get(s,s))}</span></div>
    <h3>{esc(t['title'])}</h3><p class="meta">Sprint {esc(t.get('sprint',''))} · {esc(t.get('owner',''))}</p>
    <details><summary>Kabul kriteri ve kanıtlar</summary><p>{esc(t.get('acceptance',''))}</p>{extra}
    <p class="detail">Bağımlılıklar: {esc(', '.join(t.get('dependencies',[])) or 'Yok')}</p>{'<p class="evidence">'+evidence+'</p>' if evidence else '<p class="meta">Henüz kanıt bağlanmadı.</p>'}</details></article>''')

schedule = ROOT/'planning/TAMAMLAMA_TAKVIMI.md'
milestones=[]
if schedule.exists():
    for line in schedule.read_text(encoding='utf-8-sig').splitlines():
        match=re.match(r'- \*\*(.+?)\*\*(.*)',line)
        if match:
            milestones.append('<div class="milestone"><strong>'+esc(match[1])+'</strong><p>'+esc(match[2].lstrip(': '))+'</p></div>')
optional=''
for path,title in [('planning/team_review.json','Ekip incelemesi ve iyileştirme kararları'),('planning/change_log.json','Değişiklik günlüğü')]:
    obj=read(path)
    if obj:
        rows=obj.get('findings',obj.get('entries',[]))
        content=''
        for row in rows:
            refs=row.get('evidence',row.get('files',[]))
            content+='<article><h3>'+esc(row.get('id',''))+' · '+esc(row.get('title',''))+'</h3><p class="meta">'+esc(row.get('severity',''))+' '+esc(row.get('status',''))+'</p><p>'+esc(row.get('decision',''))+'</p>'
            if row.get('verification'):content+='<p>'+esc(' · '.join(row['verification']))+'</p>'
            if refs:content+='<p>'+ ' · '.join(link(ref) for ref in refs)+'</p>'
            content+='</article>'
        optional += '<section class="panel"><div class="section-head"><h2>'+title+'</h2>'+link(path,'Kaynak kayıt')+'</div><p class="meta">'+esc(obj.get('type',''))+'</p><div class="record">'+content+'</div></section>'

placement=read('pcb_b1/control/placement_report.json')
preview=ROOT/'pcb_b1/control/placement.png'
if placement and preview.exists():
    optional='<section class="panel"><h2>Kontrol kartı — gerçek PCB ilk yerleşimi</h2><p>'+esc(str(placement['size_mm'])+' mm · '+str(placement['copper_layers'])+' katman · '+str(placement['electrical_footprints'])+' bileşen · '+str(placement['checked_pads'])+' pad eşleşmesi. Açık bağlantı: '+str(placement.get('unconnected_items','?'))+'; DRC ihlali: '+str(placement.get('drc_violations','?'))+'. Durum: '+placement['status'])+'</p><img alt="KiCad kontrol kartı ilk yerleşimi" style="width:100%;height:auto" src="data:image/png;base64,'+base64.b64encode(preview.read_bytes()).decode()+'"><p>'+link('pcb_b1/control/ESC_3kW_CONTROL_B1_PLACEMENT.kicad_pcb','KiCad PCB dosyası')+' · '+link('pcb_b1/control/placement_report.json','Yerleşim ve aday kılıf raporu')+'</p></section>'+optional

artifacts=[('planning/AGILE_ROADMAP.md','Agile yol haritası'),('planning/CHECKPOINT.md','Operasyon devir kaydı'),('pcb_b1/TASARIM_KURALLARI.md','Çizim ve üretim kuralları'),('hardware_b1/README.md','B1 şema durumu'),('hardware_b1/ESC_3kW_B1.kicad_pro','KiCad B1 projesi'),('verification/b1_checks.json',str(checks.get('checks_passed','—'))+' kontrolün kaynak raporu'),('pcb_b1/verification/interface_audit.json','Kartlar arası bağlantı denetimi'),('pcb_b1/verification/rule_validation.json','KiCad kural sınaması')]
artifact_html=''.join('<li>'+link(p,label)+'</li>' for p,label in artifacts if (ROOT/p).exists())
bom_html=''.join('<tr><td class="mono">'+esc(p['ref'])+'</td><td>'+esc(p.get('value',''))+'</td><td>'+esc(', '.join(p.get('missing',[])))+'</td></tr>' for p in bom)
stamp=datetime.now().astimezone().isoformat(timespec='seconds')
pcb_text=f'{len(boards)} PCB çalışma dosyası bulundu; yönlendirme ve üretim onayı ayrıca incelenmelidir.' if boards else 'Ürün PCB dosyası henüz yok. Kural test kuponu, ürün kartı olarak sayılmaz.'
data={'generated_at':stamp,'plan_revision':plan.get('revision'),'task_count':len(tasks),'done_count':done,'bom_open_count':len(bom),'pcb_files':[p.relative_to(ROOT).as_posix() for p in boards]}
template='''<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>ESC · Geliştirme Operasyonu</title><style>
:root{--ink:#182a37;--muted:#536674;--line:#dce4e8;--teal:#087c72;--paper:#f3f6f7}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.6 system-ui,-apple-system,Segoe UI,sans-serif}a{color:#006d78;text-underline-offset:3px}header{background:#142e3b;color:#fff;padding:42px max(5vw,20px)}header p{color:#c0d6df;max-width:800px}h1{font-size:clamp(28px,4vw,42px);line-height:1.2;margin:12px 0}h2{font-size:22px;margin:0}h3{font-size:16px;line-height:1.5;margin:13px 0 7px}.eyebrow{font-size:12px;letter-spacing:2px;color:#9ed4cd}.mono{font-family:ui-monospace,Consolas,monospace;font-size:12px}main{max-width:1460px;margin:auto;padding:28px max(3vw,20px) 60px}.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}.metric,.panel,.task{background:#fff;border:1px solid var(--line);border-radius:12px}.metric{padding:22px}.metric b{display:block;font-size:32px;line-height:1.2}.metric span,.meta{color:var(--muted);font-size:13px}.metric small{display:block;color:var(--muted);margin-top:8px}.notice{border-left:4px solid #ba791c;background:#fff7e9;margin:22px 0;padding:17px 22px}.notice p{margin:5px 0}.panel{padding:24px;margin-top:22px}.section-head{display:flex;justify-content:space-between;align-items:baseline;gap:15px;flex-wrap:wrap;margin-bottom:18px}.filters{display:flex;gap:12px;flex-wrap:wrap;margin:20px 0}label{font-size:12px;font-weight:650;display:flex;flex-direction:column;gap:5px}select,input{font:inherit;font-size:14px;border:1px solid #bacbd3;border-radius:6px;padding:10px 12px;background:white;color:var(--ink)}input{min-width:240px}.tasks{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.task{padding:19px}.task-top{display:flex;justify-content:space-between;gap:8px}.badge{font-size:11px;padding:2px 9px;border-radius:20px;background:#edf1f3;color:#455966;white-space:nowrap}.DONE{background:#daf1e8;color:#136b4c}.IN_PROGRESS{background:#deedf9;color:#205b87}.BLOCKED{background:#fae6e3;color:#9b3329}summary{cursor:pointer;font-size:13px;color:#087c72;font-weight:650;margin-top:17px}details p{font-size:13px}.detail,.evidence{overflow-wrap:anywhere}.milestones{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}.milestone{border-top:3px solid #b4d5d1;padding-top:14px}.milestone p{font-size:13px;color:var(--muted)}.columns{display:grid;grid-template-columns:1fr 1fr;gap:24px}.record{font-size:13px;overflow-wrap:anywhere}.record dl{display:grid;grid-template-columns:minmax(100px,180px) 1fr;gap:8px;border-top:1px solid var(--line);padding-top:14px}.record dt{font-weight:650}.record dd{margin:0}.record ul{padding-left:20px}.table-wrap{overflow:auto}table{border-collapse:collapse;width:100%;font-size:13px}th,td{text-align:left;padding:10px;border-bottom:1px solid var(--line)}th{background:#f3f6f7}.missing{color:#a45220}.muted{color:var(--muted)}footer{margin-top:25px;font-size:12px;color:var(--muted)}[hidden]{display:none!important}@media(max-width:1000px){.tasks,.milestones{grid-template-columns:repeat(2,1fr)}}@media(max-width:650px){.metrics,.tasks,.milestones,.columns{grid-template-columns:1fr}.panel{padding:18px}.record dl{display:block}.record dd{margin-bottom:12px}}@media print{header{background:white;color:black}.filters{display:none}.task{break-inside:avoid}body{background:white}.tasks{display:block}.task{margin-bottom:10px}}
</style></head><body><header><div class="eyebrow">MÜHENDİSLİK OPERASYONU / ESC V2</div><h1>Karardan doğrulanmış tasarıma.</h1><p>3 kW hedefli motor sürücü geliştirme programı. Şema, parça seçimi, PCB ve test işlerini kaynak kayıtlarıyla birlikte izleyin.</p><div class="mono">@REV@ · B1 tasarım tabanı · Güncelleme: @STAMP@</div></header><main>
<section class="metrics"><div class="metric"><b>@DONE@ / @TOTAL@</b><span>Tamamlanan ana görev</span><small>İş takibi; ürün hazır olma yüzdesi değildir.</small></div><div class="metric"><b>@ACTIVE@</b><span>Devam eden ana görev</span><small>Kabul kriteri kapanana kadar açık kalır.</small></div><div class="metric"><b>@BOM@</b><span>Eksik BOM bileşeni</span><small>Güncel B1 açık parça kaydından.</small></div><div class="metric"><b>@CHECKS@</b><span>Geçen şema kontrolü</span><small>ERC: @ERC@ ihlal · fiziksel doğrulama değil.</small></div></section>
<aside class="notice"><strong>Geliştirme aşaması · üretim serbest bırakılmadı</strong><p>@PCB@</p><p>Standart referansları ve dijital kontroller, tam standart uygunluğu veya 3 kW fiziksel performans kanıtı değildir.</p></aside>
<section class="panel"><div class="section-head"><h2>Sprint uygulama panosu</h2><span id="result-count" class="meta"></span></div><div class="filters"><label>Durum<select id="status"><option value="">Tüm durumlar</option>@STATUSOPTIONS@</select></label><label>Sprint<select id="sprint"><option value="">Tüm sprintler</option>@SPRINTOPTIONS@</select></label><label>Görev ara<input id="search" type="search" placeholder="Örn. ESC-03, koruma, şema"></label></div><div class="tasks">@TASKS@</div><p id="empty" hidden class="muted">Filtreyle eşleşen görev yok.</p></section>
<section class="panel"><div class="section-head"><h2>Tamamlama takvimi</h2>@SCHEDULELINK@</div><p class="meta">Hedef tarihler; tedarik, kullanım kapasitesi ve test kapılarına bağlıdır. Seri ürün teslim taahhüdü değildir.</p><div class="milestones">@MILESTONES@</div></section>
@OPTIONAL@
<section class="panel"><h2>Kanıt ve teslimler</h2><div class="columns"><div><h3>Doğrulamanın sınırı</h3><p>@PAGES@ şema sayfası, @NETS@ net ve @COMPONENTS@ elektriksel bileşen dijital bağlantı kontrolünde.</p><p>Çalışma zarfı: @ENVCOUNT@ model kontrolü / @SAMPLES@ örnek. Masa başı hesapları; motor, batarya, termal, EMC ve ilk enerji testlerinin yerine geçmez.</p><p>ERC ayarları ve devre dışı kontroller kaynak raporda kayıtlıdır. PCB DRC sonucu, şema ERC sonucundan ayrı tutulur.</p></div><div><h3>Kaynak dosyaları aç</h3><ul>@ARTIFACTS@</ul></div></div></section>
<section class="panel"><div class="section-head"><h2>Parça seçimi açıkları</h2>@BOMLINK@</div><p class="meta">Ana görevlerden ayrı bileşen kayıtları; kapatma için tam MPN, veri sayfası ve pad eşleşmesi gerekir.</p><details><summary>@BOM@ bileşeni göster</summary><div class="table-wrap"><table><thead><tr><th>Referans</th><th>Değer / işlev</th><th>Eksik alan</th></tr></thead><tbody>@BOMROWS@</tbody></table></div></details></section>
<footer>Bu dosya çevrimdışı bir anlık görüntüdür. Kaynaklar değiştikçe build_dashboard.py yeniden çalıştırılır; tarayıcı tek başına dosyaları izlemez. Tüm bağlantılar proje içindedir. Oluşturulma: @STAMP@.</footer></main><script id="snapshot" type="application/json">@JSON@</script><script>
const statusFilter=document.getElementById('status'),sprintFilter=document.getElementById('sprint'),search=document.getElementById('search');function filter(){let count=0;document.querySelectorAll('.task').forEach(card=>{const match=(!statusFilter.value||card.dataset.status===statusFilter.value)&&(!sprintFilter.value||card.dataset.sprint===sprintFilter.value)&&card.textContent.toLocaleLowerCase('tr').includes(search.value.toLocaleLowerCase('tr'));card.hidden=!match;if(match)count++});document.getElementById('result-count').textContent=count+' görev gösteriliyor';document.getElementById('empty').hidden=count!==0}for(const input of [statusFilter,sprintFilter,search])input.addEventListener('input',filter);filter();
</script></body></html>'''
values={'REV':esc(plan.get('revision','')),'STAMP':esc(stamp),'DONE':done,'TOTAL':len(tasks),'ACTIVE':active,'BOM':len(bom),'CHECKS':checks.get('checks_passed','—'),'ERC':checks.get('erc_violations','—'),'PCB':esc(pcb_text),'TASKS':''.join(cards),'STATUSOPTIONS':''.join('<option value="'+esc(s)+'">'+esc(status_names.get(s,s))+'</option>' for s in sorted({t.get('status','TODO') for t in tasks})),'SPRINTOPTIONS':''.join('<option value="'+str(s)+'">Sprint '+str(s)+'</option>' for s in sorted({t['sprint'] for t in tasks})),'SCHEDULELINK':link('planning/TAMAMLAMA_TAKVIMI.md','Takvim kaydı'),'MILESTONES':''.join(milestones),'OPTIONAL':optional,'PAGES':checks.get('pages','—'),'NETS':checks.get('nets','—'),'COMPONENTS':checks.get('electrical_components','—'),'ENVCOUNT':len(envelope.get('checks',[])),'SAMPLES':len(envelope.get('samples',[])),'ARTIFACTS':artifact_html,'BOMLINK':link('hardware_b1/bom_open_items.json','BOM kaynak kaydı'),'BOMROWS':bom_html,'JSON':json.dumps(data,ensure_ascii=False).replace('<','\u003c')}
for key,value in values.items():
    template=template.replace('@'+key+'@',str(value))
HERE.mkdir(parents=True,exist_ok=True)
(HERE/'index.html').write_text(template,encoding='utf-8')
(HERE/'snapshot.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(data,ensure_ascii=False))
