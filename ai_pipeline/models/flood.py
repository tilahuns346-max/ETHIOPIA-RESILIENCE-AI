class RiverineFloodEstimator:
    def estimate_inundation_risk(self, catchment_rainfall_mm: float, upstream_discharge_m3s: float) -> float:
        score = (catchment_rainfall_mm / 150.0) * 0.6 + (upstream_discharge_m3s / 800.0) * 0.4
        return round(min(max(score, 0.0), 1.0), 4)

flood_model = RiverineFloodEstimator()
