# PB-06 whole-pack current-path resistance / thermal budget

Date: 2026-09-19  
Branch: `uav-rebaseline`  
Status: **ENGINEERING BUDGET SCREEN / NO COMPONENT RELEASE**  
Authority: `PRODUCT_BASELINE_PB-06.json`

## Purpose

The PB-06 battery system now has three distinct current regions that must not be confused:

- nominal 165 kg hover reference: about **322 A** on the 66.6 V system convention;
- maximum 180 kg hover reference: about **367 A** on the 66.6 V system convention;
- frozen pack capability: **>=500 A continuous**;
- short-duration vehicle stress capability: **>=1050 A for >=3 s**.

The 1050 A point is not normal hover. It is the short-duration PB-06 stress requirement derived from the frozen 1.6 T/W vehicle point. This artifact converts those currents into a resistance and heat budget before exact busbar, fuse, contactor, service disconnect, connector or cable geometry is selected.

## Why milli-ohms matter

For any series path element:

`P = I^2 R`  
`Vdrop = I R`

| Total series resistance | Loss @ 500 A | Drop @ 500 A | Loss @ 1050 A | Drop @ 1050 A | 3 s peak heat |
|---:|---:|---:|---:|---:|---:|
| 0.1 mOhm | 25 W | 0.05 V | 110.25 W | 0.105 V | 331 J |
| 0.2 mOhm | 50 W | 0.10 V | 220.5 W | 0.210 V | 662 J |
| 0.3 mOhm | 75 W | 0.15 V | 330.75 W | 0.315 V | 992 J |
| 0.5 mOhm | 125 W | 0.25 V | 551.25 W | 0.525 V | 1.65 kJ |
| 1.0 mOhm | 250 W | 0.50 V | 1.10 kW | 1.05 V | 3.31 kJ |

Therefore an exact pack design cannot treat the fuse, contactor, service disconnect, connector, busbar and cable as independent components. Their resistances add directly and become a thermal-system requirement.

No total-resistance limit is frozen yet because the allowable heat rejection and component temperature limits belong to S1.4/S1.5.

## Copper busbar geometry sensitivity

First-order copper model:

- resistivity at 20 C: `1.724e-8 ohm*m`;
- temperature coefficient: `0.00393 /C`;
- 100 C sensitivity multiplier relative to 20 C: `1.3144`.

The following values are **per 100 mm of uniform copper bar**. They exclude joints, plating interfaces, bolts, welds and terminal constriction resistance.

| Cu bar | R @20 C | R @100 C | 500 A loss @100 C | 1050 A loss @100 C |
|---|---:|---:|---:|---:|
| 30x5 mm | 0.01149 mOhm | 0.01511 mOhm | 3.78 W | 16.66 W |
| 40x5 mm | 0.00862 mOhm | 0.01133 mOhm | 2.83 W | 12.49 W |
| 50x5 mm | 0.00690 mOhm | 0.00906 mOhm | 2.27 W | 9.99 W |
| 60x5 mm | 0.00575 mOhm | 0.00755 mOhm | 1.89 W | 8.33 W |
| 40x10 mm | 0.00431 mOhm | 0.00567 mOhm | 1.42 W | 6.25 W |

These numbers show that a reasonably large copper bar itself can be low-loss over short distances; the more dangerous contributors may become joints, contactors, fuse elements and connectors. This does **not** prove any bar cross-section is thermally or mechanically adequate.

## Cable resistance sensitivity

The following is ideal copper conductor resistance **per 1 m** before terminal/contact losses. Ampacity is not claimed because insulation class, bundling, airflow, ambient temperature and installation rules remain OPEN.

| Cu conductor area | R @20 C | R @100 C | 500 A loss @100 C | 1050 A loss @100 C |
|---:|---:|---:|---:|---:|
| 70 mm2 | 0.2463 mOhm | 0.3237 mOhm | 80.9 W | 356.9 W |
| 95 mm2 | 0.1815 mOhm | 0.2385 mOhm | 59.6 W | 263.0 W |
| 120 mm2 | 0.1437 mOhm | 0.1888 mOhm | 47.2 W | 208.2 W |
| 150 mm2 | 0.1149 mOhm | 0.1511 mOhm | 37.8 W | 166.6 W |
| 185 mm2 | 0.0932 mOhm | 0.1225 mOhm | 30.6 W | 135.0 W |
| 240 mm2 | 0.0718 mOhm | 0.0944 mOhm | 23.6 W | 104.1 W |

This strongly favors short pack-to-distribution distances. Long flexible high-current harnesses quickly consume the resistance and thermal budget.

## Element-by-element budget state

| ID | Series element | Current design state | Resistance authority |
|---|---|---|---|
| CP-01 | cell parallel collectors / series group interconnects | OPEN | exact P-count, weld/tab/busbar geometry required |
| CP-02 | main fuse | OPEN | fault-current + time-current/I2t coordination required |
| CP-03 | main contactor | TE EV200 candidate only | TE publishes typical 0.2 mOhm contact resistance at 200 A; not a guaranteed hot value |
| CP-04 | service disconnect | OPEN | exact load-break/isolation role required |
| CP-05 | pack current sensor | LEM HAX 1000-S / LTC 1000-T candidates | Hall architecture can avoid an intentional series shunt; conductor resistance still remains |
| CP-06 | internal busbar | OPEN | geometry/layout required |
| CP-07 | output connector | SurLok Plus candidate at the published 500 A family boundary | exact configuration/contact resistance/1050 A pulse evidence required |
| CP-08 | external cable + terminations | OPEN | length, area, insulation, ambient and terminal geometry required |

## Contactor observation

The TE EV200 screening anchor is important because its published **typical 0.2 mOhm** contact resistance would arithmetically correspond to:

- 50 W at 500 A;
- 220.5 W while 1050 A flows.

That does not reject EV200 by itself, because the value is typical, is specified at a stated condition, and the 1050 A event is only 3 s. But it means contactor terminal temperature, hot resistance, conductor size and pulse carry evidence must be treated as first-class selection criteria. We will not freeze EV200 from headline current rating alone.

## Design direction created by this budget

1. Keep the high-current path physically short.
2. Prefer busbar-based internal distribution over long flexible conductors where packaging permits.
3. Avoid adding a high-current series shunt for whole-pack current measurement unless later accuracy requirements force it; Hall candidates remain preferable at this stage because they do not intentionally add a shunt resistance.
4. Treat every bolted/welded/mated interface as its own resistance/temperature item.
5. Do not select the fuse before prospective pack fault current and I2t coordination are defined.
6. Do not claim a 500 A continuous component automatically survives or interrupts 1050 A / 3 s.

These are engineering directions, not released hardware selections.

## Next closure evidence

The next S1.3 work package should supply:

- exact candidate pack topology and parallel count;
- first mechanical pack layout with approximate positive/negative current-path lengths;
- weld/joint/collector architecture;
- credible pack prospective short-circuit calculation or manufacturer-supported bound;
- fuse time-current and interrupt coordination inputs;
- contactor/connector 1050 A / 3 s pulse evidence;
- pack current-path thermal test plan;
- complete path resistance sum at cold/nominal/hot conditions;
- pack mass roll-up including current-path hardware.

## Configuration-control result

No G1 row is closed by this resistance study alone. No exact cell, busbar, fuse, contactor, connector, cable or service-disconnect part is frozen. No schematic revision is allocated. Physical verification remains **NOT PERFORMED**.
