from dataclasses import dataclass
from typing import Optional

@dataclass
class BroadcastNotificationLog:
    id: str
    alert_id: str
    channel: str  # SMS_CELL_BROADCAST, MOBILE_PUSH, RADIO_BULLETIN_API
    target_region_or_woreda: str
    recipients_estimate: int
    status: str  # QUEUED, TRANSMITTING, DELIVERED, FAILED
    dispatched_at: str
    gateway_reference_id: Optional[str] = None
    cost_etb: float = 0.0
