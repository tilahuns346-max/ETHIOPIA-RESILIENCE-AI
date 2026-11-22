import uuid
import datetime
from backend.app.router import router
from backend.app.auth.rbac import require_roles
from backend.database.connection import get_db_context

@router.post("/api/v1/alerts/{alert_id}/broadcast/")
def broadcast_alert(req: dict):
    is_ok, user, msg = require_roles(req, ["NATIONAL_EDRMC_OFFICER", "REGIONAL_DIRECTOR", "SUPER_ADMIN"])
    if not is_ok:
        return 403, {"status": "FORBIDDEN", "message": msg}
        
    alert_id = req.get("path_params", {}).get("alert_id")
    
    with get_db_context() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alerts WHERE id = ?", (alert_id,))
        alert = cursor.fetchone()
        
        if not alert:
            return 404, {"status": "NOT_FOUND", "message": "Alert not found"}
            
        if alert["status"] != "APPROVED_BY_OFFICER":
            return 400, {
                "status": "SAFETY_INVARIANT_VIOLATION",
                "message": "Cannot broadcast unapproved alert. Officer cryptographic sign-off is mandatory."
            }
            
        cursor.execute("UPDATE alerts SET status = 'DISSEMINATED', disseminated_at = CURRENT_TIMESTAMP WHERE id = ?", (alert_id,))
        
        # Log to broadcast table
        log_id = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO broadcast_logs (id, alert_id, channel, target_area, recipients_estimate, status, dispatched_at)
            VALUES (?, ?, 'SMS_CELL_BROADCAST', ?, 5400, 'TRANSMITTING', CURRENT_TIMESTAMP)
        """, (log_id, alert_id, alert["affected_woredas"]))
        
    return 202, {
        "status": "ACCEPTED",
        "data": {
            "alert_id": alert_id,
            "broadcast_task_id": f"task-ethio-telecom-{uuid.uuid4().hex[:8]}",
            "channels": ["SMS_CELL_BROADCAST", "MOBILE_PUSH", "RADIO_BULLETIN_API"],
            "target_population_estimate": 5400,
            "languages": ["am", "en", "om"]
        }
    }
