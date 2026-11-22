from backend.app.main import router
from backend.database.connection import get_db_context

@router.get("/api/v1/incidents/")
def list_incidents(req: dict):
    params = req.get("query_params") or {}
    hazard = params.get("hazard")
    status = params.get("status")
    woreda = params.get("woreda")
    limit = int(params.get("limit", 50))
    
    query = "SELECT * FROM incidents WHERE 1=1"
    args = []
    
    if hazard:
        query += " AND hazard_type_code = ?"
        args.append(hazard)
    if status:
        query += " AND status = ?"
        args.append(status)
    if woreda:
        query += " AND woreda_code = ?"
        args.append(woreda)
        
    query += " ORDER BY reported_at DESC LIMIT ?"
    args.append(limit)
    
    with get_db_context() as conn:
        cursor = conn.cursor()
        cursor.execute(query, tuple(args))
        rows = cursor.fetchall()
        
    results = []
    for r in rows:
        d = dict(r)
        d["location"] = {
            "type": "Point",
            "coordinates": [d["longitude"], d["latitude"]]
        }
        results.append(d)
        
    return 200, {
        "status": "SUCCESS",
        "count": len(results),
        "data": results
    }
