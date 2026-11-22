from backend.app.router import router
from backend.app.auth.rbac import require_roles
from backend.database.connection import get_db_context
import uuid

@router.get("/api/v1/users/")
def list_users(req: dict):
    is_ok, user, msg = require_roles(req, ["SUPER_ADMIN", "NATIONAL_EDRMC_OFFICER", "REGIONAL_DIRECTOR"])
    if not is_ok:
        return 403, {"status": "FORBIDDEN", "message": msg}
        
    with get_db_context() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, phone_number, full_name, email, role, jurisdiction_level, jurisdiction_id, can_authorize_alerts, is_active FROM users")
        rows = cursor.fetchall()
        
    return 200, {
        "status": "SUCCESS",
        "data": [dict(r) for r in rows]
    }
