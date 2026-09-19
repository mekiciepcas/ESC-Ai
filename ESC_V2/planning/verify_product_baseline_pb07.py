from pathlib import Path
import json
import math

root = Path(__file__).resolve().parent

pb = json.loads((root / 'PRODUCT_BASELINE_PB-07.json').read_text(encoding='utf-8'))
mission = json.loads((root / 'mission_requirements.json').read_text(encoding='utf-8'))
g1 = json.loads((root / 'G1_REQUIREMENTS_MATRIX.json').read_text(encoding='utf-8'))
progress = json.loads((root / 'REQUIREMENTS_PROGRESS.json').read_text(encoding='utf-8'))
backlog = json.loads((root / 'uav_backlog.json').read_text(encoding='utf-8'))
register = json.loads((root / 'SCHEMATIC_REVISION_REGISTER.json').read_text(encoding='utf-8'))

assert pb['revision'] == 'PB-07'
assert pb['supersedes'] == 'PRODUCT_BASELINE_PB-06.json'
assert pb['status'] == 'PRODUCT_REBASELINE_DIRECTION_FROZEN_PARTIAL'

power = next(x for x in pb['new_frozen_decisions'] if x['id'] == 'PB-033')
assert power['min'] == 1500 and power['max'] == 3000

sup = next(x for x in pb['new_frozen_decisions'] if x['id'] == 'PB-034')
assert sup['value'] == 'SUPERSEDED_AS_ACTIVE_PRODUCT_SCOPE'
assert any('1050 A' in x for x in sup['superseded_items'])
assert any('150 V' in x for x in sup['superseded_items'])

req = mission['requirements']
assert req['propulsion']['aggregate_input_power_range_w'] == [1500, 3000]
assert req['payload']['nominal_kg'] is None
assert req['vehicle']['architecture'] is None
assert req['vehicle']['leading_architecture_candidate'] == 'HEXA_NON_COAXIAL'
assert req['battery']['series_count'] is None
assert req['battery']['leading_series_count_candidate'] == 12
assert req['esc']['continuous_input_power_w_min'] is None
assert req['esc']['phase_rms_current_a'] is None
assert req['control_and_interface']['flight_controller_interface'] == 'CAN_FD_CAPABLE_CLASSIC_CAN_COMPATIBLE'

assert g1['product_baseline_authority'] == 'PRODUCT_BASELINE_PB-07.json'
assert g1['summary'] == {'required_rows': 48, 'pass': 6, 'open': 42}
row = {x['id']: x for x in g1['rows']}
assert row['G0-14']['status'] == 'PASS'
assert row['G0-14']['value'].startswith('1.5-3.0 kW')
assert row['G1A-01']['status'] == 'OPEN'
assert row['G1C-01']['status'] == 'OPEN'
assert row['G1-01']['status'] == 'OPEN'
assert row['G1-17']['status'] == 'PASS'
assert row['G1-18']['status'] == 'PASS'

p = progress['g1_system_freeze']
assert p['pass_rows'] == 6 and p['required_rows'] == 48 and p['open_rows'] == 42
assert math.isclose(float(p['percent']), 12.5, abs_tol=1e-9)
assert progress['backlog']['done_tasks'] == 1
assert progress['backlog']['total_tasks'] == 25
assert math.isclose(float(progress['backlog']['done_percent']), 4.0, abs_tol=1e-9)

assert backlog['active_sprint']['id'] == 'S1R'
assert backlog['active_sprint']['current_step'] == 'S1R.2_ROTOR_ARCHITECTURE_MTOW_PAYLOAD'
tasks = {x['id']: x for x in backlog['tasks']}
assert tasks['UAV-002']['status'] == 'IN_PROGRESS'
assert tasks['UAV-003']['status'] == 'DONE'

assert register['revision_series']['next_component_bearing_revision'] == 'U1-SCH-R001'
assert register['allocated_revisions'] == []

print('PASS PB-07 consistency')
print('aggregate_propulsion_range_w=1500..3000')
print('g1=6/48=12.5%')
print('backlog_done=1/25=4.0%')
print('rotor_architecture=OPEN_HEXA_LEADING_QUAD_ALTERNATE')
print('battery_series=OPEN_12S_LEADING_14S_ALTERNATE')
print('U1-SCH-R001=UNALLOCATED')
