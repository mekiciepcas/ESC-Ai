from pathlib import Path
import json, math

ROOT = Path(__file__).resolve().parents[1]
source = json.loads((ROOT / 'planning/PROPULSION_SCREENING_PRETRADE.json').read_text(encoding='utf-8'))
trade = json.loads((ROOT / 'planning/ESC_ELECTRICAL_ENVELOPE_PRETRADE.json').read_text(encoding='utf-8'))

candidates = source['primary_source_candidates']
observed_voltages = []
observed_cont = []
observed_peak = []
observed_power = []
for c in candidates:
    for key in ('max_input_voltage_v',):
        if isinstance(c.get(key), (int, float)):
            observed_voltages.append(float(c[key]))
    if isinstance(c.get('input_voltage_range_v'), list):
        observed_voltages.append(float(max(c['input_voltage_range_v'])))
    if isinstance(c.get('esc_continuous_current_a'), (int, float)):
        observed_cont.append(float(c['esc_continuous_current_a']))
    for key in ('max_input_current_short_a', 'max_allowable_current_a', 'esc_peak_current_a'):
        if isinstance(c.get(key), (int, float)):
            observed_peak.append(float(c[key]))
    for key in ('rated_input_power_w', 'rated_output_power_max_continuous_w'):
        if isinstance(c.get(key), (int, float)):
            observed_power.append(float(c[key]))

env = trade['commercial_reference_envelope']
assert math.isclose(env['highest_observed_input_voltage_v'], max(observed_voltages), abs_tol=1e-9)
assert math.isclose(env['highest_observed_continuous_bus_current_a'], max(observed_cont), abs_tol=1e-9)
assert math.isclose(env['highest_observed_peak_or_short_bus_current_a'], max(observed_peak), abs_tol=1e-9)
assert math.isclose(env['highest_observed_rated_input_power_w'], max(observed_power), abs_tol=1e-9)
assert math.isclose(env['derived_power_over_voltage_current_a'], env['highest_observed_rated_input_power_w']/env['representative_rated_voltage_v'], rel_tol=1e-5)

vref = env['highest_observed_input_voltage_v']
for row in trade['semiconductor_voltage_class_screen']:
    klass = float(row['class_v'])
    expected = klass - vref
    assert math.isclose(row['headroom_to_81v_v'], expected, abs_tol=1e-9)
    assert math.isclose(row['headroom_fraction_of_device_rating_percent'], expected/klass*100.0, rel_tol=1e-9)

rules = trade['current_domain_rules']
assert rules['bus_current_is_not_phase_current'] is True
for key in ('phase_rms_current_a','phase_peak_current_a','switch_rms_current_a','switch_peak_current_a','parallel_devices_per_switch'):
    assert rules[key] is None, key
assert trade['speed_domain_rules']['electrical_rpm'] is None
assert trade['status'] == 'TRADE_STUDY_ONLY_NOT_G1_BASELINE'

print('PASS')
print(f"reference_voltage_v={vref:g}")
print(f"reference_continuous_bus_current_a={env['highest_observed_continuous_bus_current_a']:g}")
print(f"reference_peak_bus_current_a={env['highest_observed_peak_or_short_bus_current_a']:g}")
print(f"reference_power_w={env['highest_observed_rated_input_power_w']:g}")
for row in trade['semiconductor_voltage_class_screen']:
    print(f"class_{row['class_v']}V_headroom={row['headroom_to_81v_v']:g}V")
print('phase_current_frozen=false')
print('product_baseline_frozen=false')
