#!/usr/bin/env python3
"""Regression harness: PB-08 evidence verifiers must reject their unpopulated templates.

This is a repository-safety test only. It does not validate physical evidence or advance gates.
"""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
CASES = [
    ("verify_pb08_axis_structure_mass.py", "PB08_INSTALLED_AXIS_STRUCTURE_MASS_RESULT.template.json"),
    ("verify_pb08_degraded_mode_decision.py", "PB08_DEGRADED_MODE_DECISION_RESULT.template.json"),
    ("verify_pb08_auxiliary_demand.py", "PB08_TRACTION_PACK_AUXILIARY_DEMAND_RESULT.template.json"),
    ("verify_pb08_installed_pack_resistance.py", "PB08_INSTALLED_PACK_RESISTANCE_MEASUREMENT_RESULT.template.json"),
    ("verify_pb08_p50b_ocv_rdc.py", "PB08_P50B_OCV_RDC_MEASUREMENT_RESULT.template.json"),
]


def main() -> int:
    failures = []
    for verifier, template in CASES:
        proc = subprocess.run(
            [sys.executable, str(ROOT / verifier), str(ROOT / template)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if proc.returncode == 0:
            failures.append(f"{verifier} unexpectedly accepted unpopulated {template}")
        else:
            print(f"PASS fail-closed: {verifier} rejected {template} (rc={proc.returncode})")
    if failures:
        print("FAIL: fail-closed regression detected", file=sys.stderr)
        for item in failures:
            print(f" - {item}", file=sys.stderr)
        return 1
    print(f"PASS: all {len(CASES)} PB-08 unpopulated evidence templates were rejected")
    print("NOTE: this proves fail-closed behavior only; it is not physical qualification or gate closure.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
