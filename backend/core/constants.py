"""
System Constants & Disaster Taxonomy for Ethiopia Resilience AI
"""

# Administrative Tiers in Ethiopia
ADMIN_TIERS = {
    "NATIONAL": 0,
    "REGION": 1,
    "ZONE": 2,
    "WOREDA": 3,
    "KEBELE": 4,
    "GOTE": 5
}

# 12 Regional States & 2 Chartered Cities
OFFICIAL_REGIONS = [
    {"code": "REG-AA", "name_en": "Addis Ababa", "name_am": "አዲስ አበባ"},
    {"code": "REG-AF", "name_en": "Afar", "name_am": "አፋር"},
    {"code": "REG-AM", "name_en": "Amhara", "name_am": "አማራ"},
    {"code": "REG-BG", "name_en": "Benishangul-Gumuz", "name_am": "ቤንሻንጉል ጉሙዝ"},
    {"code": "REG-DD", "name_en": "Dire Dawa", "name_am": "ድሬዳዋ"},
    {"code": "REG-CB", "name_en": "Central Ethiopia", "name_am": "ማዕከላዊ ኢትዮጵያ"},
    {"code": "REG-GA", "name_en": "Gambela", "name_am": "ጋምቤላ"},
    {"code": "REG-HA", "name_en": "Harari", "name_am": "ሐረሪ"},
    {"code": "REG-OR", "name_en": "Oromia", "name_am": "ኦሮሚያ"},
    {"code": "REG-SE", "name_en": "South Ethiopia", "name_am": "ደቡብ ኢትዮጵያ"},
    {"code": "REG-SW", "name_en": "South West Ethiopia", "name_am": "ደቡብ ምዕራብ ኢትዮጵያ"},
    {"code": "REG-SI", "name_en": "Sidama", "name_am": "ሲዳማ"},
    {"code": "REG-SO", "name_en": "Somali", "name_am": "ሶማሌ"},
    {"code": "REG-TG", "name_en": "Tigray", "name_am": "ትግራይ"}
]

# Severity Levels
SEVERITY_LEVELS = {
    "LEVEL_1_LOW": {"rank": 1, "color": "#10b981", "name_am": "ደረጃ 1 - ዝቅተኛ"},
    "LEVEL_2_MODERATE": {"rank": 2, "color": "#f59e0b", "name_am": "ደረጃ 2 - መካከለኛ"},
    "LEVEL_3_HIGH": {"rank": 3, "color": "#f97316", "name_am": "ደረጃ 3 - ከፍተኛ"},
    "LEVEL_4_CRITICAL": {"rank": 4, "color": "#dc2626", "name_am": "ደረጃ 4 - እጅግ አደገኛ"}
}

# Ethiopia Geographic Bounding Box
ETHIOPIA_GEO_BOUNDS = {
    "min_lat": 3.4,
    "max_lat": 14.9,
    "min_lon": 32.9,
    "max_lon": 48.0
}

# Phone Regex for Ethiopia (+251 9... or +251 7...)
ETHIO_PHONE_REGEX = r"^\+251(9|7)\d{8}$"
