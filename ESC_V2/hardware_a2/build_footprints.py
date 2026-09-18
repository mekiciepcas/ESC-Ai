"""Local RTA0040B land pattern from TI DRV8353F Rev B pp80-82.
Dimensions checked against drawing text; assembler stencil/via review still required.
"""
from pathlib import Path
import json
root=Path(__file__).resolve().parent
lib=root/'ESC_A2.pretty';lib.mkdir(exist_ok=True)
name='TI_RTA0040B_6x6_P0.5_EP4.15'
s=f'(footprint "{name}" (version 20241229) (generator "pcbnew") (layer "F.Cu") (attr smd) (descr "TI RTA0040B; DRV8353F Rev B pp80-82; assembly review required")'
for prop,val,y,layer in [('Reference','REF**',-4,'F.SilkS'),('Value',name,4,'F.Fab')]:
 s+=f'(property "{prop}" "{val}" (at 0 {y} 0) (layer "{layer}") (effects (font (size 1 1) (thickness 0.15))))'
s+='(fp_rect (start -3 -3) (end 3 3) (stroke (width 0.1) (type default)) (layer "F.Fab"))'
s+='(fp_rect (start -3.5 -3.5) (end 3.5 3.5) (stroke (width 0.05) (type default)) (layer "F.CrtYd"))'
s+='(fp_circle (center -3.5 -2.8) (end -3.35 -2.8) (stroke (width 0.15) (type default)) (fill solid) (layer "F.SilkS"))'
for i in range(40):
 side=i//10;j=i%10
 if side==0:x,y,w,h=-2.9,-2.25+j*.5,.6,.22
 elif side==1:x,y,w,h=-2.25+j*.5,2.9,.22,.6
 elif side==2:x,y,w,h=2.9,2.25-j*.5,.6,.22
 else:x,y,w,h=2.25-j*.5,-2.9,.22,.6
 s+=f'(pad "{i+1}" smd roundrect (at {x:.3f} {y:.3f}) (size {w} {h}) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.2))'
s+='(pad "41" smd rect (at 0 0) (size 4.15 4.15) (layers "F.Cu" "F.Mask"))'
for x in [-1.37,0,1.37]:
 for y in [-1.37,0,1.37]:s+=f'(pad "" smd rect (at {x} {y}) (size 1.17 1.17) (layers "F.Paste"))'
(lib/(name+'.kicad_mod')).write_text(s+')',encoding='utf-8')
(root/'fp-lib-table').write_text('(fp_lib_table (lib (name "ESC_A2") (type "KiCad") (uri "${KIPRJMOD}/ESC_A2.pretty") (options "") (descr "Local engineering footprints")))',encoding='utf-8')
(root/'footprint_sources.json').write_text(json.dumps({name:{'source':'https://www.ti.com/lit/ds/symlink/drv8353f.pdf','revision':'B','drawing':'RTA0040B 4219112/A 07/2018','source_pages_1_based':[80,81,82],'body_mm':[6,6],'pitch_mm':.5,'pad_center_span_mm':5.8,'pad_mm':[.6,.22],'EP_mm':[4.15,4.15],'paste_coverage_percent':9*1.17**2/4.15**2*100,'thermal_vias':'PCB placement pending; filled/plugged/tented process to be agreed','status':'DIMENSIONED_FROM_DATASHEET_NOT_ASSEMBLY_QUALIFIED'}},indent=2),encoding='utf-8')
print('RTA0040B: 40 perimeter + EP41, 9 paste windows generated.')
