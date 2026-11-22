import time
import json
from backend.app.main import router

@router.get("/api/v1/events/stream/")
def stream_events(req: dict):
    """Endpoint descriptor for Server-Sent Events stream of live disaster telemetry."""
    return 200, {
        "status": "STREAM_ACTIVE",
        "protocol": "text/event-stream",
        "heartbeat_interval_seconds": 15,
        "supported_topics": ["INCIDENT_CREATED", "ALERT_PUBLISHED", "UNIT_TELEMETRY"]
    }
