# PB-08 degraded-mode / single-motor-failure decision contract

Status: EVIDENCE CONTRACT / NO ARCHITECTURE FREEZE

## Purpose
Close the non-mass half of S1R.2 without inferring a safety requirement from rotor count. This contract defines the evidence required before `degraded_operation_requirement` or `single_motor_failure_requirement` may become a controlled PB-08 value.

## Allowed decision classes
A controlled decision shall explicitly select exactly one class:
- `CONTROLLED_LANDING_AFTER_ONE_PROPULSION_AXIS_LOSS`: continued controlled flight is required only long enough to execute a defined landing response after loss of one propulsion axis.
- `CONTINUED_MISSION_AFTER_ONE_PROPULSION_AXIS_LOSS`: continued mission capability after one-axis loss is required; quantitative duration/control-authority criteria are mandatory.
- `NO_SINGLE_AXIS_LOSS_FLIGHT_REQUIREMENT`: no airborne controllability requirement after one propulsion-axis loss; the system-level safe response and rationale must still be explicitly controlled.
- `OTHER_CONTROLLED_REQUIREMENT`: allowed only with a complete normative requirement statement and quantitative acceptance criteria.

`OPEN`, `null`, missing evidence, or architecture-derived inference are not decisions.

## Mandatory evidence
A promoted decision requires all of:
1. unique decision/revision identifier and approver/authority;
2. normative requirement statement;
3. applicability to the PB-08 utility multirotor product family;
4. explicit selected decision class;
5. triggering failure boundary (minimum: complete loss of one propulsion axis; additional failures may be listed);
6. required vehicle response and prohibited unsafe responses;
7. quantitative acceptance criteria where the selected class claims controlled landing or continued mission;
8. source/evidence reference to an explicit user/system-safety decision, approved requirement, or controlled safety analysis;
9. architecture-independence attestation: Quad/Hexa shall be evaluated against the requirement, not used to invent it;
10. review status and date.

## Gate rule
This record can close only the degraded-mode requirement input to S1R.2. It cannot by itself freeze Quad/Hexa, MTOW, motor/prop, pack, G0 or G1. Rotor architecture still requires TR-084/TR-085 controlled installed-axis/structure mass evidence plus thrust/control-authority evidence applicable to the selected degraded-mode class.

## Anti-hallucination rule
No default is selected. In particular, Hexa does not automatically imply one-motor-out capability, and Quad does not automatically imply that such capability is waived. Unknown acceptance criteria remain OPEN/null.
