from pathlib import Path
import json,shutil,hashlib
import pcbnew as k
r=Path(__file__).resolve().parent; root=r.parents[1]
p=r/'ESC_3kW_CONTROL_B1_PLACEMENT.kicad_pcb'
backup=r/'before_bom_passives_20260915.pcb_snapshot'
if backup.exists():
    assert backup.read_bytes()==p.read_bytes(), 'Existing backup differs; inspect instead of replaying.'
else: shutil.copy2(p,backup)
b=k.LoadBoard(str(p))
def pads(board): return sorted((f.GetReference(),a.GetNumber(),a.GetNetname()) for f in board.GetFootprints() for a in f.Pads())
before=pads(b)
old=json.loads((root/'verification/before_bom_20260915/connection_manifest.json').read_text(encoding='utf-8'))
new=json.loads((root/'hardware_b1/connection_manifest.json').read_text(encoding='utf-8'))
assert {x['ref']:x['nets'] for x in old}=={x['ref']:x['nets'] for x in new}
selected={x['ref']:x for x in new if x['ref'] in ('C1807','C2101','C2102','C2103')}
for f in b.GetFootprints():
    if f.GetReference() in selected:
        x=selected[f.GetReference()]
        assert f.GetFPID().GetLibItemName()=='C_0805_2012Metric'
        f.SetField('MPN',x['mpn'])
        f.SetField('Manufacturer','Murata' if f.GetReference()=='C1807' else 'KEMET')
        for name in ('MPN','Manufacturer'): f.GetField(name).SetVisible(False)
k.SaveBoard(str(p),b)
check=k.LoadBoard(str(p)); assert pads(check)==before
for f in check.GetFootprints():
    if f.GetReference() in selected: assert f.GetFieldText('MPN')==selected[f.GetReference()]['mpn']
result={'date':'2026-09-15','selected':{ref:x['mpn'] for ref,x in selected.items()},'schematic_nets_unchanged':True,'pcb_pad_nets_unchanged':True,'pcb_mpn_readback':'PASS','status':'POC_COMPONENT_SELECTION_NOT_BOARD_RELEASE','sources':['https://www.murata.com/en-us/products/productdetail?partno=GRM21BR71C105KA01%23','https://www.digikey.com/en/products/detail/murata-electronics/GRM21BR71C105KA01K/2546959','https://search.kemet.com/download/specsheet/C0805C102J5GACTU','https://www.digikey.com/en/products/detail/kemet/C0805C102J5GACTU/411135'],'stock_note':'Distributor pages reported active and in stock when consulted; not reserved; purchase-time recheck required.'}
(root/'verification/bom_passives_20260915.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
rp=r/'placement_report.json'; report=json.loads(rp.read_text(encoding='utf-8')); report['source_manifest_sha256']=hashlib.sha256((root/'hardware_b1/connection_manifest.json').read_bytes()).hexdigest();report['board_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
rp.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(result)
