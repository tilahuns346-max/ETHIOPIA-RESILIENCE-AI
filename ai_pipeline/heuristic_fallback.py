def offline_heuristic_risk(rainfall_mm: float, slope_deg: float) -> str:
    if rainfall_mm > 100 and slope_deg > 30:
        return "LEVEL_4_CRITICAL"
    return "LEVEL_3_HIGH" if rainfall_mm > 60 else "LEVEL_2_MODERATE"
