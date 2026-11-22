import unittest
from backend.app.auth.security import create_jwt_token, decode_jwt_token, hash_password
from backend.app.services.safety_guardrail import validate_alert_authorization_permission
from backend.app.schemas.incident import validate_incident_payload

class TestBackendEndpoints(unittest.TestCase):
    def test_jwt_encoding_decoding(self):
        payload = {"user_id": "usr_test_123", "role": "NATIONAL_EDRMC_OFFICER"}
        token = create_jwt_token(payload, expires_in_seconds=60)
        decoded = decode_jwt_token(token)
        self.assertIsNotNone(decoded)
        self.assertEqual(decoded["user_id"], "usr_test_123")
        
    def test_safety_invariant_br01(self):
        unauthorized_user = {"user_id": "u1", "role": "COMMUNITY_REPORTER", "can_authorize_alerts": False}
        allowed, msg = validate_alert_authorization_permission(unauthorized_user, "LEVEL_4_CRITICAL")
        self.assertFalse(allowed)
        self.assertIn("BR-01", msg)
        
        authorized_officer = {"user_id": "u2", "role": "NATIONAL_EDRMC_OFFICER", "can_authorize_alerts": True}
        allowed, _ = validate_alert_authorization_permission(authorized_officer, "LEVEL_4_CRITICAL")
        self.assertTrue(allowed)

    def test_incident_validation_bounds(self):
        # Point inside Ethiopia
        valid_payload = {
            "hazard_type_code": "HAZ-LANDSLIDE",
            "location": {"coordinates": [36.9214, 6.2241]}
        }
        ok, _, _ = validate_incident_payload(valid_payload)
        self.assertTrue(ok)
        
        # Point outside Ethiopia
        invalid_payload = {
            "hazard_type_code": "HAZ-LANDSLIDE",
            "location": {"coordinates": [-0.1278, 51.5074]}
        }
        ok, err, _ = validate_incident_payload(invalid_payload)
        self.assertFalse(ok)
        self.assertIn("outside Ethiopian boundaries", err)

if __name__ == "__main__":
    unittest.main()
