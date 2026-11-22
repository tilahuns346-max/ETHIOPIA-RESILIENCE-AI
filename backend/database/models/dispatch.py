from dataclasses import dataclass
from typing import Optional

@dataclass
class EmergencyResponseTeam:
    id: str
    team_name: str
    agency: str  # RED_CROSS, FIRE_BRIGADE, SEARCH_AND_RESCUE, MEDICAL_TRIAGE
    base_region: str
    base_woreda: str
    contact_phone: str
    personnel_count: int
    current_status: str  # AVAILABLE, DISPATCHED, ON_SCENE, RESTING
    current_latitude: float
    current_longitude: float

@dataclass
class TacticalTask:
    id: str
    task_code: str
    alert_id: Optional[str]
    incident_id: Optional[str]
    assigned_team_id: str
    task_type: str  # SEARCH_AND_RESCUE, EVACUATION, MEDICAL_FIRST_AID, RELIEF_DISTRIBUTION
    priority: str
    instructions_en: str
    instructions_am: str
    target_latitude: float
    target_longitude: float
    status: str  # PENDING, ACKNOWLEDGED, IN_PROGRESS, COMPLETED, CANCELLED
    dispatched_at: str
    completed_at: Optional[str] = None
