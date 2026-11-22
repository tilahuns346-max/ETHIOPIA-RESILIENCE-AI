import unittest
from backend.database.geo_utils import haversine_distance_km, validate_ethiopian_coordinates, point_to_geojson
from backend.database.models.administrative import Region, Woreda
from backend.database.models.user import UserRole

class TestDatabaseAndGeo(unittest.TestCase):
    def test_haversine_distance(self):
        # Distance between Kencho Shacha (Gofa) and Sawla
        dist = haversine_distance_km(6.2241, 36.9214, 6.2300, 36.9450)
        self.assertTrue(2.0 < dist < 4.0, f"Distance {dist} should be around 2.6 km")
        
    def test_coordinate_validation(self):
        self.assertTrue(validate_ethiopian_coordinates(9.0300, 38.7400))  # Addis Ababa
        self.assertTrue(validate_ethiopian_coordinates(6.2241, 36.9214))  # Gofa
        self.assertFalse(validate_ethiopian_coordinates(51.5074, -0.1278)) # London
        
    def test_point_to_geojson(self):
        geojson = point_to_geojson(9.0, 38.0, {"hazard": "flood"})
        self.assertEqual(geojson["geometry"]["coordinates"], [38.0, 9.0])
        self.assertEqual(geojson["properties"]["hazard"], "flood")
        
    def test_user_roles(self):
        self.assertEqual(UserRole.NATIONAL_EDRMC_OFFICER, "NATIONAL_EDRMC_OFFICER")
        self.assertEqual(UserRole.COMMUNITY_REPORTER, "COMMUNITY_REPORTER")

if __name__ == "__main__":
    unittest.main()
