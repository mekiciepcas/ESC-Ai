# Battery pack architecture and mass framework — PB-06

Date: 2026-09-19  
Branch: `uav-rebaseline`  
Status: **S1.3 ARCHITECTURE FRAMEWORK / EXACT PACK OPEN**

## Frozen parent requirements

- 18S architecture.
- >=5.0 kWh gross rated pack energy.
- 54.0 V minimum loaded bus for full rated power.
- >=500 A continuous whole-pack capability.
- >=1050 A for >=3 s whole-pack peak capability.
- <=80 V outer normal input ceiling at U1.

## Current candidate cell topologies

| Candidate | Topology | Minimum cell energy | Cell-only max mass | 500 A current/cell | 1050 A current/cell | Status |
|---|---:|---:|---:|---:|---:|---|
| Molicel P45B | 18S18P | 5.022 kWh | 22.68 kg | 27.8 A | 58.3 A | mature alternate / exact qualification open |
| Molicel P50B | 18S16P | 5.040 kWh | 20.45 kg | 31.3 A | 65.6 A | primary qualification candidate |
| Molicel P60B | 18S14P | 5.368 kWh | 18.90 kg | 35.7 A | 75.0 A | mass-optimization candidate |

Cell-only current arithmetic is not pack qualification.

## Pack architecture decision framework

The first prototype pack shall not be frozen merely as a cell count. The selected architecture must explicitly close these layers:

1. **Cell parallel group** — cell orientation, spacing, retention, cell-level fuse strategy if used, current-sharing geometry.
2. **Series group interconnect** — busbar material/cross-section, weld or bonded joint process, Kelvin/sense separation.
3. **Service segmentation** — electrically contiguous 18S pack versus internal 6S/9S service sections. Any removable high-current series connector is treated as a reliability and mass penalty that must be justified.
4. **Main current path** — positive/negative busbars, contactor arrangement, service disconnect, fuse, precharge branch and output connector.
5. **BMS** — 18S cell monitoring, temperature sensing, current sensing, contactor authority, communication and fault logging.
6. **Thermal path** — cell-to-structure heat transfer, forced/passive airflow decision, hottest-cell monitoring and thermal propagation barriers.
7. **Mechanical containment** — compression/retention, vibration restraint, crash/impact considerations, insulation and ingress strategy.
8. **Charging interface** — charge connector, allowed charge current, interlock and turnaround target.

## Preferred architecture direction for prototype study

Use a **single electrical 18S pack with internal service segmentation rather than multiple externally series-connected flight packs** as the default study direction.

Reason:
- the whole-pack current target is 500 A continuous / 1050 A short-duration;
- every external series connector/contact interface would carry the full pack current;
- avoiding unnecessary high-current series connectors reduces contact-resistance, thermal and single-point-failure burden.

This is an architecture direction, not yet a released mechanical design. Exact module count and service-disconnect placement remain OPEN.

## Mass roll-up template

The current operating-empty vehicle budget is <=80 kg and therefore pack overhead cannot be ignored. The final battery mass shall be calculated from:

`battery_mass = cells + cell_holders/retention + busbars/interconnect + weld/bond material + cell_fuses + BMS + current_sensor + contactors + main_fuse + precharge + service_disconnect + output_connectors + HV_cabling + enclosure + insulation + thermal_material + vents/fire_barriers + fasteners + labels/harness`

For every candidate pack, record separately:

| Mass item | P45B 18S18P | P50B 18S16P | P60B 18S14P |
|---|---:|---:|---:|
| cells | 22.68 kg | 20.45 kg | 18.90 kg |
| busbars/interconnect | OPEN | OPEN | OPEN |
| BMS/sensors | OPEN | OPEN | OPEN |
| contactors/fuse/precharge | OPEN | OPEN | OPEN |
| enclosure/retention | OPEN | OPEN | OPEN |
| thermal/fire barriers | OPEN | OPEN | OPEN |
| connectors/HV cable | OPEN | OPEN | OPEN |
| **total pack mass** | **OPEN** | **OPEN** | **OPEN** |

No synthetic overhead percentage is inserted. Exact mass must come from selected hardware/CAD or measured prototype parts.

## Electrical acceptance before exact pack freeze

The exact pack topology shall not be frozen until it can be shown, by calculation plus later test, to satisfy all of the following:

- >=5.0 kWh gross rated energy using controlled cell minimum-energy data;
- >=54.0 V loaded terminal voltage throughout the declared full-rated-power envelope;
- >=500 A continuous without BMS trip or unacceptable thermal/cell-group spread;
- >=1050 A for >=3 s in the declared peak-capable envelope;
- current sharing across parallel cells/groups is bounded;
- contactor/fuse/service disconnect/output connector are rated for the actual duty;
- BMS and precharge logic cannot unintentionally open the pack under expected regen/transient behavior;
- final mass fits the frozen vehicle mass budget after airframe and mission-equipment allocations close.

## Next design actions

1. Build an exact high-current path shortlist for contactor, fuse, current sensor, service disconnect and output connector.
2. Create busbar/weld resistance and thermal budget from actual geometry candidates.
3. Define low-SOC/cold/EOL peak-capable envelope and verify 54 V/500 A plus 1050 A/3 s against it.
4. Add pack mass as a G0 closure item once real hardware/CAD masses exist.

No production pack, transport compliance or flight qualification is claimed by this framework.
