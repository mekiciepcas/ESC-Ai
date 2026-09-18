"""Check KiCad-exported connectivity against design intent and export review BOM."""
import json, html
from pathlib import Path
from collections import defaultdict
from sexpr import parse, child, children
base=Path(__file__).resolve().parent
parts=json.loads((base/'connection_manifest.json').read_text(encoding='utf-8'))
tree=parse((base.parent/'verification/ESC_3kW_A1.net').read_text(encoding='utf-8'))
nets={};pin_net={}
for net in children(child(tree,'nets'),'net'):
    name=child(net,'name')[1]
    ns={(child(n,'ref')[1],child(n,'pin')[1]) for n in children(net,'node')}
    nets[name]=ns
    for pair in ns:pin_net[pair]=name
checks=[]
def check(name,condition):
    checks.append({'check':name,'passed':bool(condition)})
    if not condition:raise AssertionError(name)
for p in parts:
    if p['kind']=='FLAG':continue
    for pin,net in p['nets'].items():
        if net is not None:check(p['ref']+'.'+pin+'='+net,pin_net.get((p['ref'],pin))==net)
bykind=defaultdict(list)
for p in parts:bykind[p['kind']].append(p)
drv=bykind['DRV'][0]['ref'];mcu=bykind['MCU'][0]['ref'];latch=bykind['LATCH'][0]['ref']
check('Exactly 12 power MOSFETs',len(bykind['NMOS'])==12)
check('Driver VM12V separate from drain bus',pin_net[drv,'3']=='+12V' and pin_net[drv,'4']=='VBUS')
check('Driver CSA VREF is 3V3 analog, not 1V65',pin_net[drv,'24']=='+3V3A')
check('MCU hardware break input PB12 wired to fault',pin_net[mcu,'34']=='HARD_FAULT_N')
check('Asynchronous latch clear wired to fault',pin_net[latch,'6']=='HARD_FAULT_N')
check('Six PWM inhibit gates',len(bykind['AND'])==6)
for a in bykind['AND']:
    check(a['ref']+' gate controlled by latch',a['nets']['1']=='LATCH_STATE' and a['nets']['2'].startswith('MCU_PWM_') and a['nets']['4'].startswith('PWM_'))
check('Hall channels on PC6 PC7 PC8',all(pin_net[mcu,pin]=='HALL_'+ph for pin,ph in [('38','A'),('39','B'),('40','C')]))
check('RC capture on separate TIM2 PA15',pin_net[mcu,'51']=='RC_PWM')
check('No merged main rails',len({pin_net[drv,'3'],pin_net[drv,'4'],pin_net[drv,'24'],pin_net[drv,'39']})==4)
erc=json.loads((base.parent/'verification/erc.json').read_text(encoding='utf-8'))
violations=[v for s in erc.get('sheets',[]) for v in s.get('violations',[])]
check('KiCad ERC zero violations',len(violations)==0)
project=json.loads((base/'ESC_3kW_A1.kicad_pro').read_text(encoding='utf-8'))
check('No project-specific ERC exclusions',not project.get('erc',{}).get('erc_exclusions'))

groups={}
for p in parts:
    if p['kind']=='FLAG':continue
    key=(p['value'],p['mpn'],p['footprint'])
    if key not in groups:groups[key]={'value':p['value'],'mpn':p['mpn'],'footprint':p['footprint'],'references':[],'notes':set()}
    groups[key]['references'].append(p['ref'])
    if p['note']:groups[key]['notes'].add(p['note'])
bom=[]
for g in groups.values():
    g['quantity']=len(g['references']);g['notes']=sorted(g['notes']);g['release_status']='REVIEW_REQUIRED' if not g['mpn'] or not g['footprint'] else 'PART_SELECTED_NOT_QUALIFIED'
    bom.append(g)
(base/'bom_review.json').write_text(json.dumps(bom,ensure_ascii=False,indent=2),encoding='utf-8')
report={'status':'CONNECTIVITY_CHECKS_PASS_NOT_HARDWARE_VALIDATION','kicad':erc['kicad_version'],'symbols':len(parts),'electrical_components':len(parts)-len(bykind['FLAG']),'nets':len(nets),'checks_passed':len(checks),'erc_violations':len(violations),'default_disabled_erc_checks':erc.get('ignored_checks',[]),'checks':checks}
(base.parent/'verification/connectivity_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')

pages=[]
for page in dict.fromkeys(p['page'] for p in parts):
    pages.append((page,base.parent/'verification/svg'/('ESC_3kW_A1-'+page+'.svg')))
style='''body{font:15px system-ui,sans-serif;background:#f7f8fa;color:#172733;margin:0}header,main{max-width:1180px;margin:auto;padding:24px}h1{font-size:26px}h2{font-size:20px}p{line-height:1.6}.note{border-left:4px solid #b56812;padding:8px 18px;background:#fff6e8}details{background:white;margin:12px 0;border:1px solid #dae1e7}summary{padding:16px;cursor:pointer;font-weight:600}img{width:100%;height:auto}table{border-collapse:collapse;width:100%;background:white}td,th{text-align:left;vertical-align:top;padding:10px;border-bottom:1px solid #dde2e7;font-size:13px}a{color:#155a91}.scroll{overflow:auto}nav{display:flex;gap:20px}code{font-size:13px}'''
s='<!doctype html><html lang="tr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ESC 3 kW — A1 şema incelemesi</title><style>'+style+'</style><header><h1>ESC 3 kW — A1 şema incelemesi</h1><p>13 Eylül 2026 • KiCad 10 • '+str(len(pages)+1)+' sayfa • '+str(report['electrical_components'])+' bileşen • '+str(len(nets))+' net</p><nav><a href="#schematics">Şemalar</a><a href="#bom">Ön BOM</a><a href="#open">Açık işler</a></nav><p class="note">İnceleme taslağıdır. ERC: 0 ihlal. Üretim, PCB ve fiziksel güç testi tamamlanmadı. Boş MPN/footprint alanları seçilmemiş parçaları belirtir.</p></header><main>'
s+='<h2 id="schematics">Bağlantılı şema sayfaları</h2><p>Sayfa başlığına tıklayarak büyütün. Aynı isimli global netler sayfalar arasında elektriksel olarak bağlıdır. Semboller pin numaralarını taşıyan işlevsel gösterimlerdir.</p>'
for name,path in pages:
    rel='../verification/svg/'+path.name
    s+='<details><summary>'+html.escape(name.replace('_',' '))+'</summary><a href="'+rel+'" target="_blank">Tam boyutta aç</a><img loading="lazy" alt="'+html.escape(name)+' şeması" src="'+rel+'"></details>'
s+='<h2 id="bom">Ön malzeme listesi</h2><p>Sipariş listesi değildir; pasiflerin tam kodları, bazı kılıflar ve yüksek akım bağlantıları henüz açık.</p><div class="scroll"><table><thead><tr><th>Adet</th><th>Değer</th><th>MPN</th><th>Referanslar</th><th>Durum</th></tr></thead><tbody>'
for g in bom:s+='<tr>'+''.join('<td>'+html.escape(str(v))+'</td>' for v in [g['quantity'],g['value'],g['mpn'] or 'Seçilecek',', '.join(g['references']),'İncelenecek' if g['release_status']=='REVIEW_REQUIRED' else 'Kod seçildi / doğrulanacak'])+'</tr>'
s+='</tbody></table></div><h2 id="open">Üretim öncesi açık işler</h2><ol><li>Şönt, MOSFET sürücü ve güç bağlantısı kılıflarını kesinleştirme; eksiksiz üretici kodları.</li><li>Giriş sigortası, ön şarj, ters kutup ve fren enerjisi için dış modülün tasarımı.</li><li>MCU pin-mux / ADC zamanlaması ve donanım koruma gecikmesi hesabı.</li><li>Kapı sürme, termal, EMI/ESD, batarya ve motor numune testleri.</li><li>İki fiziksel PCB için net ayrımı, yerleşim, DRC ve üretim dosyaları.</li></ol><p><a href="README.md">Tasarım notları ve dosya listesi</a></p></main></html>'
(base/'inceleme.html').write_text(s,encoding='utf-8')
print(f'{len(checks)} connectivity checks PASS; ERC={len(violations)}; {len(bom)} BOM groups.')
