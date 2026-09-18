"""Initial editable control-board placement; provisional packages are explicit.
No routing, power planes or manufacturing release. Do not overwrite manual PCB edits.
"""
from pathlib import Path
import pcbnew as k,json,shutil,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
name='ESC_3kW_CONTROL_B1_PLACEMENT';target=HERE/(name+'.kicad_pcb')
if target.exists():raise SystemExit('PCB exists; preserve manual edits. Modify through KiCad or reviewed revision.')
parts=json.loads((ROOT/'hardware_b1/connection_manifest.json').read_text(encoding='utf-8'))
parts=[p for p in parts if p['page'][:2] in ('10','11','12','13') or p['ref']=='J2702']
lib=Path('C:/Program Files/KiCad/10.0/share/kicad/footprints')
board=k.BOARD();board.SetCopperLayerCount(4)
vec=lambda x,y:k.VECTOR2I(k.FromMM(x),k.FromMM(y))
pos={'U1701':(55,45),'J2702':(108,24),'U2001':(29,32),'J2001':(17,28),'J2002':(17,47),'J2003':(17,64),'J1901':(37,76),'J2101':(78,76),'Y1901':(41,40),
'C1801':(47,37),'C1802':(47,53),'C1803':(63,53),'C1804':(63,37),'C1805':(69,32),'C1806':(47,33),'C1807':(52,55),'C1808':(56,55),'C1809':(60,57),'R1801':(40,45),'C1810':(40,49),'R1802':(66,41),
'R1901':(70,45),'R1902':(70,49),'C1901':(40,36),'R1903':(89,70),'D1901':(94,70),'R2001':(28,25),'C2001':(34,35),'R2002':(22,28),
'R2101':(71,65),'R2102':(71,60),'C2101':(71,56),'R2103':(77,65),'R2104':(77,60),'C2102':(77,56),'R2105':(83,65),'R2106':(83,60),'C2103':(83,56)}
assert set(pos)=={p['ref'] for p in parts}
nets={}
for n in sorted({n for p in parts for n in p['nets'].values() if n}):
 net=k.NETINFO_ITEM(board,n);board.Add(net);nets[n]=net
candidate=[];placed=[]
for p in parts:
 fp=p['footprint']
 if not fp:
  if p['kind']=='C':fp='Capacitor_SMD:C_0805_2012Metric'
  elif p['kind'].startswith('CONN'):
   count=int(p['kind'][4:]);form='2x20' if count==40 else f'1x{count:02}'
   fp='Connector_PinHeader_2.54mm:PinHeader_'+form+'_P2.54mm_Vertical'
  elif p['kind']=='OSC':fp='Oscillator:Oscillator_SMD_Abracon_ASE-4Pin_3.2x2.5mm'
  elif p['ref']=='D1901':fp='LED_SMD:LED_0805_2012Metric'
  else:raise ValueError(p)
  candidate.append(dict(ref=p['ref'],footprint=fp,status='PLACEMENT_ENVELOPE_ONLY_MPN_NOT_APPROVED',reason='B1 symbol had no assigned package; dimensions and pin mapping must match selected orderable part before routing freeze'))
 family,item=fp.split(':');f=k.FootprintLoad(str(lib/(family+'.pretty')),item);assert f,fp
 f.SetReference(p['ref']);f.SetValue(p['value']);board.Add(f);f.SetPosition(vec(*pos[p['ref']]))
 f.Value().SetVisible(False);f.Reference().SetTextSize(vec(1,1));f.Reference().SetTextThickness(k.FromMM(.15))
 f.Reference().SetPosition(vec(pos[p['ref']][0],pos[p['ref']][1]-2))
 pad_numbers={pad.GetNumber() for pad in f.Pads() if pad.GetNumber()}
 assert pad_numbers==set(p['nets']), (p['ref'],pad_numbers,set(p['nets']))
 for pad in f.Pads():
  n=p['nets'].get(pad.GetNumber())
  if n:pad.SetNet(nets[n])
 placed.append(dict(ref=p['ref'],footprint=fp,at_mm=pos[p['ref']],nets=p['nets']))
for i,(x,y) in enumerate([(15,15),(105,15),(105,85),(15,85)],1):
 f=k.FootprintLoad(str(lib/'MountingHole.pretty'),'MountingHole_3.2mm_M3');board.Add(f);f.SetReference('H'+str(i));f.SetPosition(vec(x,y));f.Value().SetVisible(False)
for start,end in [((10,10),(110,10)),((110,10),(110,90)),((110,90),(10,90)),((10,90),(10,10))]:
 e=k.PCB_SHAPE();e.SetShape(k.SHAPE_T_SEGMENT);e.SetStart(vec(*start));e.SetEnd(vec(*end));e.SetLayer(k.Edge_Cuts);e.SetWidth(k.FromMM(.05));board.Add(e)
for text,x,y in [('ESC CONTROL B1 / PLACEMENT',55,16),('NO POWER STAGE / NOT FOR FAB',55,19),('J2702 PIN38 TEMP_MOTOR',82,23)]:
 t=k.PCB_TEXT(board);t.SetText(text);t.SetPosition(vec(x,y));t.SetTextSize(vec(1,1));t.SetTextThickness(k.FromMM(.15));t.SetLayer(k.F_SilkS);board.Add(t)
title=board.GetTitleBlock();title.SetTitle('ESC 3kW control board / initial placement');title.SetRevision('B1-P0');title.SetDate('2026-09-14');board.SetTitleBlock(title)
k.SaveBoard(str(target),board)
(HERE/(name+'.kicad_pro')).write_text('{}',encoding='utf-8')
shutil.copyfile(ROOT/'pcb_b1/ESC_B1.kicad_dru',HERE/(name+'.kicad_dru'))
readback=k.LoadBoard(str(target));refs={f.GetReference():f for f in readback.GetFootprints()}
checked=0
for p in parts:
 for pad in refs[p['ref']].Pads():
  n=p['nets'].get(pad.GetNumber())
  assert pad.GetNetname()==(n or ''),(p['ref'],pad.GetNumber(),pad.GetNetname(),n)
  checked+=1
report={'status':'INITIAL_PLACEMENT_UNROUTED_NOT_FOR_FABRICATION','size_mm':[100,80],'copper_layers':4,'intended_layers':['F.Cu signal','In1.Cu GND (not poured)','In2.Cu power/signal (not poured)','B.Cu signal'],'electrical_footprints':len(parts),'mounting_holes':4,'net_count':len(nets),'checked_pads':checked,'track_count':len(list(readback.GetTracks())),'provisional_packages':candidate,'placed':placed,'source_manifest_sha256':hashlib.sha256((ROOT/'hardware_b1/connection_manifest.json').read_bytes()).hexdigest()}
(HERE/'placement_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print({k:v for k,v in report.items() if k not in ('placed','provisional_packages')})
