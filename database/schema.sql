-- ============================================================================
-- ETHIOPIA RESILIENCE AI — PRODUCTION DATABASE SCHEMA
-- Target Engine: PostgreSQL 15+ with PostGIS 3.3+ Extension
-- Geographic Coordinate Reference System: EPSG:4326 (WGS 84)
-- Character Set: UTF-8 (Full Ethiopic Script / Unicode Support)
-- ============================================================================

-- 1. Enable Required Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gist";

-- 2. Enumerated Domain Types
CREATE TYPE user_role_type AS ENUM (
    'SUPER_ADMIN',
    'NATIONAL_EDRMC_OFFICER',
    'REGIONAL_DIRECTOR',
    'ZONAL_COORDINATOR',
    'WOREDA_FOCAL_PERSON',
    'KEBELE_REPRESENTATIVE',
    'FIRST_RESPONDER',
    'COMMUNITY_REPORTER'
);

CREATE TYPE incident_status_type AS ENUM (
    'REPORTED',
    'TRIAGED',
    'VERIFIED',
    'RESPONDING',
    'CONTAINED',
    'RESOLVED',
    'REJECTED_FALSE_ALARM'
);

CREATE TYPE verification_status_type AS ENUM (
    'UNVERIFIED',
    'COMMUNITY_CORROBORATED',
    'OFFICIALLY_VERIFIED',
    'REJECTED'
);

CREATE TYPE severity_level_type AS ENUM (
    'LEVEL_1_LOW',
    'LEVEL_2_MODERATE',
    'LEVEL_3_HIGH',
    'LEVEL_4_CRITICAL'
);

CREATE TYPE alert_status_type AS ENUM (
    'DRAFT',
    'PENDING_HUMAN_REVIEW',
    'APPROVED_BY_OFFICER',
    'DISSEMINATED',
    'CANCELLED',
    'EXPIRED'
);

CREATE TYPE notification_channel_type AS ENUM (
    'SMS',
    'MOBILE_PUSH',
    'USSD_BROADCAST',
    'RADIO_BULLETIN',
    'WEB_PORTAL'
);

CREATE TYPE team_org_type AS ENUM (
    'EDRMC',
    'ETHIOPIAN_RED_CROSS',
    'FIRE_AND_EMERGENCY',
    'MINISTRY_OF_HEALTH',
    'DEFENSE_FORCES_DISASTER_UNIT',
    'COMMUNITY_VOLUNTEER_CORPS'
);

CREATE TYPE task_status_type AS ENUM (
    'PENDING',
    'ACCEPTED',
    'EN_ROUTE',
    'ON_SCENE',
    'COMPLETED',
    'ABORTED'
);

-- ============================================================================
-- 3. ADMINISTRATIVE GEOGRAPHIC HIERARCHY OF ETHIOPIA
-- ============================================================================

CREATE TABLE regions (
    region_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(10) UNIQUE NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    name_am VARCHAR(100) NOT NULL,
    capital_en VARCHAR(100) NOT NULL,
    capital_am VARCHAR(100) NOT NULL,
    population BIGINT NOT NULL,
    area_sqkm NUMERIC(10, 2) NOT NULL,
    geom GEOMETRY(MultiPolygon, 4326),
    centroid GEOMETRY(Point, 4326),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE zones (
    zone_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    region_id UUID NOT NULL REFERENCES regions(region_id) ON DELETE RESTRICT,
    code VARCHAR(15) UNIQUE NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    name_am VARCHAR(100) NOT NULL,
    administration_center VARCHAR(100) NOT NULL,
    geom GEOMETRY(MultiPolygon, 4326),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE woredas (
    woreda_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    zone_id UUID NOT NULL REFERENCES zones(zone_id) ON DELETE RESTRICT,
    code VARCHAR(20) UNIQUE NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    name_am VARCHAR(100) NOT NULL,
    risk_profile_json JSONB DEFAULT '{}'::jsonb,
    geom GEOMETRY(MultiPolygon, 4326),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE kebeles (
    kebele_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    woreda_id UUID NOT NULL REFERENCES woredas(woreda_id) ON DELETE RESTRICT,
    code VARCHAR(25) UNIQUE NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    name_am VARCHAR(100) NOT NULL,
    emergency_contact_phone VARCHAR(20),
    population INTEGER NOT NULL DEFAULT 0,
    geom GEOMETRY(MultiPolygon, 4326),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE communities (
    community_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    kebele_id UUID NOT NULL REFERENCES kebeles(kebele_id) ON DELETE RESTRICT,
    name_en VARCHAR(100) NOT NULL,
    name_am VARCHAR(100) NOT NULL,
    focal_person_name VARCHAR(100),
    focal_phone VARCHAR(20),
    location GEOMETRY(Point, 4326) NOT NULL,
    vulnerability_index NUMERIC(3, 2) DEFAULT 0.50 CHECK (vulnerability_index BETWEEN 0.00 AND 1.00),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 4. USERS, ROLES, AND AUTHENTICATION
-- ============================================================================

CREATE TABLE roles (
    role_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code user_role_type UNIQUE NOT NULL,
    title_en VARCHAR(100) NOT NULL,
    title_am VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE permissions (
    permission_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(100) UNIQUE NOT NULL,
    module VARCHAR(50) NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE role_permissions (
    role_id UUID NOT NULL REFERENCES roles(role_id) ON DELETE CASCADE,
    permission_id UUID NOT NULL REFERENCES permissions(permission_id) ON DELETE CASCADE,
    PRIMARY KEY (role_id, permission_id)
);

CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(60) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(120) NOT NULL,
    role_id UUID NOT NULL REFERENCES roles(role_id) ON DELETE RESTRICT,
    assigned_region_id UUID REFERENCES regions(region_id),
    assigned_woreda_id UUID REFERENCES woredas(woreda_id),
    assigned_kebele_id UUID REFERENCES kebeles(kebele_id),
    preferred_language VARCHAR(10) NOT NULL DEFAULT 'am' CHECK (preferred_language IN ('am', 'en', 'om', 'ti')),
    badge_number VARCHAR(50),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_phone_verified BOOLEAN NOT NULL DEFAULT FALSE,
    trust_score NUMERIC(3, 2) NOT NULL DEFAULT 1.00 CHECK (trust_score BETWEEN 0.00 AND 5.00),
    last_login_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 5. HAZARD CATALOG & METEOROLOGICAL SENSOR STREAMS
-- ============================================================================

CREATE TABLE hazards (
    hazard_type_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(50) UNIQUE NOT NULL,
    name_en VARCHAR(100) NOT NULL,
    name_am VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL, -- HYDROLOGICAL, CLIMATOLOGICAL, GEOPHYSICAL, BIOLOGICAL, URBAN
    description_en TEXT,
    description_am TEXT,
    monitoring_parameters_json JSONB DEFAULT '[]'::jsonb,
    icon_name VARCHAR(50),
    color_hex VARCHAR(7) DEFAULT '#ef4444',
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE weather_stations (
    station_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    woreda_id UUID NOT NULL REFERENCES woredas(woreda_id) ON DELETE RESTRICT,
    location GEOMETRY(Point, 4326) NOT NULL,
    elevation_meters NUMERIC(6, 1),
    station_type VARCHAR(50) NOT NULL DEFAULT 'SYNOPTIC', -- SYNOPTIC, AGROMET, RIVER_GAUGE, SEISMIC
    data_provider VARCHAR(100) NOT NULL DEFAULT 'ETHIOPIAN_METEOROLOGY_INSTITUTE',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    last_reported_at TIMESTAMPTZ
);

CREATE TABLE weather_observations (
    observation_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    station_id UUID NOT NULL REFERENCES weather_stations(station_id) ON DELETE RESTRICT,
    recorded_at TIMESTAMPTZ NOT NULL,
    temperature_c NUMERIC(4, 1),
    rainfall_1h_mm NUMERIC(5, 1),
    rainfall_24h_mm NUMERIC(6, 1),
    relative_humidity_pct NUMERIC(4, 1),
    wind_speed_kph NUMERIC(5, 1),
    river_discharge_m3s NUMERIC(7, 2),
    soil_moisture_pct NUMERIC(4, 1),
    source_payload JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 6. INCIDENT MANAGEMENT & EVIDENCE REPOSITORY
-- ============================================================================

CREATE TABLE incidents (
    incident_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    incident_number VARCHAR(30) UNIQUE NOT NULL,
    reporter_user_id UUID REFERENCES users(user_id) ON DELETE SET NULL,
    hazard_type_id UUID NOT NULL REFERENCES hazards(hazard_type_id) ON DELETE RESTRICT,
    kebele_id UUID NOT NULL REFERENCES kebeles(kebele_id) ON DELETE RESTRICT,
    title_en VARCHAR(200) NOT NULL,
    title_am VARCHAR(200) NOT NULL,
    description_raw TEXT NOT NULL,
    description_summary_ai TEXT,
    detected_language VARCHAR(10) DEFAULT 'am',
    location GEOMETRY(Point, 4326) NOT NULL,
    altitude_m NUMERIC(6, 1),
    status incident_status_type NOT NULL DEFAULT 'REPORTED',
    verification_status verification_status_type NOT NULL DEFAULT 'UNVERIFIED',
    severity_level severity_level_type NOT NULL DEFAULT 'LEVEL_2_MODERATE',
    estimated_affected_people INTEGER DEFAULT 0,
    casualties_count INTEGER DEFAULT 0,
    infrastructure_damage_summary JSONB DEFAULT '{}'::jsonb,
    is_offline_submission BOOLEAN NOT NULL DEFAULT FALSE,
    offline_created_at TIMESTAMPTZ,
    sync_batch_id UUID,
    reported_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    verified_at TIMESTAMPTZ,
    verified_by_user_id UUID REFERENCES users(user_id) ON DELETE SET NULL,
    verification_notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE incident_evidence (
    evidence_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    incident_id UUID NOT NULL REFERENCES incidents(incident_id) ON DELETE CASCADE,
    file_type VARCHAR(20) NOT NULL CHECK (file_type IN ('IMAGE', 'AUDIO_VOICE_NOTE', 'VIDEO', 'DOCUMENT')),
    file_url TEXT NOT NULL,
    thumbnail_url TEXT,
    file_size_bytes BIGINT NOT NULL,
    sha256_hash CHAR(64) NOT NULL,
    captured_at TIMESTAMPTZ,
    capture_location GEOMETRY(Point, 4326),
    uploader_notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 7. AI RISK PREDICTIONS & HUMAN OVERSIGHT DECISION GATEWAY
-- ============================================================================

CREATE TABLE ai_predictions (
    prediction_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    model_name VARCHAR(100) NOT NULL,
    model_version VARCHAR(50) NOT NULL,
    hazard_type_id UUID NOT NULL REFERENCES hazards(hazard_type_id) ON DELETE RESTRICT,
    target_woreda_id UUID NOT NULL REFERENCES woredas(woreda_id) ON DELETE RESTRICT,
    target_kebele_id UUID REFERENCES kebeles(kebele_id) ON DELETE SET NULL,
    target_geometry GEOMETRY(Geometry, 4326) NOT NULL,
    predicted_severity severity_level_type NOT NULL,
    risk_probability NUMERIC(4, 3) NOT NULL CHECK (risk_probability BETWEEN 0.000 AND 1.000),
    uncertainty_lower NUMERIC(4, 3) NOT NULL,
    uncertainty_upper NUMERIC(4, 3) NOT NULL,
    feature_importance_weights JSONB NOT NULL DEFAULT '{}'::jsonb,
    input_features_digest CHAR(64) NOT NULL,
    generated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    valid_until TIMESTAMPTZ NOT NULL,
    is_reviewed_by_human BOOLEAN NOT NULL DEFAULT FALSE,
    review_status VARCHAR(50) DEFAULT 'PENDING_OFFICER_REVIEW', -- ACCEPTED, CALIBRATED, REJECTED
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 8. EARLY WARNING ALERTS (MANDATORY HUMAN-IN-THE-LOOP APPROVAL)
-- ============================================================================

CREATE TABLE alerts (
    alert_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    alert_code VARCHAR(30) UNIQUE NOT NULL,
    hazard_type_id UUID NOT NULL REFERENCES hazards(hazard_type_id) ON DELETE RESTRICT,
    severity_level severity_level_type NOT NULL,
    status alert_status_type NOT NULL DEFAULT 'DRAFT',
    title_en VARCHAR(255) NOT NULL,
    title_am VARCHAR(255) NOT NULL,
    message_en TEXT NOT NULL,
    message_am TEXT NOT NULL,
    affected_polygon GEOMETRY(MultiPolygon, 4326) NOT NULL,
    evacuation_order_issued BOOLEAN NOT NULL DEFAULT FALSE,
    evacuation_routes_json JSONB DEFAULT '[]'::jsonb,
    ai_prediction_id UUID REFERENCES ai_predictions(prediction_id) ON DELETE SET NULL,
    drafted_by_user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE RESTRICT,
    
    -- MANDATORY HUMAN APPROVAL AUDIT FIELD (SAFETY INVARIANT)
    approved_by_officer_id UUID REFERENCES users(user_id) ON DELETE RESTRICT,
    approval_timestamp TIMESTAMPTZ,
    officer_digital_signature TEXT,
    approval_reasoning TEXT,
    
    valid_from TIMESTAMPTZ NOT NULL,
    valid_until TIMESTAMPTZ NOT NULL,
    dissemination_summary JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Safety Check: Level 3 and Level 4 alerts MUST NOT be marked DISSEMINATED without an approved officer
    CONSTRAINT chk_human_signoff_for_dissemination 
        CHECK (
            status != 'DISSEMINATED' OR 
            (approved_by_officer_id IS NOT NULL AND approval_timestamp IS NOT NULL)
        )
);

-- ============================================================================
-- 9. EMERGENCY RESPONSE TEAMS & FIELD TASK COORDINATION
-- ============================================================================

CREATE TABLE response_teams (
    team_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(120) NOT NULL,
    organization_type team_org_type NOT NULL,
    base_woreda_id UUID NOT NULL REFERENCES woredas(woreda_id) ON DELETE RESTRICT,
    leader_name VARCHAR(100) NOT NULL,
    leader_phone VARCHAR(20) NOT NULL,
    personnel_count INTEGER NOT NULL DEFAULT 5,
    equipment_manifest_json JSONB DEFAULT '{}'::jsonb,
    current_status VARCHAR(50) NOT NULL DEFAULT 'STANDBY', -- STANDBY, MOBILIZING, ON_MISSION, RESTING
    current_location GEOMETRY(Point, 4326),
    last_telemetry_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE response_tasks (
    task_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    incident_id UUID REFERENCES incidents(incident_id) ON DELETE SET NULL,
    alert_id UUID REFERENCES alerts(alert_id) ON DELETE SET NULL,
    team_id UUID NOT NULL REFERENCES response_teams(team_id) ON DELETE RESTRICT,
    task_code VARCHAR(30) UNIQUE NOT NULL,
    task_type VARCHAR(80) NOT NULL, -- SEARCH_AND_RESCUE, MEDICAL_TRIAGE, EVACUATION_ESCORT, RELIEF_DISTRIBUTION, HAZARD_CONTAINMENT
    priority severity_level_type NOT NULL DEFAULT 'LEVEL_3_HIGH',
    status task_status_type NOT NULL DEFAULT 'PENDING',
    instructions_en TEXT NOT NULL,
    instructions_am TEXT NOT NULL,
    target_location GEOMETRY(Point, 4326) NOT NULL,
    assigned_by_user_id UUID NOT NULL REFERENCES users(user_id) ON DELETE RESTRICT,
    assigned_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    acknowledged_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    field_report_notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 10. MULTI-CHANNEL NOTIFICATIONS & AUDIT LOGS
-- ============================================================================

CREATE TABLE notifications (
    notification_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    alert_id UUID REFERENCES alerts(alert_id) ON DELETE CASCADE,
    incident_id UUID REFERENCES incidents(incident_id) ON DELETE CASCADE,
    channel notification_channel_type NOT NULL,
    recipient_phone VARCHAR(20),
    recipient_user_id UUID REFERENCES users(user_id) ON DELETE SET NULL,
    target_woreda_id UUID REFERENCES woredas(woreda_id) ON DELETE SET NULL,
    message_text TEXT NOT NULL,
    delivery_status VARCHAR(30) NOT NULL DEFAULT 'QUEUED', -- QUEUED, SENT, DELIVERED, FAILED
    telecom_gateway_id VARCHAR(100), -- Ethio Telecom Gateway message ID
    sent_at TIMESTAMPTZ,
    delivered_at TIMESTAMPTZ,
    retry_count INTEGER NOT NULL DEFAULT 0,
    error_message TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE audit_logs (
    audit_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    actor_user_id UUID REFERENCES users(user_id) ON DELETE SET NULL,
    action_type VARCHAR(100) NOT NULL, -- INCIDENT_VERIFIED, ALERT_APPROVED, AI_OVERRIDE, TEAM_DISPATCHED
    entity_table VARCHAR(50) NOT NULL,
    entity_id UUID NOT NULL,
    client_ip INET,
    user_agent TEXT,
    old_state JSONB,
    new_state JSONB,
    cryptographic_hash CHAR(64),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 11. SPATIAL & PERFORMANCE INDEXES
-- ============================================================================

-- Spatial GiST Indexes for Ultra-Fast Proximity and Bounding Box Searches
CREATE INDEX idx_regions_geom ON regions USING GIST (geom);
CREATE INDEX idx_regions_centroid ON regions USING GIST (centroid);
CREATE INDEX idx_zones_geom ON zones USING GIST (geom);
CREATE INDEX idx_woredas_geom ON woredas USING GIST (geom);
CREATE INDEX idx_kebeles_geom ON kebeles USING GIST (geom);
CREATE INDEX idx_communities_location ON communities USING GIST (location);
CREATE INDEX idx_weather_stations_loc ON weather_stations USING GIST (location);
CREATE INDEX idx_incidents_location ON incidents USING GIST (location);
CREATE INDEX idx_ai_predictions_geom ON ai_predictions USING GIST (target_geometry);
CREATE INDEX idx_alerts_polygon ON alerts USING GIST (affected_polygon);
CREATE INDEX idx_response_teams_loc ON response_teams USING GIST (current_location);
CREATE INDEX idx_response_tasks_loc ON response_tasks USING GIST (target_location);

-- B-Tree Performance & Foreign Key Indexes
CREATE INDEX idx_users_phone ON users (phone_number);
CREATE INDEX idx_users_role ON users (role_id);
CREATE INDEX idx_woredas_zone ON woredas (zone_id);
CREATE INDEX idx_kebeles_woreda ON kebeles (woreda_id);
CREATE INDEX idx_weather_obs_station_time ON weather_observations (station_id, recorded_at DESC);
CREATE INDEX idx_incidents_status_time ON incidents (status, reported_at DESC);
CREATE INDEX idx_incidents_kebele ON incidents (kebele_id);
CREATE INDEX idx_incidents_hazard ON incidents (hazard_type_id);
CREATE INDEX idx_alerts_status_validity ON alerts (status, valid_from, valid_until);
CREATE INDEX idx_ai_predictions_woreda_time ON ai_predictions (target_woreda_id, generated_at DESC);
CREATE INDEX idx_notifications_status ON notifications (delivery_status, channel);
CREATE INDEX idx_audit_logs_actor_time ON audit_logs (actor_user_id, created_at DESC);

-- Trigram Text Search Indexes for Rapid Emergency Location Search
CREATE INDEX idx_woredas_name_en_trgm ON woredas USING GIN (name_en gin_trgm_ops);
CREATE INDEX idx_woredas_name_am_trgm ON woredas USING GIN (name_am gin_trgm_ops);
CREATE INDEX idx_incidents_desc_trgm ON incidents USING GIN (description_raw gin_trgm_ops);

-- ============================================================================
-- 12. AUTOMATIC TIMESTAMP & AUDIT TRIGGERS
-- ============================================================================

CREATE OR REPLACE FUNCTION update_timestamp_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_users_timestamp BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_timestamp_column();
CREATE TRIGGER trg_update_regions_timestamp BEFORE UPDATE ON regions FOR EACH ROW EXECUTE FUNCTION update_timestamp_column();
CREATE TRIGGER trg_update_zones_timestamp BEFORE UPDATE ON zones FOR EACH ROW EXECUTE FUNCTION update_timestamp_column();
CREATE TRIGGER trg_update_woredas_timestamp BEFORE UPDATE ON woredas FOR EACH ROW EXECUTE FUNCTION update_timestamp_column();
CREATE TRIGGER trg_update_kebeles_timestamp BEFORE UPDATE ON kebeles FOR EACH ROW EXECUTE FUNCTION update_timestamp_column();
CREATE TRIGGER trg_update_incidents_timestamp BEFORE UPDATE ON incidents FOR EACH ROW EXECUTE FUNCTION update_timestamp_column();
CREATE TRIGGER trg_update_alerts_timestamp BEFORE UPDATE ON alerts FOR EACH ROW EXECUTE FUNCTION update_timestamp_column();
CREATE TRIGGER trg_update_response_teams_timestamp BEFORE UPDATE ON response_teams FOR EACH ROW EXECUTE FUNCTION update_timestamp_column();
CREATE TRIGGER trg_update_response_tasks_timestamp BEFORE UPDATE ON response_tasks FOR EACH ROW EXECUTE FUNCTION update_timestamp_column();
