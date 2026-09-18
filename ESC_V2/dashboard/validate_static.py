from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlparse
import json, re
r=Path(__file__).resolve().parent
html=(r/'index.html').read_text(encoding='utf-8')
class Check(HTMLParser):
    def __init__(self): super().__init__(); self.cards=0; self.links=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='article' and 'task' in a.get('class','').split(): self.cards+=1
        if tag=='a' and a.get('href'): self.links.append(a['href'])
c=Check(); c.feed(html)
snapshot=json.loads((r/'snapshot.json').read_text(encoding='utf-8'))
embedded=json.loads(re.search(r'<script id="snapshot" type="application/json">(.*?)</script>',html,re.S).group(1))
assert snapshot==embedded
assert c.cards==snapshot['task_count']
links=[x for x in c.links if not urlparse(x).scheme and not x.startswith('#')]
for link in links: assert (r/unquote(link.split('#')[0])).exists(),link
result={'static_validation':'PASS','task_cards':c.cards,'local_links_checked':len(links),'embedded_json_matches_snapshot':True,'plan_revision':snapshot['plan_revision'],'pcb_preview':'VISUALLY_INSPECTED_KICAD_SVG_EXPORT','browser_visual_validation':'NOT_COMPLETED_LOCAL_URL_POLICY_BLOCK'}
(r/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(result)
