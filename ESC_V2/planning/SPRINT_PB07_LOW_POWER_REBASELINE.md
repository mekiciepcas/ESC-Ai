# Sprint S1R — PB-07 low-power rebaseline -> G1 SYSTEM FREEZE

Date: 2026-09-19  
Status: **ACTIVE**  
Authority: `PRODUCT_BASELINE_PB-07.json`

## Purpose

The previous S1 execution sprint was built around the PB-02..PB-06 heavy-lift vehicle. PB-07 changes the active product family to **1.5–3.0 kW aggregate propulsion input**, so the old high-current closure path is no longer the correct execution order.

S1R is a rebaseline sprint, not a new major product gate. G1 remains the governing system electrical freeze gate.

## Steps

### S1R.1 — Product power rebaseline
Status: **DONE**

- Freeze 1.5–3.0 kW aggregate propulsion family range.
- Retire incompatible heavy-lift payload/MTOW/X8/18S/high-current sizing from active authority.
- Preserve all PB-06 work as historical evidence.

Evidence: `PRODUCT_BASELINE_PB-07.json`, `LOW_POWER_PROPULSION_REBASELINE_PB07.md`.

### S1R.2 — Rotor architecture + MTOW/payload band
Status: **IN_PROGRESS**

- Compare non-coaxial Quad and Hexa using current 28–30 inch manufacturer curves.
- Close rotor count.
- Close static thrust margin.
- Freeze an MTOW band.
- Build a mass budget and only then freeze payload min/nom/max.

Current leading candidate: Hexa. Quad remains alternate. No selection yet.

### S1R.3 — Battery voltage + mission energy
Status: **READY_AFTER_S1R_2_PARTIAL**

- Compare 12S and 14S.
- Retain >=10 min mission target and 20% gross energy reserve unless a later controlled decision changes them.
- Close nominal/min/full-charge bus, pack current, gross energy and mass target.
- Evaluate P50B 12S3P/12S4P only as calculation candidates until sag/thermal evidence exists.

### S1R.4 — Per-ESC electrical envelope + legacy reuse audit
Status: **BLOCKED_BY_S1R_2_S1R_3**

- Derive per-channel continuous/peak DC power/current from selected rotor count and propulsion curve.
- Derive phase-current measurement envelope from exact motor data or bounded model.
- Re-audit B1/Faz2/Faz3. The earlier ~3 kW / ~48 V / 100 V-device work may now be reusable, but no legacy value becomes product authority automatically.

### S1R.5 — PWM / semiconductor / protection / thermal pre-freeze
Status: **BLOCKED_BY_S1R_4**

- Obtain exact motor Ld/Lq/effective ripple inductance.
- Freeze PWM.
- Re-derive transient voltage ceiling and semiconductor class.
- Close OVP/UVP/OCP/OTP/watchdog/command timeout and baseplate/ambient targets.
- Complete bounded G2 candidate shortlist.

### S1R.6 — G1 closeout
Status: **BLOCKED**

- Every required G1 row numeric/bounded and traceable.
- G0 mission/mass/environment parents closed or explicitly controlled.
- Configuration-control consistency check passes.
- Only then unblock S2/G2 and later U1-SCH-R001 allocation.

## Important reset semantics

A fall in G1 percentage after PB-07 is expected and correct. It means former heavy-lift PASS rows were invalidated by a deliberate product-scope change, not that engineering evidence was lost. Historical PB-01..PB-06 files remain preserved and can still support reuse analysis.

## Dependency chain

`PB-07 -> S1R.2 Quad/Hexa + MTOW/payload -> S1R.3 12S/14S + energy -> S1R.4 per-ESC envelope + B1 reuse -> S1R.5 PWM/protection/thermal -> S1R.6 G1 -> S2/G2 -> U1-SCH-R001`
