from backend.app.router import router
from backend.database.connection import get_db_context

@router.get("/api/v1/analytics/overview/")
def get_analytics_overview(req: dict):
    with get_db_context() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as total_incidents FROM incidents")
        inc_count = cursor.fetchone()["total_incidents"]
        
        cursor.execute("SELECT COUNT(*) as verified_count FROM incidents WHERE status = 'VERIFIED'")
        ver_count = cursor.fetchone()["verified_count"]
        
        cursor.execute("SELECT COUNT(*) as active_alerts FROM alerts WHERE status IN ('APPROVED_BY_OFFICER', 'DISSEMINATED')")
        alert_count = cursor.fetchone()["active_alerts"]
        
        cursor.execute("SELECT COUNT(*) as deployed_teams FROM emergency_teams WHERE current_status != 'AVAILABLE'")
        deployed_teams = cursor.fetchone()["deployed_teams"]
        
        cursor.execute("SELECT hazard_type_code, COUNT(*) as cnt FROM incidents GROUP BY hazard_type_code")
        hazard_dist = [dict(r) for r in cursor.fetchall()]
        
    return 200, {
        "status": "SUCCESS",
        "data": {
            "total_incidents_reported": inc_count,
            "officially_verified_incidents": ver_count,
            "active_early_warning_alerts": alert_count,
            "deployed_response_units": deployed_teams,
            "hazard_distribution": hazard_dist,
            "national_threat_level": "ELEVATED" if alert_count > 0 else "NORMAL"
        }
    }
