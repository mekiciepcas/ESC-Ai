# B1 auxiliary load and power-domain inventory

Date: 2026-09-19  
Branch: `uav-rebaseline`  
Status: **LEGACY B1 EVIDENCE / U1 INPUT — NOT A U1 LOAD REQUIREMENT**

## Purpose

Capture what the existing B1 repository actually proves about the auxiliary rails and their connected loads before selecting the U1 auxiliary-power architecture. This document deliberately separates converter **source capability** from actual ESC **load demand**. A regulator headline current rating is not a measured or required load current.

## Evidence classification

- **REPOSITORY SOURCE EVIDENCE** — directly present in B1 schematic / connection manifest / notes.
- **PRIMARY MANUFACTURER EVIDENCE** — current manufacturer product/datasheet information.
- **DERIVED CALCULATION** — arithmetic from repository values, with inputs shown.
- **OPEN** — no defensible U1 value exists yet.

## B1 rail topology

Repository tracing gives the following legacy tree:

`VBUS -> LM5164DDAT -> +12V -> TPS62160DGKR -> +5V -> TLV75533PDBVR -> +3V3 -> analog link -> +3V3A`

This topology is historical B1 evidence only. It is not automatically valid for the UAV U1 design because the final VBUS transient envelope and auxiliary load budget remain open.

## Source devices and capability anchors

| Rail / source | B1 device | Repository role | Manufacturer capability anchor | Interpretation |
|---|---|---|---|---|
| `+12V` | LM5164DDAT | VBUS to nominal ~12.09 V | TI LM5164: 6–100 V input, 1 A synchronous buck | 1 A is device capability, **not** evidence that B1 or U1 consumes 1 A. Final VBUS transient can disqualify the 100 V domain. |
| `+5V` | TPS62160DGKR | +12 V to nominal ~4.984 V | TI TPS62160: 3–17 V input, up to 1 A output | 1 A is source capability only. Actual Hall/interface/3.3 V load is not closed. |
| `+3V3` | TLV75533PDBVR | +5 V to 3.3 V logic | TI TLV755P family: up to 500 mA, 1.45–5.5 V input | 500 mA is regulator rating, not actual load. B1 schematic note checks 200 mA operation but does not prove a 200 mA system load. |
| `+3V3A` | derived from +3V3 | analog / sensing reference domain | no separate source rating proven | Existing B1 rail coupling/backfeed behavior is under revalidation; U1 sequencing must be explicitly designed. |

Primary manufacturer references:
- TI LM5164: https://www.ti.com/product/LM5164
- TI TPS62160 / exact B1 orderable `TPS62160DGKR`: https://www.ti.com/product/TPS62160/part-details/TPS62160DGKR
- TI TLV755P: https://www.ti.com/product/TLV755P

## B1 loads visible from repository evidence

### +12 V domain

Known connected functions:
- `DRV8353FSRTAR` VM/gate-driver supply.
- `TPS62160DGKR` input, which feeds all downstream +5 V / +3V3 / +3V3A loads.
- external 12 V fan connector.

The B1 schematic records **fan <= 0.2 A continuous as a starting budget** and explicitly states fan inrush must be measured. This is a B1 design assumption, not a U1 requirement.

The gate-drive component of +12 V load is **OPEN** for U1 because it depends on selected MOSFET total gate charge, number of devices driven, PWM frequency, switching pattern, gate-driver architecture and quiescent current. It shall later be budgeted from the selected topology rather than copied from B1.

### +5 V domain

Known connected functions:
- input to `TLV75533PDBVR` for the +3V3 domain;
- `HALL 5V` external connector;
- +5 V exported on the B1 board interface (pin 39).

Therefore the repository cannot prove a closed +5 V load merely from the onboard BOM: the external Hall load and exported interface load are not bounded as product requirements.

### +3V3 domain

Known connected functions include:
- `STM32G474RET3` MCU;
- `SN65HVD230DR` CAN transceiver;
- fault latch logic (`SN74LVC1G74DCUR`), pull-ups and digital support;
- connection into the +3V3A analog domain.

The B1 CAN part is Classic CAN only; protocol/CAN-FD requirements remain a separate U1 control-interface decision.

### +3V3A domain

Known connected functions include:
- DRV8353 VREF/current-shunt-amplifier reference domain;
- four B1 BAT54H upper voltage-sense clamps (known rail-backpower concern);
- temperature-divider/reference circuits;
- two `TLV1704PWR` hardware-trip comparator devices;
- over-current / over-voltage reference divider networks.

The three visible static trip-reference dividers draw, from their nominal resistor values at 3.3 V:

- OC_LOW: `3.3 / (26.1k + 10k) = 91.4 uA`
- OC_HIGH: `3.3 / (10k + 26.1k) = 91.4 uA`
- OV_REF: `3.3 / (7.5k + 10k) = 188.6 uA`
- subtotal: approximately **0.371 mA**

This derived subtotal is only the passive reference-divider current. It is not the +3V3A rail load because comparator, CSA/reference, sensing, NTC and transient clamp currents remain separate.

## What the B1 repository does **not** prove

The following values remain OPEN and must not be fabricated:

- total +12 V continuous and peak current;
- fan inrush current;
- actual gate-drive average/peak power at the eventual U1 MOSFET/PWM point;
- external Hall sensor current;
- maximum +5 V board-interface exported load;
- STM32 dynamic current at the final clock/peripheral/FOC workload;
- CAN/transceiver bus-state load at the final interface design;
- +3V3A total analog current and clamp/fault current in every sequencing state;
- converter efficiency and thermal rise at the final U1 operating envelope.

The legacy LM5164 1 A, TPS62160 1 A and TLV755 500 mA ratings are therefore **upper source capabilities**, not a validated auxiliary-load budget.

## Derived U1 requirements to carry forward

Under PWR / CTRL / SAF domains, U1 shall eventually define and verify:

1. per-rail steady-state current budget for all operating modes;
2. per-rail startup/inrush and transient load budget;
3. gate-drive dynamic power budget derived from selected MOSFET Qg, switch count and PWM;
4. external loads (fan, Hall, board interface) as explicit bounded interface contracts;
5. rail sequencing / powered-down behavior so no domain is unintentionally back-powered;
6. converter current-limit, thermal and transient margin at min/nom/max bus and environmental conditions;
7. power-good / brownout behavior and the resulting PWM-inhibit/fault state.

## Architecture implication

The current B1 auxiliary tree is useful as a functional decomposition, but it cannot select the U1 converter family. The earlier high-voltage auxiliary trade (`LM5164` vs `LTC3639` / `LTC7801` architecture anchors) must be evaluated only after two parent inputs close:

- final G1 bus/transient envelope;
- evidence-based U1 auxiliary load budget.

Until then, auxiliary converter MPN/topology remains **REVALIDATE / OPEN**, not frozen.
