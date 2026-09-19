# RUN 2026-09-19 19:35 +03:00 — Product Baseline PB-01

Branch: `uav-rebaseline`  
Status: `PRODUCTIZATION_FREEZE`  
Authority: `PRODUCT_BASELINE_PB-01.json`

## Why this run exists

The project moved from benchmark/pretrade-only exploration into controlled productization. The user explicitly asked to stop leaving every decision open and to begin making firm, consistent decisions. This run therefore freezes architecture choices that can be defended now while preserving current/power/thermal/mechanical unknowns as OPEN.

## Decisions frozen

1. Payload target remains 70–100 kg payload, not MTOW.
2. Vehicle propulsion architecture is X8 coaxial: 4 arms, 8 independently controlled motor/ESC channels.
3. Complete loss of one motor/ESC requires controlled landing. Continued hover at maximum payload is not required.
4. U1 full-charge DC-bus operating ceiling is bounded at `<=80 V`.
5. Repetitive controlled semiconductor-terminal transient ceiling is `<=120 V`; normal repetitive operation shall not rely on avalanche.
6. U1 power semiconductor voltage class is `>=150 V`; exact MOSFET MPN and parallel count remain OPEN.
7. Gate-drive architecture is three independent high-voltage half-bridge drivers. Legacy `DRV8353FSRTAR` is excluded from the U1 primary baseline; exact high-voltage driver MPN remains OPEN.
8. Flight-controller physical link is CAN-FD capable with Classic CAN compatibility. Bitrate, termination, exact transceiver and upper-layer message map remain OPEN implementation values.
9. Power-up/reset state is DISARMED; valid flight-controller command may request arm; independent hardware inhibit has final authority; latched fault inhibits PWM; automatic re-arm after fault/reset is prohibited.
10. Core power/control topology is frozen as 3-phase BLDC/PMSM + three-phase two-level six-switch VSI + FOC/SVPWM-capable control.

## Why 150 V class was selected over 120 V

The current U1 product baseline now deliberately bounds full-charge bus operation at `<=80 V` and repetitive controlled terminal stress at `<=120 V`. A 120 V MOSFET would have no rating margin at that transient ceiling. A 150 V device class preserves 30 V of rating margin at the frozen transient ceiling and 70 V of static rating margin at the 80 V operating ceiling.

Current source-backed candidate anchors show the efficiency trade is real rather than ignored: Infineon `IPT017N12NM6` is a 120 V / 1.7 mOhm-max class device, while `IAUTN15S6N025` is a 150 V / 2.5 mOhm-max class device. The 150 V class therefore accepts a higher conduction-resistance burden in exchange for voltage robustness. Exact device count, hot loss and cooling must still be optimized after phase/DC current and PWM are frozen.

The voltage-class decision is therefore a product architecture choice, not a claim that the final MOSFET is already selected or thermally verified.

## Gate-driver consequence

TI documents `DRV8353` as a 102 V-max / 100 V-class three-phase smart driver. That domain is not retained as the U1 primary path after the 120 V repetitive terminal-stress requirement and 150 V switch-class freeze. A high-voltage half-bridge-driver architecture is frozen instead. `UCC27712-Q1` is retained only as a source-backed candidate anchor pending gate-charge/current, switch-node negative transient, PWM/dead-time and fault-path analysis.

## G1 closure impact

`G1_REQUIREMENTS_MATRIX.json` advanced from 1 PASS / 46 to 8 PASS / 46:

- `G0-01` payload target bounds
- `G0-13` single propulsion failure policy
- `G1A-01` X8 coaxial vehicle architecture
- `G1A-02` rotor count = 8
- `G1C-04` full-charge bus <=80 V
- `G1C-05` repetitive controlled transient <=120 V
- `G1-17` CAN-FD / Classic CAN-compatible FC interface
- `G1-18` arming/re-arm state policy

This is `17.4%` G1 value closure. G0 and G1 remain OPEN overall because mass, MTOW, mission energy/environment, thrust, motor/propeller, exact battery, current, power, PWM, eRPM and thermal requirements remain unresolved.

## Automated consistency evidence

`verify_product_baseline_pb01.py` cross-checks PB-01 against `mission_requirements.json`, `design_basis.json`, `G1_REQUIREMENTS_MATRIX.json` and `REQUIREMENTS_PROGRESS.json`.

GitHub Actions run `35455224602` completed SUCCESS and printed:

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

This is configuration-consistency evidence only, not physical verification.

## Values intentionally still OPEN

- nominal payload and MTOW
- airframe, battery and mission-equipment mass
- flight duration / reserve
- ambient / altitude / wind / ingress
- coaxial interference factor and exact arm geometry
- hover and peak thrust per rotor
- exact motor/propeller and RPM/eRPM
- exact battery chemistry/series/nominal/minimum voltage
- continuous/peak DC and phase currents
- PWM frequency
- MOSFET exact MPN / parallel count
- exact gate-driver MPN
- current-sense, DC-link, precharge and regen hardware values
- thermal/cooling solution
- connectors/harness
- MCU final production selection

## Next productization step

Run the X8 mass/thrust/energy loop until a coherent nominal MTOW and per-axis operating point exists. Then freeze motor/propeller operating point, exact battery architecture, DC/phase current and power. Those values unlock exact 150 V MOSFET parallel-count, gate-drive current, current-sense, DC-link and thermal design.
