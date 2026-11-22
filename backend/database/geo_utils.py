import math
from typing import Dict, Any, Tuple

def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates great circle distance in kilometers between two GPS coordinates."""
    R = 6371.0  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def point_to_geojson(latitude: float, longitude: float, properties: Dict[str, Any] = None) -> Dict[str, Any]:
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [longitude, latitude]
        },
        "properties": properties or {}
    }

def validate_ethiopian_coordinates(latitude: float, longitude: float) -> bool:
    """Checks if coordinate lies within Ethiopian territorial boundaries."""
    return 3.4 <= latitude <= 14.9 and 32.9 <= longitude <= 48.0
