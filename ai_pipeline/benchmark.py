import time
from ai_pipeline.models.landslide import landslide_model

def benchmark_inference_speed(iterations: int = 5000):
    start = time.time()
    for _ in range(iterations):
        landslide_model.predict_probability(140.0, 35.0, 0.9)
    return time.time() - start
