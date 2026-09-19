"""Build the offline UAV ESC project dashboard from current planning records.

The dashboard intentionally separates planning/structure progress from product-value
closure and physical validation. It never infers missing engineering values.
"""
from pathlib import Path
from datetime import datetime
from html import escape
from urllib.parse import quote
import json
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = ROOT.parent


def read(path, fallback=None):
    p = ROOT / path
    if not p.exists():
        return fallback
    return json.loads(p.read_text(encoding="utf-8-sig"))


def esc(value):
    return escape(str(value), quote=True)


def link(path, label=None, base=None):
    p = ((base or ROOT) / path).resolve()
    if not p.is_relative_to(ROOT.resolve()) or not p.is_file():
        return '<span class="missing">' + esc(label or path) + ' · dosya yok</span>'
    href = '../' + quote(p.relative_to(ROOT.resolve()).as_posix(), safe='/')
    return '<a href="' + href + '">' + esc(label or p.name) + ' ↗</a>'


def git_head():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short=12", "HEAD"],
            cwd=REPO,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "—"


def pct(value):
    try:
        n = float(value)
    except (TypeError, ValueError):
        n = 0.0
    return max(0.0, min(100.0, n))


def friendly_machine_text(text):
    if not text:
        return "—"
    words = str(text).replace("_", " ").strip()
    replacements = {
        "G0 INPUT CLOSURE": "G0 araç bilgilerini tamamlama",
        "G1 SYSTEM FREEZE": "G1 sistem değerlerini dondurma",
        "REQUIREMENT INDEPENDENT MIGRATION EVIDENCE": "şemaya güvenli geçiş için bağımsız kanıt çalışmaları",
        "component bearing": "komponent içeren",
        "schematic": "şema",
    }
    for old, new in replacements.items():
        words = words.replace(old, new)
    return words[:1].upper() + words[1:]


backlog = read('planning/uav_backlog.json', {}) or {}
progress = read('planning/REQUIREMENTS_PROGRESS.json', {}) or {}
state = read('planning/autonomy_state.json', {}) or {}
register = read('planning/SCHEMATIC_REVISION_REGISTER.json', {}) or {}
g0 = read('planning/G0_INPUT_CLOSURE_PACKET.json', {}) or {}
kicad = read('planning/KICAD_CI_VERIFICATION.json', {}) or {}
b1_audit = read('planning/B1_KICAD_BASELINE_AUDIT.json', {}) or {}

tasks = backlog.get('tasks', [])
done = sum(t.get('status') == 'DONE' for t in tasks)
active = sum(t.get('status') == 'IN_PROGRESS' for t in tasks)
blocked = sum(t.get('status') == 'BLOCKED' for t in tasks)
status_names = {
    'DONE': 'Tamamlandı',
    'IN_PROGRESS': 'Sürüyor',
    'BLOCKED': 'Bekliyor',
    'TODO': 'Sırada',
    'READY': 'Hazır',
}

requirements_structure = pct(progress.get('requirements_structure', {}).get('percent'))
g1_freeze = pct(progress.get('g1_system_freeze', {}).get('percent'))
backlog_done = pct(progress.get('backlog', {}).get('done_percent'))
major_gates = pct(progress.get('gate_closure', {}).get('percent'))
state_p = state.get('progress_percentages', {})
scaffold = pct(state_p.get('u1_kicad_architecture_scaffold_percent'))
component_schematic = pct(state_p.get('u1_component_bearing_schematic_percent'))
revision_control = pct(state_p.get('schematic_revision_control_policy_percent'))

required_inputs = g0.get('required_inputs', [])
missing_g0 = [x for x in required_inputs if x.get('value') is None]

field_names = {
    'payload_nominal_kg': 'Nominal faydalı yük',
    'airframe_empty_mass_kg': 'Boş gövde ağırlığı',
    'battery_mass_kg': 'Batarya ağırlığı',
    'mission_equipment_mass_kg': 'Görev ekipmanı ağırlığı',
    'target_total_flight_time_min': 'Hedef toplam uçuş süresi',
    'target_hover_time_min': 'Hedef hover süresi',
    'minimum_ambient_c': 'Minimum ortam sıcaklığı',
    'maximum_ambient_c': 'Maksimum ortam sıcaklığı',
    'maximum_operating_altitude_m': 'Maksimum çalışma irtifası',
    'maximum_wind_m_s': 'Maksimum rüzgâr',
    'single_motor_failure_requirement': 'Tek motor arızasında istenen davranış',
    'coaxial_allowed': 'Coaxial rotor kullanımına izin',
    'maximum_vehicle_span_m': 'Maksimum araç açıklığı',
    'rain_dust_ingress_target': 'Yağmur/toz koruma hedefi',
}

simple_updates = []
if revision_control >= 100:
    simple_updates.append('Şema versiyonlama kuralı aktif: eski şemaların üzerine yazılmıyor; her elektriksel değişiklik yeni revizyon açacak.')
if state_p.get('legacy_b1_kicad_reproducible_baseline_audit_percent') == 100.0:
    simple_updates.append('Eski B1 KiCad şeması gerçek KiCad CLI ile açıldı, netlist üretildi ve kayıtlı ERC kontrolleri tekrarlandı.')
if state_p.get('u1_kicad_scaffold_parser_erc_validation_percent') == 100.0:
    simple_updates.append('Yeni U1 şema iskeleti KiCad parser/netlist/ERC hattından geçti; bu sadece iskelet doğrulamasıdır.')
if component_schematic == 0:
    simple_updates.append('Gerçek U1 güç devresine henüz komponent yerleştirilmedi; yanlış parça/değer kilitlememek için G0/G1/G2 girdileri bekleniyor.')
if missing_g0:
    simple_updates.append(f'Gerçek boyutlandırmayı başlatmak için {len(missing_g0)} araç/görev girdisi hâlâ eksik.')

cards = []
for t in tasks:
    s = t.get('status', 'TODO')
    evidence_links = []
    for ev in t.get('evidence', []):
        evidence_links.append(link(ev, base=ROOT/'planning'))
    details = []
    if t.get('remaining'):
        details.append('<p><strong>Kalan:</strong> ' + esc(t['remaining']) + '</p>')
    if t.get('acceptance'):
        details.append('<p><strong>Bitti sayılması için:</strong> ' + esc(t['acceptance']) + '</p>')
    if evidence_links:
        details.append('<p><strong>Kanıt:</strong> ' + ' · '.join(evidence_links) + '</p>')
    cards.append(
        '<article class="task" data-status="{status}" data-gate="{gate}">'
        '<div class="task-top"><span class="mono">{id} · {priority} · {gate}</span>'
        '<span class="badge {status}">{status_name}</span></div>'
        '<h3>{title}</h3>'
        '<details><summary>Teknik detay</summary>{details}</details>'
        '</article>'.format(
            status=esc(s), gate=esc(t.get('gate', '')),
            id=esc(t.get('id', '')), priority=esc(t.get('priority', '')),
            status_name=esc(status_names.get(s, s)), title=esc(t.get('title', '')),
            details=''.join(details) or '<p>Ek detay yok.</p>',
        )
    )

blocker_items = []
for b in state.get('blocked_tasks', [])[:8]:
    blocker_items.append(
        '<li><strong>{}</strong><span>{}</span></li>'.format(
            esc(friendly_machine_text(b.get('task'))),
            esc(friendly_machine_text(b.get('reason'))),
        )
    )

next_items = [
    '<li>' + esc(friendly_machine_text(x)) + '</li>'
    for x in state.get('next_candidates', [])[:6]
]

g0_rows = []
for x in missing_g0:
    name = field_names.get(x.get('field'), x.get('field', ''))
    unit = x.get('unit') or ''
    g0_rows.append(
        '<tr><td>{}</td><td class="mono">{}</td><td>{}</td></tr>'.format(
            esc(name), esc(x.get('id', '')), esc(unit or 'seçim / metin')
        )
    )

allocated = register.get('allocated_revisions', [])
next_rev = register.get('revision_series', {}).get('next_component_bearing_revision', '—')

source_links = [
    ('planning/REQUIREMENTS_PROGRESS.json', 'Yüzde kaynağı'),
    ('planning/uav_backlog.json', 'Ana backlog'),
    ('planning/autonomy_state.json', 'Son çalışma state'),
    ('planning/G0_USER_INPUT_FORM.md', 'Eksik araç girdileri formu'),
    ('planning/SCHEMATIC_REVISION_REGISTER.json', 'Şema revizyon kaydı'),
    ('planning/SCHEMATIC_VERSIONING_POLICY.md', 'Şema versiyonlama kuralı'),
    ('planning/U1_G3_ERC_POLICY.json', 'G3 ERC kontrol kuralı'),
    ('planning/KICAD_CI_VERIFICATION.json', 'U1 KiCad CI kanıtı'),
    ('planning/B1_KICAD_BASELINE_AUDIT.json', 'B1 KiCad audit kanıtı'),
]
source_html = ''.join('<li>'+link(p, label)+'</li>' for p, label in source_links if (ROOT/p).exists())

stamp = datetime.now().astimezone().isoformat(timespec='seconds')
head = git_head()
snapshot = {
    'generated_at': stamp,
    'source_commit': head,
    'plan_revision': backlog.get('revision'),
    'task_count': len(tasks),
    'done_count': done,
    'active_count': active,
    'blocked_count': blocked,
    'requirements_structure_percent': requirements_structure,
    'g1_system_freeze_percent': g1_freeze,
    'backlog_done_percent': backlog_done,
    'major_gate_closure_percent': major_gates,
    'u1_kicad_scaffold_percent': scaffold,
    'u1_component_bearing_schematic_percent': component_schematic,
    'schematic_revision_control_percent': revision_control,
    'missing_g0_inputs': len(missing_g0),
    'next_schematic_revision': next_rev,
    'current_task': state.get('current_task'),
    'last_run_status': state.get('last_run_status'),
}


def metric(title, value, note, cls=''):
    return f'''<div class="metric {cls}"><span>{esc(title)}</span><b>{esc(value)}</b><small>{esc(note)}</small></div>'''

metrics = ''.join([
    metric('Requirement yapısı', f'{requirements_structure:g}%', 'Başlıklar ve takip yapısı hazır; ürün değerleri anlamına gelmez.'),
    metric('G1 gerçek değer kapanışı', f'{g1_freeze:g}%', '46 kritik satırın kanıtla kapanma oranı.'),
    metric('Backlog tamamlanma', f'{backlog_done:g}%', f'{done}/{len(tasks)} ana görev resmi DONE.'),
    metric('Gerçek U1 şeması', f'{component_schematic:g}%', 'Komponent içeren production-intent şema; henüz başlamadı.'),
])

progress_rows = [
    ('Requirement altyapısı', requirements_structure, 'Yapı hazır'),
    ('G1 sistem değerleri', g1_freeze, 'Gerçek voltaj/akım/mission değerlerinin kapanışı'),
    ('Ana backlog', backlog_done, 'Sadece DONE görevler sayılıyor'),
    ('Major gate kapanışı', major_gates, 'G0/G1 açık olduğu için henüz gate kapanmadı'),
    ('U1 KiCad iskeleti', scaffold, 'Blok yapısı ve araç zinciri'),
    ('Şema revision kontrolü', revision_control, 'Yeni revizyon açmadan eski şema değiştirilmeyecek'),
    ('Gerçek komponentli U1 şeması', component_schematic, 'G1/G2 sonrası başlayacak'),
]
progress_html = ''.join(
    f'''<div class="progress-row"><div><strong>{esc(name)}</strong><span>{esc(note)}</span></div><div class="bar"><i style="width:{pct(value):g}%"></i></div><b>{pct(value):g}%</b></div>'''
    for name, value, note in progress_rows
)

simple_updates_html = ''.join('<li>'+esc(x)+'</li>' for x in simple_updates)

html = f'''<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ESC Sistemi · UAV Proje Dashboard</title>
<style>
:root{{--ink:#172b38;--muted:#60717c;--line:#dae3e7;--paper:#f4f7f8;--panel:#fff;--teal:#087c72;--blue:#23638a;--amber:#b87816;--red:#9b3c35;--green:#227052}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--paper);color:var(--ink);font:15px/1.55 system-ui,-apple-system,Segoe UI,sans-serif}} a{{color:#006d78;text-underline-offset:3px}}
header{{background:#132e3c;color:white;padding:38px max(4vw,20px)}} header p{{max-width:920px;color:#c5d8e0;margin:8px 0}} h1{{margin:4px 0;font-size:clamp(27px,4vw,42px)}} h2{{font-size:21px;margin:0}} h3{{font-size:16px;margin:10px 0}} .mono{{font-family:ui-monospace,Consolas,monospace;font-size:12px}}
main{{max-width:1480px;margin:auto;padding:24px max(3vw,18px) 60px}} .metrics{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}} .metric,.panel,.task{{background:var(--panel);border:1px solid var(--line);border-radius:12px}} .metric{{padding:20px}} .metric span,.metric small,.muted{{color:var(--muted)}} .metric span{{display:block;font-size:13px}} .metric b{{display:block;font-size:31px;line-height:1.2;margin:5px 0}} .metric small{{font-size:12px}}
.panel{{padding:22px;margin-top:18px}} .section-head{{display:flex;align-items:baseline;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:16px}} .simple{{font-size:16px}} .simple li{{margin:8px 0}} .notice{{background:#fff8e9;border-left:4px solid var(--amber);padding:16px 18px;margin-top:18px}} .good{{background:#eef8f4;border-left-color:var(--green)}}
.progress-row{{display:grid;grid-template-columns:minmax(250px,1.6fr) minmax(160px,3fr) 65px;gap:15px;align-items:center;padding:10px 0;border-bottom:1px solid #edf1f3}} .progress-row span{{display:block;font-size:12px;color:var(--muted)}} .bar{{height:9px;background:#e5ecef;border-radius:8px;overflow:hidden}} .bar i{{height:100%;display:block;background:var(--teal)}}
.columns{{display:grid;grid-template-columns:1fr 1fr;gap:18px}} .blockers{{padding:0;margin:0;list-style:none}} .blockers li{{border-bottom:1px solid var(--line);padding:10px 0}} .blockers strong,.blockers span{{display:block}} .blockers span{{font-size:13px;color:var(--muted);margin-top:2px}}
.filters{{display:flex;gap:12px;flex-wrap:wrap;margin:12px 0 18px}} label{{font-size:12px;font-weight:650;display:flex;flex-direction:column;gap:4px}} select,input{{padding:9px 11px;border:1px solid #b9c9d1;border-radius:7px;background:#fff;font:inherit}} input{{min-width:250px}} .tasks{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}} .task{{padding:16px}} .task-top{{display:flex;justify-content:space-between;gap:8px}} .badge{{font-size:11px;border-radius:15px;padding:3px 9px;background:#edf1f3;white-space:nowrap}} .DONE{{background:#daf2e8;color:#17694d}} .IN_PROGRESS{{background:#dfeef8;color:#205b87}} .BLOCKED{{background:#f9e5e2;color:#91392f}} details summary{{cursor:pointer;color:var(--teal);font-size:13px;font-weight:650}} details p{{font-size:13px}}
table{{border-collapse:collapse;width:100%;font-size:13px}} th,td{{padding:9px;border-bottom:1px solid var(--line);text-align:left}} th{{background:#f3f6f7}} .table-wrap{{overflow:auto}} .chips{{display:flex;gap:8px;flex-wrap:wrap}} .chip{{background:#edf3f5;border-radius:20px;padding:6px 10px;font-size:12px}} .sources li{{margin:6px 0}} .missing{{color:#a14e20}} footer{{font-size:12px;color:var(--muted);margin-top:22px}}
@media(max-width:1000px){{.metrics,.tasks{{grid-template-columns:repeat(2,1fr)}}.columns{{grid-template-columns:1fr}}}} @media(max-width:650px){{.metrics,.tasks{{grid-template-columns:1fr}}.progress-row{{grid-template-columns:1fr 60px}}.progress-row .bar{{grid-column:1/-1;grid-row:2}}}}
</style></head>
<body><header><div class="mono">ESC SİSTEMİ · UAV REBASELINE · {esc(state.get('branch','uav-rebaseline'))}</div><h1>Proje nerede, ne yaptık, sırada ne var?</h1><p>70–100 kg faydalı yük hedefli ağır UAV ESC çalışmasının sade görünümü. Yüzdeler birbirine karıştırılmaz: “yapı hazır” demek “ürün hazır” demek değildir.</p><div class="mono">Kaynak commit: {esc(head)} · Dashboard üretim zamanı: {esc(stamp)}</div></header>
<main>
<section class="metrics">{metrics}</section>
<aside class="notice"><strong>Tek cümlelik durum:</strong> KiCad ve versiyonlama altyapısı çalışıyor; şimdi gerçek drone girdilerini kapatıp voltaj/akım değerlerini kanıtla dondurmamız gerekiyor. Bu yapılmadan güç devresine rastgele komponent koymuyoruz.</aside>
<section class="panel"><div class="section-head"><h2>Son güncellemeler — basit anlatım</h2><span class="muted">{esc(state.get('last_run_status',''))}</span></div><ul class="simple">{simple_updates_html}</ul></section>
<section class="panel"><div class="section-head"><h2>İlerleme çubukları</h2><span class="muted">Aynı yüzde farklı anlamlara gelmez</span></div>{progress_html}</section>
<section class="columns">
<div class="panel"><div class="section-head"><h2>Şu anda ne yapıyoruz?</h2></div><p class="simple"><strong>{esc(friendly_machine_text(state.get('current_task')))}</strong></p><p class="muted">Sıradaki şema revizyonu: <strong>{esc(next_rev)}</strong> · Açılmış gerçek U1 revizyonu: <strong>{len(allocated)}</strong></p><div class="chips"><span class="chip">B1: frozen reference</span><span class="chip">U1-R000: boş iskelet</span><span class="chip">U1-R001: henüz açılmadı</span></div></div>
<div class="panel"><div class="section-head"><h2>Sıradaki işler</h2></div><ol>{''.join(next_items) or '<li>State içinde sıradaki iş kaydı yok.</li>'}</ol></div>
</section>
<section class="columns">
<div class="panel"><div class="section-head"><h2>Neden bazı işler bekliyor?</h2></div><ul class="blockers">{''.join(blocker_items) or '<li>Aktif blocker kaydı yok.</li>'}</ul></div>
<div class="panel"><div class="section-head"><h2>Senden gereken gerçek girdiler</h2>{link('planning/G0_USER_INPUT_FORM.md','Formu aç')}</div><p>{len(missing_g0)} alan eksik. Bunları rakip dronelardan veya eski B1 tasarımından tahmin etmiyoruz.</p><div class="table-wrap"><table><thead><tr><th>Bilgi</th><th>ID</th><th>Birim/tip</th></tr></thead><tbody>{''.join(g0_rows)}</tbody></table></div></div>
</section>
<section class="panel"><div class="section-head"><h2>Ana görevler</h2><span id="result-count" class="muted"></span></div><div class="filters"><label>Durum<select id="status"><option value="">Tümü</option>{''.join('<option value="'+esc(s)+'">'+esc(status_names.get(s,s))+'</option>' for s in sorted({t.get('status','TODO') for t in tasks}))}</select></label><label>Gate<select id="gate"><option value="">Tümü</option>{''.join('<option value="'+esc(g)+'">'+esc(g)+'</option>' for g in sorted({t.get('gate','') for t in tasks if t.get('gate')}) )}</select></label><label>Ara<input id="search" type="search" placeholder="Örn. batarya, şema, PCB"></label></div><div class="tasks">{''.join(cards)}</div><p id="empty" hidden class="muted">Filtreye uyan görev yok.</p></section>
<section class="columns"><div class="panel"><h2>KiCad / şema kontrol durumu</h2><p>U1 iskelet doğrulaması: <strong>{'kayıtlı' if kicad else 'kayıt yok'}</strong></p><p>B1 tekrar üretilebilir audit: <strong>{'kayıtlı' if b1_audit else 'kayıt yok'}</strong></p><p>Revision policy: <strong>{revision_control:g}%</strong></p><p class="muted">Bunlar fiziksel motor testi, termal test veya uçuş onayı değildir.</p></div><div class="panel"><h2>Kaynak kayıtları</h2><ul class="sources">{source_html}</ul></div></section>
<footer>Bu sayfa kaynak JSON/MD kayıtlarından üretilir. Bilinmeyen değerler dashboard tarafından tahmin edilmez. Güncelleme kaynağı: build_dashboard.py. Commit: {esc(head)}.</footer>
</main>
<script id="snapshot" type="application/json">{json.dumps(snapshot,ensure_ascii=False).replace('<','\\u003c')}</script>
<script>
const statusFilter=document.getElementById('status'),gateFilter=document.getElementById('gate'),search=document.getElementById('search');
function filter(){{let count=0;document.querySelectorAll('.task').forEach(card=>{{const ok=(!statusFilter.value||card.dataset.status===statusFilter.value)&&(!gateFilter.value||card.dataset.gate===gateFilter.value)&&card.textContent.toLocaleLowerCase('tr').includes(search.value.toLocaleLowerCase('tr'));card.hidden=!ok;if(ok)count++}});document.getElementById('result-count').textContent=count+' görev gösteriliyor';document.getElementById('empty').hidden=count!==0}}
for(const el of [statusFilter,gateFilter,search])el.addEventListener('input',filter);filter();
</script></body></html>'''

HERE.mkdir(parents=True, exist_ok=True)
(HERE/'index.html').write_text(html, encoding='utf-8')
(HERE/'snapshot.json').write_text(json.dumps(snapshot, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(snapshot, ensure_ascii=False))
