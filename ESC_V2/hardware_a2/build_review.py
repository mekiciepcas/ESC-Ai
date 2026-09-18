"""Portable Turkish review index for the KiCad engineering project."""
from pathlib import Path
import json,html,re,math
root=Path(__file__).resolve().parent
pages=json.loads((root/'page_manifest.json').read_text(encoding='utf-8'))
report=json.loads((root.parent/'verification/a2_checks.json').read_text(encoding='utf-8'))
bom=json.loads((root/'bom_review.json').read_text(encoding='utf-8'))
issues=json.loads((root/'release_register.json').read_text(encoding='utf-8'))
e=html.escape
ratio=3320/(99800+3320)
budget={'revision':'A2','assumptions':'Nominal resistor calculations, NOT worst-case electrical qualification','voltage_ratio':ratio,'adc_54_6v':54.6*ratio,'adc_80v':80*ratio,'oc_low_v':3.3*10/36.1,'oc_high_v':3.3*26.1/36.1,'oc_nominal_a':(3.3*26.1/36.1-1.65)/.005,'bus_ov_nominal_v':(3.3*10/17.5)/ratio,'divider_filter_hz':1/(2*math.pi*(1000+99800*3320/103120)*1e-9),'bulk_energy_j':.5*.001410*54.6**2,'bleed_to_5v_seconds':100000*.001410*math.log(54.6/5),'current_shunt_upper_bound_w':80**2*.0005,'future_precharge_example':{'scope':'330 ohm unloaded-capacitor example ONLY, no implemented precharge circuit','resistance_ohm':330,'initial_current_a':54.6/330,'initial_power_w':54.6**2/330,'time_to_99_percent_s':4.60517*330*.001410,'load_caveat':'Auxiliary power draw can prevent charging to 99 percent; size with actual load.'}}
(root/'engineering_calculations.json').write_text(json.dumps(budget,ensure_ascii=False,indent=2),encoding='utf-8')
style='''body{margin:0;background:#f3f5f7;color:#182935;font:16px system-ui,sans-serif}header,main{max-width:1250px;margin:auto;padding:28px}header{border-bottom:3px solid #234e65}h1{font-size:30px}h2{margin-top:36px;font-size:22px}p,li{line-height:1.6}a{color:#12618b}nav{display:flex;gap:22px;flex-wrap:wrap}.status{padding:16px;background:#fff2d9;border-left:5px solid #986214}.metrics{display:flex;gap:32px;margin:24px 0}.metrics strong{display:block;font-size:29px}.metrics span{color:#526675}details{background:white;border:1px solid #ced7de;margin:14px 0}summary{cursor:pointer;padding:18px;font-weight:650}.content{padding:0 20px 20px}.schematic{width:100%;height:auto;background:#fff}table{border-collapse:collapse;width:100%;background:white;font-size:13px}td,th{padding:10px;text-align:left;vertical-align:top;border-bottom:1px solid #dce1e5}.scroll{overflow:auto}.badge{font-size:12px;color:#754500}code{font-size:13px}@media print{details{break-inside:avoid}nav{display:none}}'''
s='<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ESC 3 kW — A2 mühendislik incelemesi</title><style>'+style+'</style></head><body><header><p>ESC V2 / 13 Eylül 2026 / A2</p><h1>3 kW ESC — mühendislik inceleme paketi</h1><p>13S batarya • 46.8 V nominal • 54.6 V tam dolu • Hall destekli motor kontrolü</p><nav><a href="#changes">Değişiklikler</a><a href="#schematics">Şemalar</a><a href="#release">Açık işler</a><a href="#bom">Ön BOM</a><a href="README.md">Tasarım dosyası</a></nav><div class="metrics">'
for value,label in [(report['pages'],'şema sayfası'),(report['electrical_components'],'bileşen'),(report['checks_passed'],'başarılı kontrol'),(report['erc_violations'],'ERC ihlali')]:s+='<div><strong>'+str(value)+'</strong><span>'+label+'</span></div>'
s+='</div><p class="status">İnceleme revizyonu. PCB, tam üretim BOM’u, çalışan firmware ve 3 kW fiziksel doğrulama tamamlanmadı. ERC geçişi güç performansı veya güvenlik onayı değildir.</p></header><main><h2 id="changes">A2 ile değişenler</h2><ul><li>İşlevsel sayfalar, Türkçe hesap/yerleşim/test notları ve sayfa bazında bileşen numaralandırması.</li><li>Kablolu faz güç yolları ve dört ADC bölücüsü; on iki test noktası.</li><li>Kartlar arası eksik +5 V bağlantısının pin39 üzerinden tamamlanması.</li><li>Gerçek dört uçlu şönt seçimi, yapay Kelvin 0R parçalarının kaldırılması.</li><li>TI mekanik çiziminden yerel DRV8353F RTA0040B footprint’i.</li></ul>'
s+='<h2 id="schematics">Şema sayfaları</h2><p>Başlıklara tıklayın; çizimleri tam boyutta açabilirsiniz. Sayfa başlıkları KiCad hiyerarşisiyle aynıdır.</p>'
svgdir=root.parent/'verification/svg_a2'
files=list(svgdir.glob('*.svg'))
for key,pg in pages.items():
 expected='ESC_3kW_A2-'+pg['title'].replace('/','_')+'.svg'
 path=next((f for f in files if f.name==expected),None)
 if path is None:raise FileNotFoundError(expected)
 rel='../verification/svg_a2/'+path.name
 s+='<details><summary>'+e(key)+' — '+e(pg['title'])+'</summary><div class="content"><p><a href="'+e(rel,quote=True)+'" target="_blank">Tam boyut SVG</a> · <a href="'+key+'.kicad_sch">KiCad sayfası</a></p><img class="schematic" loading="lazy" src="'+e(rel,quote=True)+'" alt="'+e(pg['title'])+'"><ul>'
 for note in pg['notes']:s+='<li>'+e(note)+'</li>'
 s+='</ul></div></details>'
s+='<h2 id="release">Üretime geçiş işleri</h2><p>Kapandı bilgisi yalnız belirtilen kapsam için geçerlidir. Açık konular bitmiş gibi gösterilmez.</p>'
for item in issues:
 s+='<details><summary>'+e(item['id']+' · '+item['item'])+' <span class="badge">'+e(item['status'])+'</span></summary><div class="content"><p>Sorumlu rol: '+e(item['owner'])+' · Öncelik: '+e(item['priority'])+'</p><p>'+e(item.get('close_when',item.get('evidence','')))+'</p></div></details>'
s+='<h2 id="bom">Ön BOM / satın alma serbest bırakması değil</h2><p>'+str(report['incomplete_bom_components'])+' bileşende MPN veya footprint alanı açık. Aynı parçanın farklı referansları ayrı bileşen sayılır.</p><div class="scroll"><table><thead><tr><th>Adet</th><th>Değer</th><th>Üretici kodu</th><th>Referanslar</th><th>Footprint</th></tr></thead><tbody>'
for g in bom:s+='<tr>'+''.join('<td>'+e(str(x))+'</td>' for x in [g['quantity'],g['value'],g['mpn'] or 'Seçilecek',', '.join(g['references']),g['footprint'] or 'Seçilecek'])+'</tr>'
s+='</tbody></table></div><p><a href="sourcing_review.json">Tarihli stok kanıtları</a> · <a href="engineering_calculations.json">Hesaplar</a> · <a href="../verification/a2_checks.json">Bağlantı kontrolleri</a></p></main></body></html>'
(root/'inceleme.html').write_text(s,encoding='utf-8')
print('Review index complete; '+str(len(pages))+' SVG links resolved.')
