import time
from typing import Dict, Tuple

class RateLimiter:
    def __init__(self, max_requests: int = 120, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.records: Dict[str, list] = {}

    def is_allowed(self, client_ip: str) -> bool:
        now = time.time()
        timestamps = self.records.get(client_ip, [])
        valid_timestamps = [t for t in timestamps if now - t < self.window_seconds]
        
        if len(valid_timestamps) >= self.max_requests:
            return False
            
        valid_timestamps.append(now)
        self.records[client_ip] = valid_timestamps
        return True

rate_limiter = RateLimiter()

def apply_security_headers(headers: dict) -> dict:
    headers["X-Frame-Options"] = "DENY"
    headers["X-Content-Type-Options"] = "nosniff"
    headers["X-XSS-Protection"] = "1; mode=block"
    headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return headers
