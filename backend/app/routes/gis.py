from backend.app.router import router
from backend.database.connection import get_db_context

@router.get("/api/v1/gis/boundaries/")
def get_gis_boundaries(req: dict):
    with get_db_context() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM regions")
        regions = cursor.fetchall()
        
        cursor.execute("SELECT * FROM woredas")
        woredas = cursor.fetchall()
        
    features = []
    for w in woredas:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [w["longitude"], w["latitude"]]
            },
            "properties": {
                "woreda_code": w["code"],
                "name_en": w["name_en"],
                "name_am": w["name_am"],
                "risk_level": w["risk_level"]
            }
        })
        
    return 200, {
        "type": "FeatureCollection",
        "features": features
    }
