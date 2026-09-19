# B1 ADC clamp / injection closure

Date: 2026-09-19
Status: ANALYSIS — not a production qualification

## Exact B1 topology
Source review of `hardware/build_schematic.py` confirms each BUS/phase voltage channel is:

`source -> 49.9k -> 49.9k -> V_DIV -> 1k -> V_ADC`

with `3.32k` from `V_DIV` to GND, `1 nF` from `V_ADC` to GND, an upper BAT54H with **K=+3V3A, A=V_ADC**, and a lower BAT54H with **K=V_ADC, A=GND**.

Therefore the upper diode conducts from the ADC node into +3V3A when `V_ADC` exceeds the analog rail by approximately one Schottky forward drop. The lower diode conducts for negative ADC-node excursions. The upper diode is explicitly a rail-injection/backfeed path; it is not a DC-bus energy clamp.

## Divider / source impedance
For Rtop = 99.8 kOhm and Rbottom = 3.32 kOhm:

- divider ratio = 3.32k / (99.8k + 3.32k) = 0.0321955
- divider Thevenin resistance = 99.8k || 3.32k = ~3.213 kOhm
- including the 1 kOhm ADC series resistor, approximate clamp-source resistance = ~4.213 kOhm

Unclamped ideal ADC-node values:

| VBUS | VADC ideal |
|---:|---:|
| 75.6 V | 2.434 V |
| 100 V | 3.220 V |
| 120 V screening only | 3.863 V |
| 150 V screening only | 4.829 V |

## Powered-rail screening
Using **3.6 V only as a screening clamp-node assumption** (3.3 V rail + illustrative 0.3 V Schottky drop; not a guaranteed BAT54H VF), conduction would begin near 111.8 V bus. Approximate source-limited injection is then:

- 120 V bus: (3.863 - 3.6) / 4.213k ~= 62 uA
- 150 V bus: (4.829 - 3.6) / 4.213k ~= 292 uA

These are screening values, not qualification limits. BAT54H VF varies with current and temperature, +3V3A is not proven able to sink injected current, and 120/150 V are not selected bus requirements.

## Unpowered-rail hazard
If +3V3A is unpowered, the upper BAT54H can conduct at ordinary 18S voltage. Using 0.3 V only as an illustrative diode-drop assumption:

- 75.6 V bus -> VADC Thevenin ~=2.434 V
- source-limited current into the dead +3V3A rail ~= (2.434 - 0.3)/4.213k ~=0.51 mA

This is sufficient to make **back-power sequencing a real architecture question** even though it is low energy. The actual rail voltage, MCU current paths, regulator reverse-current behavior, and startup state must be measured/analyzed before qualification.

## STM32G474 primary-source constraints
ST's STM32G474 datasheet states that normal-operation current injection caused by external voltages outside the supply range should be avoided. The absolute current table gives injected-current limits dependent on pin type; for FT_xxx/TT_xx/NRST the listed per-pin injected-current rating is -5/0 mA and total injected-current rating is +/-25 mA, with positive injection not possible on the cited FT-class pins when VIN remains below their specified maximum. ST also requires the device power/ground supplies to remain connected in their permitted range.

These absolute/characterization limits are **not design targets** and do not prove the present external BAT54H-to-+3V3A topology safe during MCU-off conditions.

Primary evidence: ST `STM32G474xB/xC/xE` datasheet, current characteristics and I/O current-injection sections.

## Decision
- Keep the existing divider as a B1 reference circuit only.
- Do not credit BAT54H as the DC-bus transient suppressor.
- Do not qualify the sense path for 18S until powered/unpowered sequencing is closed.
- A UAV revision should either prove +3V3A can safely absorb the worst clamp current in every power state or use a sensing/clamp architecture that cannot back-power the MCU/analog rail.

## Closure evidence required
1. Exact STM32 pin assignment and pin-class check for V_BUS_ADC and phase ADC channels.
2. TLV75533 and upstream 5 V rail reverse-current/back-power behavior.
3. Worst-case BAT54H VF/leakage across temperature.
4. Worst-case divider tolerances and selected final bus measurement range.
5. Powered and unpowered bench test with current-limited VBUS source before any high-energy test.
6. Demonstrated rail voltage and current during clamp events.

No physical validation is claimed.