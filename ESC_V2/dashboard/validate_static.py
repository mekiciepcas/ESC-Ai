from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlparse
import json
import re
import subprocess

r = Path(__file__).resolve().parent
root = r.parent
repo = root.parent
html = (r / 'index.html').read_text(encoding='utf-8')


def load_json(path):
    return json.loads((root / path).read_text(encoding='utf-8-sig'))


def pct(value):
    """Mirror build_dashboard.py semantics for optional progress dimensions."""
    try:
        n = float(value)
    except (TypeError, ValueError):
        n = 0.0
    return max(0.0, min(100.0, n))


class Check(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cards = 0
        self.links = []
        self.h2 = []
        self._capture_h2 = False
        self._h2_buf = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'article' and 'task' in a.get('class', '').split():
            self.cards += 1
        if tag == 'a' and a.get('href'):
            self.links.append(a['href'])
        if tag == 'h2':
            self._capture_h2 = True
            self._h2_buf = []

    def handle_data(self, data):
        if self._capture_h2:
            self._h2_buf.append(data)

    def handle_endtag(self, tag):
        if tag == 'h2' and self._capture_h2:
            self.h2.append(''.join(self._h2_buf).strip())
            self._capture_h2 = False
            self._h2_buf = []


c = Check()
c.feed(html)
snapshot = json.loads((r / 'snapshot.json').read_text(encoding='utf-8'))
embedded_match = re.search(r'<script id="snapshot" type="application/json">(.*?)</script>', html, re.S)
assert embedded_match, 'embedded dashboard snapshot missing'
embedded = json.loads(embedded_match.group(1))
assert snapshot == embedded, 'snapshot.json and embedded dashboard JSON differ'

backlog = load_json('planning/uav_backlog.json')
progress = load_json('planning/REQUIREMENTS_PROGRESS.json')
state = load_json('planning/autonomy_state.json')
g0 = load_json('planning/G0_INPUT_CLOSURE_PACKET.json')
register = load_json('planning/SCHEMATIC_REVISION_REGISTER.json')

tasks = backlog.get('tasks', [])
state_p = state.get('progress_percentages', {})
expected = {
    'plan_revision': backlog.get('revision'),
    'task_count': len(tasks),
    'done_count': sum(t.get('status') == 'DONE' for t in tasks),
    'active_count': sum(t.get('status') == 'IN_PROGRESS' for t in tasks),
    'blocked_count': sum(t.get('status') == 'BLOCKED' for t in tasks),
    'requirements_structure_percent': float(progress['requirements_structure']['percent']),
    'g1_system_freeze_percent': float(progress['g1_system_freeze']['percent']),
    'backlog_done_percent': float(progress['backlog']['done_percent']),
    'major_gate_closure_percent': float(progress['gate_closure']['percent']),
    # These are legacy/optional dashboard dimensions. AUTO-STATE may intentionally
    # omit them; the builder then renders 0 via pct(None). Validation must mirror
    # that behavior instead of crashing with KeyError.
    'u1_kicad_scaffold_percent': pct(state_p.get('u1_kicad_architecture_scaffold_percent')),
    'u1_component_bearing_schematic_percent': pct(state_p.get('u1_component_bearing_schematic_percent')),
    'schematic_revision_control_percent': pct(state_p.get('schematic_revision_control_policy_percent')),
    'missing_g0_inputs': sum(x.get('value') is None for x in g0.get('required_inputs', [])),
    'next_schematic_revision': register['revision_series']['next_component_bearing_revision'],
    'current_task': state.get('current_task'),
    'last_run_status': state.get('last_run_status'),
}
for key, value in expected.items():
    assert snapshot.get(key) == value, f'snapshot/source mismatch for {key}: {snapshot.get(key)!r} != {value!r}'

assert c.cards == snapshot['task_count'], f"task card count mismatch: {c.cards} != {snapshot['task_count']}"
links = [x for x in c.links if not urlparse(x).scheme and not x.startswith('#')]
for link in links:
    target = (r / unquote(link.split('#')[0])).resolve()
    assert target.exists(), f'broken local dashboard link: {link}'

required_sections = {
    'Son güncellemeler — basit anlatım',
    'İlerleme çubukları',
    'Şu anda ne yapıyoruz?',
    'Sıradaki işler',
    'Neden bazı işler bekliyor?',
    'Senden gereken gerçek girdiler',
    'Ana görevler',
}
missing_sections = sorted(required_sections - set(c.h2))
assert not missing_sections, f'missing dashboard sections: {missing_sections}'

required_text = [
    'UAV REBASELINE',
    'Requirement yapısı',
    'G1 gerçek değer kapanışı',
    'Gerçek U1 şeması',
    'U1-SCH-R001',
]
for text in required_text:
    assert text in html, f'missing current-UAV dashboard text: {text}'

forbidden_stale_text = [
    '3 kW hedefli motor sürücü geliştirme programı',
    'B1 tasarım tabanı · Güncelleme:',
    'Sprint uygulama panosu',
]
for text in forbidden_stale_text:
    assert text not in html, f'legacy dashboard text leaked into current dashboard: {text}'

try:
    current_head = subprocess.check_output(
        ['git', 'rev-parse', '--short=12', 'HEAD'], cwd=repo, text=True
    ).strip()
except Exception:
    current_head = None
if current_head:
    assert snapshot.get('source_commit') == current_head, (
        f"snapshot source_commit stale during validation: {snapshot.get('source_commit')} != {current_head}"
    )

result = {
    'static_validation': 'PASS',
    'source_consistency_validation': 'PASS',
    'legacy_dashboard_leak_check': 'PASS',
    'task_cards': c.cards,
    'local_links_checked': len(links),
    'embedded_json_matches_snapshot': True,
    'required_sections_checked': len(required_sections),
    'source_fields_checked': len(expected),
    'plan_revision': snapshot['plan_revision'],
    'browser_visual_validation': 'NOT_PERFORMED',
    'note': 'Validation proves generated HTML/snapshot consistency with current repository records; it is not a browser rendering or engineering-design qualification test.'
}
(r / 'validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(result)
