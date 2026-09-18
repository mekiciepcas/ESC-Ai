from pathlib import Path
import json,shutil,hashlib
import pcbnew as k
r=Path(__file__).resolve().parent; root=r.parents[1]; hw=root/'hardware_b1'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
refs={'J1901':5,'J2001':3,'J2002':3,'J2003':2,'J2101':5}
lib=hw/'ESC_B1.pretty'; std='C:/Program Files/KiCad/10.0/share/kicad/footprints/Connector_PinHeader_2.54mm.pretty'
for n in (2,3,5):
    mpn=f'61300{n}11121'; name=f'WE_{mpn}_1x{n:02d}_P2.54_Drill1.10'
    f=k.FootprintLoad(std,f'PinHeader_1x{n:02d}_P2.54mm_Vertical')
    f.SetFPID(k.LIB_ID('ESC_B1',name)); f.SetLibDescription(f'Wurth {mpn}; 2.54mm pitch; manufacturer nominal 1.10mm holes. PoC header.')
    for pad in f.Pads():pad.SetDrillSize(k.VECTOR2I(k.FromMM(1.1),k.FromMM(1.1)))
    k.FootprintSave(str(lib),f)
p=r/'ESC_3kW_CONTROL_B1_PLACEMENT.kicad_pcb'; backup=r/'before_headers_20260916.pcb_snapshot'
if backup.exists(): raise SystemExit('Already applied: inspect before replay.')
shutil.copy2(p,backup); b=k.LoadBoard(str(p))
def sig(b):return sorted((f.GetReference(),a.GetNumber(),a.GetNetname(),a.GetPosition().x,a.GetPosition().y) for f in b.GetFootprints() for a in f.Pads())
before=sig(b)
for f in b.GetFootprints():
    ref=f.GetReference()
    if ref not in refs:continue
    n=refs[ref];mpn=f'61300{n}11121';name=f'WE_{mpn}_1x{n:02d}_P2.54_Drill1.10'
    assert len(list(f.Pads()))==n
    pads=sorted(f.Pads(),key=lambda a:int(a.GetNumber()))
    for a,z in zip(pads,pads[1:]):assert abs(k.ToMM((a.GetPosition()-z.GetPosition()).EuclideanNorm())-2.54)<.001
    for pad in pads:pad.SetDrillSize(k.VECTOR2I(k.FromMM(1.1),k.FromMM(1.1)))
    f.SetFPID(k.LIB_ID('ESC_B1',name))
    for key,value in [('MPN',mpn),('Manufacturer','Wurth Elektronik')]:f.SetField(key,value);f.GetField(key).SetVisible(False)
k.SaveBoard(str(p),b); check=k.LoadBoard(str(p));assert sig(check)==before
for f in check.GetFootprints():
    if f.GetReference() in refs:
        assert all(abs(k.ToMM(a.GetDrillSize().x)-1.1)<.0001 for a in f.Pads())
(r/'fp-lib-table').write_text('(fp_lib_table (lib (name "ESC_B1") (type "KiCad") (uri "${KIPRJMOD}/../../hardware_b1/ESC_B1.pretty") (options "") (descr "Project footprints")))\n',encoding='utf-8')
rp=r/'placement_report.json'; report=read(rp); report['provisional_packages']=[x for x in report['provisional_packages'] if x['ref'] not in refs]
for x in report['placed']:
    if x['ref'] in refs:
        n=refs[x['ref']];x['footprint']=f'ESC_B1:WE_61300{n}11121_1x{n:02d}_P2.54_Drill1.10'
report['board_sha256']=hashlib.sha256(p.read_bytes()).hexdigest();write(rp,report)
write(root/'verification/headers_20260916.json',{'refs':refs,'pad_nets_and_positions_unchanged':True,'pitch_mm':2.54,'drill_mm':1.1,'readback':'PASS','scope':'Unkeyed PoC headers, not final locking harness','sources':[f'https://www.we-online.com/components/products/datasheet/61300{n}11121.pdf' for n in (2,3,5)]})
print('PASS: five headers, unchanged nets/positions, 1.10mm holes, local library saved.')
