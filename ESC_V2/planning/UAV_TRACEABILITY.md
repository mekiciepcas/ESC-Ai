# UAV ESC tasarım izlenebilirlik matrisi

Tarih: 19.09.2026  
Amaç: Faz 2 / Faz 3 dokümanları ile mevcut B1 tasarımını yeni UAV ürün gereksinimine bağlamak.

Durum etiketleri: **KEEP**, **REVALIDATE**, **RECALCULATE**, **REPLACE IF REQUIRED**, **OPEN**, **FROZEN**.

| ID | Fonksiyon / karar | Faz 2/3 | B1 | UAV rebaseline kararı | Sonraki kanıt |
|---|---|---|---|---|---|
| TR-001 | 3 faz 2-level VSI | Ana topoloji | Aynı | **FROZEN PB-01, inherited by PB-03** core topology: 3-phase two-level six-switch VSI; exact semiconductor/count remains G2 | G1 envelope, loss/SOA, G2 |
| TR-002 | BLDC/PMSM | Evet | Uyumlu aday | KEEP / frozen motor class is BLDC/PMSM; exact production motor MPN OPEN | motor/prop exact MPN + eRPM correlation |
| TR-003 | FOC + SVPWM | Hedef | Firmware yok | **FROZEN capability target**; implementation/benchmark still pending | `CONTROL_PLATFORM_BENCH_CONTRACT.md` + SIL + bench |
| TR-004 | Sensorless | Hedef/opsiyon | Firmware yok | REVALIDATE; exact rotor-position strategy OPEN | startup/observer tests |
| TR-005 | 3 low-side shunt | Seçili | Mevcut | Sensing topology still REVALIDATE, but PB-03 now freezes a **minimum +/-400 A instantaneous phase-current measurement range**. Exact shunt/CSA/gain/bandwidth remain G2 after PWM windows are known. | `PHASE_CURRENT_MODEL_PB02.json`, S1.2 PWM -> G2 sensing |
| TR-006 | DC-bus + U/V/W sensing | Var | Divider + BAT54H rail clamps | Divider concept RECALCULATE; B1 rail-clamp/back-power implementation REPLACE IF REQUIRED. Existing divider ideal FS ~102.5 V, but VBUS-present/control-rails-off can back-power +3V3A/+3V3 through BAT54H and TLV75533 output. LT6015/LT6016/LT6017 provide exact primary-source evidence for a power-off-high-impedance input study path. Output sequencing is explicit: LT6017-on / STM32-VDDA-off is prohibited as a normal study state unless separately proven; preferred study rule is shared analog shutdown domain plus a series path sized from ADC settling/fault-current constraints. | `ADC_CLAMP_INJECTION_CLOSURE.md`, `ANALOG_RAIL_BACKPOWER_AUDIT.md`, `NON_BACKPOWER_HV_SENSE_ARCHITECTURES.md`, `POWER_OFF_TOLERANT_SENSE_CANDIDATES.md`, `HV_SENSE_OUTPUT_SEQUENCING.md`, final 18S VBUS/transient + sequencing/bench evidence |
| TR-007 | CAN | Var | SN65HVD230DR / optional 120R / TVS placeholder | **FROZEN functional requirement:** CAN-FD capable physical layer with Classic CAN compatibility. Exact transceiver, bit rate, topology, termination, TVS, isolation and harness remain G2/G3 implementation choices; B1 SN65HVD230DR is legacy reference only. | `CAN_PHYSICAL_LAYER_PRETRADE.md`, exact MPN + EMC/bus test |
| TR-008 | SPI gate-driver | Var | Var | OPEN implementation detail; PB-01 froze driver architecture to three independent high-voltage half-bridge drivers, not a requirement to preserve SPI | final driver/control architecture |
| TR-009 | service/debug | UART/JTAG | SWD/UART | KEEP functionally | MCU pin contract |
| TR-010 | Gate driver | DRV8353 | DRV8353FSRTAR | **PB-01 architecture frozen:** three independent high-voltage half-bridge drivers. Legacy DRV8353 is excluded from U1 primary baseline. Exact driver MPN remains OPEN; UCC27712/UCC21540-Q1 are evidence anchors only. | PB-03 phase current + S1.2 PWM + MOSFET Qg -> exact gate-driver selection |
| TR-011 | MCU | TMS320F280041C | STM32G474RET3 | OPEN trade; source-backed pretrade complete and common executable benchmark contract defined. Existing STM32 reuse and TI motor-control integration are trade factors only, not selection evidence. | `CONTROL_PLATFORM_PRETRADE.md`, `CONTROL_PLATFORM_BENCH_CONTRACT.md`, exact-package timing/trip/FOC benchmark |
| TR-012 | Aux buck | LM5164 | LM5164 | REVALIDATE / likely replace as needed for 18S rated U1; legacy input domain and loads are not product authority. | rated 18S min/max/transient + U1 auxiliary load budget |
| TR-013 | MOSFET exact MPN / parallel count | CSD19536KTT single/switch | 2 parallel/switch candidate | RECALCULATE / REPLACE. **Voltage class >=150 V and phase-current envelope 125/265/375 A are frozen by PB-03**, but exact MPN/count remain OPEN until PWM/hot-loss/SOA/thermal closure. | S1.2/S1.5 + `POWER_STAGE_LOSS_MODEL.md` -> G2 exact selection |
| TR-014 | MOSFET voltage class | 100 V | 100 V target | **FROZEN >=150 V by PB-01, inherited by PB-03**. 100 V/120 V remain historical/trade references only; normal operation shall satisfy <=120 V repetitive controlled terminal stress without relying on repetitive avalanche. | exact 150 V MPN, switching overshoot and physical G6 measurement |
| TR-015 | PWM | 40 kHz | 20 kHz | RECALCULATE / **OPEN; S1.2 ACTIVE**. Selection must use motor L/electrical time constant, >=60 keRPM, PB-03 phase-current limits and exact >=150 V device losses/ripple. | `SPRINT_PB02_TO_G1_CLOSURE.md`, `PWM_RIPPLE_LOSS_STUDY_PB03.md` |
| TR-016 | continuous phase current | 60 A RMS | 80 A RMS target | **FROZEN PB-03: >=125 A RMS continuous phase-current capability.** Derived from source-backed X13 G2 torque curve plus bounded 45KV/42-pole back-EMF constants with explicit margin; physical production-motor correlation remains mandatory. | `PHASE_CURRENT_MODEL_PB02.md`, G6 phase/DC correlation |
| TR-017 | overload/peak phase current | ~80/~100 A | 120 A SW/150 A sense | **FROZEN PB-03: >=265 A RMS for >=3 s and >=375 A instantaneous sinusoidal phase peak.** Legacy 120/150 A values are not U1 authority. | `PHASE_CURRENT_MODEL_PB02.md`, S1.2 loss/SOA, G6 measurement |
| TR-018 | power target | 1.5/3 kW | 3 kW candidate | **FROZEN DC capability inherited by PB-03:** >=4.8 kW continuous input and >=11.5 kW short-duration input for >=3 s. Legacy 3 kW is not U1 authority. | PWM/thermal correlation and G6 proof |
| TR-019 | Battery | 12–60 V generic | 13S | **FROZEN architecture inherited by PB-03:** 18S high-rate lithium, 66.6 V nominal convention, 75.6 V full charge, <=80 V outer full-charge ceiling. Ah/Wh, minimum loaded bus, sag, exact cell/pouch and disconnect behavior remain OPEN. | Sprint S1.3 18S energy/min-bus closure |
| TR-020 | Hardware trip | CMPSS/Trip Zone + driver | TLV1704 comparator path + latch + PWM inhibit | KEEP principle + REVALIDATE. PB-03 now supplies the 375 A design peak and +/-400 A sensing parent, but exact OCP threshold/blanking/end-to-end latency remain OPEN. | S1.4 protection thresholds + `CONTROL_PLATFORM_BENCH_CONTRACT.md` |
| TR-021 | Motor/FET/PCB temp | desired | exact FET/PCB NTC; motor sensor type unproven | KEEP sensing function; FET/PCB `NTCG203NH103JT1` REVALIDATE; motor sensor electrical model OPEN. | environment/thermal baseline + motor supplier/sensor evidence |
| TR-022 | DC-link | open | 3x470uF 100V bulk + 3x2.2uF 100V local, exact cap MPNs open | RECALCULATE / NOT 18S U1 QUALIFIED | Sprint S1.2/S1.3 ripple/transient/energy prework -> G2 |
| TR-023 | Precharge | open | external assembly required, exact design open | OPEN P0 | 18S pack energy + input-module contract + precharge model |
| TR-024 | Regen/BMS disconnect | conceptual | external brake interface, clamp sizing open | OPEN P0 | 18S BMS/disconnect energy acceptance + OV path |
| TR-025 | Parallel FET sharing | not primary | candidate | OPEN | exact >=150 V MPN/count, PB-03 phase-current envelope, symmetry/thermal/gate loops |
| TR-026 | Control PCB | concept | partial PoC | REUSE selectively | G2/G3 review |
| TR-027 | Power PCB | concept | incomplete | NEW DESIGN after freeze | power/thermal/mechanical review |
| TR-028 | Firmware | goals | no complete tree | NEW IMPLEMENTATION; common candidate workload/measurement contract defined but no buildable U1 firmware or physical benchmark exists yet. | `CONTROL_PLATFORM_BENCH_CONTRACT.md`, build + SIL + bench |
| TR-029 | Production package | intended | incomplete | OPEN | after G5 |
| TR-030 | Physical validation | target | incomplete | REQUIRED | staged G6 |
| TR-031 | G0 trade bounds | none | none | Historical 125/150/175 kg trade cases remain analysis-only. PB-03 inherits product sizing with frozen **150/165/180 kg design targets** at 70/85/100 kg payload. | `PRODUCT_BASELINE_PB-03.json`, later measured mass |
| TR-032 | Rotor count / architecture | not frozen | not applicable | **FROZEN PB-01/PB-02, inherited by PB-03:** X8 coaxial, four arms, eight independent propulsion channels; 0.85 coaxial sizing factor; >=1.6 normal static T/W. | physical coaxial correlation + G6 propulsion validation |
| TR-033 | U1 preliminary BOM evidence map | none | B1 BOM exists | `U1_BOM_CANDIDATES.json` records legacy references, exact source-backed candidates and G1-blocked/open functions without claiming production release. | G1/G2 closure -> U1 schematic -> `hardware_u1/bom_release.json` |
| TR-034 | Auxiliary load budget | not closed | B1 rail tree and partial assumptions exist | OPEN for U1; rated 18S first-release strategy means auxiliary startup/UVLO is optimized for U1 Rated rather than guaranteed 12S compatibility. | `U1_RATED_VARIANT_STRATEGY.md`, final gate/control/fan/Hall/interface load budget |
| TR-035 | MCU benchmark acceptance | conceptual | no comparable benchmark | DEFINED pre-freeze contract; exact numeric limits remain OPEN until remaining G1/G2 requirements freeze. | `CONTROL_PLATFORM_BENCH_CONTRACT.md` CPB-01..12 evidence |
| TR-036 | Fault latch / deliberate arm / PWM inhibit | general safety target | SN74LVC1G74 latch + six SN74LVC1G08 PWM AND gates | **Safety policy frozen:** power-up/reset DISARMED, independent hardware inhibit final authority, latched fault inhibits PWM, no automatic re-arm. Exact implementation REVALIDATE. | G2 implementation + physical end-to-end fault latency |
| TR-037 | External auxiliary/sensor/safety interface contracts | incomplete | fan, Hall, motor temp, E-stop and exported +5V have partial PoC definitions | OPEN; null-only contract template created so voltage/current/inrush/output type/fault behavior/connector values cannot be silently guessed. | vehicle/motor/fan/harness decisions |
| TR-038 | Production signal/control connectors | concept | WR-PHD Hall/motor-temp PoC headers + logical 2x20 board interface | REVALIDATE / REPLACE as required; legacy unkeyed headers are reference-only and SAME_NETS does not prove physical mating/orientation. | exact harness/mechanical/environment evidence |
| TR-039 | CAN physical-layer candidate architecture | generic CAN target | SN65HVD230DR Classic CAN | Functional CAN-FD/Classic-CAN requirement is FROZEN; exact non-isolated/isolated transceiver architecture remains OPEN trade among documented candidates. | frozen harness/ENV/grounding + timing/EMC bench evidence |
| TR-040 | Production connector qualification structure | conceptual | PoC headers / logical board interface | DEFINED structure, product values OPEN. Exact connector, mate, contact, keying, retention, derating, vibration, ingress and service evidence required before release. | frozen electrical/ENV/harness requirements |
| TR-041 | Fault tree / FMEA structure | conceptual protection goals | partial B1 hardware fault paths | STRUCTURAL PREWORK ONLY; 12 initial failure modes mapped without invented scores/timing. PB-03 closes phase-current parent values; threshold/timeout architecture and physical evidence remain later work. | `FAULT_FMEA_SKELETON.json`, S1.4, G2/G4/G6 evidence |
| TR-042 | U1 KiCad migration policy | intended B2/U1 revision | B1 multi-sheet schematic | PRE-G3 structure defined. No component-bearing `hardware_u1/` revision is allocated until G1 and page-level G2 allocation conditions pass. | `U1_SCHEMATIC_ALLOCATION_READINESS.json`, G2 -> U1-SCH-R001 |
| TR-043 | Controlled product baseline | none | none | **PB-03 ACTIVE/FROZEN:** inherits PB-02 X8/18S/MTOW/DC/eRPM baseline and adds >=125 A RMS continuous phase, >=265 A RMS/3 s overload, >=375 A phase peak and >=+/-400 A measurement range. | `PRODUCT_BASELINE_PB-03.json`, G1 matrix |
| TR-044 | Product-family voltage strategy | none | none | **CONTROLLED STRATEGY:** U1 Rated is optimized for the 18S upper-performance baseline. Lower-S products are future controlled derivatives, not initial-release compatibility requirements. | `U1_RATED_VARIANT_STRATEGY.md` |
| TR-045 | Active execution sprint | none | none | **S1 ACTIVE: S1.1 DONE / S1.2 ACTIVE.** Next path is PWM/ripple/loss -> 18S energy/min bus -> environment/protection -> exact power-stage G2 prework -> configuration closeout. | `SPRINT_PB02_TO_G1_CLOSURE.md` |
| TR-046 | Phase-current derivation | old phase-current targets | B1 80/120/150 A concepts | **NEW PB-03 authority:** phase current is derived from X13 G2 torque points and bounded 45KV/42-pole back-EMF constants; DC current is explicitly not used as phase current. Physical motor characterization is a later acceptance item. | `PHASE_CURRENT_MODEL_PB02.md`, `PHASE_CURRENT_MODEL_PB02.json`, `verify_phase_current_pb03.py` |

## Güncel kaynaklı sonuçlar

- `PRODUCT_BASELINE_PB-03.json` is the current product baseline authority. It inherits all PB-02 frozen values and adds the S1.1 phase-current/sensing-range requirements; these values are not reopened without PB-04/ECO.
- X8 coaxial / 8 independent propulsion channels, 0.85 coaxial sizing factor and >=1.6 normal static thrust-to-weight remain frozen design requirements; physical coaxial correlation is still required.
- Propulsion performance class remains frozen at 56x20 inch / 45 KV / 18S with >=27 kgf rated and >=60 kgf isolated max capability; exact production MPN remains open.
- 18S remains frozen for U1 Rated: 66.6 V nominal convention, 75.6 V full charge and <=80 V outer full-charge ceiling. Pack energy, minimum loaded bus and exact cell remain open.
- Power semiconductor voltage class remains frozen at >=150 V. Exact MOSFET MPN/count now has a frozen phase-current parent but still depends on S1.2 PWM/hot-loss/SOA and thermal closure.
- DC capability remains >=70 A continuous, >=200 A for >=3 s, >=4.8 kW continuous input and >=11.5 kW short-duration input.
- **PB-03 phase-current capability is now frozen at >=125 A RMS continuous, >=265 A RMS for >=3 s, >=375 A instantaneous phase peak, with a minimum +/-400 A current-measurement range.** These are design requirements from a bounded source-backed model, not physical measurements.
- Gate-driver architecture remains three independent high-voltage half-bridge drivers; legacy DRV8353 is excluded from the primary U1 path, exact driver MPN remains open.
- CAN-FD-capable / Classic-CAN-compatible FC link and deliberate arming/no-auto-rearm policy remain frozen; exact physical-layer MPN and protocol timing remain implementation work.
- `SPRINT_PB02_TO_G1_CLOSURE.md` now records **S1.1 DONE / S1.2 ACTIVE**. PWM remains open and is the immediate critical path.
- `U1_SCHEMATIC_MIGRATION_CONTRACT.md`, revision policy, G3 ERC policy and allocation guard remain active; no component-bearing U1 schematic exists yet.
- B1 voltage-sense upper BAT54H can back-power +3V3A/+3V3 in an unpowered-control state, so rail-clamp sensing is not a default KEEP.
- Calculators and manufacturer curves are analysis evidence; physical/thermal/EMI/dyno/flight claims require later-gate measurements.

## Korunacak çekirdek

Üç faz VSI, PWM-senkron akım ölçümü, FOC/SVPWM hedefi, CAN işlevi, hızlı donanımsal kapatma, sıcaklık/gerilim telemetrisi, modüler kontrol/güç kartı ve otomatik ERC/netlist/interface kontrolleri korunur.

## Yeniden hesaplanacak / kapanacak çekirdek

Eski Faz2/Faz3/B1 phase-current hedefleri artık U1 ürün authority değildir; PB-03 125/265/375 A envelope'u onların yerini alır. Sprint S1 tamamlanmadan 20/40 kHz PWM, B1 FET sayısı, shunt/gain, DC-link, connector/fuse/cable ve thermal budget U1 ürün değeri olarak taşınmaz. PB-03 ile frozen olan 18S, >=150 V class, DC-side capability ve phase-current envelope kontrollü parent requirement'tır.

## Çelişki çözme sırası

1. güncel kontrollü product baseline / UAV requirement,
2. doğrulanmış motor/prop operating point,
3. electrical/thermal calculation,
4. datasheet/source evidence,
5. prototype measurement.

Eski doküman geçmiş tasarım gerekçesidir; otomatik design authority değildir.
