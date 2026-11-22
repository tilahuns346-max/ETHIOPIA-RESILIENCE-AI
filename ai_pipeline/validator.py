def validate_model_sanity(predictor) -> bool:
    return predictor.predict_probability(0.0, 0.0, 0.1) < 0.10 and predictor.predict_probability(200.0, 45.0, 0.95) > 0.85
