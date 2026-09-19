# B1 exact VBUS-exposed BOM audit

Date: 2026-09-19
Status: SOURCE AUDIT / NOT QUALIFICATION

## Repository findings
The current B1 BOM explicitly contains:

| Function | B1 reference/value | Exact MPN | UAV rebaseline status |
|---|---|---|---|
| Bulk DC link | C101-C103, 3 x 470 uF 100 V | OPEN | NOT QUALIFIED |
| Local half-bridge ceramic | C104-C106, 2.2 uF 100 V X7R | OPEN | NOT QUALIFIED |
| Power MOSFET | Q201-404, CSD19536KTT, 2 parallel/switch | CSD19536KTT | REVALIDATE/LIKELY VOLTAGE-LIMITED UNTIL TRANSIENT CLOSED |
| Gate driver HV sense/domain | U501 DRV8353FSRTAR, VDRAIN=VBUS | DRV8353FSRTAR | REVALIDATE; 100 V operating-domain constraint already tracked |
| Charge-pump capacitor | C501, 47 nF 100 V | OPEN | NOT QUALIFIED |
| Auxiliary buck | LM5164DDAT VIN=VBUS | LM5164DDAT | REVALIDATE; 100 V input-domain constraint already tracked |
| Aux buck HV input caps | 2.2 uF 160 V + 100 nF 160 V | exact MPN OPEN | RATING HEADROOM EXISTS ON LABEL ONLY; effective C/MPN OPEN |
| Bus/phase divider | 2 x 49.9 k 0.1% upper legs | RT0805BRD0749K9L | WORKING-VOLTAGE / PULSE / TOLERANCE AUDIT OPEN |
| ADC clamp | BAT54H,115 | BAT54H,115 | INJECTION/BACKFEED AUDIT OPEN |
| External DC input protection | fused/precharged/reverse-polarity-protected assembly | OPEN | SYSTEM BLOCKER |
| Regen clamp/chopper | external brake module interface | OPEN | SYSTEM BLOCKER |

## Critical result
B1 is not an 18S-qualified power stage merely because some local capacitors are marked 160 V. The main energy-storage bank and local inverter ceramics are still nominally 100 V, exact capacitor MPNs are missing, and the MOSFET/driver/auxiliary domains remain tied to the unresolved transient ceiling.

At 18S full charge (75.6 V), a nominal 100 V component has only 24.4 V of static nameplate headroom. This number is not a permitted overshoot budget: capacitor derating/lifetime, semiconductor absolute maximums, switching overshoot, regen, BMS disconnect and tolerances require separate limits.

## Protection topology finding
Repository evidence describes the DC input as coming from an external fused, precharged and reverse-polarity-protected assembly and exposes an external brake-module interface. The B1 board therefore does not currently contain a source-backed, closed TVS/clamp/precharge/fuse solution that can be credited for UAV bus-transient qualification.

## Actions
1. Do not freeze 100 V bulk capacitors for 18S.
2. Select exact bulk/DC-link capacitor candidates only after ripple RMS, effective capacitance, lifetime, temperature and transient voltage are known.
3. Treat C104-C106 100 V X7R as legacy candidate parts; DC-bias effective capacitance and transient rating must be checked.
4. Audit RT0805 upper-divider resistor working voltage/pulse rating against the final divider topology; do not infer suitability from resistance/tolerance alone.
5. Define the external input/protection module electrical contract before G2: fuse, precharge, reverse polarity, disconnect behavior, clamp/regen energy path and harness inductance.
6. Couple semiconductor, DRV8353, LM5164, DC-link and sensing decisions to one common VBUS transient requirement.

## Evidence
- `hardware_b1/bom_review.json`
- `hardware_b1/build_b1.py`
- `hardware_b1/connection_manifest.json`
- existing `B1_VBUS_COMPONENT_AUDIT.md`

No physical measurements or component qualification are claimed here.
