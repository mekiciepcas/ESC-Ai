"""B1 engineering review schematics. Builds from A1 circuit source without running its exporter.
Electrical definition, presentation and validation are separate. No manufacturing release.
"""
from pathlib import Path
import sys, json, math, uuid, collections, textwrap, re
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'hardware'))
from sexpr import load_symbol, pins
source=(HERE.parent/'hardware/build_schematic.py').read_text(encoding='utf-8')
scope={'__file__':str(HERE.parent/'hardware/build_schematic.py')}
exec(compile(source.split('# Output structure:')[0],'<A1 electrical baseline>','exec'),scope)
parts=scope['parts']; definitions=scope['definitions']
PROJECT='ESC_3kW_B1'; LIB='ESC_B1'
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,PROJECT+'/'+str(s)))
def q(s):return json.dumps(str(s),ensure_ascii=False)
def ef(size=1.0,extra=''):return f'(effects (font (size {size} {size})) {extra})'
def snap(n):return round(round(n/1.27)*1.27,2)
def text(s,x,y,size=1.1):return f'(text {q(s)} (at {x} {y} 0) {ef(size,"(justify left top)")} (uuid {q(uid(s+str(x)+str(y)))}))'
def line(points,width=.254):return '(polyline (pts '+''.join(f'(xy {x} {y})' for x,y in points)+f') (stroke (width {width}) (type default)) (fill (type none)))'

# Close pin-interface and package omissions without pretending procurement is qualified.
for p in parts:
    p['baseline_ref']=p['ref']
    if p['kind']=='R' and p['nets'].get('2')=='BUCK_RON':
        p['nets']['1']='GND'
        p['note']+=' DR-002 ELEC-01: LM5164 Rev D Table 4-1 requires RON resistor to GND; corrected from VBUS. Frequency/ripple qualification remains open.'
    if p['mpn']=='BAT54H':
        p.update(mpn='BAT54H,115',footprint='Diode_SMD:D_SOD-123F')
    if p['kind']=='SHUNT':
        p.update(mpn='CSS4J-4026R-L500F',value='0.5mR 1% Kelvin',note='Bourns CSS4J-4026: 5 W at 130 C terminals. Four-terminal geometry must match local footprint before release.')
    if p['kind']=='CONN40':p['nets']['38']='TEMP_MOTOR';p['nets']['39']='+5V';p['note']+=' B1 pin38 TEMP_MOTOR; pin39 +5V; both connector ends use the same numbering. Not compatible with A2 pin38 GND.'
    if p['kind']=='DRV':p.update(footprint='ESC_B1:TI_RTA0040B_6x6_P0.5_EP4.15',note='TI DRV8353F Rev B. VM=12V, VDRAIN=DC link. SPI variant; configure 6-PWM and CSA gain10. Local RTA0040B land pattern from TI drawing; assembler review pending.')
    if p['kind']=='R' and 'NTC' not in p['value'] and 'NET-TIE' not in p['value']:
        match=re.match(r'([\d.]+)([RkM])',p['value'])
        if match:
            number,unit=match.groups();unit=unit.upper();code=number.replace('.',unit) if '.' in number else number+unit
            size='1206' if '0.25W' in p['value'] else '0805'
            p['mpn']=('RT'+size+'BRD07' if '0.1%' in p['value'] else 'RC'+size+('JR-07' if number=='0' else 'FR-07'))+code+'L'
            p['footprint']='Resistor_SMD:R_'+size+('_3216Metric' if size=='1206' else '_2012Metric')
            p['selection_evidence']='YAGEO family ordering code; individual orderability and stock not yet verified'
            p['note']+=' YAGEO series-code selection; verify individual MPN orderability before procurement.'
    if p['kind']=='R' and 'NTC' in p['value']:
        p.update(mpn='NTCG203NH103JT1',footprint='Resistor_SMD:R_0805_2012Metric',value='NTC 10k B25/85=3650K',note='TDK production part. 10k +/-5%; B25/85=3650K +/-3%; use manufacturer R-T table, not old B3435 model.')
    if p['kind']=='C' and p['value'].startswith('100n') and '160V' not in p['value']:
        p.update(mpn='C2012X7R2A104K125AA',footprint='Capacitor_SMD:C_0805_2012Metric')
        p['note']+=' TDK 100nF 100V X7R +/-10%, production family; local DC-bias/assembly review applies.'

# Remove misleading external net-tie components: Kelvin terminals are internally common,
# and KiCad correctly represents the four pads as distinct routed nets at the shunt.
parts[:]=[p for p in parts if 'NET-TIE ONLY' not in p['value']]

# Add useful measurement access; only 1-pin passive test points, never oscilloscope earth assumptions.
definitions['TP']=[{'number':'1','name':'TP','type':'passive'}]
for i,net in enumerate(['VBUS','GND','+12V','+5V','+3V3','+3V3A','HARD_FAULT_N','LATCH_STATE','DRV_FAULT_N','I_A_RAW','I_B_RAW','I_C_RAW'],1):
    parts.append(dict(ref=f'TP{i}',baseline_ref='',page='13_test_points',kind='TP',value=net,nets={'1':net},mpn='PCB TEST PAD',footprint='TestPoint:TestPoint_Pad_D1.5mm',note='VBUS and switching-node measurements require appropriately rated differential probes.'))

# Repartition by engineering function, not arbitrary component counts.
pages=collections.OrderedDict()
def page(key,title,rows,notes,mode='grid'):
    pages[key]=dict(title=title,parts=rows,notes=notes,mode=mode)
    for p in rows:p['page']=key
original=collections.defaultdict(list)
for p in parts:original[p['page']].append(p)
page('01_DC_LINK','DC bara / enerji deposu',original['01_DC_link'],[
 'HEDEF: 39–54.6 V çalışma; 3 kW mil gücü. 44 V altında güç azaltılır.',
 'Giriş, sigorta + ön şarj + kutup doğrulama düzeneğinden gelir. Doğrudan batarya bağlantısı için yayımlanmadı.',
 '3 x 470 uF = 1410 uF. 54.6 V üzerinde depolanan enerji yaklaşık 2.10 J.',
 '100 kohm boşaltma: tau=141 s; 54.6 V → 5 V yaklaşık 337 s. Gerilim ölçülmeden servis yapılmaz.',
 'Her yarım köprüye 2.2 uF yerel seramik; DC bias ve RMS ripple kontrol edilecek.',
 'AÇIK R01: giriş modülü. AÇIK R02: geri sürülme / fren enerjisi. PWM kapatmak DC barayı kelepçelemez.'
], 'dc')
for ph in 'ABC':page('02_PHASE_'+ph,'Faz '+ph+' / paralel MOSFET yarım köprüsü',original['02_phase_'+ph],[
 '100 V CSD19536KTT; her anahtarda iki paralel MOSFET. Üç faz toplam 12 MOSFET.',
 'Kalın hatlar güç yolunu gösterir. Her MOSFET kendi 4.7 ohm kapı direncine sahiptir.',
 '4.7 ohm başlangıç değeridir. VGS, VDS taşması ve açma/kapama kaybıyla ayarlanır.',
 'Kelvin sense uçları sadece sürücü ölçüm girişlerine gider. Güç akımı sense izi üzerinden geçirilmez.',
 '0.5 mohm: 80 A sürekli varsayımında I²R=3.2 W üst sınır hesabı. Gerçek şönt RMS akımı PWM ile değişir.',
 'PCB: paralel kollar simetrik; ortak kaynak endüktansı azaltılır. Tab pin2=Drain. Soğutucu izolasyonu ayrıca tasarlanır.',
 'AÇIK R03: şönt pad yönü/termal. AÇIK R04: double-pulse ve kısa devre koruma süresi.'
], 'phase')
g=original['03_gate_driver']
page('03_DRIVER','Üç faz kapı sürücü / SPI / besleme',g[:8],[
 'TI DRV8353FSRTAR; F-SPI varyantı. H donanım varyantı aynı firmware ile kullanılmaz.',
 'VM=12 V yardımcı besleme. VDRAIN=VBUS. VREF=3V3A; CSA sıfırı nominal VREF/2.',
 'CPH–CPL: 47 nF. VCP kondansatörü toprağa değil VBUS hattına döner.',
 'GHA/GLA, GHB/GLB, GHC/GLC faz sayfalarına; SPA/SNA uçları Kelvin sense hatlarına.',
 'SPI: önce kimlik/durum ve yapılandırma geri okuması. 6-PWM, gain10, OCP ve deglitch değerleri kayıt altına alınır.',
 'Yerel RTA0040B footprint: 6x6 mm, 0.5 mm pitch, EP=4.15 mm. TI çiziminden oluşturuldu; stencil/via süreci montajcıyla doğrulanacak.'
])
page('04_DRIVER_DEFAULTS','Sürücü / reset anı lojik seviyeleri',g[8:],[
 'ENABLE ve altı PWM girişi donanım pull-down ile varsayılan kapalıdır.',
 'nFAULT ve SDO open-drain/open-collector çıkışları 3.3 V seviyesine çekilir.',
 'CS yüksek: SPI pasif. Boşta kalan MCU pinine güvenilmez.',
 'RUN_REQUEST sürücüyü uyandırır. Anahtarlama izni ayrı LATCH_STATE sinyalidir.'
])
volts=original['04_voltage_sensing']
for i,name in enumerate(['BUS','A','B','C']):page('05_SENSE_'+name,'Gerilim ölçümü / '+('DC bara' if name=='BUS' else 'faz '+name),volts[i*8:(i+1)*8],[
 'Rüst=2 x 49.9 kohm; Ralt=3.32 kohm; oran=0.032196.',
 '54.6 V → 1.758 V. 80 V kontrol noktası → 2.576 V. ADC referansı 3.3 V.',
 '1 kohm + 1 nF ADC filtresi. Kaynak empedansı yaklaşık 4.21 kohm; fc yaklaşık 37.8 kHz.',
 'BAT54H: pin1 katot, pin2 anot. Kelepçe kaçağı ve 3V3A geri beslemesi hata bütçesine dahildir.',
 'ADC acquisition süresi ve PWM ile örnekleme anı firmware sözleşmesinde belirlenir.',
 'Bu bölücü 80 V sürekli sistem izni vermez; güç katının geçici rejim marjı ayrıca doğrulanır.'
], 'divider')
s=original['05_current_and_temperature']
page('06_CURRENT','Faz akımı / ADC filtreleri',s[:6],[
 'SOA/SOB/SOC → 100 ohm / 1 nF → ADC. Filtre köşe frekansı yaklaşık 1.59 MHz.',
 '0.5 mohm ve CSA gain10: nominal 5 mV/A. Sıfır nominal 1.65 V.',
 'Yazılım ilk aşama limiti düşük akımdan yükseltilir; hedef anlık faz limiti 120 A.',
 'ADC: üç şönt düşük taraf ölçümü. Geçerli pencere, minimum darbe ve yeniden kurma algoritması gerektirir.',
 'Üç ADC kanalının eş zamanlı ölçüldüğü varsayılmaz. ADC1/ADC2 planı ayrıca derlenerek doğrulanacak.'
])
page('07_TEMPERATURE','Sıcaklık / motor sensörü',s[6:],[
 'FET/PCB: TDK NTCG203NH103JT1, 10k %5; B25/85=3650K %3. Eski B3435 varsayımı kaldırıldı; üretici R-T tablosu kullanılır.',
 'FET sensörü sıcak noktaya yakın fakat elektriksel izolasyon korunarak yerleştirilir.',
 'Motor girişi direnç tipi sensör varsayar. Hall kablosu ile karıştırılmaz.',
 'Açık ve kısa sensör arızası algılanır. Motorun gerçek termistör tipi henüz ölçülmedi.'
])
page('08_AUX_12V','DC bara → 12 V yardımcı güç',original['06_aux_12V'],[
 'LM5164DDAT: 100 V giriş sınıfı; A1 DDAR paketleme alternatifi yerine DDAT seçildi.',
 '68 uH ve Type-3 ripple ağı TI referans topolojisini izler. FB=453k/49.9k; hedef yaklaşık 12.09 V.',
 'RON=100k. 453k / 3.3n / 56p ripple ağı sıradan RC filtre ile değiştirilmez.',
 'Fan için 0.2 A başlangıç bütçesi. Kontrol beslemeleri dahil worst-case yük/doyma doğrulanacak.',
 'EN bölücüsü yardımcı kaynağı başlatır; motor düşük gerilim korumasının yerine geçmez.',
 'VIN kapasitörü–IC GND sıcak döngüsü kısa. SW bakırı analog ölçüm altında bulunmaz.'
])
aux=original['07_aux_5V_3V3']
page('09_AUX_LOGIC','12 V → 5 V → 3.3 V / analog besleme',aux,[
 'TPS62160: 5 V Hall ve lojik ara besleme. FB=523k/100k; nominal 4.984 V.',
 'TLV75533: 5 V → 3.3 V. 200 mA yükte yaklaşık 0.34 W kayıp; SOT23 termal kontrol gerekli.',
 '3V3A, 3V3 üzerinden kontrollü tek noktadan beslenir; analog ve güç dönüş yolları yerleşimde ayrılır.',
 '5 V hattı B1 kart arayüzünde pin39 üzerinden kontrol kartına taşınır. A1 arayüz eksiği kapatıldı.'
])
mc=original['08_MCU']
page('10_MCU','STM32G474 / kontrol çekirdeği',[mc[0]],[
 'TIM1: PA8/9/10 high; PB13/14/15 complementary low. PB12 donanım break girişi.',
 'Hall: PC6/7/8 (TIM3). RC: PA15 (TIM2). Bir zamanlayıcının periyodu diğer girişle paylaşılmaz.',
 'SPI1: PB3/4/5. CAN: PA11/12. UART: PC10/11. SWD: PA13/14.',
 'PG10 pin7 NRST olarak kalır. Option-byte değiştirilmeden reset davranışı korunur.',
 'PB8 BOOT0 pull-down. HSE bypass 8 MHz başlangıç seçimi. Saat ağacı CubeMX/derleme ile doğrulanacak.',
 'RET3 stok kaydı yalnız 4 adet gösterdi; seri üretim tedarik kapısı açık.'
], 'mcu')
page('11_MCU_SUPPORT','MCU / bypass / reset / programlama',mc[1:],[
 'Her VDD için 100 nF fiziksel olarak pine yakın; bulk ve analog referans ayrı yerleşir.',
 'SWD VTref ölçüm referansıdır. İki farklı kaynaktan 3.3 V basılmaz.',
 'NRST: 10k / 100n. Brown-out ve bağımsız watchdog firmware başlangıcında etkinleştirilir.',
 'RUN_REQUEST ve ARM_CLK reset boyunca düşük tutulur. İlk açılışta otomatik motor çalıştırma yok.'
])
com=original['09_comms']
page('12_CAN_UART','CAN / servis / RC arayüzleri',com[:7],[
 'SN65HVD230 ile Classic CAN. CAN-FD haberleşmesi bu transceiver seçimiyle yayımlanmıyor.',
 '120 ohm terminasyon DNP; yalnız hat sonunda takılır.',
 'UART ve RC seviyesi 3.3 V. 5 V push-pull girişi doğrudan uygulanmaz.',
 'AÇIK R05: konektör tarafı ESD/TVS ve kablo testleri; haberleşme kaybı tork sıfırlar.'
])
page('13_HALL','Motor / Hall sensör arayüzü',com[7:],[
 'Motor Hall beslemesi 5 V; çıkışlar open-collector kabul edildi.',
 'Pull-up 3.3 V üzerindedir. Push-pull 5 V Hall için seviye dönüştürücü gerekir.',
 '1k / 1n EMI filtresi ilk değerdir; maksimum elektriksel hızda kenar gecikmesi ölçülür.',
 'Hall 000/111 ve geçersiz sıra: hata. Gerçek faz/Hall sırası düşük enerjili ölçümle bulunur.'
])
trip=original['10_hardware_trip']
page('14_TRIP_COMPARATORS','Donanım / akım penceresi ve bara aşırı gerilim',trip[:4],[
 '6 karşılaştırıcı: üç faz için alt/üst akım penceresi. Ortak çıkış HARD_FAULT_N.',
 'OC_LOW≈0.914 V; OC_HIGH≈2.386 V. 5mV/A için yaklaşık ±147 A nominal eşik.',
 'Yedinci karşılaştırıcı VBUS aşırı gerilimi algılar: yaklaşık 58.57 V nominal.',
 'TLV1704 ve CSA gecikmesi kısa devreyi tek başına garanti etmez. DRV VDS koruması birlikte ayarlanır.',
 'Kullanılmayan komparatör girişleri tanımlı; çıkışı NC. Eşik toleransları hesap dosyasında.'
])
page('15_TRIP_REFERENCES','Donanım / rasyometrik eşik referansları',trip[4:13],[
 'Akım referansları 26.1k / 10k ve ters bölücüdür. VREF ile aynı 3V3A kaynağını kullanır.',
 'Bara OV referansı 7.5k / 10k. Dirençler %0.1 başlangıç şartı.',
 '10 nF referans filtreleri açılışta yerleşme süresi oluşturur; ölçüm stabil olmadan ARM gönderilmez.',
 'Komparatör offset, CSA gain/offset ve şönt toleransı nihai eşiğe eklenir.'
])
page('16_FAULT_LATCH','Donanım / arıza hafızası ve yeniden kurma',trip[13:],[
 'nFAULT, reset ve güç-good hatları diyot OR ile HARD_FAULT_N hattını aşağı çeker.',
 'HARD_FAULT_N hem TIM1 BKIN hem asenkron CLR girişine gider.',
 'Arıza LATCH_STATE değerini sıfırlar. Arıza kalkınca kendiliğinden yeniden başlamaz.',
 'Başlatma: PWM düşük → RUN_REQUEST → SPI/CSA kontrol → fault sağlıklı → ARM yükselen kenar.',
 'DRV_ENABLE, latch ile kesilmez: CSA sıfır çıkışından kaynaklanan açılış kilidi önlenir.',
 'Acil durdurma kontağı kısa devre ederek keser; kablo kopması algılanmaz. Sertifikalı güvenlik fonksiyonu değildir.'
])
page('17_PWM_INHIBIT','Altı PWM / donanımsal izin kapıları',original['11_PWM_interlock'],[
 'Her AND kapısının A girişi LATCH_STATE; B girişi MCU PWM; çıkış DRV PWM.',
 'İzin düşükken altı sürücü girişi düşük. DRV 6-PWM modu zorunludur.',
 'Dead-time TIM1 ve sürücü yapılandırmasında hesaplanır; başlangıç değeri ölçülmeden kesinleşmez.',
 'Arıza → kapı kesme toplam gecikmesi osiloskopla ölçülür; yazılım kesmesi beklenmez.'
])
page('18_BOARD_INTERFACE','Güç / kontrol kartı arayüzü',original['12_board_interface'],[
 'İki konnektör eşleşmiş kablonun sistem modelidir; aynı net isimleri elektriksel olarak ortaktır.',
 'B1 düzeltme: pin38 TEMP_MOTOR (A2 GND ile uyumsuz); pin39 +5V; pin40 GND. Pin1 ve bakış yönü fiziksel montaj çiziminde sabitlenecek.',
 'Güç kartı: köprü, driver, şönt, fault latch, AND kapıları. Kontrol kartı: MCU ve iletişim.',
 'Yerleşim öncesi iki PCB için netlist ayrılır. Bu birleşik sistem dosyası doğrudan iki PCB üretmez.'
])
page('19_TEST_POINTS','Devreye alma / test erişimi',original['13_test_points'],[
 'Önce yardımcı kaynaklar, ardından fault zinciri, sonra düşük gerilim motor deneyi.',
 'TP VBUS ölçümünde prob gerilim sınıfı ve referansı kontrol edilir.',
 'İlk motor deneyi batarya yerine akım sınırlı kaynakla; akım limiti kademeli artırılır.',
 'Ölçüm kaydı: kart revizyonu, firmware hash, motor seri no, batarya/PSU, sıcaklık, dalga şekilleri.'
])

# Stable engineering numbering: sheet * 100 + local count. Original refs remain traceable.
for sheetno,(key,p) in enumerate(pages.items(),1):
    counts=collections.defaultdict(int)
    for part in p['parts']:
        prefix=''.join(c for c in part['ref'] if not c.isdigit())
        counts[prefix]+=1;part['ref']=prefix+str(sheetno*100+counts[prefix])

def sym(kind):
    ps=definitions[kind];n=len(ps);simple=kind in ['R','C','L','DIODE']
    positions=[]
    if simple:
        positions=[(ps[0],-7.62,0,0),(ps[1],7.62,0,180)];h=2.54;w=5.08
    elif kind=='NMOS':
        positions=[(ps[0],-10.16,0,0),(ps[1],0,10.16,270),(ps[2],0,-10.16,90)];h=7.62;w=7.62
    elif kind=='TP':positions=[(ps[0],-5.08,0,0)];h=2.54;w=2.54
    else:
        half=math.ceil(n/2);w=25.4 if n>30 else 15.24 if n>8 else 10.16;h=max(5.08,half*1.27+2.54)
        for i,p in enumerate(ps):
            left=i<half;j=i if left else i-half
            positions.append((p,(-w-2.54 if left else w+2.54),(half-1)*1.27-j*2.54,0 if left else 180))
    if kind=='C':shape=line([(-5.08,0),(-1.27,0)])+line([(-1.27,-2.54),(-1.27,2.54)])+line([(1.27,-2.54),(1.27,2.54)])+line([(1.27,0),(5.08,0)])
    elif kind=='DIODE':shape=line([(-5.08,0),(-1.27,0)])+line([(-1.27,-2.54),(-1.27,2.54)])+line([(-1.27,0),(2.54,2.54),(2.54,-2.54),(-1.27,0)])+line([(2.54,0),(5.08,0)])
    elif kind=='L':
        # Four winding arcs distinguish an inductor from a zigzag resistor.
        # Keep the original passive pin coordinates and electrical identity.
        shape=''.join(f'(arc (start {x} 0) (mid {x+1.27} 1.27) (end {x+2.54} 0) (stroke (width .254) (type default)) (fill (type none)))' for x in [-5.08,-2.54,0,2.54])
    elif kind=='NMOS':
        shape=line([(-7.62,0),(-5.08,0)])+line([(-5.08,-4),(-5.08,4)])+line([(-2.54,-4),(-2.54,4)])+line([(-2.54,4),(0,4),(0,7.62)])+line([(-2.54,-4),(0,-4),(0,-7.62)])+line([(-2.54,0),(0,0),(0,-4)])+line([(-1.8,1),(-2.54,0),(-1.8,-1)])
        # Intrinsic N-channel body diode: anode at source (pin 3, -Y),
        # cathode at drain (pin 2, +Y). This is graphics, not an extra device.
        shape+=line([(0,-4),(4,-4),(4,-1.27)])+line([(2.73,-1.27),(5.27,-1.27),(4,1.27),(2.73,-1.27)])+line([(2.73,1.27),(5.27,1.27)])+line([(4,1.27),(4,4),(0,4)])
    elif kind=='TP':shape='(circle (center 0 0) (radius 2.54) (stroke (width 0.254) (type default)) (fill (type none)))'
    else:shape=f'(rectangle (start {-w} {h}) (end {w} {-h}) (stroke (width .254) (type default)) (fill (type background)))'
    out=f'(symbol {q(LIB+":"+kind)} (pin_names (offset .8) {"(hide yes)" if simple else ""}) (in_bom yes) (on_board yes) (property "Reference" "U" (at 0 0 0) {ef()}) (property "Value" {q(kind)} (at 0 0 0) {ef()}) (symbol {q(kind+"_0_1")} {shape}) (symbol {q(kind+"_1_1")}'
    for p,x,y,a in positions:out+=f'(pin {p["type"]} line (at {x} {y} {a}) (length 2.54) (name {q(p["name"])} {ef(.8)}) (number {q(p["number"])} {ef(.75)}))'
    return out+'))',positions,h

def base(name,title):return f'(kicad_sch (version 20250114) (generator "eeschema") (uuid {q(uid(name))}) (paper "A3") (title_block (title {q(title)}) (date "2026-09-14") (rev "B1 REVIEW") (company "ESC V2 | AR-GE") (comment 1 "TASARIM INCELEMESI / URETIM SERBEST BIRAKMA DEGIL") (comment 2 "39-54.6V | 3kW mil hedefi | 20kHz | 13S Li-ion"))'

def layout(page):
    rows=page['parts'];mode=page['mode']
    if mode=='mcu':rows[0].update(x=139.7,y=101.6,rot=0);return
    if mode=='divider':
        positions=[(63.5,81.28,0),(101.6,81.28,0),(132.08,111.76,270),(170.18,81.28,0),(208.28,111.76,270),(238.76,55.88,270),(238.76,132.08,270)]
        # actual group is 7 components (3R+seriesR+C+2diodes); see partition below.
        for p,pos in zip(rows,positions):p.update(x=pos[0],y=pos[1],rot=pos[2])
        return
    if mode=='phase':
        fets=[p for p in rows if p['kind']=='NMOS']
        for i,p in enumerate(fets):p.update(x=[101.6,203.2][i%2],y=[81.28,157.48][i//2],rot=0)
        rs=[p for p in rows if p['kind']=='R']
        for i,p in enumerate(rs):
            f=fets[i//2]
            p.update(x=f['x']-(12.7 if i%2 else 30.48),y=f['y']+(22.86 if i%2 else 0),rot=270 if i%2 else 0)
        for p in rows:
            if p['kind']=='SHUNT':p.update(x=152.4,y=218.44,rot=0)
            if p['kind']=='C':p.update(x=254,y=101.6,rot=270)
        return
    cols=[42.,42.]
    for p in rows:
        _,_,h=sym(p['kind']);col=min(range(2),key=lambda c:cols[c]);y=snap(cols[col]+h+10)
        p.update(x=[78.74,215.9][col],y=y,rot=0);cols[col]=y+h+17
        if cols[col]>257:raise ValueError('Page overflow: '+p['page']+' '+p['ref'])

# Correct voltage groups from baseline: seven components per channel.
for i,name in enumerate(['BUS','A','B','C']):
    rows=volts[i*7:(i+1)*7];pages['05_SENSE_'+name]['parts']=rows
    for p in rows:p['page']='05_SENSE_'+name
# Re-number after final partition.
expanded=collections.OrderedDict()
for key,pg in pages.items():
    limit=100 if pg['mode'] in ['phase','divider','mcu'] else 9 if key=='17_PWM_INHIBIT' else 12
    for offset in range(0,len(pg['parts']),limit):
        suffix='' if offset==0 else '_'+str(offset//limit+1)
        clone={**pg,'parts':pg['parts'][offset:offset+limit]}
        if suffix:clone['title']+=' / devam '+str(offset//limit+1)
        expanded[key+suffix]=clone
        for p in clone['parts']:p['page']=key+suffix
pages=expanded
for sheetno,(key,p) in enumerate(pages.items(),1):
    counts=collections.defaultdict(int)
    for part in p['parts']:
        prefix=''.join(c for c in (part['baseline_ref'] or part['ref']) if not c.isdigit());counts[prefix]+=1;part['ref']=prefix+str(sheetno*100+counts[prefix])

# PoC BOM selections applied after stable sheet reference assignment.
for part in parts:
    if part['ref'] in ('J1901','J2001','J2002','J2003','J2101'):
        count=len(part['nets']); mpn=f'61300{count}11121'
        part.update(mpn=mpn,footprint=f'ESC_B1:WE_{mpn}_1x{count:02d}_P2.54_Drill1.10')
        part['note']+=' BOM-20260916: Wurth WR-PHD PoC header; 2.54mm pitch, 1.10mm nominal finished holes, pin1 square. Unkeyed bench connection, not final locking harness. Verify cable orientation before use.'
    if part['ref'] in ('C701','C801','C901','C1001','C1101','C1102','C1103'):
        part.update(mpn='C0805C102J5GACTU',footprint='Capacitor_SMD:C_0805_2012Metric')
        part['note']+=' BOM-BATCH2: KEMET 1nF +/-5%, 50V C0G 0805; ADC-side filter, not raw bus/phase. Nominal filter capacitance unchanged; ADC settling validation remains open.'
    if part['ref'] in ('C1201','C1202','C1203','C2301','C2302','C2303'):
        part.update(mpn='C0805C103J5GACTU',footprint='Capacitor_SMD:C_0805_2012Metric')
        part['note']+=' BOM-BATCH2: KEMET 10nF +/-5%, 50V C0G 0805; low-voltage temperature/reference node. Nominal capacitance unchanged; reference startup and protection response remain validation items.'
    if part['ref']=='C1805':
        part.update(mpn='C0805C475K8RACTU',footprint='Capacitor_SMD:C_0805_2012Metric')
        part['note']+=' BOM-BATCH2: KEMET 4.7uF +/-10%, 10V X7R 0805 on 3.3V rail. Bulk bypass only; effective capacitance under DC bias and transient response require bench validation.'
    if part['ref'] in ('C2101','C2102','C2103'):
        part.update(mpn='C0805C102J5GACTU',footprint='Capacitor_SMD:C_0805_2012Metric')
        part['note']+=' BOM-20260915: KEMET 1nF +/-5%, 50V C0G, 0805; non-polar Hall input filter. Manufacturer specification and DigiKey active/stock listing checked. Hall signal timing remains a physical PoC validation.'
    if part['ref']=='C1807':
        part.update(mpn='GRM21BR71C105KA01K',footprint='Capacitor_SMD:C_0805_2012Metric')
        part['note']+=' BOM-20260915: Murata 1uF +/-10%, 16V X7R, 0805; VDDA 3.3V nominal. Manufacturer in-production family, DigiKey active/stock listing checked. DC-bias and assembled supply validation remain PoC tests.'

rootuuid=uid(PROJECT)
for key,pageinfo in pages.items():
    layout(pageinfo);rows=pageinfo['parts'];title=pageinfo['title']
    s=base(key,title)+'(lib_symbols '+''.join(sym(k)[0] for k in sorted({p['kind'] for p in rows}))+')'
    s+=text(title,15,14,2.3)+text('ESC-3K | '+key+' | B1 | TASARIM INCELEMESI',15,23,1.2)
    s+=text('TASARIM NOTLARI / KABUL KRITERLERI',300,37,1.25)
    ny=48
    for j,note in enumerate(pageinfo['notes'],1):
        wrapped=textwrap.fill(str(j)+'. '+note,width=62)
        s+=text(wrapped,300,ny,1.4);ny+=len(wrapped.splitlines())*2.35+6
    s+=f'(polyline (pts (xy 292 35) (xy 292 256)) (stroke (width .254) (type default)) (uuid {q(uid(key+"divider"))}))'
    nodes={};handled=set();segments=[];labels=[]
    for p in rows:
        _,positions,h=sym(p['kind']);x=p['x'];y=p['y'];rot=p['rot'];rid=uid(p['ref'])
        if p['kind']=='C' and 'bulk' in p['value']:
            # Polarized bulk capacitor pin 1 is the positive terminal. Fail
            # closed if a future edit changes this placement or net mapping.
            assert rot==0 and p['nets']=={'1':'VBUS','2':'GND'}, p['ref']
            s+=text('+',x-4.2,y-4.0,1.5)
        s+=f'(symbol (lib_id {q(LIB+":"+p["kind"])}) (at {x} {y} {rot}) (unit 1) (in_bom {"no" if p["kind"]=="FLAG" else "yes"}) (on_board {"no" if p["kind"]=="FLAG" else "yes"}) (dnp {"yes" if "DNP" in p["value"] else "no"}) (uuid {q(rid)})'
        px=x+4 if rot else x;py=y-5 if rot else y-h-7
        for name,val,viz,dy in [('Reference',p['ref'],True,0),('Value',p['value'],True,3),('Footprint',p['footprint'],False,0),('MPN',p['mpn'],False,0),('Review',p['note'],False,0),('A1_Reference',p['baseline_ref'],False,0)]:
            s+=f'(property {q(name)} {q(val)} (at {px} {py+dy} 0) {ef(.95,"" if viz else "(hide yes)")})'
        for pin,*_ in positions:s+=f'(pin {q(pin["number"])} (uuid {q(uid(p["ref"]+"/"+pin["number"]))}))'
        s+=f'(instances (project {q(PROJECT)} (path {q("/"+rootuuid+"/"+uid("sheet/"+key))} (reference {q(p["ref"])}) (unit 1)))))'
        for pin,xx,yy,a in positions:
            rad=math.radians(rot);dx=xx*math.cos(rad)-yy*math.sin(rad);dy=xx*math.sin(rad)+yy*math.cos(rad)
            ax=round(x+dx,2);ay=round(y-dy,2);ang=(a+rot)%360
            nodes[(p['ref'],pin['number'])]=(ax,ay,p['nets'][pin['number']],ang)
    def point(p,pin):return nodes[(p['ref'],str(pin))][:2]
    def wire(a,b):
        if a!=b:segments.append((a,b))
    def route(p,pin,points):
        start=point(p,pin)
        for end in points:wire(start,end);start=end
        handled.add((p['ref'],str(pin)))
    if pageinfo['mode']=='divider':
        a,b,c,d,e,up,dn=rows
        route(a,2,[point(b,1)]);route(b,1,[])
        junction=(132.08,81.28)
        route(b,2,[junction,point(d,1)]);route(d,1,[]);route(c,1,[junction])
        labels.append((nodes[(b['ref'],'1')][2],point(b,1),0))
        labels.append((nodes[(b['ref'],'2')][2],junction,90))
        out=(208.28,81.28);route(d,2,[out,(238.76,81.28)])
        route(e,1,[out]);route(up,2,[(238.76,81.28)]);route(dn,1,[(238.76,81.28)])
        labels.append((nodes[(d['ref'],'2')][2],(238.76,81.28),0))
    if pageinfo['mode']=='phase':
        fs=[p for p in rows if p['kind']=='NMOS'];rs=[p for p in rows if p['kind']=='R'];sh=next(p for p in rows if p['kind']=='SHUNT')
        for idx,f in enumerate(fs):
            rr=rs[idx*2];route(rr,2,[point(f,1)]);route(f,1,[])
            pull=rs[idx*2+1]
            route(pull,1,[(pull['x'],f['y'])])
            route(pull,2,[(f['x'],point(pull,2)[1])])
            labels.append((nodes[(f['ref'],'1')][2],point(f,1),90))
        topy=50.8;midy=127.;lowy=198.12
        for f in fs[:2]:route(f,2,[(f['x'],topy)])
        wire((101.6,topy),(203.2,topy));labels.append(('VBUS',(101.6,topy),0))
        for f in fs[:2]:route(f,3,[(f['x'],midy)])
        for f in fs[2:]:route(f,2,[(f['x'],midy)])
        wire((101.6,midy),(203.2,midy));labels.append(('PH_'+key[-1],(203.2,midy),180))
        for f in fs[2:]:route(f,3,[(f['x'],lowy)])
        wire((101.6,lowy),(203.2,lowy));labels.append(('SHUNT_'+key[-1]+'_P',(203.2,lowy),180))
        route(sh,1,[(119.38,point(sh,1)[1]),(119.38,lowy)])
    for pair,(x,y,net,a) in nodes.items():
        if pair in handled:continue
        if net is None:s+=f'(no_connect (at {x} {y}) (uuid {q(uid(str(pair)+"NC"))}))';continue
        vx,vy={0:(-5.08,0),180:(5.08,0),90:(0,5.08),270:(0,-5.08)}[a]
        end=(round(x+vx,2),round(y+vy,2));wire((x,y),end);labels.append((net,end,a))
    for i,(a,b) in enumerate(segments):s+=f'(wire (pts (xy {a[0]} {a[1]}) (xy {b[0]} {b[1]})) (stroke (width {0.4 if pageinfo["mode"]=="phase" else 0}) (type default)) (uuid {q(uid(key+"wire"+str(i)))}))'
    # Explicit T junctions at wire endpoints prevent accidental crossing joins.
    endpoints=collections.Counter(pt for seg in segments for pt in seg)
    for pt,count in endpoints.items():
        onmid=any((a[0]==b[0]==pt[0] and min(a[1],b[1])<pt[1]<max(a[1],b[1])) or (a[1]==b[1]==pt[1] and min(a[0],b[0])<pt[0]<max(a[0],b[0])) for a,b in segments)
        if count>=3 or onmid:s+=f'(junction (at {pt[0]} {pt[1]}) (diameter 0) (color 0 0 0 0) (uuid {q(uid(key+"junction"+str(pt)))}))'
    for i,(net,(x,y),a) in enumerate(labels):
        s+=f'(global_label {q(net)} (shape bidirectional) (at {x} {y} {a}) {ef(.8,"(justify "+("right" if a in [0,90] else "left")+")")} (uuid {q(uid(key+"label"+str(i)))}))'
    (HERE/(key+'.kicad_sch')).write_text(s+')',encoding='utf-8')

s=base(PROJECT,'ESC 3 kW / Sistem mimarisi ve tasarım kapıları')+'(lib_symbols)'
s+=text('ESC 3 kW | B1 MÜHENDİSLİK İNCELEMESİ',15,15,2.8)
s+=text('13S / 46.8 V nominal / 54.6 V tam dolu | Golden Motor HPM3000B 48 V referans | 3 kW mil gücü hedefi',15,26,1.2)
s+=text('REVİZYON: işlevsel sayfa düzeni, güç/ölçüm yolları, sayfa bazlı notlar, test noktaları, pin39 +5V düzeltmesi.',15,34,1.1)
for i,(key,pg) in enumerate(pages.items()):
    x=18+(i%4)*98;y=51+(i//4)*22
    s+=f'(sheet (at {x} {y}) (size 90 12) (fields_autoplaced yes) (stroke (width .254) (type solid)) (fill (color 0 0 0 0)) (uuid {q(uid("sheet/"+key))}) (property "Sheetname" {q(pg["title"])} (at {x} {y-1} 0) {ef(.85,"(justify left)")}) (property "Sheetfile" {q(key+".kicad_sch")} (at {x} {y+13} 0) {ef(.7,"(justify left)")}) (instances (project {q(PROJECT)} (path {q("/"+rootuuid)} (page {q(str(i+2))})))) )'
s+=text('KAPILAR: G1 şema + parça/footprint | G2 PCB/DRC | G3 düşük enerji test | G4 1.5 kW termal | G5 3 kW yük testi',15,254,1.05)
s+=text('Durum: G1 sürüyor. ERC geçişi; EMC, güvenilirlik, kısa devre dayanımı veya 3 kW doğrulaması anlamına gelmez.',15,261,1.05)
s+='(sheet_instances (path "/" (page "1"))))'
(HERE/(PROJECT+'.kicad_sch')).write_text(s,encoding='utf-8')
# Preserve board setup, net classes and review exclusions across regeneration.
if not (HERE/(PROJECT+'.kicad_pro')).exists():
    (HERE/(PROJECT+'.kicad_pro')).write_text('{}\n',encoding='utf-8')
(HERE/'sym-lib-table').write_text('(sym_lib_table (lib (name "ESC_B1") (type "KiCad") (uri "${KIPRJMOD}/ESC_B1.kicad_sym") (options "") (descr "B1 pin-numbered engineering symbols")))',encoding='utf-8')
(HERE/'ESC_B1.kicad_sym').write_text('(kicad_symbol_lib (version 20241209) (generator "kicad_symbol_editor")'+''.join(sym(k)[0].replace(q(LIB+':'+k),q(k),1) for k in sorted({p['kind'] for p in parts}))+')',encoding='utf-8')
(HERE/'connection_manifest.json').write_text(json.dumps(parts,ensure_ascii=False,indent=2),encoding='utf-8')
(HERE/'page_manifest.json').write_text(json.dumps({k:{'title':p['title'],'notes':p['notes']} for k,p in pages.items()},ensure_ascii=False,indent=2),encoding='utf-8')
print(f'B1: {len(pages)+1} pages; {len(parts)} symbols; {sum(len(p["parts"]) for p in pages.values())} placed.')

(HERE/(PROJECT+'.kicad_dru')).write_text((HERE.parent/'pcb_b1/ESC_B1.kicad_dru').read_text(encoding='utf-8'),encoding='utf-8')
