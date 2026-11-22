def extract_spatial_features(rainfall_72h_mm: float, slope_deg: float, soil_sat: float):
    return {
        "rainfall_norm": min(rainfall_72h_mm / 200.0, 1.0),
        "slope_norm": min(slope_deg / 60.0, 1.0),
        "soil_sat_norm": max(0.0, min(soil_sat, 1.0)),
        "composite_hazard_indicator": (0.5 * min(rainfall_72h_mm / 200.0, 1.0) +
                                       0.3 * min(slope_deg / 60.0, 1.0) +
                                       0.2 * max(0.0, min(soil_sat, 1.0)))
    }
