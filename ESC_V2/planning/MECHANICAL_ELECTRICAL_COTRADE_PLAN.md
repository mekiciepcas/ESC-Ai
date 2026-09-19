# Mechanical–electrical co-design path

Status: **TRADE STUDY ONLY — not a G0/G1 freeze**

## Why this path exists

The airframe/mechanical design has not been created yet, so empty mass, battery mass, vehicle span, mission duration and environmental limits cannot be supplied as real product values. Those fields remain `OPEN/null` in the G0 closure packet.

Instead of blocking the ESC project completely, we will run a **mechanical–electrical co-design loop**. Market data is used only to define a search space, never as a hidden product requirement.

## Primary-source commercial anchors

DJI AGRAS T70P official specifications list a 70 kg spraying payload, aircraft weight of 52 or 56 kg including battery depending on battery option, maximum takeoff weights up to 130 kg depending on configuration, 62-inch propellers, 65 rpm/V motors and a 52 V nominal flight battery.

Source: https://ag.dji.com/t70p/specs

DJI AGRAS T100 official specifications list a 100 kg spraying payload, 75 kg spraying aircraft weight, 175 kg maximum takeoff weight for spraying, 62-inch propellers, 60 rpm/V motors and a 52 V nominal flight battery.

Source: https://ag.dji.com/t100/specs

These facts show commercially relevant reference points around the user's 70–100 kg payload target. They do **not** freeze our vehicle MTOW, rotor count, battery voltage, motor KV or ESC current.

## Screening cases

For concept sensitivity only, evaluate MTOW cases `130 / 150 / 175 kg` and rotor-count cases `4 / 6 / 8`.

Hover load per rotor before any reserve factor:

| MTOW | 4 rotors | 6 rotors | 8 rotors |
|---:|---:|---:|---:|
| 130 kg | 32.50 kgf / 318.7 N | 21.67 kgf / 212.5 N | 16.25 kgf / 159.4 N |
| 150 kg | 37.50 kgf / 367.7 N | 25.00 kgf / 245.2 N | 18.75 kgf / 183.9 N |
| 175 kg | 43.75 kgf / 429.0 N | 29.17 kgf / 286.0 N | 21.88 kgf / 214.5 N |

No peak-thrust multiplier is frozen yet. Thrust reserve, motor-out policy, coaxial permission and maximum vehicle span remain `OPEN`.

## What we can do now

1. Build rotor-count and propeller-size sensitivity tables.
2. Search motor/prop families capable of the required hover-load regions.
3. From those candidate operating points, derive **trade-only** electrical ranges for per-motor power, battery voltage and ESC current.
4. Compare MOSFET/driver/sensing architectures against the resulting range instead of one guessed point.
5. Feed estimated motor/battery masses back into the vehicle mass model and iterate.
6. Only promote values into G0/G1 after a coherent vehicle concept exists and the values are explicitly accepted/validated.

## Anti-hallucination boundary

- Competitor values stay tagged `BENCHMARK`, not `REQUIREMENT`.
- Screening MTOW/rotor values stay tagged `TRADE_ONLY`.
- `mission_requirements.json` and `G1_REQUIREMENTS_MATRIX.json` remain unchanged until actual design evidence exists.
- No production component is selected solely because it fits a benchmark case.
- No thermal, endurance, EMI or flight result is claimed without physical evidence.

## Immediate next engineering work

Create a parametric propulsion pretrade across the 130/150/175 kg screening cases and 4/6/8 rotor counts. Use primary manufacturer motor/prop data where available. The output must identify feasible operating regions and electrical load ranges, not a final motor winner.
