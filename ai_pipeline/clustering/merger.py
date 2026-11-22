def merge_cluster_reports(cluster: list) -> dict:
    primary = cluster[0].copy()
    count = len(cluster)
    primary["corroborated_report_count"] = count
    primary["confidence_level"] = min(0.5 + (count * 0.15), 0.98)
    primary["total_affected_estimate"] = sum(c.get("estimated_affected_people", 0) for c in cluster)
    return primary
