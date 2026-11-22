import uuid
import datetime
from backend.app.router import router
from backend.app.auth.rbac import extract_current_user
from backend.app.schemas.incident import validate_incident_payload
from backend.database.connection import get_db_context

@router.post("/api/v1/incidents/")
def create_incident(req: dict):
    body = req.get("body") or {}
    is_valid, err_msg, cleaned = validate_incident_payload(body)
    if not is_valid:
        return 400, {"status": "BAD_REQUEST", "message": err_msg}
        
    user = extract_current_user(req)
    reporter_id = user.get("user_id") if user else None
    reporter_phone = user.get("phone_number") if user else req.get("body", {}).get("contact_phone")
    
    incident_id = str(uuid.uuid4())
    year = datetime.datetime.utcnow().year
    
    with get_db_context() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as cnt FROM incidents")
        count = cursor.fetchone()["cnt"] + 1
        incident_number = f"INC-{year}-{count:05d}"
        
        cursor.execute("""
            INSERT INTO incidents (
                id, incident_number, hazard_type_code, kebele_code, woreda_code,
                title_en, title_am, description_raw, detected_language,
                latitude, longitude, altitude_m, estimated_affected_people,
                status, verification_status, reporter_user_id, reporter_phone,
                is_offline_submission, reported_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'REPORTED', 'UNVERIFIED', ?, ?, ?, CURRENT_TIMESTAMP)
        """, (
            incident_id, incident_number, cleaned["hazard_type_code"], cleaned["kebele_code"], cleaned["woreda_code"],
            cleaned["title_en"], cleaned["title_am"], cleaned["description_raw"], cleaned["detected_language"],
            cleaned["latitude"], cleaned["longitude"], cleaned["altitude_m"], cleaned["estimated_affected_people"],
            reporter_id, reporter_phone, 1 if cleaned["is_offline_submission"] else 0
        ))
        
    return 201, {
        "status": "CREATED",
        "data": {
            "incident_id": incident_id,
            "incident_number": incident_number,
            "status": "REPORTED",
            "verification_status": "UNVERIFIED",
            "reported_at": datetime.datetime.utcnow().isoformat() + "Z"
        }
    }
