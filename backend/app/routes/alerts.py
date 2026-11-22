import uuid
import json
import datetime
from backend.app.main import router
from backend.app.auth.rbac import require_auth
from backend.app.services.safety_guardrail import validate_alert_authorization_permission
from backend.database.connection import get_db_context

@router.get("/api/v1/alerts/")
def list_alerts(req: dict):
    with get_db_context() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alerts ORDER BY created_at DESC")
        rows = cursor.fetchall()
        
    results = []
    for r in rows:
        d = dict(r)
        d["affected_woredas"] = json.loads(d["affected_woredas"]) if d["affected_woredas"] else []
        results.append(d)
    return 200, {"status": "SUCCESS", "data": results}

@router.post("/api/v1/alerts/{alert_id}/authorize/")
def authorize_alert(req: dict):
    is_authed, user, msg = require_auth(req)
    if not is_authed:
        return 401, {"status": "UNAUTHORIZED", "message": msg}
        
    alert_id = req.get("path_params", {}).get("alert_id")
    body = req.get("body") or {}
    signature = body.get("officer_digital_signature", "").strip()
    reasoning = body.get("approval_reasoning", "").strip()
    
    if not signature:
        return 400, {"status": "BAD_REQUEST", "message": "Cryptographic officer signature required"}
        
    with get_db_context() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alerts WHERE id = ?", (alert_id,))
        alert = cursor.fetchone()
        
        if not alert:
            return 404, {"status": "NOT_FOUND", "message": f"Alert {alert_id} not found"}
            
        is_safe, safety_err = validate_alert_authorization_permission(user, alert["severity"])
        if not is_safe:
            return 403, {"status": "SAFETY_INVARIANT_BLOCKED", "message": safety_err}
            
        cursor.execute("""
            UPDATE alerts
            SET status = 'APPROVED_BY_OFFICER',
                approved_by = ?,
                approved_at = CURRENT_TIMESTAMP,
                officer_digital_signature = ?
            WHERE id = ?
        """, (user.get("full_name"), signature, alert_id))
        
    return 200, {
        "status": "SUCCESS",
        "data": {
            "alert_id": alert_id,
            "status": "APPROVED_BY_OFFICER",
            "approved_by": user.get("full_name"),
            "approved_at": datetime.datetime.utcnow().isoformat() + "Z",
            "broadcast_queued": True
        }
    }
