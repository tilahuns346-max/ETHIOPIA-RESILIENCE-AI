import os
import sqlite3
from backend.database.connection import DB_PATH
from backend.database.seeds.regions_zones import REGIONS_DATA, ZONES_DATA
from backend.database.seeds.woredas_kebeles import WOREDAS_DATA, KEBELES_DATA
from backend.database.seeds.hazards import HAZARD_TYPES_DATA, HISTORICAL_DISASTERS_DATA
from backend.database.seeds.officers_teams import USERS_DATA, TEAMS_DATA

DDL_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS regions (
        code TEXT PRIMARY KEY,
        name_en TEXT NOT NULL,
        name_am TEXT NOT NULL,
        capital_city TEXT,
        population INTEGER,
        area_sq_km REAL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS zones (
        code TEXT PRIMARY KEY,
        region_code TEXT NOT NULL REFERENCES regions(code),
        name_en TEXT NOT NULL,
        name_am TEXT NOT NULL,
        focal_officer_phone TEXT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS woredas (
        code TEXT PRIMARY KEY,
        zone_code TEXT NOT NULL REFERENCES zones(code),
        name_en TEXT NOT NULL,
        name_am TEXT NOT NULL,
        risk_level TEXT,
        latitude REAL,
        longitude REAL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS kebeles (
        code TEXT PRIMARY KEY,
        woreda_code TEXT NOT NULL REFERENCES woredas(code),
        name_en TEXT NOT NULL,
        name_am TEXT NOT NULL,
        latitude REAL,
        longitude REAL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS hazard_types (
        code TEXT PRIMARY KEY,
        name_en TEXT NOT NULL,
        name_am TEXT NOT NULL,
        category TEXT NOT NULL,
        description_en TEXT,
        description_am TEXT,
        icon_name TEXT,
        color_code TEXT,
        default_warning_radius_km REAL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        phone_number TEXT UNIQUE NOT NULL,
        full_name TEXT NOT NULL,
        email TEXT,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL,
        jurisdiction_level TEXT NOT NULL,
        jurisdiction_id TEXT,
        is_active INTEGER DEFAULT 1,
        can_authorize_alerts INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS incidents (
        id TEXT PRIMARY KEY,
        incident_number TEXT UNIQUE NOT NULL,
        hazard_type_code TEXT NOT NULL REFERENCES hazard_types(code),
        kebele_code TEXT,
        woreda_code TEXT,
        title_en TEXT NOT NULL,
        title_am TEXT NOT NULL,
        description_raw TEXT,
        detected_language TEXT DEFAULT 'am',
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        altitude_m REAL,
        estimated_affected_people INTEGER DEFAULT 0,
        status TEXT DEFAULT 'REPORTED',
        verification_status TEXT DEFAULT 'UNVERIFIED',
        reporter_user_id TEXT,
        reporter_phone TEXT,
        is_offline_submission INTEGER DEFAULT 0,
        ai_risk_score REAL,
        cluster_id TEXT,
        reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS verifications (
        id TEXT PRIMARY KEY,
        incident_id TEXT NOT NULL REFERENCES incidents(id),
        officer_user_id TEXT NOT NULL REFERENCES users(id),
        officer_name TEXT NOT NULL,
        verification_decision TEXT NOT NULL,
        confirmed_severity TEXT NOT NULL,
        verification_notes TEXT,
        evidence_urls TEXT,
        verified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS alerts (
        id TEXT PRIMARY KEY,
        alert_code TEXT UNIQUE NOT NULL,
        title_en TEXT NOT NULL,
        title_am TEXT NOT NULL,
        hazard_type_code TEXT NOT NULL REFERENCES hazard_types(code),
        severity TEXT NOT NULL,
        status TEXT DEFAULT 'DRAFT',
        affected_woredas TEXT NOT NULL,
        evacuation_order_issued INTEGER DEFAULT 0,
        designated_shelters TEXT,
        instructions_en TEXT,
        instructions_am TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        approved_by TEXT,
        approved_at TIMESTAMP,
        officer_digital_signature TEXT,
        disseminated_at TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS emergency_teams (
        id TEXT PRIMARY KEY,
        team_name TEXT NOT NULL,
        agency TEXT NOT NULL,
        base_region TEXT,
        base_woreda TEXT,
        contact_phone TEXT,
        personnel_count INTEGER DEFAULT 10,
        current_status TEXT DEFAULT 'AVAILABLE',
        current_latitude REAL,
        current_longitude REAL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS tactical_tasks (
        id TEXT PRIMARY KEY,
        task_code TEXT UNIQUE NOT NULL,
        alert_id TEXT REFERENCES alerts(id),
        incident_id TEXT REFERENCES incidents(id),
        assigned_team_id TEXT NOT NULL REFERENCES emergency_teams(id),
        task_type TEXT NOT NULL,
        priority TEXT NOT NULL,
        instructions_en TEXT,
        instructions_am TEXT,
        target_latitude REAL,
        target_longitude REAL,
        status TEXT DEFAULT 'PENDING',
        dispatched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS broadcast_logs (
        id TEXT PRIMARY KEY,
        alert_id TEXT NOT NULL REFERENCES alerts(id),
        channel TEXT NOT NULL,
        target_area TEXT NOT NULL,
        recipients_estimate INTEGER,
        status TEXT DEFAULT 'QUEUED',
        dispatched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        gateway_reference_id TEXT,
        cost_etb REAL DEFAULT 0.0
    );
    """
]

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for ddl in DDL_STATEMENTS:
        cursor.execute(ddl)
    
    # Seed regions
    cursor.executemany(
        "INSERT OR IGNORE INTO regions VALUES (?, ?, ?, ?, ?, ?)",
        REGIONS_DATA
    )
    # Seed zones
    cursor.executemany(
        "INSERT OR IGNORE INTO zones VALUES (?, ?, ?, ?, ?)",
        ZONES_DATA
    )
    # Seed woredas
    cursor.executemany(
        "INSERT OR IGNORE INTO woredas VALUES (?, ?, ?, ?, ?, ?, ?)",
        WOREDAS_DATA
    )
    # Seed kebeles
    cursor.executemany(
        "INSERT OR IGNORE INTO kebeles VALUES (?, ?, ?, ?, ?, ?)",
        KEBELES_DATA
    )
    # Seed hazards
    cursor.executemany(
        "INSERT OR IGNORE INTO hazard_types VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        HAZARD_TYPES_DATA
    )
    # Seed users
    cursor.executemany(
        "INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)",
        USERS_DATA
    )
    # Seed emergency teams
    cursor.executemany(
        "INSERT OR IGNORE INTO emergency_teams VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        TEAMS_DATA
    )
    
    conn.commit()
    conn.close()
    print("Database schema created and seed data initialized successfully.")

if __name__ == "__main__":
    init_db()
