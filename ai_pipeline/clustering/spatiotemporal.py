from backend.database.geo_utils import haversine_distance_km

def cluster_incidents_spatiotemporal(incidents: list, distance_km_threshold: float = 1.5):
    clusters, visited = [], set()
    for i, inc1 in enumerate(incidents):
        if i in visited:
            continue
        curr = [inc1]
        visited.add(i)
        for j, inc2 in enumerate(incidents):
            if j not in visited and haversine_distance_km(inc1["latitude"], inc1["longitude"], inc2["latitude"], inc2["longitude"]) <= distance_km_threshold:
                if inc1.get("hazard_type_code") == inc2.get("hazard_type_code"):
                    curr.append(inc2)
                    visited.add(j)
        clusters.append(curr)
    return clusters
