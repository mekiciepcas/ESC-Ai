# B1 VBUS-exposed component audit for 18S candidate

Date: 2026-09-19
Status: PARTIAL_PRIMARY_SOURCE_AUDIT
Known candidate battery maximum: 18S x 4.2 V = 75.6 V. Transient ceiling remains OPEN.

## Direct findings

| Domain / component | B1 evidence | Verified / known limit | 18S disposition |
|---|---|---|---|
| Gate driver DRV8353FSRTAR VDRAIN domain | B1 driver connected to VBUS through VDRAIN; VM is 12 V | TI: 100 V operating supply domain, 102 V absolute max previously recorded | REVALIDATE / voltage-margin critical |
| LM5164DDAT VIN | B1 auxiliary buck VIN=VBUS | TI LM5164: recommended input range up to 100 V; TI Rev D design example explicitly uses 15–100 V | REVALIDATE / cannot accept an undefined >100 V surge |
| Power MOSFET CSD19536KTT | B1 notes 100 V class, two parallel per switch | 100 V class in B1 | NOT_QUALIFIED for 18S until overshoot ceiling established |
| DC-link local ceramics | B1 contains 2.2 uF 160 V parts in the VBUS/local power-domain design | 160 V nominal value in repository; exact MPN/DC-bias capability still open | voltage rating promising, capacitance-at-bias and ripple still OPEN |
| 100 nF HV ceramics | B1 generation logic distinguishes 160 V parts; exact role/MPN must be checked by ref | nominal value alone is not qualification | OPEN per reference |
| Bus/phase divider resistors | 2 x 49.9 kΩ top leg | total divider arithmetic supports 75.6 V measurement; individual resistor working/pulse voltage not yet source-qualified | REVALIDATE |
| Bulk DC-link capacitors | B1 legacy design sized around 39–54.6 V; exact production MPN/rating not frozen in this audit | legacy voltage domain is insufficient evidence for 18S | REPLACE/RESELECT likely; OPEN until exact BOM audit |

## LM5164 consequence
TI currently specifies LM5164 as a 6–100 V input converter. Because the UAV transient ceiling is not yet known, a 75.6 V battery maximum alone does not qualify it. If the required unclamped/clamped VBUS ceiling can exceed 100 V, LM5164 must either be protected by a proven upstream clamp/filter domain or replaced by an auxiliary architecture with adequate voltage rating and surge evidence.

## Audit rule
No component is marked PASS from a nominal printed voltage alone. PASS requires exact MPN, relevant recommended/absolute ratings, derating/transient policy, and—where applicable—DC-bias/ripple/thermal evidence.

## Open follow-up
1. Extract exact B1 bulk capacitor references/MPNs and voltage ratings.
2. Audit all VBUS-connected protection parts and connector/input module once exact refs are identified.
3. Audit per-resistor working voltage for the bus/phase dividers.
4. Resolve transient ceiling, then convert REVALIDATE items into PASS/REPLACE decisions.
5. If >100 V transient domain is required, trade a higher-voltage auxiliary front end rather than relying on LM5164 absolute behavior.
