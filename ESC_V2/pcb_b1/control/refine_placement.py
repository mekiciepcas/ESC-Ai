"""Reviewed first-placement adjustments, leaves electrical assignments unchanged."""
from pathlib import Path
import pcbnew as k,json
root=Path(__file__).resolve().parent
path=root/'ESC_3kW_CONTROL_B1_PLACEMENT.kicad_pcb'
b=k.LoadBoard(str(path));f={x.GetReference():x for x in b.GetFootprints()}
v=lambda x,y:k.VECTOR2I(k.FromMM(x),k.FromMM(y))
for ref,xy in {'J2702':(102,24),'C2001':(36,37),'C1807':(51,55),'C1808':(57,55),'C1809':(63,59)}.items():f[ref].SetPosition(v(*xy))
for ref,xy in {'J2702':(103,20),'U1701':(55,34),'U2001':(29,39),'Y1901':(40,43),'J2001':(17,24),'J2002':(17,43),'J2003':(17,60),'J1901':(37,72),'J2101':(78,72),'C1807':(50,57),'C1808':(57,57),'C1809':(63,61),'C2001':(36,35)}.items():f[ref].Reference().SetPosition(v(*xy))
k.SaveBoard(str(path),b)
report=json.loads((root/'placement_report.json').read_text(encoding='utf-8'))
for p in report['placed']:
    fp=f[p['ref']];p['at_mm']=[k.ToMM(fp.GetPosition().x),k.ToMM(fp.GetPosition().y)]
    for pad in fp.Pads():assert pad.GetNetname()==(p['nets'].get(pad.GetNumber()) or '')
report['refinement']='Moved interboard header inside outline, separated CAN capacitor courtyard, relocated references; all pad nets preserved.'
(root/'placement_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
