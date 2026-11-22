import uuid
import datetime
from backend.app.main import router
from backend.app.auth.rbac import require_roles
from backend.database.connection import get_db_context

@router.post("/api/v1/tasks/dispatch/")
def dispatch_task(req: dict):
    is_ok, user, msg = require_roles(req, ["NATIONAL_EDRMC_OFFICER", "REGIONAL_DIRECTOR", "ZONAL_COORDINATOR"])
    if not is_ok:
        return 403, {"status": "FORBIDDEN", "message": msg}
        
    body = req.get("body") or {}
    team_id = body.get("team_id")
    task_type = body.get("task_type", "SEARCH_AND_RESCUE")
    priority = body.get("priority", "LEVEL_3_HIGH")
    inst_en = body.get("instructions_en", "")
    inst_am = body.get("instructions_am", "")
    loc = body.get("target_location", {}).get("coordinates", [36.9220, 6.2250])
    
    task_id = str(uuid.uuid4())
    year = datetime.datetime.utcnow().year
    
    with get_db_context() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as cnt FROM tactical_tasks")
        cnt = cursor.fetchone()["cnt"] + 1
        task_code = f"TSK-{year}-{cnt:04d}"
        
        cursor.execute("""
            INSERT INTO tactical_tasks (
                id, task_code, alert_id, incident_id, assigned_team_id,
                task_type, priority, instructions_en, instructions_am,
                target_latitude, target_longitude, status, dispatched_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'PENDING', CURRENT_TIMESTAMP)
        """, (
            task_id, task_code, body.get("alert_id"), body.get("incident_id"),
            team_id, task_type, priority, inst_en, inst_am, loc[1], loc[0]
        ))
        
        cursor.execute("SELECT team_name FROM emergency_teams WHERE id = ?", (team_id,))
        team_row = cursor.fetchone()
        team_name = team_row["team_name"] if team_row else "Response Unit"
        
    return 201, {
        "status": "CREATED",
        "data": {
            "task_id": task_id,
            "task_code": task_code,
            "status": "PENDING",
            "dispatched_to_team": team_name
        }
    }

@router.patch("/api/v1/tasks/{task_id}/status/")
def update_task_status(req: dict):
    task_id = req.get("path_params", {}).get("task_id")
    body = req.get("body") or {}
    new_status = body.get("status", "IN_PROGRESS")
    
    with get_db_context() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tactical_tasks SET status = ? WHERE id = ?", (new_status, task_id))
        
    return 200, {"status": "SUCCESS", "data": {"task_id": task_id, "status": new_status}}
