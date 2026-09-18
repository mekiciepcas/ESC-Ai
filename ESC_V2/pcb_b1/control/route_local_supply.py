"""Bounded, non-repeatable MCU bypass routing change; preserves original snapshot."""
from pathlib import Path
import json, shutil
import pcbnew as k

root = Path(__file__).resolve().parent
path = root / 'ESC_3kW_CONTROL_B1_PLACEMENT.kicad_pcb'
backup = root / 'before_supply_routes_20260915.pcb_snapshot'
if backup.exists():
    raise SystemExit('Snapshot exists: inspect current board before applying again.')
shutil.copy2(path, backup)
b = k.LoadBoard(str(path))
fp = {f.GetReference(): f for f in b.GetFootprints()}
def signature():
    return sorted((f.GetReference(), p.GetNumber(), p.GetNetname()) for f in b.GetFootprints() for p in f.Pads())
before = signature()
def point(x,y): return k.VECTOR2I(k.FromMM(x),k.FromMM(y))
def pad(ref,n): return next(p for p in fp[ref].Pads() if p.GetNumber()==str(n))
def xy(p): return [k.ToMM(p.GetPosition().x),k.ToMM(p.GetPosition().y)]
def move(ref,x,y,angle,rx,ry):
    f=fp[ref]; f.SetOrientationDegrees(angle); f.SetPosition(point(x,y)); f.Reference().SetPosition(point(rx,ry))
move('C1802',46.8,48.5,90,43.5,46)
move('C1803',58.5,54,180,59,56)
move('C1804',63.5,41.5,270,63.5,38.5)
move('R1802',68,39,0,68,37)
connections=[]
def route(ref,n,mpin,intermediate):
    a=pad(ref,n); z=pad('U1701',mpin)
    assert a.GetNetname()==z.GetNetname()
    pts=[xy(a)]+intermediate+[xy(z)]
    for start,end in zip(pts,pts[1:]):
        t=k.PCB_TRACK(b); t.SetStart(point(*start)); t.SetEnd(point(*end)); t.SetWidth(k.FromMM(.2)); t.SetLayer(k.F_Cu); t.SetNet(a.GetNet()); b.Add(t)
    connections.append({'from':f'{ref}.{n}','to':f'U1701.{mpin}','net':a.GetNetname(),'path_mm':pts})
route('C1802',1,16,[[47.5,48.75]])
route('C1802',2,15,[[47.5,48.25]])
route('C1803',1,32,[[58.75,53.3]])
route('C1803',2,31,[[58.25,53.3]])
route('C1804',1,48,[[62.8,41.25]])
route('C1804',2,47,[[62.8,41.75]])
assert signature()==before
k.SaveBoard(str(path),b)
(root/'supply_routes_20260915.json').write_text(json.dumps({'connections':connections,'pad_nets_unchanged':True,'checked_pads':len(before),'track_count':len(b.GetTracks()),'scope':'Three local digital bypass pairs; supply distribution and ground plane still incomplete.'},indent=2),encoding='utf-8')
print(json.dumps(connections,indent=2))
