# Run traceability — 2026-09-19 18:55+03:00

Scope: continue heavy-lift UAV ESC design without pretending unresolved mechanical inputs are product requirements.

## Added evidence

- `ESC_ELECTRICAL_ENVELOPE_PRETRADE.json` — machine-readable trade-only electrical stress envelope derived from `PROPULSION_SCREENING_PRETRADE.json`.
- `POWER_STAGE_VOLTAGE_CLASS_SCREENING.md` — explicit 100/120/150 V static-headroom screen against the current 81 V commercial benchmark reference.
- `verify_esc_electrical_pretrade.py` — executable source-to-derived-value consistency check.
- `.github/workflows/esc-pretrade-check.yml` — CI execution of the consistency check.
- GitHub Actions run `35453244140` — completed SUCCESS.

## Derived results verified by CI

- Highest observed commercial input-voltage reference: 81 V.
- Highest observed continuous DC-bus current reference in the current benchmark set: 120 A.
- Highest observed peak/short DC-bus current reference: 300 A.
- Highest observed rated input-power reference: 4640 W.
- Static semiconductor-class headroom to 81 V: 100 V -> 19 V, 120 V -> 39 V, 150 V -> 69 V.
- Phase current remains OPEN/null.
- Product baseline remains unfrozen.

## Engineering disposition

- 100 V class is deprioritized as the primary path for the current 80 V-class stress screen, but not globally forbidden if the final battery/transient envelope later proves materially lower.
- 120 V and 150 V classes remain carried-forward candidates for normalized loss/package/gate-drive/transient comparison.
- No MOSFET MPN, parallel-device count, gate driver, current sensor, DC-link capacitance, battery series count, PWM frequency or phase-current requirement was frozen.

## Trace links

- TR-057: propulsion benchmark electrical references -> `ESC_ELECTRICAL_ENVELOPE_PRETRADE.json`.
- TR-058: electrical pretrade -> 100/120/150 V voltage-class screening -> `POWER_STAGE_VOLTAGE_CLASS_SCREENING.md`.
- TR-059: derived pretrade arithmetic/source consistency -> `verify_esc_electrical_pretrade.py` -> Actions run `35453244140` SUCCESS.

Evidence level: calculation/configuration verification only. No bench, thermal, EMC, dyno or flight validation.
