"""Generate reviewable KiCad A1 schematics and connection manifest.
Custom functional symbols retain electrical pin types and physical pin numbers.
This is a design review draft, NOT a manufacturing release.
"""
from pathlib import Path
import json, math, uuid
from collections import defaultdict
from sexpr import load_symbol, pins

ROOT=Path(__file__).resolve().parent
PROJECT='ESC_3kW_A1'
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,PROJECT+'/'+s))
def q(s):return json.dumps(str(s),ensure_ascii=False)
def effects(size=1.0,extra=''):return f'(effects (font (size {size} {size})) {extra})'
parts=[]; counts=defaultdict(int); definitions={}
def pinlist(names,types=None):
    return [{'number':str(i+1),'name':n,'type':(types or {}).get(n,'passive')} for i,n in enumerate(names)]
def define(name,ps):definitions[name]=ps
def fromlib(name,lib,symbol):define(name,pins(load_symbol(lib,symbol)))
for key,lib,name in [('MCU','MCU_ST_STM32G4','STM32G474RETx'),('BUCK12','Regulator_Switching','LM5164DDA'),('BUCK5','Regulator_Switching','TPS62160DGK'),('LDO','Regulator_Linear','TLV75533PDBV'),('CAN','Interface_CAN_LIN','SN65HVD230')]:fromlib(key,lib,name)
define('R',pinlist(['1','2']));define('C',pinlist(['1','2']));define('L',pinlist(['1','2']))
define('NMOS',pinlist(['G','D','S'],{'G':'input'}))
define('DIODE',pinlist(['K','A']))
define('SHUNT',pinlist(['I+','I-','S+','S-']))
drv='CPL CPH VM VDRAIN VCP GHA SHA GLA SPA SNA SNB SPB GLB SHB GHB GHC SHC GLC SPC SNC SOC SOB SOA VREF AGND nFAULT SDO SDI SCLK nSCS ENABLE INHA INLA INHB INLB INHC INLC DVDD GND VGLS EP'.split()
types={x:'input' for x in drv}
for x in ['GHA','GLA','GHB','GLB','GHC','GLC','SOA','SOB','SOC']:types[x]='output'
for x in ['nFAULT','SDO']:types[x]='open_collector'
for x in ['VM','VREF','AGND','GND','EP']:types[x]='power_in'
for x in ['DVDD','VGLS','VCP']:types[x]='power_out'
for x in ['CPH','CPL']:types[x]='passive'
define('DRV',pinlist(drv,types))
comp=['OUT2','OUT1','VCC','IN1-','IN1+','IN2-','IN2+','IN3-','IN3+','IN4-','IN4+','GND','OUT4','OUT3']
define('COMP',pinlist(comp,{**{x:'input' for x in comp if x.startswith('IN')},**{x:'open_collector' for x in comp if x.startswith('OUT')},'VCC':'power_in','GND':'power_in'}))
define('LATCH',pinlist(['CLK','D','Qn','GND','Q','CLRn','PREn','VCC'],{'CLK':'input','D':'input','Qn':'output','GND':'power_in','Q':'output','CLRn':'input','PREn':'input','VCC':'power_in'}))
define('AND',pinlist(['A','B','GND','Y','VCC'],{'A':'input','B':'input','GND':'power_in','Y':'output','VCC':'power_in'}))
define('FLAG',[{'number':'1','name':'POWER','type':'power_out'}])

def add(page,kind,value,nets,mpn='',footprint='',note='',prefix=None):
    pref=prefix or {'R':'R','C':'C','L':'L','NMOS':'Q','DIODE':'D','SHUNT':'RS','FLAG':'#FLG'}.get(kind,'U')
    counts[pref]+=1;ref=pref+str(counts[pref])
    if isinstance(nets,list):mapping={str(i+1):v for i,v in enumerate(nets)}
    else:
        mapping={p['number']:nets.get(p['name']) for p in definitions[kind]}
    assert set(mapping)=={p['number'] for p in definitions[kind]},ref
    if not footprint and kind=='R' and 'NET-TIE' not in value and 'NTC' not in value:footprint='Resistor_SMD:R_0805_2012Metric'
    if not footprint and kind=='C' and not any(x in value for x in ['100V','160V','bulk','22u','10u','4.7u']):footprint='Capacitor_SMD:C_0805_2012Metric'
    parts.append(dict(ref=ref,page=page,kind=kind,value=value,nets=mapping,mpn=mpn,footprint=footprint,note=note))
    return ref
def r(pg,val,a,b,**kw):return add(pg,'R',val,[a,b],**kw)
def c(pg,val,a,b='GND',**kw):return add(pg,'C',val,[a,b],**kw)
def conn(pg,name,nets,note=''):
    key='CONN'+str(len(nets))
    define(key,pinlist([str(i+1) for i in range(len(nets))]))
    return add(pg,key,name,nets,prefix='J',note=note)

pg='01_DC_link'
conn(pg,'DC LINK INPUT',['VBUS','GND'],'From external fused, precharged, reverse-polarity-protected DC input assembly; not raw battery.')
conn(pg,'MOTOR U V W',['PH_A','PH_B','PH_C'],'High current terminal system: mechanical selection pending.')
conn(pg,'EXTERNAL BRAKE MODULE',['VBUS','GND'],'Regen energy clamp/chopper sizing and interface remain release blockers.')
for i in range(3):c(pg,'470u 100V bulk','VBUS',note='Provisional total 1410uF; exact ESR/ripple/lifetime and MPN pending.',footprint='')
for i in range(3):c(pg,'2.2u 100V X7R','VBUS',note='At each half bridge; effective capacitance under bias required.')
r(pg,'100k 0.25W','VBUS','GND',note='Bleed only; discharge time must be checked before service.')
for net in ['VBUS','GND']:add(pg,'FLAG',net,[net])

for phase in 'ABC':
    pg='02_phase_'+phase
    for side in ['H','L']:
        for k in range(2):
            gate=f'G{side}{phase}_{k+1}';source=f'PH_{phase}' if side=='H' else f'SHUNT_{phase}_P'
            drain='VBUS' if side=='H' else f'PH_{phase}'
            add(pg,'NMOS','CSD19536KTT',[gate,drain,source],mpn='CSD19536KTT',footprint='Package_TO_SOT_SMD:TO-263-3_TabPin2',note='Pin 2 is drain tab. Parallel pair requires symmetric routing and separate gate resistor.')
            r(pg,'4.7R gate',f'G{side}{phase}',gate,note='Starting value, tune with VGS/VDS measurements.')
            r(pg,'47k G-S',gate,source)
    add(pg,'SHUNT','0.5mR Kelvin',[f'SHUNT_{phase}_P','GND',f'IS_{phase}_P',f'IS_{phase}_N'],note='4-terminal symbol. 5W minimum candidate class; exact pad numbering, MPN and pulse rating pending.')
    # Kelvin terminals are physically common within a four-terminal resistor;
    # explicit net ties model this without hiding separate sense routing.
    r(pg,'0R NET-TIE ONLY',f'SHUNT_{phase}_P',f'IS_{phase}_P',note='Replace by net tie at shunt sense terminal in PCB; not a discrete routing shortcut.')
    r(pg,'0R NET-TIE ONLY','GND',f'IS_{phase}_N',note='Replace by net tie at shunt sense terminal in PCB.')
    c(pg,'100n 100V','VBUS')

pg='03_gate_driver'
n={x:x for x in drv}
n.update(VM='+12V',VDRAIN='VBUS',VREF='+3V3A',AGND='GND',GND='GND',EP='GND',nFAULT='DRV_FAULT_N',SDO='SPI_MISO',SDI='SPI_MOSI',SCLK='SPI_SCK',nSCS='DRV_CS_N',ENABLE='DRV_ENABLE',DVDD='DRV_DVDD',VGLS='DRV_VGLS')
for ph in 'ABC':n.update({f'SH{ph}':f'PH_{ph}',f'SP{ph}':f'IS_{ph}_P',f'SN{ph}':f'IS_{ph}_N',f'SO{ph}':f'I_{ph}_RAW',f'INH{ph}':f'PWM_H{ph}',f'INL{ph}':f'PWM_L{ph}'})
add(pg,'DRV','DRV8353FSRTAR',n,mpn='DRV8353FSRTAR',note='F variant selected for supply evidence. RTA0040 footprint must be checked against mechanical drawing; not assigned by package-name guess.')
c(pg,'47n 100V','CPH','CPL');c(pg,'1u 25V','VCP','VBUS');c(pg,'1u 25V','DRV_VGLS');c(pg,'1u 10V','DRV_DVDD')
c(pg,'100n 25V','+12V');c(pg,'10u 25V','+12V');c(pg,'100n 10V','+3V3A')
r(pg,'4.7k pull-up','SPI_MISO','+3V3');r(pg,'4.7k pull-up','DRV_FAULT_N','+3V3');r(pg,'10k pull-up','DRV_CS_N','+3V3');r(pg,'10k pull-down','DRV_ENABLE','GND')
for ph in 'ABC':
    for side in 'HL':r(pg,'47k pull-down',f'PWM_{side}{ph}','GND')

pg='04_voltage_sensing'
for key,source in [('BUS','VBUS'),('A','PH_A'),('B','PH_B'),('C','PH_C')]:
    mid='V_'+key+'_MID';raw='V_'+key+'_DIV';adc='V_'+key+'_ADC'
    r(pg,'49.9k 0.1%',source,mid);r(pg,'49.9k 0.1%',mid,raw);r(pg,'3.32k 0.1%',raw,'GND')
    r(pg,'1k ADC series',raw,adc);c(pg,'1n C0G',adc,note='Provisional ~38kHz including divider source impedance; validate ADC acquisition and phase delay.')
    add(pg,'DIODE','BAT54H upper',['+3V3A',adc],mpn='BAT54H',note='Clamp leakage and 3V3 rail backfeed require worst-case review.')
    add(pg,'DIODE','BAT54H lower',[adc,'GND'],mpn='BAT54H')

pg='05_current_and_temperature'
for ph in 'ABC':
    r(pg,'100R ADC',f'I_{ph}_RAW',f'I_{ph}_ADC');c(pg,'1n C0G',f'I_{ph}_ADC')
for t in ['FET','PCB']:
    r(pg,'10k 0.1%','+3V3A','TEMP_'+t);r(pg,'NTC 10k B3435','TEMP_'+t,'GND',note='MPN, tolerance and actual placement pending; firmware must use selected curve.')
    c(pg,'10n','TEMP_'+t)
conn(pg,'MOTOR TEMP',['TEMP_MOTOR_RAW','GND'],note='Sensor type not yet confirmed; A1 assumes resistance sensor for interface review only.')
r(pg,'10k provision','+3V3A','TEMP_MOTOR_RAW');r(pg,'1k','TEMP_MOTOR_RAW','TEMP_MOTOR');c(pg,'10n','TEMP_MOTOR')

pg='06_aux_12V'
add(pg,'BUCK12','LM5164DDAT',{'GND':'GND','VIN':'VBUS','EN/UVLO':'BUCK_UVLO','RON':'BUCK_RON','FB':'BUCK_FB','PGOOD':'PG_12V','BST':'BUCK_BST','SW':'BUCK_SW','EP':'GND'},mpn='LM5164DDAT',footprint='Package_SO:HSOP-8-1EP_3.9x4.9mm_P1.27mm_EP2.41x3.1mm_ThermalVias')
add(pg,'L','68uH >=1.5A',['BUCK_SW','+12V'],note='Effective L, saturation current, DCR and footprint pending exact MPN.')
c(pg,'2.2u 160V','VBUS');c(pg,'100n 160V','VBUS');c(pg,'22u 25V','+12V');c(pg,'22u 25V','+12V');c(pg,'2.2n C0G','BUCK_BST','BUCK_SW')
r(pg,'100k','VBUS','BUCK_RON');r(pg,'453k','+12V','BUCK_FB');r(pg,'49.9k','BUCK_FB','GND')
r(pg,'453k ripple','BUCK_SW','BUCK_RIPPLE');c(pg,'3.3n','BUCK_RIPPLE','+12V');c(pg,'56p C0G','BUCK_RIPPLE','BUCK_FB')
r(pg,'1M UVLO','VBUS','BUCK_UVLO');r(pg,'100k UVLO','BUCK_UVLO','GND',note='Aux powers early for diagnostics; this is NOT the traction undervoltage cutoff.')
r(pg,'10k','PG_12V','+3V3');conn(pg,'FAN 12V',['+12V','GND'],note='Fan <=0.2A continuous budget. Inrush must be measured.')

pg='07_aux_5V_3V3'
add(pg,'BUCK5','TPS62160DGKR',{'PGND':'GND','VIN':'+12V','EN':'+12V','AGND':'GND','FB':'FB_5V','VOS':'+5V','SW':'SW_5V','PG':'PG_5V'},mpn='TPS62160DGKR',footprint='Package_SO:VSSOP-8_3x3mm_P0.65mm')
add(pg,'L','2.2uH >=1.5A',['SW_5V','+5V'],note='Check DC bias and saturation against converter peak current.')
c(pg,'10u 25V','+12V');c(pg,'22u 10V','+5V');r(pg,'523k','+5V','FB_5V');r(pg,'100k','FB_5V','GND');r(pg,'10k','PG_5V','+3V3')
add(pg,'LDO','TLV75533PDBVR',{'IN':'+5V','GND':'GND','EN':'+5V','NC':None,'OUT':'+3V3'},mpn='TLV75533PDBVR',footprint='Package_TO_SOT_SMD:SOT-23-5')
c(pg,'1u 10V','+5V');c(pg,'4.7u 10V','+3V3')
r(pg,'0R analog link','+3V3','+3V3A',note='Optional ferrite only after analog rail impedance review.')
c(pg,'4.7u 10V','+3V3A');c(pg,'100n','+3V3A')

pg='08_MCU'
mcu={p['name']:None for p in definitions['MCU']}
mcu.update(VBAT='+3V3',VDD='+3V3',VSS='GND',VSSA='GND',VDDA='+3V3A',**{'VREF+':'+3V3A'})
mcu.update(PG10='NRST',PF0='HSE_IN',PF1=None,PA8='MCU_PWM_HA',PA9='MCU_PWM_HB',PA10='MCU_PWM_HC',PB13='MCU_PWM_LA',PB14='MCU_PWM_LB',PB15='MCU_PWM_LC',PB12='HARD_FAULT_N',PA11='CAN_RX',PA12='CAN_TX',PB3='SPI_SCK',PB4='SPI_MISO',PB5='SPI_MOSI',PC4='DRV_CS_N',PC5='ARM_CLK',PC6='HALL_A',PC7='HALL_B',PC8='HALL_C',PC9='RUN_REQUEST',PC10='UART_TX',PC11='UART_RX',PA13='SWDIO',PA14='SWCLK',PA0='I_A_ADC',PA1='I_B_ADC',PA2='I_C_ADC',PC0='V_BUS_ADC',PC1='V_A_ADC',PC2='V_B_ADC',PC3='V_C_ADC',PA3='TEMP_FET',PA4='TEMP_PCB',PB0='TEMP_MOTOR',PB1=None,PA15='RC_PWM',PB2='PG_12V',PB10='PG_5V',PB11='DRV_FAULT_N',PC12='STATUS_LED',PD2='LATCH_STATE',PB8='BOOT0')
add(pg,'MCU','STM32G474RET3',mcu,mpn='STM32G474RET3',footprint='Package_QFP:LQFP-64_10x10mm_P0.5mm',note='PG10 must remain NRST option. PB8 BOOT0 option bytes reviewed before flashing. Verify AF/ADC schedule before PCB.')
for i in range(4):c(pg,'100n at VDD','+3V3')
c(pg,'4.7u','+3V3');c(pg,'100n at VBAT','+3V3');c(pg,'1u VDDA','+3V3A');c(pg,'100n VDDA','+3V3A');c(pg,'100n VREF','+3V3A')
r(pg,'10k','NRST','+3V3');c(pg,'100n reset','NRST');r(pg,'10k BOOT0','BOOT0','GND');r(pg,'10k','ARM_CLK','GND');r(pg,'10k','RUN_REQUEST','GND')
conn(pg,'SWD',['+3V3','SWDIO','GND','SWCLK','NRST'],note='VTref only; avoid powering rail from two sources.')
define('OSC',pinlist(['OE','GND','OUT','VDD'],{'OE':'input','GND':'power_in','OUT':'output','VDD':'power_in'}))
add(pg,'OSC','8MHz 3V3 CMOS oscillator',['+3V3','GND','HSE_IN','+3V3'],prefix='Y',note='4-pad 3225 oscillator candidate; pinout and MPN pending. HSE BYPASS mode.')
c(pg,'100n oscillator','+3V3');r(pg,'1k LED','+3V3','LED_A');add(pg,'DIODE','LED GREEN',['STATUS_LED','LED_A'])

pg='09_comms'
add(pg,'CAN','SN65HVD230DR',{'D':'CAN_TX','GND':'GND','VCC':'+3V3','R':'CAN_RX','Vref':None,'CANL':'CAN_L','CANH':'CAN_H','Rs':'CAN_RS'},mpn='SN65HVD230DR',footprint='Package_SO:SOIC-8_3.9x4.9mm_P1.27mm',note='Classic CAN only, not CAN FD. TVS array selection pending.')
r(pg,'10k slope','CAN_RS','GND');c(pg,'100n CAN','+3V3');r(pg,'120R DNP','CAN_H','CAN_L',note='Fit only at bus end; DNP by default.')
conn(pg,'CAN',['GND','CAN_H','CAN_L']);conn(pg,'UART 3V3',['GND','UART_RX','UART_TX']);conn(pg,'RC PWM 3V3',['GND','RC_PWM'])
conn(pg,'HALL 5V',['+5V','GND','HALL_A_EXT','HALL_B_EXT','HALL_C_EXT'],note='Interface requires open-collector Hall outputs; push-pull sensor needs level conversion.')
for ph in 'ABC':
    r(pg,'4.7k 3V3 pull-up','+3V3',f'HALL_{ph}_EXT');r(pg,'1k',f'HALL_{ph}_EXT',f'HALL_{ph}');c(pg,'1n',f'HALL_{ph}')

pg='10_hardware_trip'
# Outputs low outside window; shared open-collector net clears latch asynchronously.
common={'VCC':'+3V3A','GND':'GND','OUT1':'HARD_FAULT_N','OUT2':'HARD_FAULT_N','OUT3':'HARD_FAULT_N','OUT4':'HARD_FAULT_N'}
a={**common,'IN1+':'I_A_RAW','IN1-':'OC_LOW','IN2+':'OC_HIGH','IN2-':'I_A_RAW','IN3+':'I_B_RAW','IN3-':'OC_LOW','IN4+':'OC_HIGH','IN4-':'I_B_RAW'}
b={**common,'IN1+':'I_C_RAW','IN1-':'OC_LOW','IN2+':'OC_HIGH','IN2-':'I_C_RAW','IN3+':'OV_REF','IN3-':'V_BUS_DIV','IN4+':'+3V3A','IN4-':'GND','OUT4':None}
for n in [a,b]:add(pg,'COMP','TLV1704PWR',n,mpn='TLV1704PWR',footprint='Package_SO:TSSOP-14_4.4x5mm_P0.65mm',note='Comparator delay plus CSA settling is not a guaranteed short-circuit limit; MOSFET VDS protection remains primary.')
for i in range(2):c(pg,'100n comparator','+3V3A')
# Ratiometric thresholds: 0.912/2.388 V -> approximately +/-148 A at 5mV/A.
r(pg,'26.1k 0.1%','+3V3A','OC_LOW');r(pg,'10k 0.1%','OC_LOW','GND');r(pg,'10k 0.1%','+3V3A','OC_HIGH');r(pg,'26.1k 0.1%','OC_HIGH','GND')
c(pg,'10n reference','OC_LOW');c(pg,'10n reference','OC_HIGH')
r(pg,'7.50k 0.1%','+3V3A','OV_REF');r(pg,'10k 0.1%','OV_REF','GND');c(pg,'10n reference','OV_REF')
r(pg,'2.2k fault pull-up','HARD_FAULT_N','+3V3');add(pg,'DIODE','BAT54H fault OR',['DRV_FAULT_N','HARD_FAULT_N'],mpn='BAT54H',note='Verify diode VOL + DRV sink voltage meets latch CLR and MCU BKIN VIL.')
add(pg,'DIODE','BAT54H reset OR',['NRST','HARD_FAULT_N'],mpn='BAT54H')
add(pg,'DIODE','BAT54H PG OR',['PG_12V','HARD_FAULT_N'],mpn='BAT54H')
add(pg,'DIODE','BAT54H PG OR',['PG_5V','HARD_FAULT_N'],mpn='BAT54H')
add(pg,'LATCH','SN74LVC1G74DCUR',{'CLK':'ARM_CLK','D':'+3V3','Qn':None,'GND':'GND','Q':'LATCH_STATE','CLRn':'HARD_FAULT_N','PREn':'+3V3','VCC':'+3V3'},mpn='SN74LVC1G74DCUR',footprint='Package_SO:VSSOP-8_2.3x2mm_P0.5mm',note='Fault clears Q. Re-arm requires deliberate rising edge with fault absent. Power-up state not assumed.')
r(pg,'0R driver wake','RUN_REQUEST','DRV_ENABLE',note='Wake DRV first with PWM inhibited. Configure CSA and wait for healthy fault net, then arm latch.')
c(pg,'100n latch','+3V3')
conn(pg,'EMERGENCY STOP',['HARD_FAULT_N','GND'],note='Shorting contact clears latch; wire-break detection not implemented.')

pg='11_PWM_interlock'
for ph in 'ABC':
    for side in 'HL':
        add(pg,'AND','SN74LVC1G08DBVR',{'A':'LATCH_STATE','B':f'MCU_PWM_{side}{ph}','GND':'GND','Y':f'PWM_{side}{ph}','VCC':'+3V3'},mpn='SN74LVC1G08DBVR',footprint='Package_TO_SOT_SMD:SOT-23-5',note='Latch low forces all DRV PWM inputs low; no automatic retry on fault release.')
        r(pg,'47k reset default',f'MCU_PWM_{side}{ph}','GND');c(pg,'100n logic','+3V3')
pg='12_board_interface'
interface=['GND','+3V3','GND','+3V3A','MCU_PWM_HA','MCU_PWM_LA','GND','MCU_PWM_HB','MCU_PWM_LB','GND','MCU_PWM_HC','MCU_PWM_LC','GND','RUN_REQUEST','ARM_CLK','LATCH_STATE','HARD_FAULT_N','DRV_FAULT_N','DRV_CS_N','SPI_SCK','SPI_MOSI','SPI_MISO','GND','I_A_ADC','I_B_ADC','I_C_ADC','GND','V_BUS_ADC','V_A_ADC','V_B_ADC','V_C_ADC','GND','TEMP_FET','TEMP_PCB','PG_12V','PG_5V','NRST','GND','GND','GND']
conn(pg,'POWER CARD 2x20',interface,note='Mate to control card pin-for-pin; connector and viewing direction not released.')
conn(pg,'CONTROL CARD 2x20',interface,note='Same system nets model mating harness; PCB partition documented in README.')
for net in ['+12V','+5V','+3V3A']:add(pg,'FLAG',net,[net],note='Derived rail after buck inductor / analog link. Flags declare actual source, not a separate supply.')

# Output structure: split dense pages, preserve global net names.
pages=defaultdict(list)
for p in parts:pages[p['page']].append(p)
expanded={}
for name,rows in pages.items():
    limit=18
    for start in range(0,len(rows),limit):
        suffix='' if start==0 else '_'+str(start//limit+1)
        newname=name+suffix
        expanded[newname]=rows[start:start+limit]
        for part in rows[start:start+limit]:part['page']=newname

def symbol_def(kind,full_name=None):
    ps=definitions[kind];n=len(ps);simple=n==2 and kind in ['R','C','L','DIODE']
    width=5.08 if simple else (20.32 if n>8 else 10.16)
    half=math.ceil(n/2);height=2.54 if simple else max(5.08,half*2.54/2+2.54)
    pinpos=[]
    for i,p in enumerate(ps):
        if simple:x=(-7.62 if i==0 else 7.62);y=0;angle=0 if i==0 else 180
        else:
            left=i<half;j=i if left else i-half
            x=-width-2.54 if left else width+2.54;y=(half-1)*1.27-j*2.54;angle=0 if left else 180
        pinpos.append((p,x,y,angle))
    name=full_name or kind
    body=f'(symbol {q(name)} (pin_names (offset 0.8) {"(hide yes)" if simple else ""}) (in_bom yes) (on_board yes) (property "Reference" "U" (at 0 0 0) {effects()}) (property "Value" {q(kind)} (at 0 0 0) {effects()})'
    def line(points):return '(polyline (pts '+''.join(f'(xy {x} {y})' for x,y in points)+') (stroke (width 0.254) (type default)) (fill (type none)))'
    if kind=='C':shape=line([(-5.08,0),(-1.27,0)])+line([(-1.27,-2.54),(-1.27,2.54)])+line([(1.27,-2.54),(1.27,2.54)])+line([(1.27,0),(5.08,0)])
    elif kind=='DIODE':shape=line([(-5.08,0),(-1.27,0)])+line([(-1.27,-2.54),(-1.27,2.54)])+line([(-1.27,0),(2.54,2.54),(2.54,-2.54),(-1.27,0)])+line([(2.54,0),(5.08,0)])
    elif kind=='L':shape=line([(-5.08,0),(-3.81,1.27),(-2.54,-1.27),(-1.27,1.27),(0,-1.27),(1.27,1.27),(2.54,-1.27),(3.81,1.27),(5.08,0)])
    else:shape=f'(rectangle (start {-width} {height}) (end {width} {-height}) (stroke (width 0.254) (type default)) (fill (type background)))'
    body+=f'(symbol {q(kind+"_0_1")} {shape})'
    body+=f'(symbol {q(kind+"_1_1")}'
    for p,x,y,a in pinpos:
        body+=f'(pin {p["type"]} line (at {x} {y} {a}) (length 2.54) (name {q(p["name"])} {effects(.9)}) (number {q(p["number"])} {effects(.8)}))'
    return body+'))',pinpos,height

def text(s,x,y,size=1.27):return f'(text {q(s)} (at {x} {y} 0) {effects(size,"(justify left)")} (uuid {q(uid(s+str(x)+str(y)))}))'
def base(name):return f'(kicad_sch (version 20250114) (generator "eeschema") (uuid {q(uid(name))}) (paper "A3") (title_block (title {q(name)}) (date "2026-09-13") (rev "A1 REVIEW DRAFT") (company "ESC V2") (comment 1 "NOT FOR FABRICATION - see release blockers"))'
rootuuid=uid(PROJECT)
for pagename,rows in expanded.items():
    pageid=uid(pagename);sheetid=uid('sheet/'+pagename)
    syms=''.join(symbol_def(k,'ESC_A1:'+k)[0] for k in sorted({p['kind'] for p in rows}))
    s=base(pagename)+'(lib_symbols '+syms+')'
    s+=text(pagename.replace('_',' '),15,15,2.0)+text('A1 REVIEW DRAFT | Global net labels connect sheets | Values and footprints pending release review',15,23,1.1)
    # Three columns, each laid out with component-specific height.
    columns=[35.,35.,35.]
    for p in rows:
        definition,positions,height=symbol_def(p['kind'])
        col=min(range(3),key=lambda x:columns[x]);x=[76.2,205.74,335.28][col];y=round(math.ceil((columns[col]+height+8)/1.27)*1.27,2)
        columns[col]=y+height+15
        if columns[col]>265:raise ValueError('Layout overflow '+pagename+' '+p['ref'])
        p['x']=x;p['y']=y
        rid=uid(p['ref']);s+=f'(symbol (lib_id {q("ESC_A1:"+p["kind"])}) (at {x} {y} 0) (unit 1) (in_bom {"no" if p["kind"]=="FLAG" else "yes"}) (on_board {"no" if p["kind"]=="FLAG" else "yes"}) (dnp {"yes" if "DNP" in p["value"] else "no"}) (uuid {q(rid)})'
        for key,val,py,hidden in [('Reference',p['ref'],y-height-4,False),('Value',p['value'],y-height-1,False),('Footprint',p['footprint'],y,True),('MPN',p['mpn'],y,True),('Review',p['note'],y,True)]:
            s+=f'(property {q(key)} {q(val)} (at {x} {py} 0) {effects(.95,"(hide yes)" if hidden else "")})'
        for pin,px,py,a in positions:s+=f'(pin {q(pin["number"])} (uuid {q(uid(p["ref"]+"/"+pin["number"]))}))'
        s+=f'(instances (project {q(PROJECT)} (path {q("/"+rootuuid+"/"+sheetid)} (reference {q(p["ref"])}) (unit 1)))))'
        for pin,px,py,a in positions:
            ax=x+px;ay=y-py;net=p['nets'][pin['number']]
            if net is None:s+=f'(no_connect (at {ax} {ay}) (uuid {q(uid(p["ref"]+pin["number"]+"nc"))}))';continue
            endx=ax+(-5.08 if a==0 else 5.08)
            s+=f'(wire (pts (xy {ax} {ay}) (xy {endx} {ay})) (stroke (width 0) (type default)) (uuid {q(uid(p["ref"]+pin["number"]+"wire"))}))'
            s+=f'(global_label {q(net)} (shape bidirectional) (at {endx} {ay} {0 if a==0 else 180}) {effects(.8,"(justify "+("right" if a==0 else "left")+")")} (uuid {q(uid(p["ref"]+pin["number"]+"label"))}))'
    (ROOT/(pagename+'.kicad_sch')).write_text(s+')',encoding='utf-8')

s=base(PROJECT)+'(lib_symbols)'+text('ESC V2 - 48 V class / 3 kW shaft target',15,15,2)+text('A1 - CONNECTED CIRCUIT REVIEW DRAFT. No PCB or production approval.',15,23,1.4)
s+=text('External battery front-end, brake energy handling, shunt/driver footprints, EMC and firmware validation remain open.',15,31,1.1)
for i,(name,rows) in enumerate(expanded.items()):
    x=20+(i%3)*130;y=45+(i//3)*30;sid=uid('sheet/'+name)
    s+=f'(sheet (at {x} {y}) (size 110 17) (fields_autoplaced yes) (stroke (width 0.1524) (type solid)) (fill (color 0 0 0 0)) (uuid {q(sid)}) (property "Sheetname" {q(name)} (at {x} {y-1} 0) {effects(1.2,"(justify left)")}) (property "Sheetfile" {q(name+".kicad_sch")} (at {x} {y+18} 0) {effects(.9,"(justify left)")}) (instances (project {q(PROJECT)} (path {q("/"+rootuuid)} (page {q(str(i+2))})))) )'
s+='(sheet_instances (path "/" (page "1"))))'
(ROOT/(PROJECT+'.kicad_sch')).write_text(s,encoding='utf-8')
(ROOT/(PROJECT+'.kicad_pro')).write_text('{}\n',encoding='utf-8')
(ROOT/'ESC_A1.kicad_sym').write_text('(kicad_symbol_lib (version 20241209) (generator "kicad_symbol_editor")'+''.join(symbol_def(k)[0] for k in definitions)+')',encoding='utf-8')
(ROOT/'sym-lib-table').write_text('(sym_lib_table (lib (name "ESC_A1") (type "KiCad") (uri "${KIPRJMOD}/ESC_A1.kicad_sym") (options "") (descr "A1 functional symbols, pin-number checked")))',encoding='utf-8')
(ROOT/'connection_manifest.json').write_text(json.dumps(parts,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Generated {len(parts)} symbols, {len(expanded)} child sheets.')

