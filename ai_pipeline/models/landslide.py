import math

class LandslideRiskPredictor:
    def __init__(self, model_version: str = "v2.4.1"):
        self.version = model_version
    def predict_probability(self, rainfall_mm: float, slope_degrees: float, soil_saturation: float) -> float:
        z = (0.025 * rainfall_mm) + (0.05 * slope_degrees) + (2.5 * soil_saturation) - 4.5
        return round(1.0 / (1.0 + math.exp(-z)), 4)

landslide_model = LandslideRiskPredictor()
