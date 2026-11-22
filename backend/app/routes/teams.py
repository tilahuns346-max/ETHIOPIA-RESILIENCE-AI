from backend.app.main import router
from backend.database.connection import get_db_context

@router.get("/api/v1/teams/")
def list_teams(req: dict):
    with get_db_context() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM emergency_teams")
        rows = cursor.fetchall()
        
    return 200, {
        "status": "SUCCESS",
        "data": [dict(r) for r in rows]
    }
