import random

def generate_ethiopian_hazard_dataset(n_samples: int = 500):
    return [
        {"rainfall": round(random.uniform(10.0, 250.0), 1),
         "slope": round(random.uniform(5.0, 55.0), 1),
         "soil_sat": round(random.uniform(0.2, 0.99), 2),
         "hazard_occurred": 1 if random.random() > 0.6 else 0}
        for _ in range(n_samples)
    ]
