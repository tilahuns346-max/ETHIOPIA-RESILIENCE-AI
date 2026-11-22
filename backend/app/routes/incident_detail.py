from backend.app.router import router
from backend.database.connection import get_db_context

@router.get("/api/v1/incidents/{incident_id}/")
def get_incident_detail(req: dict):
    incident_id = req.get("path_params", {}).get("incident_id")
    
    with get_db_context() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM incidents WHERE id = ? OR incident_number = ?", (incident_id, incident_id))
        row = cursor.fetchone()
        
        if not row:
            return 404, {"status": "NOT_FOUND", "message": f"Incident {incident_id} not found"}
            
        cursor.execute("SELECT * FROM verifications WHERE incident_id = ? ORDER BY verified_at DESC", (row["id"],))
        verif_rows = cursor.fetchall()
        
    data = dict(row)
    data["location"] = {
        "type": "Point",
        "coordinates": [data["longitude"], data["latitude"]]
    }
    data["verifications"] = [dict(v) for v in verif_rows]
    
    return 200, {"status": "SUCCESS", "data": data}
