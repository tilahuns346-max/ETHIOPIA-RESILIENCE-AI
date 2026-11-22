from dataclasses import dataclass
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    NATIONAL_EDRMC_OFFICER = "NATIONAL_EDRMC_OFFICER"
    REGIONAL_DIRECTOR = "REGIONAL_DIRECTOR"
    ZONAL_COORDINATOR = "ZONAL_COORDINATOR"
    WOREDA_FOCAL_PERSON = "WOREDA_FOCAL_PERSON"
    KEBELE_REPRESENTATIVE = "KEBELE_REPRESENTATIVE"
    FIRST_RESPONDER = "FIRST_RESPONDER"
    COMMUNITY_REPORTER = "COMMUNITY_REPORTER"

@dataclass
class User:
    id: str
    phone_number: str
    full_name: str
    email: Optional[str]
    password_hash: str
    role: UserRole
    jurisdiction_level: str
    jurisdiction_id: Optional[str]
    is_active: bool = True
    can_authorize_alerts: bool = False
    created_at: Optional[str] = None
