from pathlib import Path
import json,shutil,hashlib
import pcbnew as k
r=Path(__file__).resolve().parent; root=r.parents[1]
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
old={x['ref']:x for x in read(root/'verification/before_bom_batch2_20260915/connection_manifest.json')}
new={x['ref']:x for x in read(root/'hardware_b1/connection_manifest.json')}
assert old.keys()==new.keys()
assert all(old[ref]['nets']==x['nets'] and old[ref]['value']==x['value'] for ref,x in new.items())
changed={ref:x for ref,x in new.items() if x['mpn']!=old[ref]['mpn']}
assert len(changed)==14
for ref,x in changed.items():
    assert x['footprint']=='Capacitor_SMD:C_0805_2012Metric'
    assert x['nets']['2']=='GND'
    assert x['nets']['1'] not in ('VBUS','PH_A','PH_B','PH_C')
board=r/'ESC_3kW_CONTROL_B1_PLACEMENT.kicad_pcb'; backup=r/'before_bom_batch2_20260915.pcb_snapshot'
if backup.exists(): raise SystemExit('Historical batch already started; inspect before replay.')
shutil.copy2(board,backup)
b=k.LoadBoard(str(board))
def signature(b): return sorted((f.GetReference(),a.GetNumber(),a.GetNetname()) for f in b.GetFootprints() for a in f.Pads())
before=signature(b); placed=[]
for f in b.GetFootprints():
    if f.GetReference() in changed:
        x=changed[f.GetReference()]; assert f.GetFPID().GetLibItemName()=='C_0805_2012Metric'
        for name,value in [('MPN',x['mpn']),('Manufacturer','KEMET')]:
            f.SetField(name,value); f.GetField(name).SetVisible(False)
        placed.append(f.GetReference())
assert placed==['C1805']
k.SaveBoard(str(board),b); b2=k.LoadBoard(str(board)); assert signature(b2)==before
assert next(f for f in b2.GetFootprints() if f.GetReference()=='C1805').GetFieldText('MPN')==changed['C1805']['mpn']
rp=r/'placement_report.json'; report=read(rp)
report['provisional_packages']=[x for x in report['provisional_packages'] if x['ref']!='C1805']
report['board_sha256']=hashlib.sha256(board.read_bytes()).hexdigest()
report['source_manifest_sha256']=hashlib.sha256((root/'hardware_b1/connection_manifest.json').read_bytes()).hexdigest(); write(rp,report)
result={'date':'2026-09-15','changed':{ref:x['mpn'] for ref,x in changed.items()},'count':14,'all_schematic_nets_and_values_unchanged':True,'pcb_pad_nets_unchanged':True,'pcb_updated':placed,'other_13_scope':'Schematic only: power PCB does not yet exist','source_urls':['https://search.kemet.com/download/specsheet/C0805C102J5GACTU','https://search.kemet.com/download/specsheet/C0805C103J5GACTU','https://search.kemet.com/download/specsheet/C0805C475K8RACTU','https://www.digikey.com/en/products/detail/kemet/C0805C102J5GACTU/411135','https://www.digikey.com/en/products/detail/kemet/C0805C103J5GACTU/2211711','https://www.digikey.com/en/products/detail/kemet/C0805C475K8RACTU/3317450'],'limits':['Stock is a consulted listing, not a reservation','C1805 effective DC-biased capacitance and transient response require test','ADC settling, reference startup and protection dynamics remain open','No production certification or physical validation claimed']}
write(root/'verification/bom_batch2_20260915.json',result)
print('PASS: 14 selections, unchanged schematic nets/values and PCB pad nets; C1805 MPN read back.')
