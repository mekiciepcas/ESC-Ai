# PB-08 installed-axis primary evidence

Date: 2026-09-20
Scope: S1R.2 Quad/Hexa mass closure support only. This is trade evidence, not a product selection or physical verification.

## Primary-source evidence captured

### Hobbywing X8 G2 integrated propulsion set

Primary manufacturer product page: https://www.hobbywing.com/en/products/xrotor-x8-g2

Current published values relevant to PB-08:
- propulsion-set mass **1095 g**, explicitly stated as including cable and propeller;
- default propeller **MFP 30x11S**;
- default propeller total mass **193 g including propeller adapter**;
- motor **8120-100KV**, 36N40P;
- rated voltage 12S-46 V, operating range 18-63 V;
- rated output power 810 W;
- ESC continuous current 20 A, maximum 80 A for 3 s;
- compatible arm tube D35/D40 mm;
- operating temperature -20 to +50 degC; IPX6.

Separate manufacturer propeller page: https://www.hobbywing.com/en/products/mfp-30x11s

It independently publishes MFP 30x11S total mass 193 g including adapter, single-blade mass 54.5 g, recommended RPM 2100-3500 RPM and maximum RPM 4050 RPM.

### T-Motor U8 Lite candidate

Primary manufacturer store page: https://store.tmotor.com/de/product/u8-lite-u-efficiency-kv190.html

The current page publishes motor-only values for several U8 Lite windings. For the PB-08 candidate region it includes:
- 85 KV, 12S, **243 g motor mass including wire**, recommended propeller 28-29 in, interphase resistance 225 +/- 5 mOhm;
- 100 KV, 12S, **238 g motor mass including wire**, recommended propeller 27-28 in, interphase resistance 170 +/- 5 mOhm.

These are motor-only masses. They are not installed-axis masses and cannot be compared directly with the 1095 g X8 G2 integrated-set mass.

## Architecture-mass implication

`PB08_QUAD_HEXA_MASS_CLOSURE_CONTRACT.md` defines the current 3 kW screen:

`Delta_residual = 2.025 - 2*m_axis - delta_structure - delta_common` kg.

Using the manufacturer-published X8 G2 integrated-set mass only as a boundary check:

- `m_axis = 1.095 kg`
- with the deliberately optimistic mathematical boundary `delta_structure = 0` and `delta_common = 0`,
- `Delta_residual = 2.025 - 2*1.095 = -0.165 kg`.

Therefore a Hexa using two additional complete X8 G2 sets cannot claim a mass-residual advantage over Quad under the current screen even before any extra Hexa arm/frame/common-system mass is added. This does **not** freeze Quad: the custom ESC propulsion axis may have materially different mass, and degraded-mode behavior remains unresolved.

The X8 set is also not electrically identical to the PB-08 custom ESC requirement: its manufacturer page states 20 A continuous ESC current while PB-08 freezes >=30 A continuous hardware capability. The 1095 g value is therefore a benchmark installed-axis mass, not a substitute custom-axis BOM mass.

## Missing evidence required for closure

The following remain OPEN and must not be inferred:
- exact custom motor MPN and exact propeller MPN;
- custom ESC PCB + power stage + enclosure/baseplate mass;
- local custom power/signal cable and connector mass;
- motor/prop mounting hardware mass;
- Quad vs Hexa arm/joint/reinforcement structural mass delta;
- architecture-dependent common-system mass delta;
- degraded/single-motor-failure policy and thrust/control evidence.

For a T-Motor-based custom axis, the 238/243 g motor figures may be used only as one line item after an exact winding is selected. Propeller, adapter, ESC, cooling/enclosure, harness/connector and mounting masses must be added separately from primary-source or measured evidence.

## Decision status

- Hobbywing X8 G2 complete-set benchmark: **SOURCE-BACKED TRADE EVIDENCE**.
- T-Motor U8 Lite motor mass: **SOURCE-BACKED PARTIAL MASS EVIDENCE**.
- PB-08 custom installed-axis mass: **OPEN**.
- Quad/Hexa rotor architecture: **OPEN**.
- No G0/G1 PASS row is claimed by this evidence alone.
