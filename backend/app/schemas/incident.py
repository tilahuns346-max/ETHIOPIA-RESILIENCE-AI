from typing import Optional, Dict, Any, List

def validate_incident_payload(data: dict) -> Tuple[bool, str, dict]:
    if not isinstance(data, dict):
        return False, "Payload must be a JSON object", {}
        
    hazard_code = data.get("hazard_type_code")
    if not hazard_code:
        return False, "hazard_type_code is required", {}
        
    loc = data.get("location")
    if not loc or not isinstance(loc, dict) or "coordinates" not in loc:
        return False, "Valid GeoJSON Point location is required", {}
        
    coords = loc.get("coordinates")
    if not isinstance(coords, (list, tuple)) or len(coords) < 2:
        return False, "location.coordinates must contain [longitude, latitude]", {}
        
    lon, lat = float(coords[0]), float(coords[1])
    if not (3.4 <= lat <= 14.9 and 32.9 <= lon <= 48.0):
        return False, f"Coordinates [{lon}, {lat}] outside Ethiopian boundaries", {}
        
    cleaned = {
        "hazard_type_code": hazard_code,
        "kebele_code": data.get("kebele_code"),
        "woreda_code": data.get("woreda_code"),
        "title_en": data.get("title_en", "Community Hazard Report"),
        "title_am": data.get("title_am", "የማህበረሰብ አደጋ ሪፖርት"),
        "description_raw": data.get("description_raw", ""),
        "detected_language": data.get("detected_language", "am"),
        "latitude": lat,
        "longitude": lon,
        "altitude_m": data.get("altitude_m"),
        "estimated_affected_people": int(data.get("estimated_affected_people", 0)),
        "is_offline_submission": bool(data.get("is_offline_submission", False))
    }
    return True, "", cleaned
