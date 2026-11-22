"""
SAFETY INVARIANT (BR-01):
Official public warnings, evacuation orders, and multi-channel broadcasts CANNOT
be disseminated without explicit, cryptographic sign-off by a designated government officer.
"""
from typing import Tuple

def validate_alert_authorization_permission(user: dict, severity: str) -> Tuple[bool, str]:
    if not user.get("can_authorize_alerts", False):
        return False, "SAFETY INVARIANT (BR-01) VIOLATION: Officer lacks designated signing authority for emergency alerts."
        
    allowed_roles = ["NATIONAL_EDRMC_OFFICER", "REGIONAL_DIRECTOR", "SUPER_ADMIN"]
    if user.get("role") not in allowed_roles:
        return False, f"Role {user.get('role')} cannot authorize high-level disaster alerts."
        
    return True, ""
