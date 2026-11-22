from dataclasses import dataclass
from typing import Optional

@dataclass
class HazardType:
    id: str
    code: str
    name_en: str
    name_am: str
    category: str  # HYDROLOGICAL, GEOLOGICAL, CLIMATOLOGICAL, METEOROLOGICAL
    description_en: str
    description_am: str
    icon_name: str
    color_code: str
    default_warning_radius_km: float

@dataclass
class HistoricalDisaster:
    id: str
    hazard_code: str
    region_code: str
    woreda_name: str
    year_gregorian: int
    affected_population: int
    economic_loss_etb: float
    details: str
