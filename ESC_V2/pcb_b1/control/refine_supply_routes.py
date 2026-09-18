from pathlib import Path
import json, re
import pcbnew as k
r=Path(__file__).resolve().parent
p=r/'ESC_3kW_CONTROL_B1_PLACEMENT.kicad_pcb'
b=k.LoadBoard(str(p)); f={x.GetReference():x for x in b.GetFootprints()}
def pt(x,y): return k.VECTOR2I(k.FromMM(x),k.FromMM(y))
report=json.loads((r/'supply_routes_20260915.json').read_text())
if report.get('final_verified'):
    raise SystemExit('Validated historical change: do not replay over current routing.')
original=(r/'before_supply_routes_20260915.pcb_snapshot').read_text(encoding='utf-8')
keep=set(re.findall(r'\(uuid "([^"]+)"\)',original))
removed=[]
for t in list(b.GetTracks()):
    if t.m_Uuid.AsString() not in keep:
        removed.append(t)
        b.Remove(t)
f['C1808'].SetPosition(pt(54,59)); f['C1808'].Reference().SetPosition(pt(54,61.5))
for ref,pos in [('C1802',(43.5,52)),('C1803',(60,56.5)),('C1804',(63.5,38))]:
    f[ref].Reference().SetTextAngle(k.EDA_ANGLE(0,k.DEGREES_T)); f[ref].Reference().SetPosition(pt(*pos))
paths=[[[47.4,49.45],[48.1,48.75]],[[47.4,47.55],[48.1,48.25]],[[59.45,52.5],[58.75,51.8]],[[57.55,52.5],[58.25,51.8]],[[62.6,40.55],[61.9,41.25]],[[62.6,42.45],[61.9,41.75]]]
for c,mid in zip(report['connections'],paths):
    pts=[c['path_mm'][0]]+mid+[c['path_mm'][-1]]; c['path_mm']=pts
    ref,n=c['from'].split('.'); pad=next(x for x in f[ref].Pads() if x.GetNumber()==n)
    for a,z in zip(pts,pts[1:]):
        t=k.PCB_TRACK(b); t.SetStart(pt(*a)); t.SetEnd(pt(*z)); t.SetWidth(k.FromMM(.2)); t.SetLayer(k.F_Cu); t.SetNet(pad.GetNet()); b.Add(t)
k.SaveBoard(str(p),b)
report['track_count']=len(b.GetTracks()); report['corrections']=['C1808 moved out of C1803 courtyard','Pad exits extended before 45 degree bends','Rotated references restored to horizontal']
(r/'supply_routes_20260915.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
