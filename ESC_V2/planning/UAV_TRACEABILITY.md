# UAV ESC tasarım izlenebilirlik matrisi

Tarih: 19.09.2026  
Amaç: Faz 2 / Faz 3 dokümanları ile mevcut B1 tasarımını yeni UAV ürün gereksinimine bağlamak.

Durum etiketleri: **KEEP**, **REVALIDATE**, **RECALCULATE**, **REPLACE IF REQUIRED**, **OPEN**, **FROZEN**.

| ID | Fonksiyon / karar | Faz 2/3 | B1 | UAV rebaseline kararı | Sonraki kanıt |
|---|---|---|---|---|---|
| TR-001 | 3 faz 2-level VSI | Ana topoloji | Aynı | **FROZEN PB-01/PB-02** core topology: 3-phase two-level six-switch VSI; exact semiconductor/count remains G2 | G1 envelope, loss/SOA, G2 |
| TR-002 | BLDC/PMSM | Evet | Uyumlu aday | KEEP / frozen motor class is BLDC/PMSM; exact production motor MPN OPEN | motor/prop exact MPN + eRPM correlation |
| TR-003 | FOC + SVPWM | Hedef | Firmware yok | **FROZEN capability target**; implementation/benchmark still pending | `CONTROL_PLATFORM_BENCH_CONTRACT.md` + SIL + bench |
| TR-004 | Sensorless | Hedef/opsiyon | Firmware yok | REVALIDATE; exact rotor-position strategy OPEN | startup/observer tests |
| TR-005 | 3 low-side shunt | Seçili | Mevcut | REVALIDATE; sensing topology not yet frozen because phase-current/PWM windows remain open | Sprint S1 phase-current/PWM -> G2 sensing |
| TR-006 | DC-bus + U/V/W sensing | Var | Divider + BAT54H rail clamps | Divider concept RECALCULATE; B1 rail-clamp/back-power implementation REPLACE IF REQUIRED. Existing divider ideal FS ~102.5 V, but VBUS-present/control-rails-off can back-power +3V3A/+3V3 through BAT54H and TLV75533 output. LT6015/LT6016/LT6017 provide exact primary-source evidence for a power-off-high-impedance input study path. Output sequencing is explicit: LT6017-on / STM32-VDDA-off is prohibited as a normal study state unless separately proven; preferred study rule is shared analog shutdown domain plus a series path sized from ADC settling/fault-current constraints. | `ADC_CLAMP_INJECTION_CLOSURE.md`, `ANALOG_RAIL_BACKPOWER_AUDIT.md`, `NON_BACKPOWER_HV_SENSE_ARCHITECTURES.md`, `POWER_OFF_TOLERANT_SENSE_CANDIDATES.md`, `HV_SENSE_OUTPUT_SEQUENCING.md`, final 18S VBUS/transient + sequencing/bench evidence |
| TR-007 | CAN | Var | SN65HVD230DR / optional 120R / TVS placeholder | **FROZEN functional requirement:** CAN-FD capable physical layer with Classic CAN compatibility. Exact transceiver, bit rate, topology, termination, TVS, isolation and harness remain G2/G3 implementation choices; B1 SN65HVD230DR is legacy reference only. | `CAN_PHYSICAL_LAYER_PRETRADE.md`, exact MPN + EMC/bus test |
| TR-008 | SPI gate-driver | Var | Var | OPEN implementation detail; PB-01 froze driver architecture to three independent high-voltage half-bridge drivers, not a requirement to preserve SPI | final driver/control architecture |
| TR-009 | service/debug | UART/JTAG | SWD/UART | KEEP functionally | MCU pin contract |
| TR-010 | Gate driver | DRV8353 | DRV8353FSRTAR | **PB-01 architecture frozen:** three independent high-voltage half-bridge drivers. Legacy DRV8353 is excluded from U1 primary baseline. Exact driver MPN remains OPEN; UCC27712/UCC21540-Q1 are evidence anchors only. | phase-current + PWM + MOSFET Qg -> exact gate-driver selection |
| TR-011 | MCU | TMS320F280041C | STM32G474RET3 | OPEN trade; source-backed pretrade complete and common executable benchmark contract defined. Existing STM32 reuse and TI motor-control integration are trade factors only, not selection evidence. | `CONTROL_PLATFORM_PRETRADE.md`, `CONTROL_PLATFORM_BENCH_CONTRACT.md`, exact-package timing/trip/FOC benchmark |
| TR-012 | Aux buck | LM5164 | LM5164 | REVALIDATE / likely replace as needed for 18S rated U1; legacy input domain and loads are not product authority. | rated 18S min/max/transient + U1 auxiliary load budget |
| TR-013 | MOSFET exact MPN / parallel count | CSD19536KTT single/switch | 2 parallel/switch candidate | RECALCULATE / REPLACE. **Voltage class is already frozen >=150 V**, but exact MPN and switch parallel count remain OPEN until phase-current/PWM/hot-loss/SOA closure. | Sprint S1 + `POWER_STAGE_LOSS_MODEL.md` -> G2 exact selection |
| TR-014 | MOSFET voltage class | 100 V | 100 V target | **FROZEN >=150 V by PB-01, inherited by PB-02**. 100 V/120 V remain historical/trade references only; normal operation shall satisfy <=120 V repetitive controlled terminal stress without relying on repetitive avalanche. | exact 150 V MPN, switching overshoot and physical G6 measurement |
| TR-015 | PWM | 40 kHz | 20 kHz | RECALCULATE / **OPEN**; Sprint S1 closes from motor L/electrical time constant + >=60 keRPM + 150 V switching loss/ripple | `SPRINT_PB02_TO_G1_CLOSURE.md`, PWM loss/ripple study |
| TR-016 | continuous phase current | 60 A RMS | 80 A RMS target | **OPEN**; DC >=70 A capability shall not be copied into phase-current domain | Sprint S1 phase-current model |
| TR-017 | overload/peak phase current | ~80/~100 A | 120 A SW/150 A sense | **OPEN**; PB-02 freezes DC >=200 A for >=3 s but phase peak remains independent | Sprint S1 phase-current model + duration |
| TR-018 | power target | 1.5/3 kW | 3 kW candidate | **FROZEN DC capability PB-02:** >=4.8 kW continuous input and >=11.5 kW short-duration input for >=3 s. Legacy 3 kW is not U1 authority. | phase-current/PWM/thermal correlation and G6 proof |
| TR-019 | Battery | 12–60 V generic | 13S | **FROZEN architecture PB-02:** 18S high-rate lithium, 66.6 V nominal convention, 75.6 V full charge, <=80 V outer full-charge ceiling. Ah/Wh, minimum loaded bus, sag, exact cell/pouch and disconnect behavior remain OPEN. | Sprint S1 18S energy/min-bus closure |
| TR-020 | Hardware trip | CMPSS/Trip Zone + driver | TLV1704 comparator path + latch + PWM inhibit | KEEP principle + REVALIDATE; B1 audit separates individual-device delay from required end-to-end asynchronous fault-to-PWM-inactive measurement. | phase-current/OCP threshold + `CONTROL_PLATFORM_BENCH_CONTRACT.md` |
| TR-021 | Motor/FET/PCB temp | desired | exact FET/PCB NTC; motor sensor type unproven | KEEP sensing function; FET/PCB `NTCG203NH103JT1` REVALIDATE; motor sensor electrical model OPEN. | environment/thermal baseline + motor supplier/sensor evidence |
| TR-022 | DC-link | open | 3x470uF 100V bulk + 3x2.2uF 100V local, exact cap MPNs open | RECALCULATE / NOT 18S U1 QUALIFIED | Sprint S1 ripple/transient/energy prework -> G2 |
| TR-023 | Precharge | open | external assembly required, exact design open | OPEN P0 | 18S pack energy + input-module contract + precharge model |
| TR-024 | Regen/BMS disconnect | conceptual | external brake interface, clamp sizing open | OPEN P0 | 18S BMS/disconnect energy acceptance + OV path |
| TR-025 | Parallel FET sharing | not primary | candidate | OPEN | exact 150 V MPN/count, symmetry/thermal/gate loops |
| TR-026 | Control PCB | concept | partial PoC | REUSE selectively | G2/G3 review |
| TR-027 | Power PCB | concept | incomplete | NEW DESIGN after freeze | power/thermal/mechanical review |
| TR-028 | Firmware | goals | no complete tree | NEW IMPLEMENTATION; common candidate workload/measurement contract defined but no buildable U1 firmware or physical benchmark exists yet. | `CONTROL_PLATFORM_BENCH_CONTRACT.md`, build + SIL + bench |
| TR-029 | Production package | intended | incomplete | OPEN | after G5 |
| TR-030 | Physical validation | target | incomplete | REQUIRED | staged G6 |
| TR-031 | G0 trade bounds | none | none | Historical 125/150/175 kg trade cases remain analysis-only. PB-02 supersedes product sizing with frozen **150/165/180 kg design targets** at 70/85/100 kg payload. | `PRODUCT_BASELINE_PB-02.json`, later measured mass |
| TR-032 | Rotor count / architecture | not frozen | not applicable | **FROZEN PB-01/PB-02:** X8 coaxial, four arms, eight independent propulsion channels; 0.85 coaxial sizing factor; >=1.6 normal static T/W. | physical coaxial correlation + G6 propulsion validation |
| TR-033 | U1 preliminary BOM evidence map | none | B1 BOM exists | `U1_BOM_CANDIDATES.json` records legacy references, exact source-backed candidates and G1-blocked/open functions without claiming production release. | G1/G2 closure -> U1 schematic -> `hardware_u1/bom_release.json` |
| TR-034 | Auxiliary load budget | not closed | B1 rail tree and partial assumptions exist | OPEN for U1; rated 18S first-release strategy means auxiliary startup/UVLO is optimized for U1 Rated rather than guaranteed 12S compatibility. | `U1_RATED_VARIANT_STRATEGY.md`, final gate/control/fan/Hall/interface load budget |
| TR-035 | MCU benchmark acceptance | conceptual | no comparable benchmark | DEFINED pre-freeze contract; exact numeric limits remain OPEN until remaining G1/G2 requirements freeze. | `CONTROL_PLATFORM_BENCH_CONTRACT.md` CPB-01..12 evidence |
| TR-036 | Fault latch / deliberate arm / PWM inhibit | general safety target | SN74LVC1G74 latch + six SN74LVC1G08 PWM AND gates | **Safety policy frozen:** power-up/reset DISARMED, independent hardware inhibit final authority, latched fault inhibits PWM, no automatic re-arm. Exact implementation REVALIDATE. | G2 implementation + physical end-to-end fault latency |
| TR-037 | External auxiliary/sensor/safety interface contracts | incomplete | fan, Hall, motor temp, E-stop and exported +5V have partial PoC definitions | OPEN; null-only contract template created so voltage/current/inrush/output type/fault behavior/connector values cannot be silently guessed. | vehicle/motor/fan/harness decisions |
| TR-038 | Production signal/control connectors | concept | WR-PHD Hall/motor-temp PoC headers + logical 2x20 board interface | REVALIDATE / REPLACE as required; legacy unkeyed headers are reference-only and SAME_NETS does not prove physical mating/orientation. | exact harness/mechanical/environment evidence |
| TR-039 | CAN physical-layer candidate architecture | generic CAN target | SN65HVD230DR Classic CAN | Functional CAN-FD/Classic-CAN requirement is FROZEN; exact non-isolated/isolated transceiver architecture remains OPEN trade among documented candidates. | frozen harness/ENV/grounding + timing/EMC bench evidence |
| TR-040 | Production connector qualification structure | conceptual | PoC headers / logical board interface | DEFINED structure, product values OPEN. Exact connector, mate, contact, keying, retention, derating, vibration, ingress and service evidence required before release. | frozen electrical/ENV/harness requirements |
| TR-041 | Fault tree / FMEA structure | conceptual protection goals | partial B1 hardware fault paths | STRUCTURAL PREWORK ONLY; 12 initial failure modes mapped without invented scores/timing. Sprint S1 may close system-level threshold/timeout parents; final architecture/physical evidence remains later-gate work. | `FAULT_FMEA_SKELETON.json`, Sprint S1, G2/G4/G6 evidence |
| TR-042 | U1 KiCad migration policy | intended B2/U1 revision | B1 multi-sheet schematic | PRE-G3 structure defined. No component-bearing `hardware_u1/` revision is allocated until G1 and page-level G2 allocation conditions pass. | `U1_SCHEMATIC_ALLOCATION_READINESS.json`, G2 -> U1-SCH-R001 |
| TR-043 | Controlled product baseline | none | none | **PB-02 ACTIVE/FROZEN:** 85 kg nominal payload, <=80 kg operating-empty budget, 150/165/180 kg MTOW, 56x20/45KV/18S class, DC >=70 A continuous / >=200 A 3 s, >=4.8 kW continuous / >=11.5 kW short, >=60 keRPM. | `PRODUCT_BASELINE_PB-02.json`, G1 matrix |
| TR-044 | Product-family voltage strategy | none | none | **CONTROLLED STRATEGY:** U1 Rated is optimized for the 18S upper-performance baseline. Lower-S products are future controlled derivatives, not initial-release compatibility requirements. | `U1_RATED_VARIANT_STRATEGY.md` |
| TR-045 | Active execution sprint | none | none | **S1 ACTIVE:** phase current -> PWM/ripple/loss -> 18S energy/min bus -> environment/protection -> exact power-stage G2 prework -> configuration closeout. This sprint does not bypass G1/G2 gates. | `SPRINT_PB02_TO_G1_CLOSURE.md` |

## Güncel kaynaklı sonuçlar

- `PRODUCT_BASELINE_PB-02.json` is the current product baseline authority; its frozen values are not reopened without PB-03/ECO.
- X8 coaxial / 8 independent propulsion channels, 0.85 coaxial sizing factor and >=1.6 normal static thrust-to-weight are frozen design requirements; physical coaxial correlation is still required.
- Propulsion performance class is frozen at 56x20 inch / 45 KV / 18S with >=27 kgf rated and >=60 kgf isolated max capability; exact production MPN remains open.
- 18S is frozen for U1 Rated: 66.6 V nominal convention, 75.6 V full charge and <=80 V outer full-charge ceiling. Pack energy, minimum loaded bus and exact cell remain open.
- Power semiconductor voltage class is frozen at >=150 V; exact MOSFET MPN/count remains open and depends on Sprint S1 phase-current/PWM/hot-loss closure.
- DC capability is frozen at >=70 A continuous, >=200 A for >=3 s, >=4.8 kW continuous input and >=11.5 kW short-duration input. Phase current remains independent/open.
- Gate-driver architecture is frozen to three independent high-voltage half-bridge drivers; legacy DRV8353 is excluded from the primary U1 path, exact driver MPN remains open.
- CAN-FD-capable / Classic-CAN-compatible FC link and deliberate arming/no-auto-rearm policy are frozen; exact physical-layer MPN and protocol timing remain implementation work.
- `U1_RATED_VARIANT_STRATEGY.md` prevents future lower-voltage derivative goals from distorting the first 18S rated design.
- `SPRINT_PB02_TO_G1_CLOSURE.md` is the active execution overlay for the remaining G1 closure. It does not allocate `U1-SCH-R001` or change any gate acceptance rule.
- `U1_SCHEMATIC_MIGRATION_CONTRACT.md`, revision policy, G3 ERC policy and allocation guard remain active; no component-bearing U1 schematic exists yet.
- B1 voltage-sense upper BAT54H can back-power +3V3A/+3V3 in an unpowered-control state, so rail-clamp sensing is not a default KEEP.
- Calculators and manufacturer curves are analysis evidence; physical/thermal/EMI/dyno/flight claims require later-gate measurements.

## Korunacak çekirdek

Üç faz VSI, PWM-senkron akım ölçümü, FOC/SVPWM hedefi, CAN işlevi, hızlı donanımsal kapatma, sıcaklık/gerilim telemetrisi, modüler kontrol/güç kartı ve otomatik ERC/netlist/interface kontrolleri korunur.

## Yeniden hesaplanacak / kapanacak çekirdek

Sprint S1 tamamlanmadan eski 60/80/100/120/150 A phase-current değerleri, 20/40 kHz PWM, B1 FET sayısı, shunt/gain, DC-link, connector/fuse/cable ve thermal budget U1 ürün değeri olarak taşınmaz. PB-02 ile frozen olan 18S, >=150 V class ve DC-side capability ise yeniden trade girdisi değil, kontrollü parent requirement'tır.

## Çelişki çözme sırası

1. güncel kontrollü product baseline / UAV requirement,
2. doğrulanmış motor/prop operating point,
3. electrical/thermal calculation,
4. datasheet/source evidence,
5. prototype measurement.

Eski doküman geçmiş tasarım gerekçesidir; otomatik design authority değildir.
