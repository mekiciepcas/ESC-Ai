#!/usr/bin/env python3
"""Plan (and later safely instantiate) a new U1 schematic revision.

Default mode is dry-run only. This helper intentionally refuses to allocate a
revision while its parent readiness record is not explicitly READY. It never
edits LEGACY-B1 or U1-SCH-R000 in place.
"""
from __future__ import annotations
import argparse, json, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "planning"
REGISTER = PLAN / "SCHEMATIC_REVISION_REGISTER.json"
READINESS = PLAN / "U1_SCHEMATIC_ALLOCATION_READINESS.json"
SCAFFOLD = ROOT / "hardware_u1_scaffold"
REVROOT = ROOT / "hardware_u1_revisions"
PATTERN = re.compile(r"^U1-SCH-R(\d{3})$")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_register(reg):
    next_id = reg["revision_series"]["next_component_bearing_revision"]
    m = PATTERN.match(next_id)
    if not m:
        raise SystemExit(f"invalid next revision id: {next_id}")
    allocated = {r["revision_id"] for r in reg.get("allocated_revisions", [])}
    if next_id in allocated:
        raise SystemExit(f"next revision already allocated: {next_id}")
    return next_id


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--allocate", action="store_true", help="instantiate only when readiness status is READY")
    args = ap.parse_args()
    reg = load(REGISTER)
    next_id = validate_register(reg)
    readiness = load(READINESS) if READINESS.exists() else {"status":"BLOCKED"}
    target = REVROOT / next_id
    print(f"next_revision={next_id}")
    print(f"readiness={readiness.get('status','BLOCKED')}")
    print(f"target={target.relative_to(ROOT)}")
    if not args.allocate:
        print("DRY_RUN_ONLY=1")
        return 0
    if readiness.get("status") != "READY":
        print("REFUSED: parent G1/G2 page readiness is not READY", file=sys.stderr)
        return 3
    if target.exists():
        print("REFUSED: target already exists", file=sys.stderr)
        return 4
    if not SCAFFOLD.is_dir():
        print("REFUSED: frozen scaffold source missing", file=sys.stderr)
        return 5
    shutil.copytree(SCAFFOLD, target)
    manifest = target / "REVISION_MANIFEST.json"
    manifest.write_text(json.dumps({
        "revision_id": next_id,
        "status": "DRAFT",
        "parent_reference": "U1-SCH-R000",
        "requirement_refs": readiness.get("requirement_refs", []),
        "qualification_claim": "NONE",
        "physical_validation": "NOT_PERFORMED"
    }, indent=2) + "\n", encoding="utf-8")
    print("ALLOCATED_FILESYSTEM_SNAPSHOT=1")
    print("REGISTER_UPDATE_REQUIRED=1")
    print("NOTE: allocation is incomplete until register/traceability are updated in the same reviewed change.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
