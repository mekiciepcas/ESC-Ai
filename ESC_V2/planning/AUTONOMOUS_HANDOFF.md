# ESC autonomous handoff

Date: 2026-09-19 19:38+03:00  
Branch: `uav-rebaseline`  
Status: `PROGRESS_PRODUCT_BASELINE_PB01_FROZEN_AND_CI_VERIFIED`

## Progress percentages

- Requirements planned-domain/schema structure: **12/12 = 100%**.
- G1 SYSTEM FREEZE value closure: **8/46 PASS = 17.4%**.
- Backlog tasks explicitly DONE: **1/25 = 4%**.
- Major product gates closed: **0/8 = 0%**.
- U1 KiCad architecture scaffold: **100% structure coverage**.
- U1 component-bearing production-intent schematic: **0%**.

This run materially increased actual product-value closure. It did not claim G0/G1 gate completion or physical verification.

## Run summary

The user explicitly requested productization and firm, consistent decisions. The project therefore created the first controlled partial product baseline: `PRODUCT_BASELINE_PB-01.json`. PB-01 is revision-controlled: changing a frozen decision requires a new PB revision or linked engineering-change record rather than silently editing the value.

The previous autonomous run's normalized 120 V vs 150 V semiconductor pretrade was preserved and used as context rather than overwritten.

## PB-01 frozen decisions

1. **Payload target:** 70–100 kg payload.
2. **Vehicle architecture:** X8 coaxial, four arms, eight independently controlled motor/ESC channels.
3. **Single motor/ESC failure:** controlled landing required; continued hover at maximum payload not required.
4. **Full-charge DC-bus ceiling:** `<=80 V`.
5. **Repetitive controlled bus/switching transient ceiling:** `<=120 V` at the semiconductor terminal stress domain; repetitive normal operation shall not rely on avalanche.
6. **Power semiconductor voltage class:** `>=150 V`; exact MOSFET and parallel count remain open.
7. **Gate-driver architecture:** three independent high-voltage half-bridge drivers. Legacy `DRV8353FSRTAR` is excluded from the U1 primary baseline; exact driver remains open.
8. **Flight-controller link:** CAN-FD capable with Classic CAN compatibility; exact bit rate/message map/transceiver remain implementation decisions.
9. **Arming policy:** power-up/reset DISARMED; valid FC command may request arm; independent hardware inhibit has final authority; latched fault inhibits PWM; no automatic re-arm.
10. **Core topology:** 3-phase BLDC/PMSM + 3-phase two-level six-switch VSI + FOC/SVPWM-capable control.

## Why 150 V class is now frozen

PB-01 deliberately bounds full-charge operation at `<=80 V` and repetitive controlled semiconductor stress at `<=120 V`. A 120 V MOSFET would consume its entire VDS rating at the allowed transient ceiling. The 150 V class preserves 30 V rating margin at the frozen transient limit and 70 V at the 80 V operating ceiling.

Source-backed current-generation anchors show the trade rather than hiding it: the 120 V Infineon `IPT017N12NM6` has lower headline RDS(on) than the 150 V `IAUTN15S6N025`, so the 150 V baseline accepts some conduction-loss burden in exchange for voltage robustness. Exact hot loss, parallel count, switching behavior, SOA and cooling remain open until current/PWM/thermal requirements close.

## G1 requirement rows now PASS

- `G0-01` payload bounds
- `G0-13` single propulsion failure policy
- `G1A-01` X8 coaxial architecture
- `G1A-02` rotor count = 8
- `G1C-04` full-charge bus <=80 V
- `G1C-05` repetitive controlled transient <=120 V
- `G1-17` FC CAN-FD / Classic CAN-compatible interface
- `G1-18` arming and re-arm state policy

G1 value closure is now **8/46 = 17.4%**. G0 and G1 remain OPEN overall because MTOW, mission/energy/environment, thrust, motor/propeller, exact battery, current, power, PWM, eRPM, protection thresholds and thermal values are still unresolved.

## Files changed

- `planning/PRODUCT_BASELINE_PB-01.json` — first revision-controlled partial product baseline.
- `planning/mission_requirements.json` -> `MISSION-01`.
- `design_basis.json` -> `U1-PB01-PARTIAL-BASELINE`.
- `planning/G1_REQUIREMENTS_MATRIX.json` -> `G1-MATRIX-04`.
- `planning/REQUIREMENTS_PROGRESS.json` -> `REQ-PROGRESS-02`.
- `planning/verify_product_baseline_pb01.py` — baseline consistency checker.
- `.github/workflows/product-baseline-pb01.yml` — PB-01 CI enforcement.
- `planning/RUN_2026-09-19_1935_PRODUCT_BASELINE_PB01.md` — additive traceability record.
- `planning/autonomy_state.json` -> `AUTO-STATE-40`.
- `planning/AUTONOMOUS_HANDOFF.md` — this handoff.

No B1/U1 electrical schematic source, PCB, Gerber, production BOM or release package was modified. `U1-SCH-R001` remains unallocated.

## Executed consistency verification

GitHub Actions run `35455224602` completed `SUCCESS`. The checker printed:

```text
PASS
product_baseline=PB-01
vehicle_architecture=X8_COAXIAL_4_ARM_8_INDEPENDENT_PROPULSION_CHANNELS
rotor_count=8
single_failure=CONTROLLED_LANDING_REQUIRED
dc_bus_full_charge_ceiling_v=80
repetitive_transient_ceiling_v=120
power_semiconductor_vds_min_v=150
flight_controller_interface=CAN_FD_CAPABLE_CLASSIC_CAN_COMPATIBLE
g1_pass=8/46
g1_percent=17.4
```

This proves repository consistency only; it is not bench/thermal/EMI/dyno/flight evidence.

## Exact next recommended tasks

1. Build the PB-01 X8 coaxial mass/thrust sensitivity loop, including explicit coaxial interference assumptions and source-backed propulsion-system masses.
2. From that loop choose a coherent **nominal MTOW working baseline** and calculate hover/peak thrust per rotor.
3. Select an exact motor/propeller operating region from manufacturer curves and derive DC power/current and RPM/eRPM.
4. Select exact battery chemistry/series/energy inside the frozen `<=80 V` full-charge boundary.
5. Freeze continuous/peak DC and phase current, power, PWM and eRPM.
6. Then optimize exact 150 V MOSFET MPN/parallel count, gate-driver MPN/current, sensing, DC-link and thermal design.
7. Update the human-readable datasheet to the next revision with all PB-01 frozen values visibly marked.

## Next-run briefing

Start from `PRODUCT_BASELINE_PB-01.json`; do not reopen its frozen decisions without a new PB revision or engineering-change record. Product critical path is now the X8 MTOW -> thrust -> motor/prop -> battery -> current/power chain. Mandatory project metrics are **100% requirements structure / 17.4% G1 value closure / 4% backlog DONE / 0% major gates / 0% component-bearing U1 schematic** until evidence changes them.
