# ETHIOPIA RESILIENCE AI — REST API SPECIFICATION
**Version:** 2.4.0-PROD  
**Specification Standard:** OpenAPI 3.0.3 Compatible  
**Base URL:** `https://api.resilience.gov.et/api/v1`  
**Security Protocols:** TLS 1.3, JWT Bearer Authentication, HMAC-SHA256 Request Signing for Sovereign Gateways  
**Default Coordinate System:** EPSG:4326 (WGS 84 GeoJSON)  
**Supported Locales:** `am` (Amharic), `en` (English), `om` (Afaan Oromoo), `ti` (Tigrinya)

---

## 1. Authentication & Session Management

### 1.1 Obtain JWT Token Pair
- **Endpoint:** `POST /auth/token/`
- **Description:** Authenticates disaster officers, system administrators, and verified field agents.
- **Headers:** `Content-Type: application/json`
- **Request Body:**
```json
{
  "phone_number": "+251911000002",
  "password": "SecureOfficerPassword2026!",
  "client_id": "EDRMC_WEB_CONSOLE_01"
}
```
- **Response `200 OK`:**
```json
{
  "status": "SUCCESS",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsIn...",
    "expires_in": 3600,
    "user": {
      "user_id": "77777777-7777-7777-7777-777777777702",
      "full_name": "Dr. Senait Hailemariam",
      "role": "NATIONAL_EDRMC_OFFICER",
      "jurisdiction": "NATIONAL",
      "can_authorize_alerts": true
    }
  }
}
```

---

## 2. Community Incident Reporting & Offline Sync

### 2.1 Submit Single Incident (Online)
- **Endpoint:** `POST /incidents/`
- **Headers:** `Authorization: Bearer <token>`, `Idempotency-Key: <uuid>`
- **Request Body:**
```json
{
  "hazard_type_code": "HAZ-LANDSLIDE",
  "kebele_code": "K-KENCHO-SHACHA",
  "title_en": "Slope fissure collapse in Kencho Shacha",
  "title_am": "በከንቾ ሻቻ የተከሰተ የመሬት መንሸራተት",
  "description_raw": "ከባድ ዝናብ ተከትሎ ተራራው ተደርምሶ መንገዱን ዘግቶታል።",
  "detected_language": "am",
  "location": {
    "type": "Point",
    "coordinates": [36.9214, 6.2241]
  },
  "altitude_m": 2140.5,
  "estimated_affected_people": 250,
  "is_offline_submission": false
}
```
- **Response `201 Created`:**
```json
{
  "status": "CREATED",
  "data": {
    "incident_id": "88888888-8888-8888-8888-888888888801",
    "incident_number": "INC-2026-00412",
    "status": "REPORTED",
    "verification_status": "UNVERIFIED",
    "reported_at": "2026-11-22T04:45:00Z"
  }
}
```

### 2.2 Offline Batch Synchronization
- **Endpoint:** `POST /incidents/sync/`
- **Description:** Idempotent ingestion endpoint for mobile devices syncing queued field reports after re-establishing internet connectivity.
- **Headers:** `Authorization: Bearer <token>`, `X-Sync-Batch-ID: <uuid>`
- **Request Body:**
```json
{
  "batch_id": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
  "device_id": "EXPO-ANDROID-88392",
  "synced_at": "2026-11-22T04:46:10Z",
  "reports": [
    {
      "local_id": "local_rec_091",
      "hazard_type_code": "HAZ-LANDSLIDE",
      "location": { "type": "Point", "coordinates": [36.9214, 6.2241] },
      "offline_created_at": "2026-11-22T01:30:00Z",
      "description_raw": "Road blocked by mudslide. Houses at risk.",
      "evidence_hashes": [
        "9f8a83d47b1e5...img1",
        "3d4e5f6a7b8c9...voice_am"
      ]
    }
  ]
}
```
- **Response `202 Accepted`:**
```json
{
  "status": "ACCEPTED",
  "data": {
    "batch_id": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
    "processed_count": 1,
    "merged_into_cluster_count": 0,
    "assigned_incident_numbers": ["INC-2026-00412"]
  }
}
```

---

## 3. Incident Ground-Truth Verification

### 3.1 Verify Incident by Woreda / Kebele Officer
- **Endpoint:** `POST /incidents/{incident_id}/verify/`
- **Description:** Submits physical ground-truth inspection results from authorized local disaster committee members.
- **Request Body:**
```json
{
  "verification_decision": "OFFICIALLY_VERIFIED",
  "confirmed_severity": "LEVEL_4_CRITICAL",
  "verification_notes": "Active ground fissure widening confirmed on hillside slope. Evacuation necessary.",
  "ground_evidence_urls": [
    "https://storage.resilience.gov.et/evidence/gofa/fissure_wide_01.jpg"
  ]
}
```
- **Response `200 OK`:**
```json
{
  "status": "SUCCESS",
  "data": {
    "incident_id": "88888888-8888-8888-8888-888888888801",
    "status": "VERIFIED",
    "verification_status": "OFFICIALLY_VERIFIED",
    "verified_by": "Mulugeta Woldeyes (Woreda Disaster Desk)",
    "verified_at": "2026-11-22T04:48:00Z"
  }
}
```

---

## 4. AI Multi-Hazard Risk Predictions

### 4.1 Query Woreda Spatial Risk Evaluation
- **Endpoint:** `GET /ai/predictions/woreda/{woreda_id}/`
- **Description:** Returns real-time probabilistic hazard risk scores computed by XGBoost and hydrological models.
- **Response `200 OK`:**
```json
{
  "status": "SUCCESS",
  "data": {
    "woreda_id": "44444444-4444-4444-4444-444444444401",
    "woreda_name": "Geze Gofa",
    "model_name": "ETH-GEO-SLOPE-RISK-XGB",
    "model_version": "v2.4.1",
    "predicted_severity": "LEVEL_4_CRITICAL",
    "risk_probability": 0.912,
    "conformal_confidence_interval": [0.865, 0.948],
    "top_contributing_features": {
      "72h_antecedent_rainfall_mm": 142.8,
      "slope_gradient_degrees": 38.4,
      "soil_saturation_index": 0.94
    },
    "requires_human_officer_review": true,
    "valid_until": "2026-11-23T04:00:00Z"
  }
}
```

---

## 5. Early Warning Alerts & Human Approval (Safety Invariant)

### 5.1 Authorize Official Disaster Alert
- **Endpoint:** `POST /alerts/{alert_id}/authorize/`
- **Description:** **SAFETY INVARIANT:** AI predictions never publish warnings automatically. Only authorized government officers (EDRMC Commander / Regional DRMC Director) can execute this endpoint.
- **Request Body:**
```json
{
  "officer_digital_signature": "SHA256:ECDSA:9f8a83d47b1e5...EDRMC-HAILMARIAM-AUTH",
  "approval_reasoning": "AI slope failure model corroborated by on-site Woreda inspection report.",
  "evacuation_order_issued": true,
  "designated_shelter_points": [
    { "name": "Sawla High School Compound", "coordinates": [36.9450, 6.2300] }
  ]
}
```
- **Response `200 OK`:**
```json
{
  "status": "SUCCESS",
  "data": {
    "alert_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
    "alert_code": "ALT-ETH-2026-089",
    "status": "APPROVED_BY_OFFICER",
    "approved_by": "Dr. Senait Hailemariam",
    "approved_at": "2026-11-22T04:50:00Z",
    "broadcast_queued": true
  }
}
```

### 5.2 Disseminate Multi-Channel Emergency Warning
- **Endpoint:** `POST /alerts/{alert_id}/broadcast/`
- **Description:** Triggers geo-fenced SMS broadcasts via Ethio Telecom cell towers and mobile push notifications.
- **Response `202 Accepted`:**
```json
{
  "status": "ACCEPTED",
  "data": {
    "alert_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
    "broadcast_task_id": "celery-task-99812",
    "channels": ["SMS_CELL_BROADCAST", "MOBILE_PUSH", "RADIO_BULLETIN_API"],
    "target_population_estimate": 4500,
    "languages": ["am", "en", "om"]
  }
}
```

---

## 6. Emergency Response Logistics & Task Routing

### 6.1 Dispatch Tactical Response Task
- **Endpoint:** `POST /tasks/dispatch/`
- **Request Body:**
```json
{
  "alert_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
  "team_id": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbb01",
  "task_type": "SEARCH_AND_RESCUE",
  "priority": "LEVEL_4_CRITICAL",
  "instructions_en": "Deploy canine units to Sector B debris zone.",
  "instructions_am": "የፍለጋና ማዳን ቡድኑ በሴክተር ቢ ፍርስራሽ ውስጥ ህይወት ያላቸውን ሰዎች እንዲፈልግ።",
  "target_location": {
    "type": "Point",
    "coordinates": [36.9220, 6.2250]
  }
}
```
- **Response `201 Created`:**
```json
{
  "status": "CREATED",
  "data": {
    "task_id": "cccccccc-cccc-cccc-cccc-cccccccccccc",
    "task_code": "TSK-2026-0091",
    "status": "PENDING",
    "dispatched_to_team": "Ethiopian Red Cross Rapid Disaster Unit"
  }
}
```
