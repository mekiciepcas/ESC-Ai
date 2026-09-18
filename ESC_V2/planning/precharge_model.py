"""Preliminary RC precharge with an assumed constant current load; not component qualification."""
from pathlib import Path
import json,math
root=Path(__file__).resolve().parent
C=.001410;R=22.0;fraction=.95
def duration(v,load):
    final=v-load*R
    if final<=fraction*v:return None
    return -R*C*math.log(1-fraction*v/final)
rows=[dict(source_v=v,assumed_aux_current_a=i,time_to_95_percent_s=duration(v,i),reachable=duration(v,i) is not None) for v in (39,44,54.6) for i in (0,.05,.1,.2,.5)]
assert abs(duration(54.6,0)-R*C*math.log(20))<1e-12
assert duration(39,.1) is None
assert duration(39,.05)>duration(39,0)
result={'status':'PRELIMINARY_MODEL_NOT_APPROVED_COMPONENT_SELECTION','capacitance_f':C,'candidate_resistance_ohm':R,'target_fraction':fraction,'initial_current_at_54_6_v_a':54.6/R,'initial_resistor_power_w':54.6**2/R,'no_load_full_charge_resistor_energy_j':.5*C*54.6**2,'maximum_constant_load_for_95_percent_at_39_v_a':39*.05/R,'samples':rows,'limitations':['C is provisional; rerun after DC-link BOM sizing','Actual buck load is voltage dependent; constant-current model only brackets scenarios','Resistor pulse curve, retry duty, tolerances and short-circuit timeout not qualified','No contactor, fuse or reverse-polarity component selected','Do not use this model as permission to energize hardware']}
(root/'precharge_checks.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print('3 checks passed; 15 load/voltage scenarios calculated.')
