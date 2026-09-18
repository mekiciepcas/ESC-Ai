"""Validate actual exported KiCad netlist, package pad numbering and release completeness."""
from pathlib import Path
import sys,json,collections,html,re
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root.parent/'hardware'))
from sexpr import parse,children,child
parts=json.loads((root/'connection_manifest.json').read_text(encoding='utf-8'))
pages=json.loads((root/'page_manifest.json').read_text(encoding='utf-8'))
netlist=parse((root.parent/'verification/ESC_3kW_A2.net').read_text(encoding='utf-8'))
actual={};nets={}
for n in children(child(netlist,'nets'),'net'):
 name=child(n,'name')[1];nets[name]=[]
 for pin in children(n,'node'):
  pair=(child(pin,'ref')[1],child(pin,'pin')[1]);actual[pair]=name;nets[name].append(pair)
checks=[]
def check(name,condition):
 checks.append({'name':name,'passed':bool(condition)})
 if not condition:raise AssertionError(name)
check('All symbol references unique',len({p['ref'] for p in parts})==len(parts))
for p in parts:
 if p['kind']=='FLAG':continue
 for pin,net in p['nets'].items():
  if net is not None:check(f'{p["ref"]}.{pin} -> {net}',actual.get((p['ref'],pin))==net)
kinds=collections.defaultdict(list)
for p in parts:kinds[p['kind']].append(p)
check('12 power MOSFETs',len(kinds['NMOS'])==12)
check('3 independent Kelvin shunts',len(kinds['SHUNT'])==3)
check('No fake discrete Kelvin net ties',not any('NET-TIE' in p['value'] for p in parts))
check('12 test points',len(kinds['TP'])==12)
for c in kinds['CONN40']:check(c['ref']+' Hall supply transferred on pin39',actual[c['ref'],'39']=='+5V')
drv=kinds['DRV'][0]['ref'];mcu=kinds['MCU'][0]['ref'];latch=kinds['LATCH'][0]['ref']
check('VM separate from VDRAIN',actual[drv,'3']=='+12V' and actual[drv,'4']=='VBUS')
check('PB12 break and asynchronous CLR share fault',actual[mcu,'34']==actual[latch,'6']=='HARD_FAULT_N')
check('Six independent PWM inhibit channels',len(kinds['AND'])==6)
for p in kinds['AND']:check(p['ref']+' inhibited by latch',p['nets']['1']=='LATCH_STATE')
erc=json.loads((root.parent/'verification/erc_a2.json').read_text(encoding='utf-8'))
violations=[v for s in erc['sheets'] for v in s['violations']]
check('KiCad ERC zero violations',not violations)
fp=parse((root/'ESC_A2.pretty/TI_RTA0040B_6x6_P0.5_EP4.15.kicad_mod').read_text(encoding='utf-8'))
check('RTA pads1..41 present',{p[1] for p in children(fp,'pad') if p[1]}=={str(i) for i in range(1,42)})
check('RTA EP41 is 4.15mm square',any(p[1]=='41' and child(p,'size')[1:]==['4.15','4.15'] for p in children(fp,'pad')))
groups={};missing=[];badfp=[]
for p in parts:
 if p['kind']=='FLAG':continue
 key=(p['value'],p['mpn'],p['footprint'])
 if key not in groups:groups[key]={'value':p['value'],'mpn':p['mpn'],'footprint':p['footprint'],'references':[],'notes':[]}
 g=groups[key];g['references'].append(p['ref'])
 if p['note'] and p['note'] not in g['notes']:g['notes'].append(p['note'])
 if not p['mpn'] or not p['footprint']:missing.append({'ref':p['ref'],'value':p['value'],'missing':[k for k in ['mpn','footprint'] if not p[k]]})
 if p['footprint']:
  lib,name=p['footprint'].split(':');f=(root/(lib+'.pretty') if lib=='ESC_A2' else Path('C:/Program Files/KiCad/10.0/share/kicad/footprints')/(lib+'.pretty'))/(name+'.kicad_mod')
  if not f.exists():badfp.append(p['footprint'])
check('Assigned footprints exist',not badfp)
for g in groups.values():g['quantity']=len(g['references']);g['status']='REVIEW_REQUIRED' if not g['mpn'] or not g['footprint'] else 'SELECTED_NOT_QUALIFIED'
report={'status':'SCHEMATIC_REVIEW_NOT_MANUFACTURING_RELEASE','pages':len(pages)+1,'symbols':len(parts),'electrical_components':len(parts)-len(kinds['FLAG']),'nets':len(nets),'checks_passed':len(checks),'erc_violations':len(violations),'default_disabled_erc_checks':erc['ignored_checks'],'incomplete_bom_components':len(missing),'checks':checks}
(root.parent/'verification/a2_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
(root/'bom_review.json').write_text(json.dumps(list(groups.values()),ensure_ascii=False,indent=2),encoding='utf-8')
(root/'bom_open_items.json').write_text(json.dumps(missing,ensure_ascii=False,indent=2),encoding='utf-8')
(root/'mcu_pin_contract.json').write_text(json.dumps(kinds['MCU'][0],ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ['checks','default_disabled_erc_checks']},ensure_ascii=False))
