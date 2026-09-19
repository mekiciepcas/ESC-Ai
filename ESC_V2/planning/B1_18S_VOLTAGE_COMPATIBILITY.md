# B1 voltage compatibility precheck — 18S candidate

Date: 2026-09-19  
Status: **DESK PRECHECK / NOT DESIGN APPROVAL**

Purpose: identify which legacy B1 voltage assumptions become critical if the UAV architecture moves to an 18S LiPo family. This does not edit or approve historical B1 hardware.

## Candidate bus envelope

18S LiPo at 4.2 V/cell reaches **75.6 V** fully charged. The current heavy-agricultural references reviewed for this project use 18S/69 V nominal systems; Hobbywing X15 G2 specifies a 25–80 V ESC range, and T-Motor A16-18S specifies an 83 V ESC maximum. Those product limits are benchmark evidence, not margins for our design.

## B1 compatibility findings

| B1 item | Existing evidence/value | 18S precheck | Action before reuse |
|---|---|---|---|
| Power MOSFET class | 100 V target | **RED / UNFROZEN** | 75.6 V leaves only 24.4 V static headroom to 100 V. Switching overshoot, wiring inductance, regen and BMS/contact opening can consume this margin. Determine measured/simulated transient ceiling before VDS freeze. |
| DC-link bulk C101–C103 | 470 uF 100 V candidate | **AMBER** | Static 18S full charge is below rating, but surge/ripple/temperature/lifetime derating is not closed. Select actual capacitor series only after ripple and transient model. |
| Local DC-link ceramics C104–C106 | 2.2 uF 100 V candidate | **RED/AMBER** | 100 V MLCC effective capacitance under ~76 V DC bias can collapse strongly depending on case/dielectric/vendor. Actual part and DC-bias curve required. |
| Aux input C1301/C1302 | 160 V candidates | **GREEN for nominal static voltage only** | Voltage rating has comfortable static headroom, but actual MPN/ripple/temperature still open. |
| LM5164 aux buck | B1 candidate | **RED for direct 18S feed** | LM5164 is a 100 V-class buck candidate, but the complete input network, transient ceiling, RON/startup and precharge interaction must be checked. Do not equate IC absolute rating with approved 18S operation. |
| DRV8353 gate driver | B1 candidate | **RED / LIKELY ARCHITECTURE LIMIT** | DRV8353 family is a 102 V-class gate driver candidate, but 18S transient margin and bootstrap/switch-node stress require worst-case validation. A 100 V power stage should not be frozen around it before transient closure. |
| Bus voltage divider | B1 preliminary 99.8k / 3.32k, ADC 3.3 V | **RED** | Ideal divider ratio gives ~2.43 V at 75.6 V and ~2.57 V at 80 V, so nominal ADC range is not the immediate issue; however B1 `bus_check_max_v=80 V` leaves essentially no measurement/diagnostic range above an 80 V benchmark ceiling. Redesign measurement full-scale after transient requirement. |
| Power connectors J101/J102 | MPN/footprint open | **OPEN** | Current, voltage, contact resistance, anti-spark/precharge, vibration and environmental rating must be selected after architecture freeze. |
| Shunts RS201/301/401 | 0.5 mOhm Kelvin, footprint open | **NOT VOLTAGE-LIMITED / CURRENT OPEN** | Recalculate current range, pulse energy, CSA gain and Kelvin layout from selected propulsion point. |
| External brake J103 | connector open | **SYSTEM ARCHITECTURE OPEN** | Decide whether energy is accepted by battery/BMS, clamped, dissipated or switching is inhibited. Heavy UAV may not need active braking in normal flight, but fault/BMS-disconnect energy path must be defined. |

## Static margin observation

A 100 V device at 75.6 V full charge has only **24.4 V absolute static headroom**, i.e. 24.4% of the device rating. This is not a design margin approval. The allowable transient must be derived from semiconductor derating policy, avalanche/repetitive stress strategy, layout parasitics, cable inductance and energy-management behavior.

## Required closure sequence

1. Freeze candidate battery maximum operating voltage and charger/cell tolerance.
2. Define BMS/contact opening and regenerative-energy cases.
3. Estimate cable + DC-link loop inductance and worst credible di/dt.
4. Establish target transient ceiling and derating rule.
5. Select semiconductor voltage class and suppression/clamp strategy.
6. Recalculate bus sensing full scale and capacitor ratings.
7. Only then freeze gate driver, MOSFETs, DC-link parts and connector voltage class.

## Decision

**Legacy B1 is not directly 18S-qualified.** Its control architecture remains reusable evidence, but the 100 V power-domain assumptions must be revalidated as a group. The immediate risk is not 75.6 V steady state itself; it is the unclosed transient/regen/BMS-disconnect envelope around that steady-state voltage.
