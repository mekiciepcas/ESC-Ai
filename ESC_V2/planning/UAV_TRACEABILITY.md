# UAV ESC tasarım izlenebilirlik matrisi

Tarih: 19.09.2026  
Amaç: Faz 2 / Faz 3 dokümanları ile mevcut B1 tasarımını yeni UAV ürün gereksinimine bağlamak.

Durum etiketleri: **KEEP**, **REVALIDATE**, **RECALCULATE**, **REPLACE IF REQUIRED**, **OPEN**.

| ID | Fonksiyon / karar | Faz 2/3 | B1 | UAV rebaseline kararı | Sonraki kanıt |
|---|---|---|---|---|---|
| TR-001 | 3 faz 2-level VSI | Ana topoloji | Aynı | KEEP + REVALIDATE | G1 envelope, loss/SOA |
| TR-002 | BLDC/PMSM | Evet | Uyumlu aday | KEEP | Motor/eRPM |
| TR-003 | FOC + SVPWM | Hedef | Firmware yok | KEEP target | `CONTROL_PLATFORM_BENCH_CONTRACT.md` + SIL + bench |
| TR-004 | Sensorless | Hedef/opsiyon | Firmware yok | REVALIDATE | startup/observer tests |
| TR-005 | 3 low-side shunt | Seçili | Mevcut | REVALIDATE | phase current + PWM windows |
| TR-006 | DC-bus + U/V/W sensing | Var | Divider + BAT54H rail clamps | Divider concept RECALCULATE; B1 rail-clamp/back-power implementation REPLACE IF REQUIRED. Existing divider ideal FS ~102.5 V, but VBUS-present/control-rails-off can back-power +3V3A/+3V3 through BAT54H and TLV75533 output. LT6015/LT6016/LT6017 provide exact primary-source evidence for a power-off-high-impedance input study path. Output sequencing is explicit: LT6017-on / STM32-VDDA-off is prohibited as a normal study state unless separately proven; preferred study rule is shared analog shutdown domain plus a series path sized from ADC settling/fault-current constraints. | `ADC_CLAMP_INJECTION_CLOSURE.md`, `ANALOG_RAIL_BACKPOWER_AUDIT.md`, `NON_BACKPOWER_HV_SENSE_ARCHITECTURES.md`, `POWER_OFF_TOLERANT_SENSE_CANDIDATES.md`, `HV_SENSE_OUTPUT_SEQUENCING.md`, `hv_sense_dynamic_model.py`, final VBUS/transient + sequencing/bench evidence |
| TR-007 | CAN | Var | SN65HVD230DR / optional 120R / TVS placeholder | KEEP functionally; exact Classic CAN/CAN-FD, temperature, termination, TVS/EMC and harness contract OPEN. B1 exact transceiver remains REVALIDATE. Primary-source CAN-FD/non-isolated and isolated trade anchors now exist, but no winner is selected. | `B1_LEGACY_TRACEABILITY_GAP_AUDIT.md`, `CAN_PHYSICAL_LAYER_PRETRADE.md`, `EXTERNAL_AUX_INTERFACE_CONTRACT.template.json`, FC protocol/failsafe + bus test |
| TR-008 | SPI gate-driver | Var | Var | KEEP if selected architecture still uses serial smart driver; otherwise interface changes with driver topology | final driver/control architecture |
| TR-009 | service/debug | UART/JTAG | SWD/UART | KEEP functionally | MCU pin contract |
| TR-010 | Gate driver | DRV8353 | DRV8353FSRTAR | REVALIDATE; shares unresolved ~100 V-domain ceiling. Primary-source alternatives now exist if G1 disqualifies this domain: UCC27712 non-isolated high-voltage half-bridge anchor and UCC21540-Q1 isolated dual-channel anchor. UCC27282 is only a 120 V bootstrap headline reference because TI still specifies a 100 V HS operating ceiling. No driver selected. | `GATE_DRIVER_AUX_SUPPLY_VOLTAGE_DOMAIN_TRADE.md`, final VBUS transient, MOSFET Qg, PWM/dead-time, fault coverage |
| TR-011 | MCU | TMS320F280041C | STM32G474RET3 | OPEN trade; source-backed pretrade complete and common executable benchmark contract now defined. Existing STM32 reuse and TI motor-control integration are trade factors only, not selection evidence. | `CONTROL_PLATFORM_PRETRADE.md`, `CONTROL_PLATFORM_BENCH_CONTRACT.md`, exact-package timing/trip/FOC benchmark |
| TR-012 | Aux buck | LM5164 | LM5164 | REVALIDATE; legacy input domain couples it to final transient ceiling. B1 load/domain inventory now separates source ratings from actual load demand. Source-backed alternatives exist: LTC3639 and LTC7801 architecture anchors. No auxiliary topology selected. | `B1_AUXILIARY_LOAD_DOMAIN_INVENTORY.md`, `GATE_DRIVER_AUX_SUPPLY_VOLTAGE_DOMAIN_TRADE.md`, final VBUS transient + U1 gate/control/fan/Hall/interface load budget |
| TR-013 | MOSFET | CSD19536KTT single/switch | 2 parallel/switch candidate | RECALCULATE / REPLACE | `POWER_STAGE_LOSS_MODEL.md`, `CSD19536KTT_REFERENCE_PARAMETERS.md`, `SEMICONDUCTOR_VOLTAGE_CLASS_CANDIDATES.md`, `power_stage_loss_calculator.py`, VDS/loss/SOA/thermal/sharing |
| TR-014 | MOSFET voltage class | 100 V | 100 V target | OPEN; primary-source trade anchors now exist for 100/120/150 V and include dynamic/thermal evidence. Class remains blocked by G1 transient/current/PWM/hot-temperature envelope. | `SEMICONDUCTOR_VOLTAGE_CLASS_CANDIDATES.md`, `POWER_STAGE_LOSS_MODEL.md`, `power_stage_loss_calculator.py` + transient ceiling |
| TR-015 | PWM | 40 kHz | 20 kHz | RECALCULATE | motor L + switching loss + `CONTROL_PLATFORM_BENCH_CONTRACT.md` |
| TR-016 | continuous phase current | 60 A RMS | 80 A RMS target | OPEN | motor operating points |
| TR-017 | overload/peak phase current | ~80/~100 A | 120 A SW/150 A sense | OPEN | motor operating points + duration |
| TR-018 | power target | 1.5/3 kW | 3 kW candidate | RECALCULATE; heavy-lift market evidence shows legacy 3 kW cannot be assumed as product rating | `propulsion_benchmark.md`, `esc_envelope_parametric.md` |
| TR-019 | Battery | 12–60 V generic | 13S | OPEN; carry ~50–53 V and 18S/69 V families | `battery_architecture_pretrade.md` |
| TR-020 | Hardware trip | CMPSS/Trip Zone + driver | TLV1704 comparator path + latch + PWM inhibit | KEEP principle + REVALIDATE; B1 audit now separates individual-device delay from required end-to-end asynchronous fault-to-PWM-inactive measurement. | `B1_LEGACY_TRACEABILITY_GAP_AUDIT.md`, `CONTROL_PLATFORM_BENCH_CONTRACT.md`, final latency/threshold/reset budget |
| TR-021 | Motor/FET/PCB temp | desired | exact FET/PCB NTC; motor sensor type unproven | KEEP sensing function; FET/PCB `NTCG203NH103JT1` REVALIDATE; motor sensor electrical model OPEN. | `B1_LEGACY_TRACEABILITY_GAP_AUDIT.md`, `SAFETY_INTERFACE_DERIVED_REQUIREMENTS.json`, motor supplier/sensor evidence + thermal correlation |
| TR-022 | DC-link | open | 3x470uF 100V bulk + 3x2.2uF 100V local, exact cap MPNs open | RECALCULATE / NOT 18S QUALIFIED | `B1_EXACT_VBUS_BOM_AUDIT.md`, ripple/ESR/life/transient |
| TR-023 | Precharge | open | external assembly required, exact design open | OPEN P0 | input-module electrical contract + `precharge_energy_model.py` with evidenced inputs |
| TR-024 | Regen/BMS disconnect | conceptual | external brake interface, clamp sizing open | OPEN P0 | energy acceptance/OV path |
| TR-025 | Parallel FET sharing | not primary | candidate | OPEN | symmetry/thermal/gate loops |
| TR-026 | Control PCB | concept | partial PoC | REUSE selectively | G2/G3 review |
| TR-027 | Power PCB | concept | incomplete | NEW DESIGN after freeze | power/thermal/mechanical review |
| TR-028 | Firmware | goals | no complete tree | NEW IMPLEMENTATION; common candidate workload/measurement contract defined but no buildable U1 firmware or physical benchmark exists yet. | `CONTROL_PLATFORM_BENCH_CONTRACT.md`, build + SIL + bench |
| TR-029 | Production package | intended | incomplete | OPEN | after G5 |
| TR-030 | Physical validation | target | incomplete | REQUIRED | staged G6 |
| TR-031 | G0 trade bounds | none | none | 125/150/175 kg cases allowed only as `ASSUMPTION_FOR_TRADE_ONLY`; never baseline requirements | `G0_TRADE_BOUNDING_CASES.md`, actual G0 vehicle inputs |
| TR-032 | Rotor count | not frozen | not applicable | OPEN; quad conditionally excluded if G0 later requires continued hover after one motor/ESC loss; hex/octo retained | `rotor_trade_study.md`, G0 failure policy + MTOW |
| TR-033 | U1 preliminary BOM evidence map | none | B1 BOM exists | `U1_BOM_CANDIDATES.json` records legacy references, exact source-backed candidates and G1-blocked/open functions without claiming production release. | G1/G2 closure -> U1 schematic -> `hardware_u1/bom_release.json` |
| TR-034 | Auxiliary load budget | not closed | B1 rail tree and partial assumptions exist | OPEN for U1; legacy inventory identifies +12V/+5V/+3V3/+3V3A consumers and explicit unknowns, but converter ratings are not load requirements. | `B1_AUXILIARY_LOAD_DOMAIN_INVENTORY.md`, selected MOSFET Qg/PWM + external fan/Hall/interface contracts + measured/derived MCU/control loads |
| TR-035 | MCU benchmark acceptance | conceptual | no comparable benchmark | DEFINED pre-freeze contract; exact numeric limits remain OPEN until parent G1/G2 requirements freeze. | `CONTROL_PLATFORM_BENCH_CONTRACT.md` CPB-01..12 evidence |
| TR-036 | Fault latch / deliberate arm / PWM inhibit | general safety target | SN74LVC1G74 latch + six SN74LVC1G08 PWM AND gates | KEEP safety principle + REVALIDATE exact implementation; no automatic re-arm assumption; physical end-to-end fault latency required. | `B1_LEGACY_TRACEABILITY_GAP_AUDIT.md`, `SAFETY_INTERFACE_DERIVED_REQUIREMENTS.json`, CPB fault/reset tests |
| TR-037 | External auxiliary/sensor/safety interface contracts | incomplete | fan, Hall, motor temp, E-stop and exported +5V have partial PoC definitions | OPEN; null-only contract template created so voltage/current/inrush/output type/fault behavior/connector values cannot be silently guessed. | `EXTERNAL_AUX_INTERFACE_CONTRACT.template.json`, vehicle/motor/fan/harness decisions |
| TR-038 | Production signal/control connectors | concept | WR-PHD Hall/motor-temp PoC headers + logical 2x20 board interface | REVALIDATE / REPLACE as required; legacy unkeyed headers are reference-only and SAME_NETS does not prove physical mating/orientation. | `B1_LEGACY_TRACEABILITY_GAP_AUDIT.md`, MFG-IF-001 + exact harness/mechanical/environment evidence |
| TR-039 | CAN physical-layer candidate architecture | generic CAN target | SN65HVD230DR Classic CAN | OPEN trade; source-backed non-isolated CAN-FD candidates `TCAN1044A-Q1`, `TCAN1042HGV-Q1`, `TJA1044GT/3` plus isolated `ISO1042-Q1` architecture anchor are documented. Bus-fault vs bus-pin limiting ratings are not treated as equivalent. | `CAN_PHYSICAL_LAYER_PRETRADE.md`, frozen protocol/harness/ENV/grounding requirements + timing/EMC bench evidence |
| TR-040 | Production connector qualification structure | conceptual | PoC headers / logical board interface | DEFINED structure, product values OPEN. Exact connector, mate, contact, keying, retention, derating, vibration, ingress and service evidence required before release. | `PRODUCTION_CONNECTOR_REQUIREMENTS_FRAMEWORK.md`, frozen electrical/ENV/harness requirements |
| TR-041 | Fault tree / FMEA structure | conceptual protection goals | partial B1 hardware fault paths | STRUCTURAL PREWORK ONLY; 12 initial failure modes mapped without severity/occurrence/detection scores, safe-state assumptions or invented timing values. | `FAULT_FMEA_SKELETON.json`, G1/G2 architecture + vehicle safety policy + physical fault evidence |
| TR-042 | U1 KiCad migration policy | intended B2/U1 revision | B1 multi-sheet schematic | PRE-G3 structure defined. No `hardware_u1/` production-intent schematic is created until page-level architecture readiness exists; known B1 risks shall not be silently copied. | `U1_SCHEMATIC_MIGRATION_CONTRACT.md`, G2 freeze -> page-by-page migration -> G3 ERC/BOM review |

## Yeni kaynaklı ön-sonuçlar

- Heavy-lift/agricultural propulsion benchmark evidence remains analysis input only; competitor values are not product requirements.
- `G0_TRADE_BOUNDING_CASES.md` governs 125/150/175 kg numerical cases as `ASSUMPTION_FOR_TRADE_ONLY`; they cannot close G0/G1.
- Rotor screening has an explicit discriminator: if continued hover after complete loss of one motor/ESC becomes a G0 requirement, ordinary quad is eliminated before detailed ESC sizing; otherwise quad remains a candidate.
- 18S full charge is 75.6 V, so a 100 V power-device domain cannot be frozen without a transient/derating proof.
- 100/120/150 V primary-source MOSFET trade anchors and mandatory-input loss tooling exist; no voltage class is selected.
- Gate-driver and auxiliary-power trades contain source-backed higher-voltage alternatives, but final selection remains blocked by G1 transient, current, PWM and auxiliary-load closure.
- `B1_AUXILIARY_LOAD_DOMAIN_INVENTORY.md` traces `VBUS -> 12V -> 5V -> 3V3 -> 3V3A`; regulator headline current ratings are not treated as U1 demand. The three visible passive trip-reference dividers total approximately 0.371 mA at 3.3 V, only a passive subtotal.
- `CONTROL_PLATFORM_PRETRADE.md` and `CONTROL_PLATFORM_BENCH_CONTRACT.md` define a fair STM32G474 vs TMS320F280041C comparison without inventing runtime or fault-latency results.
- `B1_LEGACY_TRACEABILITY_GAP_AUDIT.md` closes the evidence classification for fault latch, PWM inhibit, hardware comparators, CAN, temperature, Hall and board interfaces. The B1 external E-stop contact cannot be credited with cable-break detection, and the legacy Hall/motor-temperature WR-PHD headers are PoC references rather than production UAV connectors.
- `CAN_PHYSICAL_LAYER_PRETRADE.md` adds current primary-source Classic-CAN/CAN-FD physical-layer alternatives, but leaves protocol, bit rate, topology, TVS, termination, isolation and exact MPN selection OPEN.
- `PRODUCTION_CONNECTOR_REQUIREMENTS_FRAMEWORK.md` defines the evidence required for connector + mate + contact + pin-map + derating + mechanical/environmental closure without selecting any connector.
- `FAULT_FMEA_SKELETON.json` provides the first machine-readable failure-mode structure; no RPN/severity/occurrence/detection score or safe-state is invented.
- `U1_SCHEMATIC_MIGRATION_CONTRACT.md` now defines the future KiCad page map and migration rules while explicitly keeping actual `hardware_u1/` creation blocked until architecture readiness.
- `EXTERNAL_AUX_INTERFACE_CONTRACT.template.json` holds fan, Hall, exported +5V, motor-temperature, E-stop/inhibit, CAN and control/power board-interconnect fields with all unknown product values kept null.
- `SAFETY_INTERFACE_DERIVED_REQUIREMENTS.json` adds explicit SAF/IF/SNS/MFG/PWR child requirements for reset-safe PWM, re-arm policy, fault latency measurement, E-stop fault states, CAN physical layer, motor/FET/PCB temperature sensing, Hall electrical contract and production connector qualification.
- `U1_BOM_CANDIDATES.json` tracks exact legacy support parts and source-backed CAN candidates as REVALIDATE/CANDIDATE/LEGACY_REFERENCE only; none is promoted to production selection.
- B1 voltage-sense upper BAT54H can back-power +3V3A/+3V3 in an unpowered-control state, so rail-clamp sensing is not a default KEEP.
- `hv_sense_dynamic_model.py` and other calculators require caller-supplied inputs and label screening results accordingly; open G1 values are not hidden defaults.
- `G1_REQUIREMENTS_MATRIX.json` remains the numerical/selection closure authority for G0/G1A/G1B/G1C/G1 and open rows are not closed with competitor values.

## Korunacak çekirdek

Üç faz VSI, PWM-senkron akım ölçümü, FOC/SVPWM hedefi, CAN işlevi, hızlı donanımsal kapatma, sıcaklık/gerilim telemetrisi, modüler kontrol/güç kartı ve otomatik ERC/netlist/interface kontrolleri korunur.

## Yeniden hesaplanacak çekirdek

UAV-001…006 kapanmadan 13S, 3 kW, 60/80/100/120/150 A, 20/40 kHz, 100 V semiconductor class, FET sayısı, shunt/gain, DC-link, connector/fuse/cable ve thermal budget taşınmaz.

## Çelişki çözme sırası

1. güncel UAV requirement,
2. doğrulanmış motor/prop operating point,
3. electrical/thermal calculation,
4. datasheet/source evidence,
5. prototype measurement.

Eski doküman geçmiş tasarım gerekçesidir; otomatik design authority değildir.
