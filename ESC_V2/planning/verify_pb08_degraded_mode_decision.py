#!/usr/bin/env python3
"""Fail-closed checker for PB-08 degraded-mode decision records. Validates evidence completeness only; never freezes architecture or advances gates."""
import json, sys
from pathlib import Path

ALLOWED={
 "CONTROLLED_LANDING_AFTER_ONE_PROPULSION_AXIS_LOSS",
 "CONTINUED_MISSION_AFTER_ONE_PROPULSION_AXIS_LOSS",
 "NO_SINGLE_AXIS_LOSS_FLIGHT_REQUIREMENT",
 "OTHER_CONTROLLED_REQUIREMENT",
}

def main(path):
 d=json.loads(Path(path).read_text())
 e=[]
 req=lambda cond,msg: e.append(msg) if not cond else None
 req(d.get("decision_id"),"decision_id missing")
 req(d.get("revision"),"revision missing")
 req(d.get("date"),"date missing")
 a=d.get("authority",{})
 req(a.get("type") and a.get("reference") and a.get("approver"),"controlled authority incomplete")
 c=d.get("selected_decision_class")
 req(c in ALLOWED,"selected_decision_class missing/invalid")
 req(d.get("normative_requirement_statement"),"normative requirement missing")
 f=d.get("failure_boundary",{})
 req(f.get("single_complete_propulsion_axis_loss") is True,"single-axis-loss boundary not explicitly applicable")
 req(d.get("required_vehicle_response"),"required vehicle response missing")
 req(len(d.get("prohibited_unsafe_responses",[]))>0,"prohibited unsafe responses missing")
 req(len(d.get("evidence_refs",[]))>0,"evidence reference missing")
 req(d.get("architecture_independence_attestation") is True,"architecture-independence attestation missing")
 r=d.get("review",{})
 req(r.get("reviewed") is True and r.get("reviewer") and r.get("date"),"review incomplete")
 ac=d.get("acceptance_criteria",{})
 if c=="CONTROLLED_LANDING_AFTER_ONE_PROPULSION_AXIS_LOSS": req(ac.get("controlled_landing_duration_s") is not None,"controlled-landing duration criterion missing")
 if c=="CONTINUED_MISSION_AFTER_ONE_PROPULSION_AXIS_LOSS": req(ac.get("continued_mission_duration_s") is not None,"continued-mission duration criterion missing")
 if c=="OTHER_CONTROLLED_REQUIREMENT": req(len(ac.get("other",[]))>0,"OTHER class quantitative acceptance criteria missing")
 req(d.get("architecture_frozen") is False,"record must not claim architecture freeze")
 req(d.get("g0_advanced") is False and d.get("g1_advanced") is False,"record must not claim gate advance")
 out={"status":"PASS_RECORD_COMPLETENESS" if not e else "FAIL","errors":e,"physical_qualification":False,"architecture_frozen":False,"g0_advanced":False,"g1_advanced":False}
 print(json.dumps(out,indent=2))
 return 0 if not e else 1
if __name__=="__main__":
 if len(sys.argv)!=2: print("usage: verify_pb08_degraded_mode_decision.py RECORD.json",file=sys.stderr); sys.exit(2)
 sys.exit(main(sys.argv[1]))
