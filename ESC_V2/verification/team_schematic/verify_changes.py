"""Compare exported electrical connectivity independently of drawing coordinates."""
from pathlib import Path
import json, xml.etree.ElementTree as ET
root=Path(__file__).resolve().parent
def netmap(path):
    tree=ET.parse(path)
    return {(node.get('ref'),node.get('pin')): net.get('name')
            for net in tree.findall('./nets/net') for node in net.findall('node')}
before=netmap(root/'before.net'); after=netmap(root/'after.net')
changes=[{'ref':key[0],'pin':key[1],'before':before.get(key),'after':after.get(key)}
         for key in sorted(before.keys() | after.keys()) if before.get(key)!=after.get(key)]
def violations(name):
    data=json.loads((root/name).read_text(encoding='utf-8'))
    return sum(len(sheet.get('violations',[])) for sheet in data['sheets'])
report={'before_connected_pins':len(before),'after_connected_pins':len(after),
        'connectivity_changes':changes,'erc_before':violations('before_erc.json'),
        'erc_after':violations('after_erc.json'),
        'scope':'Graphics readability and explicit reviewed electrical corrections; no standards certification.'}
(root/'comparison.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
