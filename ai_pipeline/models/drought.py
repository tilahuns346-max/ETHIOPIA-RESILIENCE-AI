class PastoralDroughtModel:
    def compute_drought_severity(self, ndvi_anomaly: float, consecutive_dry_dekads: int) -> str:
        if consecutive_dry_dekads >= 6 and ndvi_anomaly < -0.35:
            return "LEVEL_4_CRITICAL"
        elif consecutive_dry_dekads >= 4 and ndvi_anomaly < -0.20:
            return "LEVEL_3_HIGH"
        elif consecutive_dry_dekads >= 2:
            return "LEVEL_2_MODERATE"
        return "LEVEL_1_LOW"

drought_model = PastoralDroughtModel()
