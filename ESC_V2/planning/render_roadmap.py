"""Render current project management state from backlog.json, preserving progress."""
from pathlib import Path
import json
out=Path(__file__).resolve().parent;data=json.loads((out/'backlog.json').read_text(encoding='utf-8'))
tasks=data['tasks'];ids={t['id'] for t in tasks};byid={t['id']:t for t in tasks}
assert len(ids)==len(tasks)
for t in tasks:
 assert all(d in ids for d in t['dependencies'])
 if t['status']=='DONE':assert t['evidence'],t['id']
 if t['status'] in ('READY','IN_PROGRESS','DONE'):assert all(byid[d]['status']=='DONE' for d in t['dependencies']),t['id']
def walk(id,path=()):
 assert id not in path
 for d in byid[id]['dependencies']:walk(d,path+(id,))
for id in ids:walk(id)
head=['# ESC — sprint uygulama yol haritası','',f'{data["revision"]} · {data["date"]} · Şema temeli {data["baseline"]}','',
'Asıl durum kaydı `backlog.json`; bu görünüm `render_roadmap.py` ile üretilir. [Sprint 1 uygulama ve karar kaydı](SPRINT_01_UYGULAMA.md).','',
'[HTML proje panosu](../dashboard/index.html) · [Ekip tasarım incelemesi](team_review.json) · [Değişiklik günlüğü](change_log.json).','',
'Hedef: ölçümle doğrulanmış 1.5 kW prototip, ardından marjlar yeterliyse 3 kW ürün adayı. İki haftalık sprintler planlama kutusudur; altı sprint 12 haftalık teslim garantisi değildir. Numune ve laboratuvar süreleri ayrıca izlenir. SP göreli karmaşıklıktır; saat değildir. Kapasite henüz ölçülmedi; yükler sprint taahhüdü sayılmaz. ESC-14 işe alınmadan daha küçük yönlendirme işlerine ayrılır.','',
'Akış: TODO → READY → IN_PROGRESS → REVIEW → DONE; engellenen iş BLOCKED ve gerekçe taşır. WIP: en fazla iki uygulama ve bir inceleme işi. DONE yalnız kabul ölçütü ve kanıtla; donanım için yazılım/DRC sonucu fiziksel test yerine geçmez. Roller ek personel ataması veya bağımsız onay anlamına gelmez.','',
'Sprint başında hazır işler seçilir; sonunda kanıt gösterimi, açık hata incelemesi ve retrospektif yapılır. Ölçümler: tamamlanan iş/SP, açık P0, eksik BOM, açık PCB bağlantısı/DRC ve fiziksel test sonucu. Henüz ölçülmeyen PCB/test verileri sıfır başarı olarak yazılmaz.','',
'Definition of Ready: girdiler, bağımlılıklar, araçlar ve ölçülebilir kabul kriteri hazır. Definition of Done: kriter geçti, kanıt ve revizyon kayıtlı, etkilenmiş şema/PCB/BOM/firmware tutarlı, inceleme tamam.','']
names={1:'Çalışma zarfı ve sistem kararları',2:'BOM, korumalar ve termal tasarım',3:'PCB ve firmware temeli',4:'Prototip üretim ve numune',5:'Devreye alma ve 1.5 kW',6:'3 kW ve ürün doğrulaması',0:'Tamamlanmış başlangıç kontrolleri'}
for s in [1,2,3,4,5,6,0]:
 head += [f'## {"Sprint "+str(s) if s else "Başlangıç"} — {names[s]}','']
 for t in tasks:
  if t['sprint']!=s:continue
  head += [f'- [{"x" if t["status"]=="DONE" else " "}] **{t["id"]} — {t["title"]}**',f'  - {t["status"]} · {t["priority"]} · {t["story_points"] if t["story_points"] is not None else "—"} SP · {t["owner"]}',f'  - Bağımlılıklar: {", ".join(t["dependencies"]) or "Yok"}. Risk: {", ".join(t["source_risks"]) or "Başlangıç kanıtı"}.',f'  - Kabul: {t["acceptance"]}']
  if t.get('remaining'):head += ['  - Kalan: '+t['remaining']]
  if t['evidence']:head += ['  - Kanıt: '+', '.join(f'[{e}]({e})' for e in t['evidence'])]
  head += ['']
head += ['## Gözden geçirme kararları','']
for d in data.get('review_decisions',[]):head += [f'- **{d["id"]} / {d["finding"]}** — {d["status"]}; ilgili işler: {", ".join(d.get("tasks",[])) or "Sprint uygulama kaydı"}.']
head += ['','## Geçiş kapıları','', '- G1: ESC-01–11 ve ESC-26 tasarım/tedarik kapsamı incelenmiş; kritik seçimler açık değil.', '- G2: ESC-14 ve ESC-17 tamam; prototip siparişi kullanıcı kararı.', '- G3: ESC-19 ve ESC-20 tamam; gerçek motor/koruma verisiyle enerji verme.', '- G4: ESC-22 tamam; yalnız 1.5 kW doğrulaması.', '- G5: ESC-23–25 tamam; güç sınıfı ve kalan resmi uygunluk kapsamı açık. Başarısız 3 kW testi kapsam/revizyon kararına döner.','', '## BOM alt işleri — ESC-10','', '61 başlangıç bileşen kaydı; farklı MPN sayısı değildir. Yeni parçalar eklenirse yeni alt iş açılır.','']
for t in data['bom_subtasks']:head += [f'- [{"x" if t["status"]=="DONE" else " "}] **{t["id"]}** — {t["value"]}; {t["status"]}; eksik: {", ".join(t["missing"])}.']
(out/'AGILE_ROADMAP.md').write_text('\n'.join(head)+'\n',encoding='utf-8')
print('Roadmap rendered; dependency graph, ready states and completion evidence checked.')
