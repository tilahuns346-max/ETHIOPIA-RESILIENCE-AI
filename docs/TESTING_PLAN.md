# ETHIOPIA RESILIENCE AI — COMPREHENSIVE SOFTWARE TESTING STRATEGY
**Frameworks:** PyTest (Backend/AI), Jest & React Native Testing Library (Frontend/Mobile), PostGIS ST_Transform Test Suite, Locust (Load Testing)  
**Target Coverage:** >= 90% Unit Test Coverage, 100% Critical Safety Guardrail Coverage  
**Simulated Environments:** 2G/EDGE Rural Latency Profiles (500ms - 2000ms RTT, 30% Packet Loss)

---

## 1. Testing Hierarchy & Methodologies

1. **Unit Testing:** Individual business logic functions, coordinate validations, Amharic tokenizers, and database constraints.
2. **Integration Testing:** API contract verification, PostGIS spatial queries, Celery background worker queues, and Redis cache invalidation.
3. **Low-Bandwidth & Offline Sync Simulation:** SQLite local queue transactions, mobile SQLite -> API sync retry with exponential backoff, and idempotent deduplication.
4. **AI Model Uncertainty & Drift Evaluation:** Brier score calibration, confusion matrix tracking across hazard domains, and conformal prediction coverage.
5. **Safety Guardrail Penetration Testing:** Automated fuzzing to verify that **NO** code path can publish a Level 3 or Level 4 alert without an authenticated human officer signature.

---

## 2. Detailed Production Test Cases

| Test Case ID | Test Objective | Pre-conditions | Test Steps | Expected Result | Pass/Fail Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Offline Mobile Incident Capture | Mobile device placed in Airplane Mode (Offline). | 1. Open mobile incident form.<br>2. Fill hazard details.<br>3. Capture photo & audio.<br>4. Tap 'Save to Offline Queue'. | Report stored in local SQLite database; UI displays 'Queued (1)'. | PASS if record persists across app restarts without network. |
| **TC-02** | Automatic Offline Batch Sync | Queued report exists in SQLite; Airplane Mode disabled. | 1. Enable network connection.<br>2. Background sync worker triggers.<br>3. POST `/incidents/sync/` executed with batch ID. | Server responds HTTP 202 Accepted; local SQLite queue transitions to 'SYNCED'. | PASS if zero report loss and server registers PostGIS geometry. |
| **TC-03** | Spatial Deduplication (1.5km Buffer) | Incident INC-01 exists in Kencho Shacha at (36.9214, 6.2241). | 1. Submit duplicate report INC-02 at (36.9220, 6.2245) within 48h.<br>2. Trigger AI deduplication Celery task. | System recognizes spatial-temporal proximity; clusters INC-02 under INC-01 master parent. | PASS if duplicate count increments and no redundant dispatch occurs. |
| **TC-04** | **CRITICAL SAFETY INVARIANT:** Automated Alert Rejection | Draft Level 4 Alert created by AI model. | 1. Call POST `/alerts/{id}/broadcast/` without `approved_by_officer_id`.<br>2. Attempt direct dispatch. | Server rejects request with HTTP 403 Forbidden; error: `HUMAN_SIGN_OFF_REQUIRED`. | PASS if database constraint `chk_human_signoff_for_dissemination` prevents save. |
| **TC-05** | Human Officer Alert Authorization | Level 4 Alert in status `PENDING_HUMAN_REVIEW`. | 1. Authenticate as National EDRMC Commander.<br>2. Attach valid cryptographic digital signature.<br>3. Call POST `/alerts/{id}/authorize/`. | Status transitions to `APPROVED_BY_OFFICER`; Celery broadcast task enqueued. | PASS if officer ID and timestamp are permanently written to audit log. |
| **TC-06** | Ethio Telecom SMS Broadcast Fan-Out | Authorized Level 4 Alert targeting Kencho Shacha (4,500 pop). | 1. Celery worker executes notification dispatch.<br>2. Messages formatted in Amharic & English.<br>3. SMPP gateway called. | 4,500 SMS payloads dispatched; delivery statuses tracked in `notifications` table. | PASS if >= 98% successfully handed over to telecom gateway in < 60s. |
| **TC-07** | PostGIS Administrative Geocoding | Raw GPS coordinate (36.9214, 6.2241) provided without kebele. | 1. POST `/incidents/` with coordinates.<br>2. System executes `ST_Contains(kebeles.geom, Point)`. | Woreda assigned as 'Geze Gofa'; Kebele assigned as 'Kencho Shacha Gozdi'. | PASS if correct hierarchical UUIDs are automatically resolved. |
| **TC-08** | Response Team KNN Proximity Routing | Emergency SAR task created at (36.9220, 6.2250). | 1. Query available response teams using `<->` PostGIS operator.<br>2. Filter by status `STANDBY`. | System selects closest equipped rescue unit (Red Cross Unit 01 at 0.4km). | PASS if dispatch recommendation ranks nearest capable unit first. |
| **TC-09** | Cryptographic Audit Log Integrity | Officer approves disaster alert. | 1. Record written to `audit_logs`.<br>2. Compute SHA-256 hash of payload.<br>3. Attempt manual database update of `old_state`. | Checksum mismatch detected; security alert triggered for data tampering. | PASS if audit records are immutable and cryptographically verifiable. |
| **TC-10** | Multilingual Ge'ez Encoding Support | Citizen submits report using Amharic Unicode characters. | 1. Input string: 'በከንቾ ሻቻ ተራራማ ቁልቁለት ላይ የተከሰተ ናዳ'.<br>2. Save to database and query back. | Text returned without mojibake or question marks; matches byte-for-byte. | PASS if UTF-8 character integrity is preserved in database and mobile UI. |
