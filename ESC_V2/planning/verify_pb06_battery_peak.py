import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8-sig'))

pb = load('PRODUCT_BASELINE_PB-06.json')
mission = load('mission_requirements.json')
g1 = load('G1_REQUIREMENTS_MATRIX.json')
progress = load('REQUIREMENTS_PROGRESS.json')
master = load('REQUIREMENTS_MASTER.json')

assert pb['revision'] == 'PB-06'
assert pb['new_frozen_decisions'][0]['field'] == 'battery_pack_peak_current_a_min'
assert pb['new_frozen_decisions'][0]['value'] == 1050
assert pb['new_frozen_decisions'][0]['duration_s_min'] == 3

bat = mission['requirements']['battery']
assert bat['peak_pack_current_a'] == 1050
assert bat['peak_pack_current_duration_s'] == 3
assert bat['continuous_pack_current_a_min'] == 500
assert bat['minimum_loaded_bus_for_full_rated_power_v'] == 54.0
assert bat['gross_rated_energy_wh_min'] == 5000

row = next(r for r in g1['rows'] if r['id'] == 'G1C-06')
assert row['status'] == 'PASS'
assert '1050 A' in row['value'] and '3 s' in row['value']
assert g1['summary'] == {'required_rows': 47, 'pass': 30, 'open': 17}

assert progress['g1_system_freeze']['pass_rows'] == 30
assert progress['g1_system_freeze']['required_rows'] == 47
assert abs(progress['g1_system_freeze']['percent'] - 63.8) < 1e-9
assert master['child_requirement_authorities']['product_baseline'] == 'PRODUCT_BASELINE_PB-06.json'
assert master['progress']['g1_required_rows'] == 47
assert master['progress']['g1_pass_rows'] == 30

print('PASS')
print('battery_peak_current_a_min=1050')
print('battery_peak_duration_s_min=3')
print('battery_continuous_current_a_min=500')
print('minimum_loaded_bus_v=54.0')
print('g1=30/47=63.8%')
