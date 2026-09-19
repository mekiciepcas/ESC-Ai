from pathlib import Path
import json
import math

root = Path(__file__).resolve().parent
repo_esc = root.parent

pb = json.loads((root / 'PRODUCT_BASELINE_PB-08.json').read_text(encoding='utf-8'))
mission = json.loads((root / 'mission_requirements.json').read_text(encoding='utf-8'))
g1 = json.loads((root / 'G1_REQUIREMENTS_MATRIX.json').read_text(encoding='utf-8'))
progress = json.loads((root / 'REQUIREMENTS_PROGRESS.json').read_text(encoding='utf-8'))
backlog = json.loads((root / 'uav_backlog.json').read_text(encoding='utf-8'))
register = json.loads((root / 'SCHEMATIC_REVISION_REGISTER.json').read_text(encoding='utf-8'))
basis = json.loads((repo_esc / 'design_basis.json').read_text(encoding='utf-8'))

assert pb['revision'] == 'PB-08'
assert pb['supersedes'] == 'PRODUCT_BASELINE_PB-07.json'
assert pb['status'] == 'PARTIAL_PRODUCT_BASELINE_FROZEN'

dec = {x['id']: x for x in pb['new_frozen_decisions']}
assert dec['PB-035']['value'] == 3000
assert dec['PB-036']['value'] == 12
assert math.isclose(dec['PB-037']['value'], 43.2)
assert math.isclose(dec['PB-038']['value'], 50.4)
assert math.isclose(dec['PB-039']['value'], 36.0)
assert dec['PB-040']['value'] == 1000
assert dec['PB-041']['value'] == 1500 and dec['PB-041']['duration_s_min'] == 3
assert dec['PB-042']['value'] == 30
assert dec['PB-043']['value'] == 50 and dec['PB-043']['duration_s_min'] == 3
assert dec['PB-044']['value'] == 100
assert dec['PB-045']['value'] == 75
assert dec['PB-046']['value'] == 750

trade = pb['rotor_architecture_mass_trade']
assert math.isclose(trade['break_even_installed_propulsion_axis_mass_kg'], 1.0125, abs_tol=1e-9)
assert trade['status'] == 'TRADE_ONLY_ROTOR_COUNT_OPEN'

req = mission['requirements']
assert req['propulsion']['aggregate_input_power_range_w'] == [1500, 3000]
assert req['vehicle']['architecture'] is None
assert req['battery']['series_count'] == 12
assert math.isclose(req['battery']['nominal_bus_v'], 43.2)
assert math.isclose(req['battery']['full_charge_bus_v'], 50.4)
assert math.isclose(req['battery']['minimum_loaded_bus_v'], 36.0)
assert req['battery']['three_kw_variant_gross_rated_energy_wh_min'] == 750
assert req['esc']['continuous_input_power_w_min'] == 1000
assert req['esc']['short_duration_input_power_w_min'] == 1500
assert req['esc']['continuous_dc_current_a_min'] == 30
assert req['esc']['peak_dc_current_a_min'] == 50
assert req['esc']['semiconductor_voltage_class_v_min'] == 100
assert req['esc']['repetitive_controlled_terminal_stress_v_max'] == 75
assert req['esc']['phase_rms_current_a'] is None

assert g1['product_baseline_authority'] == 'PRODUCT_BASELINE_PB-08.json'
assert g1['summary'] == {'required_rows': 48, 'pass': 15, 'open': 33}
row = {x['id']: x for x in g1['rows']}
for rid in ['G1C-01','G1C-02','G1C-03','G1C-04','G1C-05','G1-01','G1-02','G1-05','G1-06']:
    assert row[rid]['status'] == 'PASS', rid
assert row['G1A-01']['status'] == 'OPEN'
assert row['G1C-06']['status'] == 'OPEN'
assert row['G1-03']['status'] == 'OPEN'
assert row['G1-07']['status'] == 'OPEN'

p = progress['g1_system_freeze']
assert p['pass_rows'] == 15 and p['required_rows'] == 48 and p['open_rows'] == 33
assert math.isclose(float(p['percent']), 31.3, abs_tol=0.05)
assert progress['backlog']['done_tasks'] == 1
assert progress['backlog']['total_tasks'] == 25
assert math.isclose(float(progress['backlog']['done_percent']), 4.0, abs_tol=1e-9)

assert backlog['active_sprint']['id'] == 'S1R'
assert backlog['active_sprint']['current_step'] == 'S1R.2_ROTOR_ARCHITECTURE_MTOW_PAYLOAD'
tasks = {x['id']: x for x in backlog['tasks']}
assert tasks['UAV-002']['status'] == 'IN_PROGRESS'
assert tasks['UAV-003']['status'] == 'DONE'
assert tasks['UAV-005']['status'] == 'IN_PROGRESS'
assert tasks['UAV-006']['status'] == 'IN_PROGRESS'

assert basis['product_baseline_authority'] == 'planning/PRODUCT_BASELINE_PB-08.json'
sys = basis['system_requirement']
assert sys['battery_series_count'] == 12
assert sys['esc_continuous_power_w'] == 1000
assert sys['esc_peak_power_w'] == 1500
assert sys['esc_continuous_dc_current_a'] == 30
assert sys['esc_peak_dc_current_a'] == 50
assert sys['power_semiconductor_vds_class_min_v'] == 100
assert sys['esc_continuous_phase_current_a'] is None

assert register['revision_series']['next_component_bearing_revision'] == 'U1-SCH-R001'
assert register['allocated_revisions'] == []

print('PASS PB-08 consistency')
print('aggregate_propulsion_range_w=1500..3000')
print('upper_continuous_design_point_w=3000')
print('bus=12S_36.0V_loaded_43.2V_nominal_50.4V_full')
print('esc=1000W_30A_continuous__1500W_50A_3s')
print('semiconductor_class>=100V__repetitive_stress<=75V')
print('g1=15/48=31.3%')
print('backlog_done=1/25=4.0%')
print('rotor_architecture=OPEN')
print('U1-SCH-R001=UNALLOCATED')
