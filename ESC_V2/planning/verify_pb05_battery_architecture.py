#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent

def load(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8-sig'))

pb = load('PRODUCT_BASELINE_PB-05.json')
mission = load('mission_requirements.json')
g1 = load('G1_REQUIREMENTS_MATRIX.json')
progress = load('REQUIREMENTS_PROGRESS.json')

assert pb['revision'] == 'PB-05'
new = {x['field']: x for x in pb['new_frozen_decisions']}
assert new['battery_gross_rated_energy_wh_min']['value'] == 5000
assert new['battery_minimum_loaded_bus_for_full_rated_power_v']['value'] == 54.0
assert new['battery_pack_continuous_current_a_min']['value'] == 500
assert pb['battery_candidate_disposition']['exact_cell_mpn_frozen'] is False

bat = mission['requirements']['battery']
assert bat['series_count'] == 18
assert bat['full_charge_bus_v'] == 75.6
assert bat['gross_rated_energy_wh_min'] == 5000
assert bat['minimum_loaded_bus_for_full_rated_power_v'] == 54.0
assert bat['continuous_pack_current_a_min'] == 500
assert bat['exact_cell_or_pouch'] is None

# 180 kg reference hover power from PB-04 sizing basis.
max_mtow_hover_w = 24420.0
rated_floor_v = 54.0
raw_pack_a = max_mtow_hover_w / rated_floor_v
margin_pack_a = raw_pack_a * 1.10
assert raw_pack_a < 500
assert margin_pack_a <= 500

rows = {x['id']: x for x in g1['rows']}
assert g1['product_baseline_authority'] == 'PRODUCT_BASELINE_PB-05.json'
assert g1['summary'] == {'required_rows': 46, 'pass': 29, 'open': 17}
assert rows['G1C-02']['status'] == 'PASS'
assert '54.0 V' in rows['G1C-02']['value']

assert progress['g1_system_freeze']['pass_rows'] == 29
assert progress['g1_system_freeze']['required_rows'] == 46
assert progress['g1_system_freeze']['open_rows'] == 17
assert progress['g1_system_freeze']['percent'] == 63.0
assert progress['requirements_structure']['percent'] == 100.0
assert progress['backlog']['done_percent'] == 8.0

print('PASS')
print(f'max_mtow_hover_pack_current_at_54V={raw_pack_a:.1f} A')
print(f'with_10pct_design_allowance={margin_pack_a:.1f} A')
print('gross_rated_pack_energy_min=5000 Wh')
print('exact_cell_mpn_frozen=false')
