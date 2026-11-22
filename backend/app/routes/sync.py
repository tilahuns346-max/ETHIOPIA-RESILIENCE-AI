import uuid
import datetime
from backend.app.router import router
from backend.database.connection import get_db_context

@router.post("/api/v1/incidents/sync/")
def sync_offline_batch(req: dict):
    body = req.get("body") or {}
    batch_id = body.get("batch_id") or str(uuid.uuid4())
    device_id = body.get("device_id", "UNKNOWN_DEVICE")
    reports = body.get("reports", [])
    
    if not isinstance(reports, list) or len(reports) == 0:
        return 400, {"status": "BAD_REQUEST", "message": "reports array cannot be empty"}
        
    year = datetime.datetime.utcnow().year
    assigned_numbers = []
    
    with get_db_context() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as cnt FROM incidents")
        current_cnt = cursor.fetchone()["cnt"]
        
        for idx, rep in enumerate(reports):
            inc_id = str(uuid.uuid4())
            inc_num = f"INC-{year}-{current_cnt + idx + 1:05d}"
            loc = rep.get("location", {}).get("coordinates", [36.9214, 6.2241])
            lon, lat = float(loc[0]), float(loc[1])
            
            cursor.execute("""
                INSERT INTO incidents (
                    id, incident_number, hazard_type_code, title_en, title_am,
                    description_raw, latitude, longitude, is_offline_submission,
                    status, verification_status, reported_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, 'REPORTED', 'UNVERIFIED', CURRENT_TIMESTAMP)
            """, (
                inc_id, inc_num, rep.get("hazard_type_code", "HAZ-LANDSLIDE"),
                rep.get("title_en", "Offline Field Report"),
                rep.get("title_am", "ከመስመር ውጭ የተላከ ሪፖርት"),
                rep.get("description_raw", ""),
                lat, lon
            ))
            assigned_numbers.append(inc_num)
            
    return 202, {
        "status": "ACCEPTED",
        "data": {
            "batch_id": batch_id,
            "device_id": device_id,
            "processed_count": len(reports),
            "assigned_incident_numbers": assigned_numbers
        }
    }
