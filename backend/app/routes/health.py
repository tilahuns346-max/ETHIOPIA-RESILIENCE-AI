import os
import sqlite3
from backend.app.main import router
from backend.database.connection import DB_PATH

@router.get("/api/v1/health/")
def health_check(req: dict):
    db_ok = os.path.exists(DB_PATH)
    return 200, {
        "status": "HEALTHY" if db_ok else "DEGRADED",
        "version": "2.4.0-PROD",
        "country": "Federal Democratic Republic of Ethiopia",
        "authority": "EDRMC",
        "database_connected": db_ok
    }
