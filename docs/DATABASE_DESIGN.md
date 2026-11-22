# ETHIOPIA RESILIENCE AI — DATABASE DESIGN SPECIFICATION
**Engine:** PostgreSQL 15+ with PostGIS 3.3+  
**Spatial Reference System:** EPSG:4326 (WGS 84 Lon/Lat)  
**Encoding:** UTF-8 (Ethiopic Ge'ez and Latin Scripts)  
**High-Availability Configuration:** Primary Master with Streaming Physical Replica and Redis Sentinel Cache

---

## 1. Relational & Spatial Entity Data Dictionary

### 1.1 Administrative Hierarchy Entities

| Entity Name | Primary Key | Foreign Keys | Spatial Column | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| `regions` | `region_id (UUID)` | None | `geom (MultiPolygon, 4326)`, `centroid (Point)` | Top-level regional states (e.g., Oromia, Amhara, Somali, Afar). |
| `zones` | `zone_id (UUID)` | `region_id -> regions` | `geom (MultiPolygon, 4326)` | Second-tier administrative boundary (e.g., Gofa Zone, Borana Zone). |
| `woredas` | `woreda_id (UUID)` | `zone_id -> zones` | `geom (MultiPolygon, 4326)` | District-level disaster management unit containing JSON risk profile. |
| `kebeles` | `kebele_id (UUID)` | `woreda_id -> woredas` | `geom (MultiPolygon, 4326)` | Neighborhood/peasant association; ground verification boundary. |
| `communities` | `community_id (UUID)` | `kebele_id -> kebeles` | `location (Point, 4326)` | Local settlement cluster with vulnerability index. |

### 1.2 User Governance & Identity Entities

| Entity Name | Primary Key | Foreign Keys | Description |
| :--- | :--- | :--- | :--- |
| `roles` | `role_id (UUID)` | None | 7 predefined roles (`SUPER_ADMIN`, `NATIONAL_EDRMC_OFFICER`, etc.). |
| `permissions` | `permission_id (UUID)` | None | Fine-grained security privileges across system modules. |
| `role_permissions`| `(role_id, permission_id)` | `roles`, `permissions` | Composite join table for Role-Based Access Control (RBAC). |
| `users` | `user_id (UUID)` | `role_id`, `assigned_woreda_id` | Officer and citizen profiles with phone verification and trust scores. |

### 1.3 Hazard Intelligence & Sensor Telemetry

| Entity Name | Primary Key | Foreign Keys | Spatial Column | Description |
| :--- | :--- | :--- | :--- | :--- |
| `hazards` | `hazard_type_id (UUID)` | None | None | Catalog of hazards: floods, landslides, droughts, wildfires, urban fires. |
| `weather_stations`| `station_id (UUID)` | `woreda_id -> woredas` | `location (Point, 4326)` | Synoptic and river gauging stations (EMI network). |
| `weather_observations` | `observation_id (UUID)` | `station_id -> weather_stations` | None | Time-series meteorological feeds (rainfall, discharge, soil moisture). |

### 1.4 Incident Management & Evidence Repository

| Entity Name | Primary Key | Foreign Keys | Spatial Column | Description |
| :--- | :--- | :--- | :--- | :--- |
| `incidents` | `incident_id (UUID)` | `hazard_type_id`, `kebele_id`, `reporter_user_id` | `location (Point, 4326)` | Real-time crowd and sensor-reported disaster incidents. |
| `incident_evidence`| `evidence_id (UUID)` | `incident_id -> incidents` | `capture_location (Point, 4326)` | Cryptographically hashed (SHA-256) photos, voice notes, and videos. |

### 1.5 AI Predictions & Human Approval Gateway

| Entity Name | Primary Key | Foreign Keys | Spatial Column | Description |
| :--- | :--- | :--- | :--- | :--- |
| `ai_predictions`| `prediction_id (UUID)` | `hazard_type_id`, `target_woreda_id` | `target_geometry (Geometry, 4326)` | Probabilistic multi-hazard spatial risk inferences with uncertainty bounds. |
| `alerts` | `alert_id (UUID)` | `hazard_type_id`, `approved_by_officer_id` | `affected_polygon (MultiPolygon, 4326)` | **Official disaster warning.** Constrained by `chk_human_signoff_for_dissemination`. |

### 1.6 Emergency Response & Notifications

| Entity Name | Primary Key | Foreign Keys | Spatial Column | Description |
| :--- | :--- | :--- | :--- | :--- |
| `response_teams` | `team_id (UUID)` | `base_woreda_id -> woredas` | `current_location (Point, 4326)` | Red Cross, Fire Brigade, and EDRMC rescue units with GPS telemetry. |
| `response_tasks` | `task_id (UUID)` | `incident_id`, `team_id`, `alert_id` | `target_location (Point, 4326)` | Specific mission orders (search & rescue, triage, evacuation escort). |
| `notifications` | `notification_id (UUID)`| `alert_id`, `incident_id` | None | SMS and push broadcast queue connecting to Ethio Telecom gateways. |
| `audit_logs` | `audit_id (UUID)` | `actor_user_id -> users` | None | Immutable forensic record of every verification, sign-off, and override. |

---

## 2. Spatial Indexing & Query Optimization

```sql
-- 1. Rapid Spatial Intersections for Hazard Polygons
CREATE INDEX idx_woredas_geom ON woredas USING GIST (geom);
CREATE INDEX idx_incidents_location ON incidents USING GIST (location);
CREATE INDEX idx_alerts_polygon ON alerts USING GIST (affected_polygon);

-- 2. Fast Proximity Search for Responding Teams (KNN Operator <->)
CREATE INDEX idx_response_teams_loc ON response_teams USING GIST (current_location);

-- 3. Composite Temporal & Status Filtering
CREATE INDEX idx_incidents_status_time ON incidents (status, reported_at DESC);
CREATE INDEX idx_weather_obs_time ON weather_observations (station_id, recorded_at DESC);

-- 4. Trigram Text Search for Amharic and English Location Names
CREATE INDEX idx_woredas_name_am_trgm ON woredas USING GIN (name_am gin_trgm_ops);
CREATE INDEX idx_woredas_name_en_trgm ON woredas USING GIN (name_en gin_trgm_ops);
```

---

## 3. High-Bandwidth Ingestion & Partitioning Strategy
- **`weather_observations`**: Range-partitioned by month on `recorded_at` to maintain millisecond write latencies during heavy monsoon seasons.
- **`notifications`**: List-partitioned by delivery channel (`SMS`, `MOBILE_PUSH`, `RADIO_BULLETIN`) to allow independent pruning and archival.
- **`audit_logs`**: Append-only table on write-optimized storage volume with cryptographic hash chains.
