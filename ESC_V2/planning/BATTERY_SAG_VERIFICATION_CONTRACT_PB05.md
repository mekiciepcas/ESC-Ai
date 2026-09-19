# PB-05 battery sag verification contract

Date: 2026-09-19
Branch: `uav-rebaseline`
Status: **S1.3 VERIFICATION CONTRACT / NO PHYSICAL RESULT CLAIMED**

## Purpose

Define the evidence required to prove that a future exact 18S battery implementation can satisfy PB-05's frozen **54.0 V minimum loaded bus for full rated-power operation** and **>=500 A continuous whole-pack capability** without converting room-temperature typical cell impedance into a false qualification claim.

## Frozen parent requirements

- 18S architecture.
- 75.6 V full-charge target; <=80 V outer full-charge system ceiling.
- >=5.0 kWh gross rated pack energy.
- >=54.0 V loaded bus for full rated-power operation.
- >=500 A continuous whole-pack capability at the rated thermal condition.
- Exact cell MPN/topology, hard BMS cutoff, peak current and pack thermal architecture remain OPEN.

## Why a separate contract is required

The PB-05 cell trade uses manufacturer typical DC impedance only as a sensitivity term. That value does not bound low-SOC, cold, aged, cell-spread, interconnect, fuse, contactor, connector or harness contributions. Therefore a pack cannot be accepted from `V = OCV - I*R_typ` alone.

## Required characterization matrix

The exact-pack qualification plan shall record, at minimum, the following independent dimensions. Numeric environmental limits remain OPEN until S1.4 freezes the environment envelope.

| Dimension | Required points | Status |
|---|---|---|
| SOC | high, mid, low usable-SOC boundary | required; exact % OPEN |
| Cell/pack temperature | warm reference, nominal, cold rated boundary | required; exact °C OPEN |
| SOH / aging | beginning-of-life and declared end-of-life condition | required; exact EOL criterion OPEN |
| Pack current | nominal mission load, 500 A continuous requirement point, future peak-current point | 500 A frozen; others as applicable |
| Duration | long enough to establish electrical sag and thermal trend at continuous point | exact duration OPEN pending thermal architecture |
| Sample spread | multiple parallel groups / representative packs or statistically justified equivalent | method OPEN |

## Mandatory measurements

For every acceptance point record:

1. pack terminal voltage immediately before load;
2. loaded pack terminal voltage versus time;
3. pack current versus time;
4. minimum loaded bus voltage;
5. cell-group minimum/maximum voltage and delta;
6. cell/pack temperatures at defined critical locations;
7. voltage drop across pack internal current path where instrumentable: cell-group/interconnect, fuse, contactor, connector and main harness;
8. BMS state, warnings, balancing state and any current/voltage derating request;
9. test fixture/harness resistance or separately measured correction;
10. calibration state and measurement uncertainty.

## Acceptance logic

### BV-01 — full-rated-power voltage floor
At every condition declared inside the future **full-rated-power operating envelope**, measured pack terminal voltage shall remain **>=54.0 V** while supplying the corresponding rated-power current demand. No correction may raise a measured terminal voltage above the actual ESC-side bus voltage.

### BV-02 — continuous-current capability
At every condition declared inside the future **continuous rated thermal envelope**, the exact pack shall sustain **>=500 A continuous** for the duration required by the final thermal/mission definition without BMS trip, contactor/fuse overtemperature, unsafe cell temperature, unacceptable cell-group divergence or voltage falling below the applicable power-policy floor.

Passing a short pulse at 500 A does not satisfy BV-02.

### BV-03 — low-voltage policy correlation
The measured approach to 54.0 V shall be correlated to the future S1.4 derating / mission-termination thresholds. The hard BMS disconnect voltage remains a separate exact-pack safety limit and shall not be equated to the 54.0 V rated-power floor.

### BV-04 — aged/cold margin
Qualification shall demonstrate the 54.0 V floor with the declared cold and end-of-life conditions, or explicitly narrow the full-rated-power envelope so those conditions invoke derating. No room-temperature BOL result may be extrapolated to cold/EOL qualification without validated correlation.

### BV-05 — current sharing
For parallel-cell architectures, evidence shall show that group/cell current sharing and thermal spread remain within the exact cell and interconnect limits. Aggregate current rating obtained by simply multiplying datasheet current by parallel count is not sufficient evidence.

## Machine-readable result fields required later

A future result record should contain at least:

`pack_revision`, `cell_mpn`, `series_count`, `parallel_count`, `gross_energy_wh`, `pack_mass_kg`, `soc_percent`, `soh_percent`, `initial_temperature_c`, `current_profile`, `minimum_terminal_voltage_v`, `minimum_cell_group_voltage_v`, `maximum_cell_group_delta_mv`, `maximum_temperature_c`, `bms_state`, `contactor_temperature_c`, `fuse_temperature_c`, `harness_drop_v`, `measurement_uncertainty`, `pass_fail`, and `evidence_files`.

Unknown values remain null until measured or frozen by the appropriate parent requirement.

## Candidate-specific interpretation

P45B 18S18P, P50B 18S16P and P60B 18S14P remain calculation candidates only. Their manufacturer current headlines and typical impedance data can define test instrumentation range and initial risk ranking, but cannot close BV-01 through BV-05 without exact-pack evidence.

## Exit criterion for S1.3 sag closure

S1.3 sag/minimum-bus work may be considered closed only when either:

- an exact pack implementation passes BV-01..BV-05 over the frozen operating envelope; or
- a validated pack model correlated to physical measurements is accepted and all remaining physical qualification is explicitly transferred to a later gate with no production/flight qualification claim.

Until then the frozen 54.0 V floor is a **design requirement**, not a demonstrated battery capability.
