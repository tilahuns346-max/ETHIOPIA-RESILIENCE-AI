from dataclasses import dataclass
from typing import Optional, List

@dataclass
class IncidentReport:
    id: str
    incident_number: str
    hazard_type_code: str
    kebele_code: Optional[str]
    woreda_id: Optional[str]
    title_en: str
    title_am: str
    description_raw: str
    detected_language: str
    latitude: float
    longitude: float
    altitude_m: Optional[float]
    estimated_affected_people: int
    status: str  # REPORTED, TRIAGED, VERIFIED, RESPONDING, CONTAINED, RESOLVED
    verification_status: str  # UNVERIFIED, COMMUNITY_CORROBORATED, OFFICIALLY_VERIFIED
    reporter_user_id: Optional[str]
    reporter_phone: Optional[str]
    is_offline_submission: bool
    reported_at: str
    ai_risk_score: Optional[float] = None
    cluster_id: Optional[str] = None

@dataclass
class IncidentVerification:
    id: str
    incident_id: str
    officer_user_id: str
    officer_name: str
    verification_decision: str  # OFFICIALLY_VERIFIED, REJECTED, NEEDS_MORE_INFO
    confirmed_severity: str
    verification_notes: str
    evidence_urls: List[str]
    verified_at: str
