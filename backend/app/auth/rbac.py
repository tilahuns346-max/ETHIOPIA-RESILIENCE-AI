from typing import List, Optional, Dict, Any, Tuple
from backend.app.auth.security import decode_jwt_token

def extract_current_user(req: dict) -> Optional[Dict[str, Any]]:
    auth_header = req.get("headers", {}).get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split("Bearer ")[1].strip()
    return decode_jwt_token(token)

def require_auth(req: dict) -> Tuple[bool, Optional[Dict[str, Any]], str]:
    user = extract_current_user(req)
    if not user:
        return False, None, "Authentication required. Invalid or expired token."
    return True, user, ""

def require_roles(req: dict, allowed_roles: List[str]) -> Tuple[bool, Optional[Dict[str, Any]], str]:
    is_authed, user, msg = require_auth(req)
    if not is_authed:
        return False, None, msg
        
    user_role = user.get("role", "")
    if user_role not in allowed_roles and user_role != "SUPER_ADMIN":
        return False, user, f"Forbidden: role {user_role} cannot access this resource."
        
    return True, user, ""
