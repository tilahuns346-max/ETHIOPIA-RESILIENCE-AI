import unittest
from ai_pipeline.models.landslide import landslide_model
from ai_pipeline.validator import validate_model_sanity

class TestAIModels(unittest.TestCase):
    def test_landslide_predictions(self):
        self.assertTrue(landslide_model.predict_probability(180.0, 42.0, 0.95) > 0.85)
    def test_model_sanity(self):
        self.assertTrue(validate_model_sanity(landslide_model))

if __name__ == "__main__":
    unittest.main()
