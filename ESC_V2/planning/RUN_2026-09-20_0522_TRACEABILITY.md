# Run traceability — PB-08 U8 Lite KV85 operating curve

Date: 2026-09-20 05:22+03:00
Branch: `uav-rebaseline`
Trace ID: TR-062

## Change

Added `PB08_U8LITE_KV85_OPERATING_CURVE_ERPM_EVIDENCE.md` from current T-Motor primary-source data.

## Trace disposition

**TR-062 — TRADE EVIDENCE / NO PRODUCT SELECTION.** T-Motor publishes U8 Lite KV85 as 12S, 36N42P and provides a 48 V G28x9.2 CF bench curve reaching 3200 mechanical RPM, 16.5 A DC input, 792 W input and 6352 g thrust at 100% throttle. With 42 poles = 21 pole pairs, the published maximum point derives to 67,200 eRPM and 1,120 Hz electrical fundamental.

The curve propeller identity is G28x9.2 CF, while prior PB-08 mass evidence used NS28x9.2. These identities are not merged. Therefore TR-062 bounds KV85 controller timing/electrical speed but does not freeze exact motor/propeller MPN, phase current or PWM.

## Requirement impact

- G1 row count unchanged: 15/48 PASS.
- UAV-004 remains IN_PROGRESS.
- UAV-006 remains IN_PROGRESS.
- PWM remains OPEN because exact selected motor/propeller and winding inductance/switching-loss evidence are absent.
- No A2/B1/U1 electrical source changed.

## Source

T-Motor U8 Lite product page, accessed 2026-09-20: https://store.tmotor.com/product/u8-lite-kv85-u-efficiency.html
