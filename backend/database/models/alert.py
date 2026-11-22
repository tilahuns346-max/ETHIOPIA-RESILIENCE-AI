from dataclasses import dataclass
from typing import Optional, List

@dataclass
class EarlyWarningAlert:
    id: str
    alert_code: str
    title_en: str
    title_am: str
    hazard_type_code: str
    severity: str  # LEVEL_1_LOW, LEVEL_2_MODERATE, LEVEL_3_HIGH, LEVEL_4_CRITICAL
    status: str    # DRAFT, PENDING_HUMAN_REVIEW, APPROVED_BY_OFFICER, DISSEMINATED
    affected_woreda_ids: List[str]
    evacuation_order_issued: bool
    designated_shelter_points: List[dict]
    instructions_en: str
    instructions_am: str
    created_at: str
    approved_by: Optional[str] = None
    approved_at: Optional[str] = None
    officer_digital_signature: Optional[str] = None
    disseminated_at: Optional[str] = None

@dataclass
class AlertAuthorizationAudit:
    id: str
    alert_id: str
    officer_user_id: str
    officer_name: str
    officer_role: str
    digital_signature: str
    approval_reasoning: str
    authorized_at: str
