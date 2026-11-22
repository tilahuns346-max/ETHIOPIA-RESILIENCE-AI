export const INIT_SQLITE_DDL = `
  CREATE TABLE IF NOT EXISTS local_reports (
    local_id TEXT PRIMARY KEY,
    hazard_type_code TEXT,
    latitude REAL,
    longitude REAL,
    description_raw TEXT,
    is_synced INTEGER DEFAULT 0
  );
`;
