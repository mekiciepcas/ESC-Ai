from pathlib import Path
import json
import math

root = Path(__file__).resolve().parent
p = root / 'CURRENT_PATH_RESISTANCE_BUDGET_PB06.json'
data = json.loads(p.read_text(encoding='utf-8'))

def close(a, b, rel=2e-3, abs_=1e-6):
    return math.isclose(float(a), float(b), rel_tol=rel, abs_tol=abs_)

assert data['authority'] == 'PRODUCT_BASELINE_PB-06.json'
env = data['controlled_envelope']
assert env['continuous_pack_current_a'] == 500
assert env['peak_pack_current_a'] == 1050
assert env['peak_duration_s'] == 3
assert close(env['normal_hover_reference']['165kg_at_66p6V_a'], 21441 / 66.6)
assert close(env['normal_hover_reference']['180kg_at_66p6V_a'], 24420 / 66.6)

# Verify generic path sensitivity from first principles.
for row in data['total_series_path_sensitivity']:
    r = row['resistance_mohm'] * 1e-3
    assert close(row['drop_v_at_500a'], 500 * r)
    assert close(row['loss_w_at_500a'], 500**2 * r)
    assert close(row['drop_v_at_1050a'], 1050 * r)
    assert close(row['loss_w_at_1050a'], 1050**2 * r)
    assert close(row['pulse_energy_j_at_1050a_3s'], 1050**2 * r * 3)

rho = data['copper_model']['rho_20c_ohm_m']
alpha = data['copper_model']['temperature_coefficient_per_c']
hot = data['copper_model']['hot_sensitivity_c']
mult = 1 + alpha * (hot - 20)
assert close(data['copper_model']['resistance_multiplier_100c_vs_20c'], mult)

# Busbar rows are per 100 mm.
for row in data['busbar_geometry_sensitivity_per_100mm']:
    area = row['area_mm2'] * 1e-6
    r20 = rho * 0.1 / area
    r100 = r20 * mult
    assert close(row['r20_mohm'], r20 * 1e3)
    assert close(row['r100_mohm'], r100 * 1e3)
    assert close(row['loss500_w_20c'], 500**2 * r20)
    assert close(row['loss500_w_100c'], 500**2 * r100)
    assert close(row['loss1050_w_20c'], 1050**2 * r20)
    assert close(row['loss1050_w_100c'], 1050**2 * r100)

# Cable rows are per 1 m.
for row in data['cable_geometry_sensitivity_per_1m']:
    area = row['area_mm2'] * 1e-6
    r20 = rho / area
    r100 = r20 * mult
    assert close(row['r20_mohm'], r20 * 1e3)
    assert close(row['r100_mohm'], r100 * 1e3)
    assert close(row['loss500_w_20c'], 500**2 * r20)
    assert close(row['loss500_w_100c'], 500**2 * r100)
    assert close(row['loss1050_w_20c'], 1050**2 * r20)
    assert close(row['loss1050_w_100c'], 1050**2 * r100)

# Do not permit the budget artifact to silently become a component release.
assert data['total_external_series_resistance_target_mohm'] is None
assert data['total_external_continuous_loss_target_w'] is None
assert data['physical_verification_status'] == 'NOT_PERFORMED'
assert all(x['status'] != 'SELECTED' for x in data['series_element_budget'])

print('PASS')
print('continuous_pack_current_a=500')
print('peak_pack_current_a=1050')
print('peak_duration_s=3')
print('busbar_geometry_rows=', len(data['busbar_geometry_sensitivity_per_100mm']))
print('cable_geometry_rows=', len(data['cable_geometry_sensitivity_per_1m']))
print('exact_component_selection=false')
