"""A deliberately invalid coupon tests KiCad rule execution, not ESC PCB compliance."""
from pathlib import Path
import pcbnew as p,json,subprocess,shutil
root=Path(__file__).resolve().parents[1]
out=root/'verification/rule_test';out.mkdir(exist_ok=True)
board=p.BOARD();board.SetCopperLayerCount(4)
vec=lambda x,y:p.VECTOR2I(p.FromMM(x),p.FromMM(y))
for a,b in [((0,0),(30,0)),((30,0),(30,20)),((30,20),(0,20)),((0,20),(0,0))]:
    e=p.PCB_SHAPE();e.SetShape(p.SHAPE_T_SEGMENT);e.SetStart(vec(*a));e.SetEnd(vec(*b));e.SetLayer(p.Edge_Cuts);e.SetWidth(p.FromMM(.05));board.Add(e)
for name,y,width in [('VBUS',5,.3),('GND',5.8,.3),('SIGNAL',12,.1)]:
    net=p.NETINFO_ITEM(board,name);board.Add(net)
    t=p.PCB_TRACK(board);t.SetStart(vec(5,y));t.SetEnd(vec(20,y));t.SetWidth(p.FromMM(width));t.SetLayer(p.F_Cu);t.SetNet(net);board.Add(t)
p.SaveBoard(str(out/'coupon.kicad_pcb'),board)
(out/'coupon.kicad_pro').write_text('{}',encoding='utf-8')
shutil.copyfile(root/'ESC_B1.kicad_dru',out/'coupon.kicad_dru')
cli='C:/Program Files/KiCad/10.0/bin/kicad-cli.exe'
r=subprocess.run([cli,'pcb','drc','--format','json','--output',str(out/'drc.json'),str(out/'coupon.kicad_pcb')],capture_output=True)
if r.returncode:raise RuntimeError(r.stdout.decode(errors='replace')+r.stderr.decode(errors='replace'))
d=json.loads((out/'drc.json').read_text(encoding='utf-8'))
v=d['violations'];descriptions='\n'.join(x['description'] for x in v)
assert 'ESC switching potential separation' in descriptions,descriptions
assert any(x['type']=='track_width' for x in v),descriptions
result={'status':'PASS','scope':'RULE_ENGINE_ONLY_NOT_PRODUCT_PCB','expected_failures_detected':['VBUS 1.00mm clearance','signal 0.20mm minimum track width'],'reported_violations':len(v)}
(root/'verification/rule_validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result))
