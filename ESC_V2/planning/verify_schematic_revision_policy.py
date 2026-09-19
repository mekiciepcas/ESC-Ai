#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
from pathlib import Path

REGISTER = Path("ESC_V2/planning/SCHEMATIC_REVISION_REGISTER.json")
REV_ROOT = Path("ESC_V2/hardware_u1/revisions")
REV_RE = re.compile(r"^U1-SCH-R\d{3}$")


def fail(msg: str) -> None:
    raise SystemExit(f"FAIL: {msg}")


def git_show_json(ref: str, path: str):
    try:
        out = subprocess.check_output(["git", "show", f"{ref}:{path}"], text=True, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return None
    return json.loads(out)


def allocated_ids(register: dict) -> set[str]:
    ids = set()
    for item in register.get("allocated_revisions", []):
        rid = item.get("revision_id")
        if not rid or not REV_RE.match(rid):
            fail(f"invalid allocated revision_id: {rid!r}")
        if rid in ids:
            fail(f"duplicate allocated revision_id: {rid}")
        ids.add(rid)
    return ids


def validate_structure(root: Path, register: dict) -> None:
    rules = register.get("rules", {})
    required_true = [
        "electrical_schematic_changes_require_new_revision",
        "superseded_revisions_immutable",
        "legacy_b1_source_immutable",
        "full_hierarchical_snapshot_required",
        "release_requires_explicit_user_approval",
        "main_merge_requires_explicit_user_approval",
    ]
    for key in required_true:
        if rules.get(key) is not True:
            fail(f"revision register rule {key} must be true")

    baselines = register.get("baselines", [])
    baseline_ids = [x.get("revision_id") for x in baselines]
    if len(baseline_ids) != len(set(baseline_ids)):
        fail("duplicate baseline revision IDs")
    if "LEGACY-B1" not in baseline_ids or "U1-SCH-R000" not in baseline_ids:
        fail("LEGACY-B1 and U1-SCH-R000 baselines are required")

    next_id = register.get("revision_series", {}).get("next_component_bearing_revision")
    if not next_id or not REV_RE.match(next_id):
        fail("next_component_bearing_revision must match U1-SCH-Rxxx")

    current_ids = allocated_ids(register)
    if next_id in current_ids:
        fail(f"next_component_bearing_revision {next_id} is already allocated")

    if REV_ROOT.exists():
        disk_dirs = {p.name for p in REV_ROOT.iterdir() if p.is_dir() and REV_RE.match(p.name)}
        unregistered = sorted(disk_dirs - current_ids)
        missing_dirs = sorted(current_ids - disk_dirs)
        if unregistered:
            fail(f"revision directories exist but are not registered: {unregistered}")
        if missing_dirs:
            fail(f"registered revisions missing directories: {missing_dirs}")
        for rid in sorted(disk_dirs):
            manifest = REV_ROOT / rid / "revision_manifest.json"
            if not manifest.is_file():
                fail(f"{rid} missing revision_manifest.json")
            data = json.loads(manifest.read_text(encoding="utf-8"))
            if data.get("revision_id") != rid:
                fail(f"{rid} manifest revision_id mismatch")
            if data.get("branch") != "uav-rebaseline":
                fail(f"{rid} manifest branch must be uav-rebaseline")


def validate_changes(root: Path, register: dict, changed_files: list[str], base_ref: str | None) -> None:
    current_ids = allocated_ids(register)
    base_ids = set()
    if base_ref:
        base_register = git_show_json(base_ref, REGISTER.as_posix())
        if base_register:
            base_ids = allocated_ids(base_register)

    for raw in changed_files:
        path = raw.strip().replace("\\", "/")
        if not path:
            continue

        if path.startswith("ESC_V2/hardware_b1/") and path.endswith(".kicad_sch"):
            fail(f"legacy B1 schematic source is immutable: {path}")

        if path.startswith("ESC_V2/hardware_u1_scaffold/") and path.endswith(".kicad_sch"):
            fail(f"U1-SCH-R000 scaffold is frozen; create a new component-bearing revision instead: {path}")

        m = re.match(r"^ESC_V2/hardware_u1/revisions/(U1-SCH-R\d{3})/(.+)$", path)
        if not m:
            continue
        rid, rel = m.groups()
        if rid not in current_ids:
            fail(f"changed U1 revision {rid} is not allocated in the revision register")
        manifest = root / REV_ROOT / rid / "revision_manifest.json"
        if not manifest.is_file():
            fail(f"changed U1 revision {rid} has no revision_manifest.json")
        if base_ref and rid in base_ids and (rel.endswith(".kicad_sch") or rel.endswith(".kicad_pro")):
            fail(f"superseded/existing revision {rid} is immutable; allocate the next revision before changing {rel}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Validate ESC U1 schematic revision-control policy")
    ap.add_argument("--root", default=".")
    ap.add_argument("--changed-files", default=None, help="newline-separated changed-file list")
    ap.add_argument("--base-ref", default=None, help="git base ref used to detect already-existing revisions")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    register_path = root / REGISTER
    if not register_path.is_file():
        fail(f"missing revision register: {REGISTER}")
    register = json.loads(register_path.read_text(encoding="utf-8"))

    validate_structure(root, register)

    changed = []
    if args.changed_files:
        changed_path = Path(args.changed_files)
        if not changed_path.is_file():
            fail(f"changed-file list not found: {changed_path}")
        changed = changed_path.read_text(encoding="utf-8").splitlines()
        validate_changes(root, register, changed, args.base_ref)

    print("PASS")
    print(f"registered_component_bearing_revisions={len(allocated_ids(register))}")
    print(f"next_component_bearing_revision={register['revision_series']['next_component_bearing_revision']}")
    print(f"changed_files_checked={len(changed)}")


if __name__ == "__main__":
    main()
