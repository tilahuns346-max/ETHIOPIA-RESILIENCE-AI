import uuid
import json
from backend.app.main import router
from backend.app.auth.rbac import require_roles
from backend.database.connection import get_db_context

@router.post("/api/v1/incidents/{incident_id}/verify/")
def verify_incident(req: dict):
    is_ok, user, msg = require_roles(req, ["WOREDA_FOCAL_PERSON", "KEBELE_REPRESENTATIVE", "NATIONAL_EDRMC_OFFICER", "REGIONAL_DIRECTOR"])
    if not is_ok:
        return 403, {"status": "FORBIDDEN", "message": msg}
        
    incident_id = req.get("path_params", {}).get("incident_id")
    body = req.get("body") or {}
    decision = body.get("verification_decision", "OFFICIALLY_VERIFIED")
    severity = body.get("confirmed_severity", "LEVEL_3_HIGH")
    notes = body.get("verification_notes", "")
    evidence = json.dumps(body.get("ground_evidence_urls", []))
    
    with get_db_context() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM incidents WHERE id = ?", (incident_id,))
        if not cursor.fetchone():
            return 404, {"status": "NOT_FOUND", "message": "Incident not found"}
            
        verif_id = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO verifications (
                id, incident_id, officer_user_id, officer_name,
                verification_decision, confirmed_severity, verification_notes,
                evidence_urls, verified_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (
            verif_id, incident_id, user.get("user_id"), user.get("full_name"),
            decision, severity, notes, evidence
        ))
        
        new_status = "VERIFIED" if decision == "OFFICIALLY_VERIFIED" else "REJECTED_FALSE_ALARM"
        cursor.execute("UPDATE incidents SET status = ?, verification_status = ? WHERE id = ?", (new_status, decision, incident_id))
        
    return 200, {
        "status": "SUCCESS",
        "data": {
            "incident_id": incident_id,
            "status": new_status,
            "verification_status": decision,
            "verified_by": user.get("full_name"),
            "confirmed_severity": severity
        }
    }
