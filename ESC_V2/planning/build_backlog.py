"""Generate the initial, evidence-linked backlog. Do not rerun over tracked progress."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
out=root/'planning'
if (out/'backlog.json').exists():
    raise SystemExit('Backlog already exists. Update backlog.json; do not overwrite tracked progress.')
tasks=[]
def add(id,sprint,title,priority,owner,points,deps,risks,acceptance):
    tasks.append(dict(id=id,sprint=sprint,title=title,priority=priority,owner=owner,story_points=points,status='TODO',dependencies=deps.split() if deps else [],source_risks=risks.split(),acceptance=acceptance,evidence=[],blocked_reason=None))
add('ESC-01',1,'Çalışma zarfını ve 1.5/3 kW geçiş koşullarını sabitle','P0','Codex — sistem',3,'','R09','13S gerilim aralığı, batarya/faz akımları, ortam sıcaklığı, sürekli/tepe süreleri ve derating eğrisi aynı tasarım temelinde tanımlı; 3 kW mil gücü ile DC giriş gücü ayrılmış.')
add('ESC-02',1,'Motor, batarya ve test düzeneği numune planı','P0','Codex plan; kullanıcı numune/ölçüm',3,'ESC-01','R09','Motor varyantı, Hall/sıcaklık arayüzü, BMS enerji kabulü ve gerekli ölçüm cihazları listeli; numune temin süresi ve ölçülecek parametreler kayıtlı. Satın alma ayrı kullanıcı kararı.')
add('ESC-03',1,'Giriş sigorta, ön şarj ve ayırma tasarımını tamamla','P0','Codex — güç',8,'ESC-01','R01','Şema, DC kesme kapasitesi, kablo/sigorta I²t koordinasyonu, ön şarj direnç darbe enerjisi ve yardımcı yükle şarj süresi hesapları tamam; ters kutup davranışı tanımlı.')
add('ESC-04',1,'Geri sürülme ve BMS açılması için enerji yönetimi seç','P0','Codex — sistem/güç',8,'ESC-01','R02','Yük ataleti bilinmeyen alanlar açıkça sınırlandırılmış; geçici enerji zarfına göre fren/enerji kabul yolu, bileşen gerilim marjı ve şema tanımlı. OV trip, gerilim kelepçesi olarak kabul edilmez.')
add('ESC-05',1,'Standart ve şema çizim incelemesini tamamla','P1','Codex — donanım',5,'','R07','IEC/IPC referans sürümleri ve erişim sınırları kayıtlı; özel sembol geometrileri, polarite, birimler, NC, sayfa referansları incelenmiş; uygulanamayan maddeler açık listede. Tam uygunluk iddiası yalnız kanıtla.')
add('ESC-06',2,'DC-link kondansatör bankasını ripple ve ömürle boyutlandır','P0','Codex — güç',8,'ESC-01 ESC-04','R03','PWM çalışma zarfında kondansatör RMS akımı, DC bias, ESR kaybı ve ömür hesabı mevcut; tam MPN ve land pattern seçili. 3×470 µF başlangıç varsayımı hesap olmadan korunmaz.')
add('ESC-07',2,'Yardımcı besleme ve küçük pasif seçimlerini kapat','P0','Codex — donanım',5,'ESC-01 ESC-03','R03','12/5/3.3 V yük bütçeleri, bobin doyma/RMS, kapasitör DC bias ve regülatör ripple/kararlılık hesapları tamam; ilgili BOM alt işleri kanıtla kapanmış.')
add('ESC-08',2,'Şönt, terminal, konektör ve mekanik arayüzleri kesinleştir','P0','Codex — PCB/mekanik',5,'ESC-01 ESC-02','R03 R07','Dört uçlu şönt sense/power yönü, konektör akımı/pin1/bakış yönü, terminal montajı ve PCB zarfı ölçülendirilmiş; B1 pin38 uyumsuzluğu montaj belgesinde görünür.')
add('ESC-09',2,'CAN, Hall, RC ve servis port korumalarını tasarla','P0','Codex — donanım',5,'ESC-02','R05','ESD elemanlarının clamp gerilimi IC sınırlarıyla koordineli; Hall çıkış tipi, kablo kopması ve servis besleme geri akışı değerlendirilmiş; şemaya işlenmiş.')
add('ESC-10',2,'BOM ve footprint çift yönlü denetimini tamamla','P0','Codex — donanım/tedarik',8,'ESC-06 ESC-07 ESC-08 ESC-09','R03 R08','61 başlangıç BOM alt işi ve sonradan eklenen parçalar dahil eksik alan sıfır; tüm MPN/pad numaraları veri sayfasıyla karşılaştırılmış; DNP ve muadil yeterlilik seviyesi kayıtlı. Aile kodu tek başına sipariş kanıtı değil.')
add('ESC-11',2,'Termal yapı, bakır ve güç bağlantılarını hesapla','P0','Codex — güç/mekanik',8,'ESC-06 ESC-08','R07','MOSFET/şönt/kondansatör kayıpları, PCB-via-TIM-soğutucu termal yolu ve bağlantı daralmaları incelenmiş; 1.5 ve 3 kW için sıcaklık bütçeleri ve ölçüm noktaları tanımlı.')
add('ESC-12',3,'Güç kartı yerleşimini tamamla','P0','Codex — PCB',8,'ESC-03 ESC-04 ESC-05 ESC-10 ESC-11','R07','Gerçek footprintlerle güç döngüsü, paralel kol simetrisi, gate dönüşü ve Kelvin yerleşimi hazır; mekanik/soğutucu keepout ve kritik yerleşim incelemesi kayıtlı.')
add('ESC-13',3,'Kontrol kartı yerleşimini tamamla','P1','Codex — PCB',5,'ESC-05 ESC-10','R07','MCU bypass, analog dönüş, CAN/servis ve konektör yerleşimleri tamam; iki kart zarfı, pin1 ve montaj erişimi doğrulanmış.')
add('ESC-14',3,'Kartları yönlendir ve elektriksel/mekanik PCB denetimini kapat','P0','Codex — PCB',13,'ESC-12 ESC-13','R07','Açık bağlantı ve kısa devre sıfır; açıklık, courtyard, kenar ve delik hataları giderilmiş; bütün istisnalar gerekçeli; şema-PCB pin/net eşleşmesi ve kritik akım yolu incelemesi tamam.')
add('ESC-15',3,'Firmware pin ve zamanlama temelini kur','P0','Codex — gömülü',8,'ESC-09 ESC-10','R06','Pin sözleşmesiyle derleme tutarlı; PWM/ADC tetikleme, dead-time ve örnekleme pencereleri hesaplanmış; kart başlatma iskeleti derleniyor.')
add('ESC-16',4,'Arıza durum makinesi ve düşük güç test yazılımı','P0','Codex — gömülü',8,'ESC-15','R06 R04','Başlatma, CSA kalibrasyonu, fault latch, haberleşme kaybı ve yeniden başlatma durumları uygulanmış; yazılım testleri kayıtlı; donanım testi yapılmamış alanlar ayrı.')
add('ESC-17',4,'DFM incelemesi ve prototip üretim paketini hazırla','P0','Codex paket; kullanıcı üretici iletişimi',5,'ESC-14','R03 R07','Gerber/drill yeniden görüntülenmiş; stackup, stencil, BOM, yerleştirme, montaj ve revizyon manifesti tutarlı; üretici DFM bulguları kapanmış. Kullanıcı üretim/sipariş kararı verir.')
add('ESC-18',4,'Prototip numuneyi üret ve montaj giriş kontrolünü yap','P0','Kullanıcı — tedarik/fiziksel kontrol',3,'ESC-17','R08','Gerçek kart/montaj numunesi mevcut; revizyon, parça/polarite, kısa devre ve kritik bağlantı ölçümleri kayıtlı. Süre üretici/teslimata bağlı.')
add('ESC-19',4,'Motor ve batarya parametrelerini ölç','P0','Kullanıcı ölçüm; Codex değerlendirme',5,'ESC-02','R09','Rs, Ld/Lq veya uygun eşdeğerleri, Ke, kutup çifti, Hall sırası, sıcaklık sensörü ve BMS davranışı raporlu; çalışma zarfı saparsa tasarım değişikliği açılmış.')
add('ESC-20',5,'Akım sınırlı ilk enerji ve donanım koruma testleri','P0','Kullanıcı ölçüm; Codex test planı',5,'ESC-16 ESC-18','R01 R04 R06','Besleme sıralaması, reset, kilitli fault, tüm PWM kapatma ve sensör doğruluğu ölçülmüş; beklenmeyen anahtarlama yok; başarısız kriterler hata kaydıyla giderilmiş.')
add('ESC-21',5,'Hall/FOC kontrolünü gerçek motorda devreye al','P0','Codex firmware; kullanıcı tezgâh',8,'ESC-19 ESC-20','R06 R09','Hall sırası ve akım polaritesi doğrulanmış; düşük enerji/yüksüz başlatma, kararlı akım kontrolü ve haberleşme kaybı testleri geçilmiş.')
add('ESC-22',5,'Anahtarlama ve 1.5 kW yük doğrulaması','P0','Kullanıcı ölçüm; Codex değerlendirme',8,'ESC-21','R04 R07','VGS/VDS taşması, fault gecikmesi, akım/gerilim sınırları ve tanımlı ortamda termal kararlılık ölçülmüş; 1.5 kW mil gücü doğrulanmış. Yalnız DC giriş wattı yeterli değil.')
add('ESC-23',6,'3 kW ve enerji yönetimi sınır testleri','P0','Kullanıcı ölçüm; Codex değerlendirme',8,'ESC-22 ESC-04','R02 R04 R07','Önceden tanımlı test düzeneğinde 3 kW mil gücü, termal marj, derating ve dolu batarya/BMS ayırma enerji senaryoları geçilmiş; geçmezse 1.5 kW ürün kapsamı veya yeni revizyon kararı kayıtlı.')
add('ESC-24',6,'EMC ve kullanım ortamına özgü doğrulama','P1','Codex plan; kullanıcı/laboratuvar ölçüm',8,'ESC-22','R05 R07','Hedef ürün kullanımına göre uygulanacak testler ve seviyeler kesin; ön uyumluluk/ESD ve çevre test raporları mevcut; kalan resmi uygunluk işleri açıkça ayrılmış.')
add('ESC-25',6,'Revizyon kapanışı ve ürün teslim dosyası','P0','Codex dokümantasyon; kullanıcı kabul',5,'ESC-23 ESC-24','R01 R02 R03 R04 R05 R06 R07 R08 R09','Kritik hata açık değil; doğrulanan güç sınıfı açık; üretim dosyası, firmware etiketi, kalibrasyon, test raporu, montaj ve servis talimatları aynı revizyona ait. Seri tedarik kanıtları tamam.')
add('ESC-26',2,'Kritik tedarik ve muadil stratejisini doğrula','P1','Codex araştırma; kullanıcı tedarik teyidi',3,'ESC-08','R08','MCU/driver/MOSFET/şönt için adet ve ülke bazlı yetkili kanal kaydı, ömür döngüsü ve muadil doğrulama planı mevcut; stok görüntüsü rezervasyon sayılmaz.')
tasks[-2]['dependencies'].append('ESC-26')
done=[('DONE-01','B1 şema kontrol tabanı','../verification/b1_checks.json'),('DONE-02','Motor sıcaklığı arayüz düzeltmesi ve 32 net denetimi','../pcb_b1/verification/interface_audit.json'),('DONE-03','KiCad kural motorunun negatif testleri','../pcb_b1/verification/rule_validation.json')]
for id,title,evidence in done:
    tasks.append(dict(id=id,sprint=0,title=title,priority='P1',owner='Codex',story_points=None,status='DONE',dependencies=[],source_risks=[],acceptance='Yalnız belirtilen rapor kapsamındaki kontrol tamam; ürün doğrulaması değildir.',evidence=[evidence],blocked_reason=None))
missing=json.loads((root/'hardware_b1/bom_open_items.json').read_text(encoding='utf-8'))
subtasks=[dict(id='BOM-'+p['ref'],parent='ESC-10',status='TODO',ref=p['ref'],value=p['value'],missing=p['missing'],acceptance='Eksik alanlar tamam; tam MPN veri sayfası ve pad eşleşme kanıtı kayıtlı.',evidence=[]) for p in missing]
data=dict(revision='PLAN-01',date='2026-09-14',baseline='B1',sprint_duration='2 haftalık planlama kutusu; teslim taahhüdü değil',tasks=tasks,bom_subtasks=subtasks)
(out/'backlog.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
titles={1:'Çalışma zarfı ve kritik sistem kararları',2:'Parça seçimi ve tasarımın sabitlenmesi',3:'PCB tasarımı ve firmware temeli',4:'Üretim paketi, numune ve test hazırlığı',5:'Devreye alma ve 1.5 kW doğrulaması',6:'3 kW kararı ve ürün doğrulaması'}
md=['# ESC 3 kW — Agile yol haritası ve yapılacaklar','', 'PLAN-01 · 14.09.2026 · Başlangıç: B1 mühendislik revizyonu','',
'Hedef: önce ölçümle doğrulanmış 1.5 kW prototip, ardından marjlar yeterliyse 3 kW ürün adayı. Tamamlanan plan, tamamlanmış donanım anlamına gelmez. Mevcut baz: 741 kontrol, sıfır ERC ihlali, 32 kartlar arası net kontrolü; 61 bileşende BOM eksikliği; ürün PCB routing henüz yok.','',
'## Çalışma düzeni','',
'İki haftalık sprintler planlama önerisidir. Altı sprint, altı iterasyon hedefidir; 12 haftalık garanti değildir. Tedarik, laboratuvar ve başarısız testlerden doğan revizyonlar süreyi değiştirebilir. Kapasite/velocity henüz ölçülmediği için aşağıdaki sprint yükleri taahhüt değildir; özellikle 13 puanlık ESC-14 işe alınmadan kart ve kritik net gruplarına bölünür.','',
'Akış: TODO → READY → IN_PROGRESS → REVIEW → DONE. BLOCKED ayrı durumdur; nedeni ve açılma koşulu yazılır. Başlangıç açık işlerin hepsi TODO, yalnız kanıtı olan üç kontrol DONE. Bağımlılıkları kapanmayan iş READY olamaz.','',
'P0 bir sonraki tasarım/üretim/test kapısını engeller; P1 güvenilirlik ve ürünleştirme işidir. P1 ürün tesliminden otomatik olarak çıkarılmaz. Story point göreli karmaşıklıktır, saat/gün değildir. Aynı anda en fazla iki IN_PROGRESS ve bir REVIEW işi önerilir. Roller çalışma sorumluluğudur; ek personel atanmış değildir.','',
'Her sprint başında hazır işler kapasiteye göre seçilir; sonunda dosya/rapor gösterimi ve kısa retrospektif yapılır. Test başarısızsa işi tamamlandı saymak yerine hata kaydı, tekrar üretim ihtiyacı ve bağımlı işlerin durumu güncellenir. Firmware işleri PCB çalışmalarına paralel yürüyebilir; üretim beklerken numune ölçümleri ilerler.','',
'**Definition of Ready:** giriş verileri mevcut, bağımlılıklar tamam, kabul ölçütü ölçülebilir, gerekli numune/araç erişimi belli. **Definition of Done:** ilgili kabul ölçütleri geçti, kanıt dosyası ve revizyon kaydedildi, değişiklikler şema/PCB/BOM/firmware arasında tutarlı, inceleme tamam. ERC/DRC geçmesi fiziksel performansı kapatmaz.','',
'## İlk sprintin seçilecek işleri','',
'Önerilen ilk çekim: ESC-01 ve ESC-05. ESC-01 kapanınca ESC-03/ESC-04 için çalışma zarfı hazır olur; ESC-02 numune tedarik belirsizliğini erkenden görünür kılar. Bu planlama turu tasarım görevlerini otomatik olarak başlatmaz.','']
for sprint,title in titles.items():
    items=[t for t in tasks if t['sprint']==sprint]
    md += [f'## Sprint {sprint} — {title}', '', f'Öngörülen backlog yükü: {sum(t["story_points"] for t in items)} SP; sprint planlamasında kapasiteye göre daraltılır.', '']
    for t in items:
        md += [f'- [ ] **{t["id"]} · {t["title"]}**',f'  - {t["priority"]} · {t["story_points"]} SP · Sorumlu: {t["owner"]} · Durum: TODO',f'  - Ön koşul: {", ".join(t["dependencies"]) or "Yok"}. Kaynak risk: {", ".join(t["source_risks"])}.',f'  - Kabul: {t["acceptance"]}', '']
md += ['## Geçiş kapıları','',
'- **G1 / Tasarım sabitleme:** ESC-01–11 ve ESC-26 kapsamı incelenmiş, kritik elektriksel seçimler açıkta değil. Numune planı tamam olabilir; gerçek parametre ölçümleri ESC-19 ile prototip testi öncesinde gerekir.',
'- **G2 / Prototip siparişi:** ESC-14 ve ESC-17 tamam. Üretim dosyası veya satın alma, kullanıcı kararıyla gerçekleşir.',
'- **G3 / Motoru enerjileme:** ESC-19 ve ESC-20 tamam; gerçek parametreler ve korumalar doğrulanmış.',
'- **G4 / 1.5 kW:** ESC-22 kabul ölçütleri geçti. Bu sonuç 3 kW izni değildir.',
'- **G5 / Ürün adayı:** ESC-23–25 tamam. 3 kW başarısızsa kapsam kararı görünür şekilde değiştirilir; test sonucu gizlenmez.','',
'## Tamamlanmış başlangıç işleri','']
for id,title,evidence in done:md += [f'- [x] **{id} — {title}** · [Kanıt]({evidence})']
md += ['','## BOM alt yapılacaklar — ESC-10','', '61 fiziksel bileşen kaydıdır; 61 farklı satın alınacak parça çeşidi anlamına gelmez. Aynı MPN ile kapanan satırlar ayrı refdes kanıtlarını korur. Yeni tasarım elemanları eklenirse bu liste büyüyebilir.','']
for t in subtasks:md += [f'- [ ] **{t["id"]}** — {t["value"]}; eksik: {", ".join(t["missing"])}.']
md += ['','## Takip ve değişiklik yönetimi','',
'Asıl takip kaydı `backlog.json` dosyasıdır. Bu Markdown, PLAN-01 anlık görünümüdür; ilerleme güncellenirken ikisi birlikte güncellenir. `build_backlog.py` mevcut takip dosyasının üzerine yazmayı reddeder. Her kapatılan işte kanıt yolu eklenir; durum/puan değişikliği gerekçesi sprint değerlendirmesine yazılır.','',
'Sprint ölçümleri: kabul edilmiş iş/SP, açık P0, kapanan BOM kayıtları, açık PCB bağlantıları ve DRC hataları, test geçiş oranı. Başlangıç PCB/test ölçümleri mevcut olmadığı için sıfır başarı veya yüzde tamamlanma uydurulmaz.','',
'Kaynaklar: `../hardware_a2/release_register.json` R01–R09; `../hardware_b1/bom_open_items.json`; `../hardware_b1/README.md`; `../pcb_b1/TASARIM_KURALLARI.md`. Eski risk kayıtları silinmedi; bu backlog uygulama işlerini ve bağımlılıklarını ayrıntılandırır.','']
(out/'AGILE_ROADMAP.md').write_text('\n'.join(md),encoding='utf-8')
ids={t['id'] for t in tasks}
assert len(ids)==len(tasks)
assert all(d in ids for t in tasks for d in t['dependencies'])
byid={t['id']:t for t in tasks}
def visit(id,path=()):
    assert id not in path,('cycle',path,id)
    for d in byid[id]['dependencies']:visit(d,path+(id,))
for id in ids:visit(id)
assert len(subtasks)==61 and len({t['id'] for t in subtasks})==61
assert set('R%02d'%i for i in range(1,10)) <= {r for t in tasks for r in t['source_risks']}
print(f'{len(tasks)} main records; {len(subtasks)} BOM subtasks; dependency graph acyclic; R01-R09 covered.')
