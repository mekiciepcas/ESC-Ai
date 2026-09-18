from pathlib import Path
import json,shutil
root=Path(__file__).resolve().parents[1];out=root/'planning'
if json.loads((out/'backlog.json').read_text(encoding='utf-8'))['revision']!='PLAN-01':
    raise SystemExit('One-time PLAN-01 migration already applied; update tracked progress directly.')
p=root/'design_basis.json';basis=json.loads(p.read_text(encoding='utf-8'))
archive=out/'design_basis_A2_snapshot.json'
if not archive.exists():shutil.copyfile(p,archive)
basis.update(revision='B1',date='2026-09-14')
basis['operating_envelope']={
 'status':'engineering_target_not_hardware_validated',
 'power_stages_shaft_w':[1500,3000], 'overload_boost_allowed':False,
 'continuous_target_acceptance':{'minimum_test_minutes':60,'final_window_minutes':15,'maximum_abs_temperature_slope_c_per_min':.2,'condition':'both duration and stability required; all component limits apply'},
 'voltage_derating':{'zero_at_or_below_v':39,'full_at_v':44,'command_inhibit_above_v':54.6,'undervoltage_reenable_v':40},
 'baseplate_derating':{'full_at_or_below_c':70,'zero_at_or_above_c':80,'measurement_mapping':'PCB NTC correlation or separate baseplate sensor required'},
 'reference_torque_nm':{'1500W':3.5809862196,'3000W':7.1619724391},
 'maximum_rpm':None,'maximum_rpm_status':'requires motor sample and commutation review before high speed tests',
 'model':'planning/sprint1_envelope.py','decision_record':'planning/SPRINT_01_UYGULAMA.md'}
p.write_text(json.dumps(basis,ensure_ascii=False,indent=2),encoding='utf-8')
p=out/'backlog.json';data=json.loads(p.read_text(encoding='utf-8'));data['revision']='PLAN-02';data['execution_record']='SPRINT_01_UYGULAMA.md'
byid={t['id']:t for t in data['tasks']}
byid['ESC-01'].update(status='DONE',evidence=['SPRINT_01_UYGULAMA.md','envelope_checks.json','../design_basis.json'],completion_scope='Engineering envelope defined; no physical performance approval')
byid['ESC-05'].update(status='IN_PROGRESS',evidence=['SPRINT_01_UYGULAMA.md'],remaining='Symbol-by-symbol geometry/polarity review and standards evidence matrix remain open')
byid['ESC-03'].update(status='READY')
for id,extra in [('ESC-11',' PCB NTC ile taban plakası sıcaklığı korelasyonu hesap/ölçüm planıyla tanımlı veya ayrı sensör seçili.'),('ESC-20',' NTC/taban plakası sıcaklık eşlemesi doğrulanmış; yanlış sensör değeriyle termal izin verilmiyor.')]:
 if extra not in byid[id]['acceptance']:byid[id]['acceptance']+=extra
data['review_decisions']=[dict(id='D-01',finding='F-01',status='CLOSED_DOCUMENTATION',evidence=['../design_basis.json','design_basis_A2_snapshot.json']),dict(id='D-02',finding='F-02',status='OPEN',tasks=['ESC-05']),dict(id='D-03',finding='F-03',status='CLOSED_TOOLING',evidence=['render_roadmap.py']),dict(id='D-04',finding='F-04',status='OPEN',tasks=['ESC-11','ESC-20'])]
p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print('PLAN-02: ESC-01 DONE; ESC-05 IN_PROGRESS; ESC-03 READY. Four review decisions recorded.')
