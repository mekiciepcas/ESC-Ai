"""Cross-board connectivity check independent of ERC; mutation-tested."""
from pathlib import Path
import json,sys,collections,copy
root=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(root/'hardware'))
from sexpr import parse,children,child
parts=json.loads((root/'hardware_b1/connection_manifest.json').read_text(encoding='utf-8'))
export=parse((root/'verification/ESC_3kW_B1.net').read_text(encoding='utf-8'))
actual={}
for net in children(child(export,'nets'),'net'):
    for pin in children(net,'node'):
        actual[child(pin,'ref')[1],child(pin,'pin')[1]]=child(net,'name')[1]
headers=[p for p in parts if p['kind']=='CONN40']
def audit(headers):
    errors=[]
    if len(headers)!=2:return ['expected two interboard headers'],[]
    if headers[0]['nets']!=headers[1]['nets']:errors.append('header pin mappings differ')
    users=collections.defaultdict(lambda:collections.defaultdict(list))
    for p in parts:
        if p['kind'] in ('FLAG','TP','CONN40'):continue
        board='control' if p['page'][:2] in ('10','11','12','13') else 'power'
        for pin,n in p['nets'].items():
            if n:users[n][board].append(p['ref']+'.'+pin)
    cross=[]
    for n,boards in sorted(users.items()):
        if len(boards)<2:continue
        pins=[i for i,v in headers[0]['nets'].items() if v==n]
        if not pins:errors.append('missing interboard net '+n)
        cross.append(dict(net=n,pins=pins,endpoints=dict(boards)))
    return errors,cross
errors,cross=audit(headers)
for p in headers:
    for pin,net in p['nets'].items():
        if actual.get((p['ref'],pin))!=net:errors.append(p['ref']+'.'+pin+' differs in exported KiCad netlist')
assert not errors,errors
mutated=copy.deepcopy(headers)
for p in mutated:p['nets']['38']='GND'
assert 'missing interboard net TEMP_MOTOR' in audit(mutated)[0]
mutated=copy.deepcopy(headers);mutated[0]['nets']['39']='GND'
assert 'header pin mappings differ' in audit(mutated)[0]
report=dict(status='PASS',cross_board_net_count=len(cross),errors=errors,mutation_checks=['A2 motor temperature omission detected','one-sided pin mismatch detected'],cross_board_nets=cross,compatibility='B1 pin38 TEMP_MOTOR replaces A2 GND; do not mix revisions')
(root/'pcb_b1/verification/interface_audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('PASS:',len(cross),'cross-board nets; exported netlist checked; two injected failures detected')
