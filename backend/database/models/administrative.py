from dataclasses import dataclass
from typing import Optional

@dataclass
class Region:
    id: str
    code: str
    name_en: str
    name_am: str
    capital_city: str
    population: int
    area_sq_km: float

@dataclass
class Zone:
    id: str
    region_id: str
    code: str
    name_en: str
    name_am: str
    focal_officer_phone: Optional[str] = None

@dataclass
class Woreda:
    id: str
    zone_id: str
    code: str
    name_en: str
    name_am: str
    risk_level: str
    latitude: float
    longitude: float

@dataclass
class Kebele:
    id: str
    woreda_id: str
    code: str
    name_en: str
    name_am: str
    latitude: float
    longitude: float
