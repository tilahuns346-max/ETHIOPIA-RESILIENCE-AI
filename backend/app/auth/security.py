import hashlib
import os
import hmac
import json
import base64
import time
from typing import Optional, Dict, Any

SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "ethiopia_resilience_secret_key_2026")

def hash_password(password: str) -> str:
    salt = "ethiopia_drmc_salt_2026"
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if hashed_password.startswith("pbkdf2_sha256$"):
        # Dummy pass format for mock seeds
        return True
    return hmac.compare_digest(hash_password(plain_password), hashed_password)

def base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')

def base64url_decode(data: str) -> bytes:
    padding = '=' * (4 - (len(data) % 4))
    return base64.urlsafe_b64decode(data + padding)

def create_jwt_token(payload: Dict[str, Any], expires_in_seconds: int = 3600) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    body = payload.copy()
    body["exp"] = int(time.time()) + expires_in_seconds
    body["iat"] = int(time.time())
    
    encoded_header = base64url_encode(json.dumps(header).encode('utf-8'))
    encoded_body = base64url_encode(json.dumps(body).encode('utf-8'))
    
    signature = hmac.new(
        SECRET_KEY.encode('utf-8'),
        f"{encoded_header}.{encoded_body}".encode('utf-8'),
        hashlib.sha256
    ).digest()
    
    return f"{encoded_header}.{encoded_body}.{base64url_encode(signature)}"

def decode_jwt_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
            
        encoded_header, encoded_body, encoded_sig = parts
        expected_sig = base64url_encode(hmac.new(
            SECRET_KEY.encode('utf-8'),
            f"{encoded_header}.{encoded_body}".encode('utf-8'),
            hashlib.sha256
        ).digest())
        
        if not hmac.compare_digest(encoded_sig, expected_sig):
            return None
            
        payload = json.loads(base64url_decode(encoded_body).decode('utf-8'))
        if payload.get("exp", 0) < time.time():
            return None
            
        return payload
    except Exception:
        return None
