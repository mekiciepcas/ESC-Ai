# B1 support-part evidence audit

Date: 2026-09-19  
Branch: `uav-rebaseline`  
Status: `LEGACY_SUPPORT_PART_REVALIDATION_EVIDENCE_ONLY`

## Scope

This audit closes exact-part/lifecycle/package evidence only for B1 support components whose basic identity can be checked independently of the still-open UAV power envelope. It does **not** select these parts for U1 and does not use regulator headline current as a U1 load requirement.

Repository source: `ESC_V2/hardware_b1/bom_review.json` and the corresponding B1 auxiliary-power sheets.

## 1. TPS62160DGKR — legacy 12 V intermediate rail to 5 V buck

### Repository evidence

B1 BOM records:
- exact MPN: `TPS62160DGKR`
- reference: `U1501`
- B1 footprint: `Package_SO:VSSOP-8_3x3mm_P0.65mm`
- B1 function: downstream conversion from the legacy +12 V intermediate rail toward +5 V.

### Current primary-source anchor

Texas Instruments currently lists exact orderable `TPS62160DGKR` as **ACTIVE** in the **DGK / VSSOP-8** package, operating-temperature range **-40 to +125 °C**. The family input range is **3 V to 17 V**, adjustable output range **0.9 V to 6 V**, with a headline maximum output-current capability of **1 A**.

Primary source:
- https://www.ti.com/product/TPS62160/part-details/TPS62160DGKR
- https://www.ti.com/lit/ds/symlink/tps62160.pdf

### U1 disposition

`REVALIDATE`, not selected.

What is reusable:
- exact MPN exists and remains active;
- B1 package family matches TI's DGK/VSSOP-8 orderable part;
- a 12 V-class intermediate rail is inside the device's published input range.

What remains open:
- whether U1 retains a 12 V -> 5 V cascade at all;
- actual +5 V continuous/peak/inrush load;
- efficiency and junction temperature at the U1 operating point;
- inductor/capacitor network and transient response;
- enable/power-good sequencing;
- powered-off/backfeed behavior of all connected loads;
- final PCB thermal/layout implementation.

**Anti-hallucination rule:** the published 1 A capability is a source rating, not evidence that U1 needs or can continuously draw 1 A.

## 2. TLV75533PDBVR — legacy 5 V to 3.3 V LDO

### Repository evidence

B1 BOM records:
- exact MPN: `TLV75533PDBVR`
- reference: `U1502`
- B1 footprint: `Package_TO_SOT_SMD:SOT-23-5`
- B1 function: +5 V -> +3V3 logic/analog-domain source.

The B1 auxiliary sheet contains a legacy thermal note using a 200 mA example load. That example is not a U1 requirement and is not promoted by this audit.

### Current primary-source anchor

Texas Instruments currently lists exact orderable `TLV75533PDBVR` as **ACTIVE**, **DBV / SOT-23-5**, **-40 to +125 °C**. The TLV755P family is specified for **1.45 V to 5.5 V input** and a headline maximum output current of **500 mA**; this exact suffix is the fixed **3.3 V** version.

Primary sources:
- https://www.ti.com/product/TLV755P/part-details/TLV75533PDBVR
- https://www.ti.com/product/TLV755P

### U1 disposition

`REVALIDATE`, not selected.

What is reusable:
- exact MPN exists and remains active;
- B1 package naming is consistent with TI's DBV/SOT-23-5 orderable part;
- a nominal 5 V source is within the family input range.

What remains open:
- actual +3V3 and +3V3A load split and whether the domains remain coupled this way;
- dropout margin under transient load;
- junction-temperature rise with real PCB copper;
- analog-noise/PSRR requirement;
- enable/startup/reset sequencing;
- reverse-current/backfeed behavior in partial-power states;
- whether a separate analog regulator or different rail architecture is preferred for U1.

**Anti-hallucination rule:** the 500 mA published capability is not used as the U1 3.3 V load budget.

## 3. Package/footprint conclusion

For these two legacy parts, manufacturer package identity is now source-backed:

| Function | Exact MPN | Manufacturer package | B1 footprint mapping | Evidence disposition |
|---|---|---|---|---|
| 12 V -> 5 V buck | `TPS62160DGKR` | DGK, VSSOP-8 | `Package_SO:VSSOP-8_3x3mm_P0.65mm` | package family consistent; land-pattern review still required before U1 release |
| 5 V -> 3.3 V LDO | `TLV75533PDBVR` | DBV, SOT-23-5 | `Package_TO_SOT_SMD:SOT-23-5` | package family consistent; exact land-pattern/thermal review still required before U1 release |

A package-name match is **not** treated as proof that the generic KiCad land pattern is production-qualified against the manufacturer's recommended land pattern. Exact pad dimensions, courtyard, assembly tolerances and thermal copper remain a G3 review item.

## Engineering conclusion

Both B1 support regulators remain legitimate **legacy revalidation candidates**. Neither is promoted to U1 selection. Their exact identity/lifecycle/package evidence is no longer an unknown, while topology, load, thermal, sequencing and partial-power qualification remain intentionally open until the U1 auxiliary-power architecture closes.
