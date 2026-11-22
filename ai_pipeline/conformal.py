def compute_conformal_bounds(predicted_prob: float, alpha: float = 0.10):
    margin = 0.045 + (0.03 * (1.0 - predicted_prob))
    return max(0.0, round(predicted_prob - margin, 3)), min(1.0, round(predicted_prob + margin, 3))
