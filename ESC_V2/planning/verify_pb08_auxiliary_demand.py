#!/usr/bin/env python3
"""Fail-closed verifier for PB08 traction-pack auxiliary demand evidence.

This tool validates completeness and arithmetic only. It cannot create engineering
or physical evidence and cannot freeze pack current or advance G1.
"""
import json, math, sys
from pathlib import Path

TOL = 1e-6

def fail(msg, errors): errors.append(msg)
def finite_pos(x): return isinstance(x,(int,float)) and math.isfinite(x) and x > 0

def main():
    if len(sys.argv) != 2:
        print("usage: verify_pb08_auxiliary_demand.py RESULT.json"); return 2
    p=Path(sys.argv[1]); d=json.loads(p.read_text(encoding="utf-8")); errors=[]
    cfg=d.get("configuration",{}); v=cfg.get("loaded_pack_voltage_V")
    for k in ("vehicle_configuration_id","esc_u1_revision","pack_configuration_id","operating_mode"):
        if not cfg.get(k): fail(f"missing configuration.{k}",errors)
    if not finite_pos(v): fail("loaded_pack_voltage_V must be positive",errors)
    loads=d.get("loads")
    if not isinstance(loads,list) or not loads: fail("loads must be a non-empty enumeration",errors); loads=[]
    aux_p=0.0
    for i,r in enumerate(loads):
        tag=f"loads[{i}]"
        for k in ("load_id","function","hardware_mpn_or_controlled_configuration","conversion_path","condition_basis","evidence_reference","evidence_type"):
            if not r.get(k): fail(f"{tag}.{k} missing",errors)
        if r.get("traction_pack_fed") is not True: fail(f"{tag}.traction_pack_fed must be true for ledger rows",errors)
        if r.get("applicable_in_operating_mode") is not True: fail(f"{tag}.applicable_in_operating_mode must be true; non-applicable rows require separate configuration evidence",errors)
        eta=r.get("path_efficiency_fraction"); sim=r.get("simultaneity_fraction"); duty=r.get("duty_fraction")
        if not (isinstance(eta,(int,float)) and 0 < eta <= 1): fail(f"{tag}.path_efficiency_fraction invalid/OPEN",errors)
        if not (isinstance(sim,(int,float)) and 0 < sim <= 1): fail(f"{tag}.simultaneity_fraction invalid/OPEN",errors)
        if not (isinstance(duty,(int,float)) and 0 < duty <= 1): fail(f"{tag}.duty_fraction invalid/OPEN",errors)
        P=r.get("load_side_power_W"); vv=r.get("load_side_voltage_V"); ii=r.get("load_side_current_A")
        if finite_pos(P): load_p=P
        elif finite_pos(vv) and finite_pos(ii): load_p=vv*ii
        else: fail(f"{tag} needs positive load_side_power_W or voltage*current evidence",errors); continue
        if not all(isinstance(x,(int,float)) for x in (eta,sim,duty)) or not finite_pos(v): continue
        pack_p=load_p/eta*sim*duty; pack_i=pack_p/v; aux_p += pack_p
        rp=r.get("pack_input_power_W_reported"); ri=r.get("pack_current_A_reported")
        if not isinstance(rp,(int,float)) or abs(rp-pack_p)>max(TOL,abs(pack_p)*1e-6): fail(f"{tag}.pack_input_power_W_reported inconsistent",errors)
        if not isinstance(ri,(int,float)) or abs(ri-pack_i)>max(TOL,abs(pack_i)*1e-6): fail(f"{tag}.pack_current_A_reported inconsistent",errors)
    review=d.get("review",{})
    if review.get("all_simultaneously_active_traction_pack_loads_enumerated") is not True: fail("active-load enumeration attestation missing",errors)
    if review.get("unknown_loads_assigned_zero") is not False: fail("unknown loads must not be assigned zero",errors)
    for k in ("reviewer","review_date","raw_data_or_source_bundle_reference"):
        if not review.get(k): fail(f"review.{k} missing",errors)
    prop=d.get("propulsion",{}).get("pack_input_power_W")
    if not finite_pos(prop): fail("propulsion.pack_input_power_W missing",errors); prop=0.0
    totals=d.get("reported_totals",{}); total_p=prop+aux_p
    expected={"auxiliary_pack_input_power_W":aux_p,"auxiliary_pack_current_A":aux_p/v if finite_pos(v) else None,"total_pack_input_power_W":total_p,"total_pack_current_A":total_p/v if finite_pos(v) else None}
    for k,x in expected.items():
        y=totals.get(k)
        if x is None or not isinstance(y,(int,float)) or abs(y-x)>max(TOL,abs(x or 0)*1e-6): fail(f"reported_totals.{k} inconsistent/OPEN",errors)
    q=d.get("qualification",{})
    if q.get("pack_current_frozen") is not False or q.get("physical_qualification") is not False or q.get("g1_advanced") is not False:
        fail("qualification flags must remain false; this verifier cannot freeze/qualify/advance G1",errors)
    out={"verifier":"PB08-AUX-DEMAND-VERIFY-001","result":"FAIL" if errors else "PASS","errors":errors,"physical_qualification":False,"pack_current_frozen":False,"g1_advanced":False,"recomputed":expected}
    print(json.dumps(out,indent=2)); return 1 if errors else 0
if __name__=="__main__": raise SystemExit(main())
