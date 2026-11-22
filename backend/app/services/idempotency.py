from typing import Dict, Any, Tuple

_PROCESSED_IDEMPOTENCY_KEYS: Dict[str, Any] = {}

def check_or_record_idempotency(key: str, response_data: Any) -> Tuple[bool, Any]:
    if not key:
        return False, None
    if key in _PROCESSED_IDEMPOTENCY_KEYS:
        return True, _PROCESSED_IDEMPOTENCY_KEYS[key]
    _PROCESSED_IDEMPOTENCY_KEYS[key] = response_data
    return False, None
