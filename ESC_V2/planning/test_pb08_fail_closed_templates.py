#!/usr/bin/env python3
"""Regression harness: PB-08 evidence verifiers must reject unpopulated templates.

Repository-safety test only. It does not validate physical evidence or advance gates.
The harness fails on coverage drift and also distinguishes an intentional fail-closed
rejection from an interpreter/runtime crash by requiring each verifier's documented
blank-template rejection exit code and structured FAIL marker.
"""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
# verifier, controlled blank template, expected rejection rc, required output marker
CASES = [
    ("verify_pb08_axis_structure_mass.py", "PB08_INSTALLED_AXIS_STRUCTURE_MASS_RESULT.template.json", 2, '"schema_check": "FAIL"'),
    ("verify_pb08_degraded_mode_decision.py", "PB08_DEGRADED_MODE_DECISION_RESULT.template.json", 1, '"status": "FAIL"'),
    ("verify_pb08_auxiliary_demand.py", "PB08_TRACTION_PACK_AUXILIARY_DEMAND_RESULT.template.json", 1, '"result": "FAIL"'),
    ("verify_pb08_installed_pack_resistance.py", "PB08_INSTALLED_PACK_RESISTANCE_MEASUREMENT_RESULT.template.json", 2, '"status": "FAIL_CLOSED"'),
    ("verify_pb08_p50b_ocv_rdc.py", "PB08_P50B_OCV_RDC_MEASUREMENT_RESULT.template.json", 2, '"evidence_record_valid": false'),
]


def main() -> int:
    failures = []
    mapped_templates = {template for _, template, _, _ in CASES}
    discovered_templates = {p.name for p in ROOT.glob("PB08_*RESULT.template.json")}

    unmapped = sorted(discovered_templates - mapped_templates)
    stale = sorted(mapped_templates - discovered_templates)
    if unmapped:
        failures.append("unmapped PB-08 result template(s): " + ", ".join(unmapped))
    if stale:
        failures.append("mapped PB-08 result template(s) missing from repository: " + ", ".join(stale))

    for verifier, template, expected_rc, fail_marker in CASES:
        verifier_path = ROOT / verifier
        template_path = ROOT / template
        if not verifier_path.is_file():
            failures.append(f"mapped verifier missing: {verifier}")
            continue
        if not template_path.is_file():
            continue
        proc = subprocess.run(
            [sys.executable, str(verifier_path), str(template_path)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if proc.returncode != expected_rc:
            failures.append(
                f"{verifier} returned rc={proc.returncode}; expected controlled blank-template rejection rc={expected_rc}"
            )
            continue
        if fail_marker not in proc.stdout:
            failures.append(
                f"{verifier} returned expected rc={expected_rc} but lacked structured rejection marker {fail_marker!r}"
            )
            continue
        print(f"PASS fail-closed: {verifier} rejected {template} with controlled rc={expected_rc}")

    if failures:
        print("FAIL: PB-08 fail-closed/coverage regression detected", file=sys.stderr)
        for item in failures:
            print(f" - {item}", file=sys.stderr)
        return 1
    print(f"PASS: all {len(CASES)} mapped PB-08 unpopulated evidence templates produced controlled fail-closed rejection")
    print("PASS: every discovered PB08_*RESULT.template.json has an explicit verifier mapping")
    print("NOTE: this proves repository fail-closed/coverage behavior only; it is not physical qualification or gate closure.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
