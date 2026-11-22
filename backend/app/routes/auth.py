import sqlite3
from backend.app.router import router
from backend.app.auth.security import create_jwt_token, verify_password
from backend.app.auth.rbac import require_auth
from backend.database.connection import get_db_context

@router.post("/api/v1/auth/token/")
def login_for_token(req: dict):
    body = req.get("body") or {}
    phone_number = body.get("phone_number", "").strip()
    password = body.get("password", "").strip()
    
    if not phone_number or not password:
        return 400, {"status": "ERROR", "message": "phone_number and password are required"}
        
    with get_db_context() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, phone_number, full_name, email, password_hash, role, jurisdiction_level, jurisdiction_id, can_authorize_alerts FROM users WHERE phone_number = ?", (phone_number,))
        user_row = cursor.fetchone()
        
    if not user_row or not verify_password(password, user_row["password_hash"]):
        return 401, {"status": "ERROR", "message": "Invalid credentials"}
        
    payload = {
        "user_id": user_row["id"],
        "phone_number": user_row["phone_number"],
        "full_name": user_row["full_name"],
        "role": user_row["role"],
        "jurisdiction": user_row["jurisdiction_level"],
        "can_authorize_alerts": bool(user_row["can_authorize_alerts"])
    }
    
    access_token = create_jwt_token(payload, expires_in_seconds=86400)
    refresh_token = create_jwt_token({"user_id": user_row["id"], "type": "refresh"}, expires_in_seconds=604800)
    
    return 200, {
        "status": "SUCCESS",
        "data": {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": 86400,
            "user": payload
        }
    }

@router.get("/api/v1/auth/me/")
def get_current_user_profile(req: dict):
    is_authed, user, msg = require_auth(req)
    if not is_authed:
        return 401, {"status": "UNAUTHORIZED", "message": msg}
    return 200, {"status": "SUCCESS", "data": user}
