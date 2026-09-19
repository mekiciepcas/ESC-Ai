# B1 bus-sense divider / ADC clamp audit

Date: 2026-09-19
Status: REVALIDATE — no UAV voltage-domain freeze

## Repository configuration
B1 BOM identifies the VBUS upper divider parts as YAGEO `RT0805BRD0749K9L`, 49.9 kOhm, 0.1%, and the clamp diode as Nexperia `BAT54H,115`. The divider used by the current B1 sensing model is two 49.9 kOhm upper resistors in series with 3.32 kOhm bottom resistance.

## Primary-source limits
YAGEO's current RT0805BRD0749K9L specification gives 150 V maximum continuous voltage at full rated power, 300 V maximum over-voltage, 200 V dielectric withstand, and 0.125 W at 70 C for the individual resistor. Nexperia's BAT54H data gives 30 V reverse-voltage rating, 200 mA forward-current rating and <=400 mV forward voltage at 10 mA pulsed; the manufacturer explicitly lists voltage clamping as an application.

Sources:
- https://yageogroup.com/component-documentation/download/specsheet/RT0805BRD0749K9L
- https://assets.nexperia.com/documents/data-sheet/BAT54H.pdf

## Divider stress screening
For the nominal resistor string `49.9k + 49.9k + 3.32k`, each upper resistor sees approximately 49.9/(49.9+49.9+3.32) = 0.4839 of VBUS before any clamp conduction.

At 18S full charge (75.6 V):
- each 49.9 kOhm resistor: ~36.6 V
- string current: ~0.733 mA
- dissipation per 49.9 kOhm: ~26.8 mW

At a hypothetical 120 V sensing-domain ceiling used only for screening:
- each 49.9 kOhm resistor: ~58.1 V
- string current: ~1.164 mA
- dissipation per 49.9 kOhm: ~67.6 mW

At a hypothetical 150 V ceiling:
- each 49.9 kOhm resistor: ~72.6 V
- string current: ~1.454 mA
- dissipation per 49.9 kOhm: ~105.5 mW

Therefore individual RT0805 continuous working voltage is not the first divider limit in these screening cases, but 150 V bus operation would consume most of the 0.125 W/70 C nominal power rating before temperature derating. This is not qualification for 150 V VBUS; PCB creepage, resistor temperature, tolerance/failure modes, ADC range and clamp behavior remain separate constraints.

## BAT54H clamp finding
The BAT54H is suitable in principle as a low-voltage clamp diode, but its 30 V reverse rating means its actual orientation and destination rail are essential. A clamp from ADC node to a ~3.3 V rail does not expose the diode to VBUS because the divider isolates it; however, clamp current can inject into the destination rail during over-range events. That rail must have a defined sink/backfeed path and the MCU absolute-maximum/injection-current limits must be checked from the final MCU datasheet and schematic topology.

The diode itself must not be credited as a VBUS transient suppressor. It protects a low-energy sensing node; it cannot replace the external DC-bus clamp/energy path.

## Required closure tests
1. Verify exact BAT54H orientation and destination rail in the B1 netlist/schematic.
2. Calculate worst-case clamp current using maximum VBUS/transient, resistor tolerances and clamp voltage.
3. Check STM32G474 pin absolute maximum and allowed injection current at powered and unpowered MCU states.
4. Check whether the 3.3 V rail can sink injected current or requires a dedicated clamp/reference solution.
5. Re-run divider power/voltage with the eventual transient ceiling and temperature derating.

## Decision
`RT0805BRD0749K9L` is not presently a blocker for the 75.6 V steady-state 18S candidate. The ADC clamp/backfeed architecture remains OPEN and must close before the bus-sense circuit is UAV-qualified. No 120 V or 150 V sensing range is frozen by this audit.
