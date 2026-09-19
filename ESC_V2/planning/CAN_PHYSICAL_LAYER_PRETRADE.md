# CAN physical-layer pretrade

Date: 2026-09-19  
Branch: `uav-rebaseline`  
Status: `TRADE_ONLY_NO_TRANSCEIVER_SELECTED`

## Purpose

Provide a source-backed CAN physical-layer trade before `IF-CAN-002` is frozen. This document does **not** choose Classic CAN versus CAN FD, isolation versus non-isolation, termination, TVS, common-mode choke, connector, cable, node count or bit rate.

## Anti-hallucination rules

1. Vehicle protocol, arbitration/data bit rates, harness length, node count, topology, termination, EMC/transient environment and isolation need remain `OPEN` until frozen by vehicle requirements.
2. Manufacturer ratings are recorded with their stated context; unlike quantities are not treated as directly comparable. In particular, a bus-pin limiting voltage is not automatically equivalent to a guaranteed bus-fault protection rating.
3. AEC-Q100, functional-safety collateral or high ESD capability do not by themselves qualify the complete ESC CAN interface.
4. No candidate below is a production BOM selection.

## Legacy reference

### TI SN65HVD230DR

Repository role: B1 legacy transceiver, `REVALIDATE` only.

Primary-source / repository anchor currently recorded:
- 3.3 V supply.
- Classic CAN class.
- Maximum signaling rate 1 Mbps.
- SOIC-8 D package.
- Operating temperature -40 to +85 degC.

Implication:
- It can remain a legacy comparison point, but it cannot be frozen until the vehicle protocol and environment are known.
- The +85 degC upper operating-temperature anchor is a visible compatibility risk if U1 ENV later requires a higher transceiver ambient range.

## Current non-isolated trade candidates

### Candidate A — TI TCAN1044A-Q1 family

Primary manufacturer evidence:
- Status: ACTIVE.
- ISO 11898-2:2016 high-speed CAN physical layer.
- Supports Classical CAN and CAN FD; TI states optimized CAN FD operation at 2, 5 and 8 Mbps, with 8 Mbps dependent on simpler network conditions.
- VCC: 4.5 V to 5.5 V.
- `V` option provides VIO-level translation for 1.8 / 2.5 / 3.3 / 5 V logic domains.
- Bus-fault protection: +/-58 V.
- AEC-Q100 Grade 1 automotive qualification.
- Unpowered bus and logic pins are specified high impedance; power up/down is described as glitch-free on the bus and RXD.
- Includes TXD dominant timeout, undervoltage detection and thermal shutdown.

Primary source:
- https://www.ti.com/product/TCAN1044A-Q1
- https://www.ti.com/lit/ds/symlink/tcan1044a-q1.pdf

Trade implications:
- Strong fit for a non-isolated CAN/CAN-FD node if the final harness/transient requirement fits its protection envelope.
- VIO variant is attractive if the selected MCU logic rail differs from the transceiver VCC domain.
- Exact package/orderable MPN remains OPEN.

### Candidate B — TI TCAN1042HGV-Q1 family

Primary manufacturer evidence:
- Status: ACTIVE.
- ISO 11898-2:2016 high-speed CAN physical layer.
- `G` option supports CAN FD data rate up to 5 Mbps.
- `V` option provides a separate I/O supply for logic-level shifting.
- VCC: 4.5 V to 5.5 V.
- I/O domain: 3.3 V / 5 V class per TI family data.
- H variants: +/-70 V bus-fault protection.
- Receiver common-mode input range headline: +/-30 V.
- Unpowered bus and logic terminals are specified high impedance.
- Typical loop-delay headline: 110 ns.
- TI lists junction-temperature range from -55 to +150 degC for the family page.
- AEC-Q100 Grade 1.

Primary source:
- https://www.ti.com/product/TCAN1042HGV-Q1

Trade implications:
- Provides a higher documented bus-fault protection headline than TCAN1044A-Q1 while retaining CAN FD capability.
- Lower headline maximum data rate than TCAN1044A-Q1; whether that matters is unknowable until protocol/bit-rate requirements freeze.
- Exact package/orderable MPN remains OPEN.

### Candidate C — NXP TJA1044GT/3

Primary manufacturer evidence:
- TJA1044 family implements high-speed CAN physical layer per ISO 11898-2.
- GT variants have timing guaranteed for CAN FD data rates up to 5 Mbps.
- VIO-capable `/3` variant supports direct MCU I/O-domain interfacing; NXP data sheet lists VIO 2.91 V to 5.5 V.
- VCC: 4.5 V to 5.5 V.
- AEC-Q100 qualified.
- Transceiver disengages from the bus when unpowered (zero load).
- Bus pins have a stated limiting voltage of -42 V to +42 V in the current data sheet.
- Virtual junction temperature range: -40 to +150 degC.
- Includes TXD/bus dominant timeout, undervoltage detection and thermal protection.

Primary source:
- https://www.nxp.com/products/TJA1044
- https://www.nxp.com/docs/en/data-sheet/TJA1044.pdf

Trade implications:
- Valid CAN FD non-isolated comparison candidate with predictable unpowered-bus behavior.
- The +/-42 V bus-pin limiting rating is **not** treated as equivalent to TI's guaranteed +/-58 V or +/-70 V bus-fault specification. Final transient protection must be evaluated as a whole interface, including external TVS/protection.
- Exact package/orderable suffix remains OPEN.

## Isolated topology anchor

### Candidate D — TI ISO1042-Q1

Primary manufacturer evidence:
- Status: ACTIVE.
- Galvanically isolated CAN transceiver.
- Classic CAN up to 1 Mbps and CAN FD up to 5 Mbps.
- Bus-fault protection: +/-70 V.
- Common-mode range: +/-30 V.
- Logic-side VCC1: 1.71 V to 5.5 V.
- Bus-side VCC2: 4.5 V to 5.5 V.
- Operating temperature: -40 to +125 degC.
- Unpowered bus terminals specified high impedance.
- 5000 Vrms one-minute isolation withstand headline; working isolation-voltage and exact insulation class depend on device option/package.
- Minimum/typical CMTI figures are manufacturer-defined and shall be checked against the exact orderable variant before selection.

Primary source:
- https://www.ti.com/product/ISO1042-Q1
- https://www.ti.com/lit/ds/symlink/iso1042-q1.pdf

Trade implications:
- Keep as an architecture anchor only if final grounding, common-mode, fault-containment or EMC needs justify galvanic isolation.
- Isolation adds an isolated/bus-side power-domain requirement, barrier layout/creepage constraints, BOM cost and another power-sequencing case.
- Isolation shall not be added merely because it appears more robust; system-level need must be explicit.

## Architecture questions that remain OPEN

| Requirement | Status | Why still open |
|---|---|---|
| Classic CAN vs CAN FD | OPEN | Flight-controller/vehicle protocol not frozen |
| Arbitration bit rate | OPEN | Vehicle protocol not frozen |
| CAN FD data-phase bit rate | OPEN | Vehicle protocol not frozen |
| Bus length / stub length | OPEN | Vehicle harness not frozen |
| Node count | OPEN | Vehicle network architecture not frozen |
| Termination topology | OPEN | Harness topology not frozen |
| TVS exact MPN | OPEN | EMC/transient environment not frozen |
| Common-mode choke | OPEN | EMC evidence and harness not frozen |
| Galvanic isolation | OPEN | Grounding/common-mode/fault-containment need not frozen |
| Connector and pinout | OPEN | Harness/mechanical requirements not frozen |
| Shield/drain strategy | OPEN | EMC/harness strategy not frozen |
| Transceiver exact package/MPN | OPEN | Above parent requirements remain open |

## Required verification before G2/G3 closure

1. Freeze FC protocol and actual CAN/CAN-FD timing contract.
2. Freeze harness topology, cable length, stub limits, node count and termination strategy.
3. Freeze environmental and electrical transient requirements.
4. Select non-isolated or isolated architecture from system need, not component preference.
5. Perform bus timing / propagation analysis for the selected bit rates.
6. Define TVS/common-mode-choke/termination values from the selected transceiver and transient/EMC requirements.
7. Bench-test powered/unpowered node behavior, hot-plug behavior, timeout/fault states and physical bus margins.
8. Perform EMC pre-compliance appropriate to the frozen product requirement.

## Current trade conclusion

The B1 `SN65HVD230DR` remains a legacy Classic-CAN reference only. Current source-backed trade anchors exist for higher-temperature/non-isolated CAN-FD (`TCAN1044A-Q1`, `TCAN1042HGV-Q1`, `TJA1044GT/3`) and an isolated CAN-FD architecture (`ISO1042-Q1`). **No winner is selected.** The selection is intentionally blocked by the vehicle interface, harness, environment and grounding requirements.
