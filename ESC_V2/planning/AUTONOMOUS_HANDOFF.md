# ESC autonomous handoff

Date: 2026-09-19 19:41+03:00  
Branch: `uav-rebaseline`  
Status: `PROGRESS_PRODUCT_BASELINE_PB01_FROZEN_DASHBOARD_G0_ALIGNED`

## Progress percentages

- Requirements planned-domain/schema structure: **12/12 = 100%**.
- G1 SYSTEM FREEZE value closure: **8/46 PASS = 17.4%**.
- Backlog tasks explicitly DONE: **1/25 = 4%**.
- Major product gates closed: **0/8 = 0%**.
- U1 KiCad architecture scaffold: **100% structure coverage**.
- U1 component-bearing production-intent schematic: **0%**.

This run materially increased actual product-value closure. It did not claim G0/G1 gate completion or physical verification.

## Controlled product baseline

`PRODUCT_BASELINE_PB-01.json` is the first controlled partial product baseline. Any change to a frozen PB-01 decision requires a new PB revision or linked engineering change record.

### PB-01 frozen decisions

1. Payload target: **70–100 kg payload**.
2. Vehicle architecture: **X8 coaxial, four arms, eight independently controlled motor/ESC channels**.
3. Single motor/ESC failure: **controlled landing required**; continued hover at maximum payload is not required.
4. Full-charge DC-bus ceiling: **<=80 V**.
5. Repetitive controlled bus/switching transient ceiling: **<=120 V** at the semiconductor terminal stress domain; repetitive normal operation shall not rely on avalanche.
6. Power semiconductor voltage class: **>=150 V**; exact MOSFET and parallel count remain open.
7. Gate-driver architecture: **three independent high-voltage half-bridge drivers**. Legacy `DRV8353FSRTAR` is excluded from the U1 primary baseline; exact driver remains open.
8. Flight-controller link: **CAN-FD capable with Classic CAN compatibility**; exact bit rate/message map/transceiver remain implementation decisions.
9. Arming policy: power-up/reset DISARMED; valid FC command may request arm; independent hardware inhibit has final authority; latched fault inhibits PWM; no automatic re-arm.
10. Core topology: **3-phase BLDC/PMSM + 3-phase two-level six-switch VSI + FOC/SVPWM-capable control**.

## G1 closure impact

The following eight rows are PASS:

- `G0-01` payload bounds
- `G0-13` single propulsion failure policy
- `G1A-01` X8 coaxial architecture
- `G1A-02` rotor count = 8
- `G1C-04` full-charge bus <=80 V
- `G1C-05` repetitive controlled transient <=120 V
- `G1-17` FC CAN-FD / Classic CAN-compatible interface
- `G1-18` arming and re-arm state policy

G1 value closure is **8/46 = 17.4%**. G0 and G1 remain OPEN because MTOW, mission/energy/environment, thrust, exact motor/propeller, exact battery, current, power, PWM, eRPM, protection thresholds and thermal values remain unresolved.

## Consistency and dashboard evidence

`verify_product_baseline_pb01.py` plus `.github/workflows/product-baseline-pb01.yml` enforce PB-01 consistency across mission requirements, design basis, G1 matrix and progress records.

GitHub Actions run `35455224602` completed SUCCESS with the expected PB-01 outputs including X8, rotor count 8, controlled landing, <=80 V bus, <=120 V repetitive transient, >=150 V semiconductor class, CAN-FD compatibility and G1 8/46 = 17.4%.

A dashboard refresh regression was detected after the baseline update: the static validator failed because `schematic_revision_control_policy_percent` had been omitted from the new autonomy state. The engineering data were correct; the dashboard-state contract was incomplete. `AUTO-STATE-41` restored the missing contract fields. Dashboard run `35455376900` then completed SUCCESS with build and static validation PASS.

After `G0_INPUT_CLOSURE_PACKET.json` was revised to `G0-CLOSURE-02`, the dashboard refreshed again. Current dashboard snapshot shows:

- requirements structure: **100%**
- G1 value closure: **17.4%**
- backlog DONE: **4%**
- schematic revision-control policy: **100%**
- remaining G0 input fields: **12**
- next schematic revision: `U1-SCH-R001`

## G0 alignment

`G0_INPUT_CLOSURE_PACKET.json` now marks two former user-input fields as closed by PB-01:

- single motor/ESC failure policy = `controlled_landing`
- coaxial allowed = `true`

`G0_USER_INPUT_FORM.md` was updated accordingly and now requests only the **12 remaining** real product inputs. It no longer asks the user to re-decide PB-01-frozen architecture/failure values.

## Files materially changed in this productization step

- `planning/PRODUCT_BASELINE_PB-01.json`
- `planning/mission_requirements.json` -> `MISSION-01`
- `design_basis.json` -> `U1-PB01-PARTIAL-BASELINE`
- `planning/G1_REQUIREMENTS_MATRIX.json` -> `G1-MATRIX-04`
- `planning/REQUIREMENTS_PROGRESS.json` -> `REQ-PROGRESS-02`
- `planning/verify_product_baseline_pb01.py`
- `.github/workflows/product-baseline-pb01.yml`
- `planning/RUN_2026-09-19_1935_PRODUCT_BASELINE_PB01.md`
- `planning/autonomy_state.json` -> `AUTO-STATE-41`
- `planning/G0_INPUT_CLOSURE_PACKET.json` -> `G0-CLOSURE-02`
- `planning/G0_USER_INPUT_FORM.md`
- dashboard generated snapshot/index/validation through CI
- `planning/AUTONOMOUS_HANDOFF.md` — this handoff

No B1/U1 electrical schematic source, PCB, Gerber, production BOM or release package was modified. `U1-SCH-R001` remains unallocated.

## Exact next recommended tasks

1. Build the PB-01 X8 coaxial **mass/thrust sensitivity loop**, including explicit coaxial interference assumptions and source-backed propulsion-system masses.
2. From that loop choose a coherent **nominal MTOW working baseline** and calculate hover/peak thrust per rotor.
3. Select an exact motor/propeller operating region from manufacturer curves and derive DC power/current and RPM/eRPM.
4. Select exact battery chemistry/series/energy inside the frozen `<=80 V` full-charge boundary.
5. Freeze continuous/peak DC and phase current, power, PWM and eRPM.
6. Optimize exact 150 V MOSFET MPN/parallel count, gate-driver MPN/current, sensing, DC-link and thermal design.
7. Create the next datasheet revision with all PB-01 frozen values visibly marked.

## Next-run briefing

Start from `PRODUCT_BASELINE_PB-01.json`; do not reopen its frozen decisions without a new PB revision or engineering-change record. Product critical path is now `X8 mass loop -> MTOW -> thrust -> motor/prop -> battery -> current/power -> exact power-stage parts`. Mandatory project metrics are **100% requirements structure / 17.4% G1 value closure / 4% backlog DONE / 0% major gates / 0% component-bearing U1 schematic** until evidence changes them.
