#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
planning = root / 'planning'

def load(name):
    return json.loads((planning / name).read_text(encoding='utf-8-sig'))

pb = load('PRODUCT_BASELINE_PB-02.json')
mission = load('mission_requirements.json')
g1 = load('G1_REQUIREMENTS_MATRIX.json')
progress = load('REQUIREMENTS_PROGRESS.json')
backlog = load('uav_backlog.json')

assert pb['revision'] == 'PB-02'
assert mission['assumption_policy']['product_baseline_authority'] == 'PRODUCT_BASELINE_PB-02.json'
assert g1['product_baseline_authority'] == 'PRODUCT_BASELINE_PB-02.json'

req = mission['requirements']
assert req['payload'] == {'min_kg': 70, 'nominal_kg': 85, 'max_kg': 100, 'status': 'FROZEN_PB-02'}
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
assert req['propulsion']['controller_electrical_rpm_capability_min'] == 60000
assert req['battery']['series_count'] == 18
assert abs(req['battery']['nominal_bus_v'] - 66.6) < 1e-12
assert abs(req['battery']['full_charge_bus_v'] - 75.6) < 1e-12
assert req['esc']['continuous_dc_current_a_min'] == 70
assert req['esc']['peak_dc_current_a_min'] == 200
assert req['esc']['peak_dc_current_duration_s_min'] == 3
assert req['esc']['continuous_input_power_w_min'] == 4800
assert req['esc']['short_duration_input_power_w_min'] == 11500

assert g1['summary'] == {'required_rows':46,'pass':22,'open':24}
assert progress['g1_system_freeze']['pass_rows'] == 22
assert progress['g1_system_freeze']['percent'] == 47.8
assert progress['backlog']['done_tasks'] == 2
assert progress['backlog']['done_percent'] == 8.0

tasks = {t['id']: t for t in backlog['tasks']}
assert tasks['UAV-002']['status'] == 'DONE'
assert tasks['UAV-003']['status'] == 'DONE'
assert sum(t['status'] == 'DONE' for t in tasks.values()) == 2

print('PASS')
print('product_baseline=PB-02')
print('payload_kg=70/85/100')
print('mtow_kg=150/165/180')
print('architecture=X8_COAXIAL_8_CHANNELS')
print('coaxial_sizing_factor=0.85')
print('static_TW_min=1.6')
print('propulsion_class=56x20_45KV_18S')
print('battery=18S_66.6V_nominal_75.6V_full')
print('esc_dc_capability=>=70A_continuous_>=200A_3s')
print('controller_erpm_capability>=60000')
print('g1_pass=22/46')
print('g1_percent=47.8')
print('backlog_done=2/25')
