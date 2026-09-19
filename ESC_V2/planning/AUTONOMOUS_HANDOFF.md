# ESC autonomous handoff

Date: 2026-09-19 08:19+03:00  
Branch: `uav-rebaseline`  
Status: `PROGRESS_EXACT_VBUS_BOM_AND_LOSS_MODEL_FRAMEWORK`

## Run summary
This run completed the exact repository-level B1 VBUS BOM audit and established the parameterized semiconductor loss-model contract. It also updated traceability so DC-link, MOSFET, DRV8353, LM5164 and sensing share one unresolved bus-transient requirement. No voltage class, MPN, phase-current rating, PWM frequency, rotor architecture or MTOW was frozen.

## Tasks attempted / completed
1. Verified previous handoff/state against current branch source.
2. Extracted B1 VBUS-exposed BOM facts from `hardware_b1/bom_review.json` and source.
3. Confirmed main DC-link bank is C101-C103 = 3 x 470 uF 100 V, exact MPN open.
4. Confirmed local half-bridge ceramics C104-C106 = 3 x 2.2 uF 100 V X7R, exact MPN open.
5. Confirmed the 160 V capacitor labels belong to the LM5164 local HV input network, not the main inverter DC-link qualification.
6. Confirmed DC input fuse/precharge/reverse-polarity assembly and regen/brake clamp are external/open interfaces, so B1 cannot claim a closed bus-clamp design.
7. Added `B1_EXACT_VBUS_BOM_AUDIT.md`.
8. Added `POWER_STAGE_LOSS_MODEL.md` with explicit conduction, switching, gate, recovery and thermal evidence requirements for 100/120/150 V trade.
9. Updated `UAV_TRACEABILITY.md` and `autonomy_state.json`.

## Files changed
- `planning/B1_EXACT_VBUS_BOM_AUDIT.md` — new
- `planning/POWER_STAGE_LOSS_MODEL.md` — new
- `planning/UAV_TRACEABILITY.md` — updated
- `planning/autonomy_state.json` — updated
- `planning/AUTONOMOUS_HANDOFF.md` — updated

## Engineering decisions / findings
- B1 is not 18S-qualified by the presence of some 160 V capacitors. Main energy-storage and local inverter ceramics are nominal 100 V candidates with exact capacitor MPNs still open.
- 75.6 V to 100 V leaves 24.4 V nameplate difference, but this is not a permitted overshoot budget and cannot substitute for transient/derating/lifetime analysis.
- The existing B1 board depends on an external protected/precharged DC-input assembly and external brake/clamp interface. These cannot be credited as protection until their electrical contracts and components are defined.
- Semiconductor class comparison now has a common loss-model framework; higher VDS is not automatically accepted because hot RDS(on), Qg/Qgd, switching/recovery loss, thermal path and gate-drive feasibility must close at the same operating point.
- Normal operation will not be allowed to rely on unspecified repetitive avalanche as a substitute for bus transient control.

## Calculations / evidence added
- First-order bridge conduction screening equation and switching/gate-loss equations documented in `POWER_STAGE_LOSS_MODEL.md`.
- Exact B1 source/BOM references documented in `B1_EXACT_VBUS_BOM_AUDIT.md`.
- Traceability TR-006/010/012/013/014/022/023/024 updated to reflect common voltage-domain dependencies.

## Assumptions and evidence level
- 18S full-charge candidate remains 75.6 V from prior rebaseline work; not a transient ceiling.
- B1 component values/references: REPOSITORY_SOURCE evidence.
- Loss equations: ENGINEERING_SCREENING framework, not thermal validation.
- Exact capacitor effective C/ESR/ripple/lifetime: OPEN.
- No physical measurements performed.

## Unresolved blockers
- G0 mass/mission/environment/failure policy.
- Rotor architecture and exact propulsion operating point.
- Phase RMS/peak current and final PWM.
- Harness/PCB inductance and switching/regen/BMS-disconnect transient ceiling.
- Exact DC-link capacitor MPN/effective capacitance/ripple/lifetime.
- External input protection and regen-clamp electrical design.

## Risks / regressions
- A 100 V bulk-capacitor nameplate is now explicitly part of the 18S voltage-margin problem; MOSFET-only voltage upgrades would not solve it.
- An external protection-module placeholder can create false confidence unless its disconnect/clamp behavior is defined together with the ESC.
- Higher-voltage MOSFET selection may increase conduction/switching loss; class cannot be chosen on VDS alone.

## Exact next recommended tasks
1. Audit RT0805 49.9k upper-divider individual working-voltage/pulse limits and BAT54H clamp injection/backfeed path.
2. Define an external DC-input/protection module electrical contract: fuse, precharge, reverse-polarity, contact/disconnect behavior, clamp/regen energy path, harness inductance interface.
3. Create a DC-link ripple/effective-capacitance/lifetime selection framework without choosing an MPN.
4. Populate the loss model with legacy CSD19536KTT parameters as reference-only if primary datasheet evidence is available; do not freeze it.
5. Continue propulsion evidence to reduce phase-current/PWM uncertainty.

## Dependency chain
`G0 vehicle inputs -> rotor/propulsion point -> battery/DC/phase envelope -> transient ceiling + input protection contract -> semiconductor/driver/aux/DC-link/sensing voltage domains -> loss/thermal closure -> schematic/firmware -> PCB -> bench/propulsion validation`

## Next-run briefing
Start with divider working-voltage/clamp injection and the external input-module contract because both are independent of final MTOW and directly close 18S safety ambiguity. Then build the DC-link selection framework. Keep all capacitor MPNs and 100/120/150 V semiconductor classes OPEN until transient and current envelopes exist. Verify any external component limits from primary manufacturer data before changing status.
