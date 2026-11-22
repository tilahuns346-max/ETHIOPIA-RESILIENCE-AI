from dataclasses import dataclass
from typing import List, Optional

@dataclass
class OfflineSyncBatch:
    batch_id: str
    device_id: str
    synced_at: str
    total_records: int
    processed_count: int
    status: str  # RECEIVED, PROCESSING, COMPLETED, FAILED

@dataclass
class QueuedReport:
    local_id: str
    batch_id: str
    hazard_type_code: str
    latitude: float
    longitude: float
    offline_created_at: str
    description_raw: str
    evidence_hashes: List[str]
    assigned_incident_id: Optional[str] = None
