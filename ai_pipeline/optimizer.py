def optimize_spatial_batch_inference(features_list):
    return [round(f.get("composite_hazard_indicator", 0.5), 4) for f in features_list]
