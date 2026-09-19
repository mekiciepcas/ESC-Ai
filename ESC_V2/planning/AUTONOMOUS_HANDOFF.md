# ESC autonomous handoff

Date: 2026-09-19 09:21+03:00  
Branch: `uav-rebaseline`  
Status: `PROGRESS_SENSE_CLAMP_INPUT_CONTRACT_DC_LINK_FRAMEWORK`

## Run summary
This run closed the first-order B1 upper-divider component stress question with primary manufacturer evidence, separated the BAT54H low-energy ADC clamp from the actual DC-bus energy-clamp requirement, defined the missing external DC-input/protection interface contract, and created the DC-link capacitor qualification framework. No voltage class, capacitor MPN, protection topology, rotor architecture, phase-current rating or MTOW was frozen.

## Tasks attempted / completed
1. Verified previous handoff/state against branch source.
2. Confirmed B1 BOM uses YAGEO `RT0805BRD0749K9L` 49.9 kOhm 0.1% upper-divider parts and Nexperia `BAT54H,115` clamp diode.
3. Verified YAGEO primary limits: 150 V max continuous voltage at full rated power, 300 V max over-voltage, 200 V dielectric withstand, 0.125 W at 70 C.
4. Calculated each 49.9 kOhm upper resistor at 75.6 V bus: ~36.6 V and ~26.8 mW; at screening-only 120 V: ~58.1 V/~67.6 mW; at screening-only 150 V: ~72.6 V/~105.5 mW.
5. Verified Nexperia BAT54H primary data: 30 V reverse, 200 mA forward, low-forward-voltage Schottky intended among other uses for voltage clamping.
6. Documented that BAT54H cannot be credited as the DC-bus transient-energy clamp and that ADC clamp-rail injection/backfeed remains to be closed.
7. Added `BUS_SENSE_CLAMP_AUDIT.md`.
8. Added `DC_INPUT_PROTECTION_CONTRACT.md` defining fuse/precharge/disconnect/regen-clamp/harness guarantees without guessing component values.
9. Added `DC_LINK_SELECTION_FRAMEWORK.md` defining effective capacitance, ESR/ripple, lifetime, voltage/transient and validation evidence requirements.
10. Updated machine-readable autonomy state.

## Files changed
- `planning/BUS_SENSE_CLAMP_AUDIT.md` — new
- `planning/DC_INPUT_PROTECTION_CONTRACT.md` — new
- `planning/DC_LINK_SELECTION_FRAMEWORK.md` — new
- `planning/autonomy_state.json` — updated
- `planning/AUTONOMOUS_HANDOFF.md` — updated

## Engineering decisions / findings
- The exact RT0805 upper-divider part is not the first steady-state blocker for the 75.6 V 18S candidate; each upper resistor is far below its 150 V continuous working-voltage rating and below its 0.125 W/70 C nominal power at that point.
- This does not qualify a 120/150 V bus range. At the 150 V screening point each upper is already about 105.5 mW before temperature derating, and the ADC/clamp/range/PCB constraints are independent.
- BAT54H is a sensing-node clamp only. The destination rail's ability to absorb injected current and STM32 powered/unpowered injection limits must close before UAV bus-sense qualification.
- External fuse/precharge/reverse-polarity/disconnect/regen-clamp behavior is now an explicit system contract rather than an implicit B1 assumption.
- DC-link selection must use effective capacitance, ESR/ripple heating, transient energy and manufacturer lifetime evidence; nominal uF/V alone is insufficient.

## Calculations / evidence added
- Divider stress calculation for 75.6/120/150 V screening cases.
- Primary-source YAGEO RT0805BRD0749K9L electrical limits.
- Primary-source Nexperia BAT54H quick-reference limits and clamp application.
- DC-input protection acceptance criteria and DC-link qualification equations/framework.

## Assumptions and evidence level
- 18S full-charge candidate = 75.6 V: prior engineering candidate, not transient ceiling.
- 120 V and 150 V divider calculations: SCREENING CASES ONLY, not selected bus requirements.
- RT0805 and BAT54H limits: PRIMARY MANUFACTURER EVIDENCE.
- Exact clamp injection/backfeed behavior: OPEN pending topology and MCU limit audit.
- No physical measurements performed.

## Unresolved blockers
- G0 mass/mission/environment/failure policy.
- Rotor architecture and final propulsion operating point.
- Phase RMS/peak current and final PWM.
- Harness/PCB inductance and switching/regen/BMS-disconnect transient ceiling.
- Exact DC-link capacitor MPN/effective capacitance/ripple/lifetime.
- Exact input protection/clamp component sizing and BMS behavior.
- ADC clamp destination-rail sink capability and MCU powered/unpowered injection limits.

## Risks / regressions
- A divider that survives steady-state voltage does not imply the sensing chain is safe during over-range or unpowered-MCU events.
- A Schottky clamp can backfeed the 3.3 V rail if the rail cannot sink the injected current.
- 100 V DC-link and semiconductor domains remain unresolved even though the divider resistors themselves have greater individual voltage capability.

## Exact next recommended tasks
1. Verify exact BAT54H orientation/destination rail in B1 source and STM32G474 ADC injection limits from ST primary documentation; calculate worst-case clamp current parametrically.
2. Populate the semiconductor loss framework with legacy CSD19536KTT primary datasheet parameters as reference-only.
3. Extend the input contract with a parametric precharge/disconnect-energy calculator using OPEN inputs rather than guessed values.
4. Continue propulsion evidence to reduce phase-current/PWM uncertainty.

## Dependency chain
`G0 vehicle inputs -> rotor/propulsion point -> battery/DC/phase envelope -> transient ceiling + input protection contract -> semiconductor/driver/aux/DC-link/sensing voltage domains -> loss/thermal closure -> schematic/firmware -> PCB -> bench/propulsion validation`

## Next-run briefing
Start by resolving the low-energy sensing clamp topology and STM32 injection/backfeed limits because the resistor working-voltage question is now screened. Then add primary-source CSD19536KTT reference parameters to the loss model and a parametric precharge/energy tool. Do not interpret the 120/150 V divider screening cases as selected voltage classes. Keep the real DC-bus transient ceiling, protection topology and capacitor/semiconductor MPNs OPEN until propulsion, harness and BMS behavior close.
