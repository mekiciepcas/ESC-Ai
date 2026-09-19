#!/usr/bin/env python3
from pathlib import Path
import json, re, sys

ROOT = Path(__file__).resolve().parent
sch = ROOT / "ESC_U1_SCAFFOLD.kicad_sch"
matrix = ROOT / "U1_PAGE_READINESS.json"

errors = []
if not sch.exists(): errors.append("missing schematic")
if not matrix.exists(): errors.append("missing readiness matrix")
if errors:
    print("FAIL:", "; ".join(errors)); sys.exit(1)

s = sch.read_text(encoding="utf-8")
m = json.loads(matrix.read_text(encoding="utf-8"))

if "(symbol " in s:
    errors.append("scaffold unexpectedly contains component symbols")
for block in m["blocks"]:
    if block["id"] not in s:
        errors.append(f"block missing from schematic: {block['id']}")
    if block["status"] != "OPEN":
        errors.append(f"non-OPEN block in pre-G2 scaffold: {block['id']}")
    if block["kicad_component_population"] != "BLOCKED":
        errors.append(f"component population not blocked: {block['id']}")

forbidden = [
    r"\b13S\b", r"\b3\s*kW\b", r"\b20\s*kHz\b", r"\b40\s*kHz\b",
    r"\b60\s*A\b", r"\b80\s*A\b", r"\b120\s*A\b", r"\b150\s*A\b",
    r"CSD19536KTT", r"DRV8353", r"LM5164", r"STM32G474", r"TMS320F280041C"
]
for pat in forbidden:
    if re.search(pat, s, re.IGNORECASE):
        errors.append(f"forbidden premature baseline token in schematic: {pat}")

depth = 0; quoted = False; escaped = False
for ch in s:
    if quoted:
        if escaped: escaped = False
        elif ch == "\\": escaped = True
        elif ch == '"': quoted = False
    else:
        if ch == '"': quoted = True
        elif ch == "(": depth += 1
        elif ch == ")": depth -= 1
        if depth < 0:
            errors.append("unbalanced closing parenthesis")
            break
if depth != 0:
    errors.append(f"unbalanced S-expression depth={depth}")

if errors:
    print("FAIL")
    for e in errors: print(" -", e)
    sys.exit(1)

print("PASS")
print(f" blocks={len(m['blocks'])}")
print(" component_symbols=0")
print(" premature_baseline_tokens=0")
print(" s_expression_balance=0")
print(" note=kicad-cli/ERC not executed in this environment")
