from pathlib import Path
import json

root = Path(__file__).resolve().parent

pb07 = json.loads((root / 'PRODUCT_BASELINE_PB-07.json').read_text(encoding='utf-8'))
register = json.loads((root / 'SCHEMATIC_REVISION_REGISTER.json').read_text(encoding='utf-8'))

# PB-07 remains immutable historical/product-lineage evidence even after PB-08 supersedes it.
assert pb07['revision'] == 'PB-07'
assert pb07['supersedes'] == 'PRODUCT_BASELINE_PB-06.json'
assert pb07['status'] == 'PRODUCT_REBASELINE_DIRECTION_FROZEN_PARTIAL'

power = next(x for x in pb07['new_frozen_decisions'] if x['id'] == 'PB-033')
assert power['min'] == 1500 and power['max'] == 3000

sup = next(x for x in pb07['new_frozen_decisions'] if x['id'] == 'PB-034')
assert sup['value'] == 'SUPERSEDED_AS_ACTIVE_PRODUCT_SCOPE'
assert any('1050 A' in x for x in sup['superseded_items'])
assert any('150 V' in x for x in sup['superseded_items'])

# If a successor exists, verify explicit change-control lineage rather than requiring
# current mission/G1 files to remain frozen at the older PB-07 state.
pb08_path = root / 'PRODUCT_BASELINE_PB-08.json'
if pb08_path.exists():
    pb08 = json.loads(pb08_path.read_text(encoding='utf-8'))
    assert pb08['revision'] == 'PB-08'
    assert pb08['supersedes'] == 'PRODUCT_BASELINE_PB-07.json'
    assert pb08['change_control']['production_release_authorized'] is False

assert register['revision_series']['next_component_bearing_revision'] == 'U1-SCH-R001'
assert register['allocated_revisions'] == []

print('PASS PB-07 historical lineage')
print('aggregate_propulsion_range_w=1500..3000')
print('PB07_successor=' + ('PB-08' if pb08_path.exists() else 'NONE'))
print('U1-SCH-R001=UNALLOCATED')
