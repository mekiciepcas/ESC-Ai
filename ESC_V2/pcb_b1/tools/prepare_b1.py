"""Preserve A2; derive the B1 schematic generators with a corrected interboard contract."""
from pathlib import Path
root=Path(__file__).resolve().parents[2]
dst=root/'hardware_b1'
if (dst/'build_b1.py').exists():
    raise SystemExit('B1 already exists. This one-time migration cannot overwrite current engineering changes. Edit the maintained B1 generator directly.')
dst.mkdir(exist_ok=True)
for name in ('build_a2.py','build_footprints.py','verify_a2.py'):
    text=(root/'hardware_a2'/name).read_text(encoding='utf-8').replace('A2','B1').replace('a2','b1').replace('2026-09-13','2026-09-14')
    if name=='build_a2.py':
        text=text.replace("if p['kind']=='CONN40':p['nets']['39']='+5V';", "if p['kind']=='CONN40':p['nets']['38']='TEMP_MOTOR';p['nets']['39']='+5V';")
        text=text.replace('B1 pin 39 now carries +5V for control-board Hall supply.', 'B1 pin38 TEMP_MOTOR; pin39 +5V; both connector ends use the same numbering. Not compatible with A2 pin38 GND.')
        text=text.replace('B1 düzeltme: pin39 +5V;', 'B1 düzeltme: pin38 TEMP_MOTOR (A2 GND ile uyumsuz); pin39 +5V;')
        text += "\n(HERE/(PROJECT+'.kicad_dru')).write_text((HERE.parent/'pcb_b1/ESC_B1.kicad_dru').read_text(encoding='utf-8'),encoding='utf-8')\n"
    if name=='verify_a2.py':
        text=text.replace("drv=kinds['DRV'][0]['ref'];", "for c in kinds['CONN40']:check(c['ref']+' motor temperature transferred on pin38',actual[c['ref'],'38']=='TEMP_MOTOR')\n\ndrv=kinds['DRV'][0]['ref'];")
    (dst/name.replace('a2','b1')).write_text(text,encoding='utf-8')
print(dst)
