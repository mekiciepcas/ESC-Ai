#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
planning = root / 'planning'


def load(name):
    return json.loads((planning / name).read_text(encoding='utf-8-sig'))


def exists(name):
    return (planning / name).exists()


pb02 = load('PRODUCT_BASELINE_PB-02.json')
mission = load('mission_requirements.json')
g1 = load('G1_REQUIREMENTS_MATRIX.json')
progress = load('REQUIREMENTS_PROGRESS.json')
backlog = load('uav_backlog.json')

assert pb02['revision'] == 'PB-02'

# Later product baselines are allowed to supersede one another. Verify an explicit,
# unbroken lineage back to PB-02 instead of assuming the current file directly
# supersedes PB-02. Each hop must either inherit its parent wholesale or explicitly
# declare inheritance with controlled supersessions.
current_authority = mission['assumption_policy']['product_baseline_authority']
assert current_authority == g1['product_baseline_authority']
assert exists(current_authority), f'missing current baseline {current_authority}'

lineage = []
name = current_authority
visited = set()
while name != 'PRODUCT_BASELINE_PB-02.json':
    assert name not in visited, f'baseline lineage cycle at {name}'
    visited.add(name)
    doc = load(name)
    lineage.append(doc.get('revision', name))
    parent = doc.get('supersedes')
    assert parent, f'{name} has no supersedes parent'
    assert exists(parent), f'{name} references missing parent {parent}'

    inheritance_flags = [
        v for k, v in doc.items()
        if k.startswith('inherits_all_') and ('decision' in k or 'frozen' in k)
    ]
    assert any(v is True for v in inheritance_flags), (
        f'{name} must explicitly inherit parent frozen decisions; controlled '
        'supersessions may then be listed in that baseline'
    )
    name = parent

assert name == 'PRODUCT_BASELINE_PB-02.json'

req = mission['requirements']
assert req['payload']['min_kg'] == 70
assert req['payload']['nominal_kg'] == 85
assert req['payload']['max_kg'] == 100
assert req['vehicle_operating_empty_mass_budget_kg'] == 80
assert req['gross_takeoff_mass']['min_kg'] == 150
assert req['gross_takeoff_mass']['nominal_kg'] == 165
assert req['gross_takeoff_mass']['max_kg'] == 180
assert req['vehicle']['rotor_count'] == 8
assert abs(req['vehicle']['coaxial_thrust_sizing_factor'] - 0.85) < 1e-12
assert abs(req['vehicle']['normal_static_thrust_to_weight_min'] - 1.6) < 1e-12
assert req['propulsion']['propeller_diameter_in'] == 56
assert req['propulsion']['propeller_pitch_in'] == 20
assert req['propulsion']['motor_kv_rpm_per_v'] == 45
# PB-04 intentionally increased the capability; inheritance means no regression.
assert req['propulsion']['controller_electrical_rpm_capability_min'] >= 60000
assert req['battery']['series_count'] == 18
nominal_bus = req['battery'].get('nominal_bus_v_system_convention', req['battery'].get('nominal_bus_v'))
assert nominal_bus is not None and abs(nominal_bus - 66.6) < 1e-12
assert abs(req['battery']['full_charge_bus_v'] - 75.6) < 1e-12
assert req['esc']['continuous_dc_current_a_min'] == 70
assert req['esc']['peak_dc_current_a_min'] == 200
assert req['esc']['peak_dc_current_duration_s_min'] == 3
assert req['esc']['continuous_input_power_w_min'] == 4800
assert req['esc']['short_duration_input_power_w_min'] == 11500

# Progress may advance beyond PB-02; it must stay internally consistent and can
# never regress below the PB-02 closure of 22/46.
summary = g1['summary']
assert summary['required_rows'] == 46
assert summary['pass'] >= 22
assert summary['open'] == summary['required_rows'] - summary['pass']
assert progress['g1_system_freeze']['required_rows'] == summary['required_rows']
assert progress['g1_system_freeze']['pass_rows'] == summary['pass']
assert progress['g1_system_freeze']['open_rows'] == summary['open']
assert abs(progress['g1_system_freeze']['percent'] - round(100.0 * summary['pass'] / summary['required_rows'], 1)) < 1e-12

# The two PB-02-closed tasks must remain DONE and progress metadata must equal the
# actual current backlog, even when the backlog revision advances.
tasks = {t['id']: t for t in backlog['tasks']}
assert tasks['UAV-002']['status'] == 'DONE'
assert tasks['UAV-003']['status'] == 'DONE'
actual_done = sum(t['status'] == 'DONE' for t in tasks.values())
assert progress['backlog']['done_tasks'] == actual_done
assert progress['backlog']['total_tasks'] == len(tasks)
assert abs(progress['backlog']['done_percent'] - round(100.0 * actual_done / len(tasks), 1)) < 1e-12

print('PASS')
print('pb02_inheritance=preserved_through_controlled_baseline_chain')
print(f'current_product_baseline={current_authority}')
print('lineage=' + ' -> '.join(lineage + ['PB-02']))
print('payload_kg=70/85/100')
print('mtow_kg=150/165/180')
print('architecture=X8_COAXIAL_8_CHANNELS')
print('coaxial_sizing_factor=0.85')
print('static_TW_min=1.6')
print('propulsion_class=56x20_45KV_18S')
print('battery=18S_66.6V_system_convention_75.6V_full')
print('esc_dc_capability=>=70A_continuous_>=200A_3s')
print(f"controller_erpm_capability={req['propulsion']['controller_electrical_rpm_capability_min']}")
print(f"g1_pass={summary['pass']}/{summary['required_rows']}")
print(f"g1_percent={progress['g1_system_freeze']['percent']}")
print(f"backlog_done={actual_done}/{len(tasks)}")
