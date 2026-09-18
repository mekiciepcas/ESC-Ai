"""Engineering command envelope only; not validated firmware or a safety function."""
from pathlib import Path
import json,math
root=Path(__file__).resolve().parents[1]
def limit(stage_w,voltage,baseplate_c,rpm):
    if stage_w not in (1500,3000):raise ValueError('unreviewed power stage')
    if not all(math.isfinite(x) for x in (voltage,baseplate_c,rpm)):return 0.0
    if voltage<39 or voltage>54.6 or baseplate_c>=80:return 0.0
    voltage_factor=min(1.,max(0.,(voltage-39)/5))
    thermal_factor=min(1.,max(0.,(80-baseplate_c)/10))
    # Same 4000 rpm reference; prevents constant-power demand at arbitrarily low speed.
    torque=stage_w/(4000*2*math.pi/60)
    return min(stage_w*voltage_factor*thermal_factor,
               voltage*90*.88*.97,
               torque*abs(rpm)*2*math.pi/60)
rows=[dict(stage_w=p,voltage_v=v,baseplate_c=t,rpm=n,shaft_command_ceiling_w=round(limit(p,v,t,n),3))
      for p in (1500,3000) for v in (38,39,40,42,44,46.8,54.6,55) for t in (40,70,75,80) for n in (1000,4000)]
checks=[]
def check(name,value):
    assert value,name
    checks.append(name)
check('39V torque release remains zero',limit(3000,39,40,4000)==0)
check('44V full target',limit(3000,44,40,4000)==3000)
check('42V derating',abs(limit(3000,42,40,4000)-1800)<1e-9)
check('75C half power',limit(3000,44,75,4000)==1500)
check('80C inhibit',limit(3000,44,80,4000)==0)
check('1000rpm torque cap',abs(limit(3000,44,40,1000)-750)<1e-9)
check('invalid measurement inhibit',limit(3000,float('nan'),40,4000)==0)
check('all samples within DC power budget',all(r['shaft_command_ceiling_w']<=r['voltage_v']*90*.88*.97+1e-3 for r in rows))
check('sinusoidal RMS target below instantaneous software target',80*math.sqrt(2)<120)
report=dict(status='MODEL_CHECKS_PASS_NOT_PHYSICAL_VALIDATION',checks=checks,samples=rows)
(root/'planning/envelope_checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(len(checks),'model checks;',len(rows),'operating points')
