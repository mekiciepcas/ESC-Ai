"""Refresh evidence and project views. No manufacturing release implied."""
from pathlib import Path
import argparse,subprocess,sys,json,hashlib,datetime
root=Path(__file__).resolve().parents[1]
a=argparse.ArgumentParser();a.add_argument('--verify-schematic',action='store_true');args=a.parse_args()
cli=Path('C:/Program Files/KiCad/10.0/bin/kicad-cli.exe')
def run(command):
    subprocess.run([str(x) for x in command],cwd=root.parent,check=True)
if args.verify_schematic:
    run([cli,'sch','export','netlist','--output',root/'verification/ESC_3kW_B1.net',root/'hardware_b1/ESC_3kW_B1.kicad_sch'])
    run([cli,'sch','erc','--format','json','--output',root/'verification/erc_b1.json',root/'hardware_b1/ESC_3kW_B1.kicad_sch'])
    run([sys.executable,root/'hardware_b1/verify_b1.py'])
    run([sys.executable,root/'pcb_b1/tools/audit_interfaces.py'])
    files=list((root/'hardware_b1').glob('*.kicad_sch'))+[root/'hardware_b1/ESC_B1.kicad_sym',root/'hardware_b1/connection_manifest.json']
    manifest={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    (root/'verification/b1_evidence_manifest.json').write_text(json.dumps({'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'schematic ERC and interface checks, not PCB or physical validation','sha256':manifest},indent=2),encoding='utf-8')
run([sys.executable,root/'planning/render_roadmap.py'])
run([sys.executable,root/'dashboard/build_dashboard.py'])
print('Roadmap and HTML refreshed. Physical/production release status unchanged.')
