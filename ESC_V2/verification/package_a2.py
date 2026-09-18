from pathlib import Path
import json,hashlib,zipfile
from PIL import Image,ImageDraw
from pypdf import PdfReader
root=Path(__file__).resolve().parents[1]
reader=PdfReader(root/'ESC_3kW_A2_semalar.pdf')
assert len(reader.pages)==29
assert all(page.mediabox.width>page.mediabox.height for page in reader.pages)
images=sorted((root/'verification').glob('a2_pdf-*.png'))
assert len(images)==29
thumbs=Image.new('RGB',(5*440,6*335),'#dce1e6');draw=ImageDraw.Draw(thumbs)
for i,p in enumerate(images):
 im=Image.open(p).convert('RGB');im.thumbnail((430,305))
 x=(i%5)*440;y=(i//5)*335
 thumbs.paste(im,(x,y+20));draw.text((x+5,y+3),'PAGE '+str(i+1),fill='black')
thumbs.save(root/'verification/a2_contact_sheet.png')
files=[]
for folder in ['hardware_a2','hardware']:
 files.extend(p for p in (root/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts and not p.name.endswith('.lck'))
files.extend((root/'verification/svg_a2').glob('*.svg'))
for name in ['START_HERE.md','ESC_3kW_A2_semalar.pdf','design_basis.json','calculate_design.py','calculated_budget.json','ESC_V2_3kW_tasarim_temeli.md','ESC_V2_inceleme_ve_aksiyonlar.md','verification/ESC_3kW_A2.net','verification/erc_a2.json','verification/a2_checks.json','verification/a2_contact_sheet.png','verification/package_a2.py']:
 files.append(root/name)
manifest={'revision':'A2','status':'ENGINEERING_REVIEW_NOT_FOR_FABRICATION','date':'2026-09-13','pdf_pages':len(reader.pages),'files':{str(p.relative_to(root)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
(root/'A2_file_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
files.append(root/'A2_file_manifest.json')
out=root/'ESC_3kW_A2_inceleme_paketi.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files:z.write(p,Path('ESC_V2')/p.relative_to(root))
with zipfile.ZipFile(out) as z:assert z.testzip() is None
print(f'PDF {len(reader.pages)} pages, {len(files)} packaged files, ZIP {out.stat().st_size} bytes, CRC check PASS.')
