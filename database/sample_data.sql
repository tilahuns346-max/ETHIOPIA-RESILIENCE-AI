-- ============================================================================
-- ETHIOPIA RESILIENCE AI — REALISTIC SEED DATA (ETHIOPIAN CONTEXT)
-- Covering: Afar, Amhara, Oromia, Somali, Sidama, South Ethiopia, Addis Ababa
-- Hazards: Floods (Awash Basin), Drought (Borana/Somali), Landslides (Gofa),
-- Wildfires (Bale National Park), Urban Fires (Mercato Addis Ababa), Severe Storms
-- ============================================================================

-- 1. Roles
INSERT INTO roles (role_id, code, title_en, title_am, description) VALUES
('11111111-1111-1111-1111-111111111101', 'SUPER_ADMIN', 'National System Administrator', 'ብሔራዊ የስርዓት አስተዳዳሪ', 'Complete administrative governance and security control'),
('11111111-1111-1111-1111-111111111102', 'NATIONAL_EDRMC_OFFICER', 'National EDRMC Commander', 'የብሔራዊ አደጋ ስጋት ስራ አመራር ኮሚሽን አዛዥ', 'Authorized to authorize national and regional alerts'),
('11111111-1111-1111-1111-111111111103', 'REGIONAL_DIRECTOR', 'Regional DRMC Director', 'የክልል አደጋ መከላከል ዳይሬክተር', 'Authorizes regional emergency warnings and team dispatch'),
('11111111-1111-1111-1111-111111111104', 'WOREDA_FOCAL_PERSON', 'Woreda Disaster Desk Officer', 'የወረዳ አደጋ መከላከል ዴስክ ኃላፊ', 'Verifies incidents in woreda and coordinates local response'),
('11111111-1111-1111-1111-111111111105', 'KEBELE_REPRESENTATIVE', 'Kebele Early Warning Committee Head', 'የቀበሌ ቅድመ ማስጠንቀቂያ ኮሚቴ ሰብሳቢ', 'Local ground verification and community broadcast'),
('11111111-1111-1111-1111-111111111106', 'FIRST_RESPONDER', 'Field First Responder', 'የአደጋ ጊዜ ፈጣን ምላሽ ሰጪ', 'Search and rescue, medical triage, logistics deployment'),
('11111111-1111-1111-1111-111111111107', 'COMMUNITY_REPORTER', 'Community Reporter / Citizen', 'የማህበረሰብ ሪፖርተር / ዜጋ', 'Submits real-time field reports with photos and voice notes');

-- 2. Regions of Ethiopia
INSERT INTO regions (region_id, code, name_en, name_am, capital_en, capital_am, population, area_sqkm, geom, centroid) VALUES
('22222222-2222-2222-2222-222222222201', 'ETH-OR', 'Oromia', 'ኦሮሚያ', 'Addis Ababa', 'አዲስ አበባ', 38000000, 284538.00, ST_Multi(ST_GeomFromText('POLYGON((38.0 7.0, 40.0 7.0, 40.0 9.0, 38.0 9.0, 38.0 7.0))', 4326)), ST_GeomFromText('POINT(39.0 8.0)', 4326)),
('22222222-2222-2222-2222-222222222202', 'ETH-AM', 'Amhara', 'አማራ', 'Bahir Dar', 'ባህር ዳር', 23000000, 154708.00, ST_Multi(ST_GeomFromText('POLYGON((36.5 10.5, 39.5 10.5, 39.5 13.5, 36.5 13.5, 36.5 10.5))', 4326)), ST_GeomFromText('POINT(38.0 12.0)', 4326)),
('22222222-2222-2222-2222-222222222203', 'ETH-AF', 'Afar', 'አፋር', 'Semera', 'ሰመራ', 2000000, 72053.00, ST_Multi(ST_GeomFromText('POLYGON((40.0 10.0, 42.5 10.0, 42.5 14.5, 40.0 14.5, 40.0 10.0))', 4326)), ST_GeomFromText('POINT(41.2 12.2)', 4326)),
('22222222-2222-2222-2222-222222222204', 'ETH-SO', 'Somali', 'ሶማሌ', 'Jijiga', 'ጅጅጋ', 6500000, 279252.00, ST_Multi(ST_GeomFromText('POLYGON((42.0 4.0, 47.0 4.0, 47.0 9.0, 42.0 9.0, 42.0 4.0))', 4326)), ST_GeomFromText('POINT(44.5 6.5)', 4326)),
('22222222-2222-2222-2222-222222222205', 'ETH-SE', 'South Ethiopia', 'ደቡብ ኢትዮጵያ', 'Wolaita Sodo', 'ወላይታ ሶዶ', 7500000, 52000.00, ST_Multi(ST_GeomFromText('POLYGON((36.0 5.5, 38.0 5.5, 38.0 7.0, 36.0 7.0, 36.0 5.5))', 4326)), ST_GeomFromText('POINT(37.0 6.2)', 4326)),
('22222222-2222-2222-2222-222222222206', 'ETH-AA', 'Addis Ababa', 'አዲስ አበባ', 'Addis Ababa', 'አዲስ አበባ', 5200000, 527.00, ST_Multi(ST_GeomFromText('POLYGON((38.65 8.85, 38.85 8.85, 38.85 9.05, 38.65 9.05, 38.65 8.85))', 4326)), ST_GeomFromText('POINT(38.75 8.98)', 4326));

-- 3. Representative Zones
INSERT INTO zones (zone_id, region_id, code, name_en, name_am, administration_center, geom) VALUES
('33333333-3333-3333-3333-333333333301', '22222222-2222-2222-2222-222222222205', 'Z-GOFA', 'Gofa Zone', 'ጎፋ ዞን', 'Sawla', ST_Multi(ST_GeomFromText('POLYGON((36.8 6.1, 37.2 6.1, 37.2 6.5, 36.8 6.5, 36.8 6.1))', 4326))),
('33333333-3333-3333-3333-333333333302', '22222222-2222-2222-2222-222222222203', 'Z-AFAR3', 'Zone 3 (Gabi Rasu)', 'ዞን 3 (ገቢ ራሱ)', 'Awash', ST_Multi(ST_GeomFromText('POLYGON((39.8 8.8, 40.5 8.8, 40.5 9.4, 39.8 9.4, 39.8 8.8))', 4326))),
('33333333-3333-3333-3333-333333333303', '22222222-2222-2222-2222-222222222201', 'Z-BORANA', 'Borana Zone', 'ቦረና ዞን', 'Yabelo', ST_Multi(ST_GeomFromText('POLYGON((37.8 4.2, 39.2 4.2, 39.2 5.3, 37.8 5.3, 37.8 4.2))', 4326))),
('33333333-3333-3333-3333-333333333304', '22222222-2222-2222-2222-222222222201', 'Z-BALE', 'Bale Zone', 'ባሌ ዞን', 'Robe', ST_Multi(ST_GeomFromText('POLYGON((39.5 6.5, 40.8 6.5, 40.8 7.5, 39.5 7.5, 39.5 6.5))', 4326))),
('33333333-3333-3333-3333-333333333305', '22222222-2222-2222-2222-222222222206', 'Z-AA-KETEMA', 'Addis Ketema Sub-City', 'አዲስ ከተማ ክፍለ ከተማ', 'Mercato', ST_Multi(ST_GeomFromText('POLYGON((38.72 9.02, 38.76 9.02, 38.76 9.05, 38.72 9.05, 38.72 9.02))', 4326)));

-- 4. Representative Woredas
INSERT INTO woredas (woreda_id, zone_id, code, name_en, name_am, risk_profile_json, geom) VALUES
('44444444-4444-4444-4444-444444444401', '33333333-3333-3333-3333-333333333301', 'W-GEZE-GOFA', 'Geze Gofa', 'ገዜ ጎፋ', '{"primary_hazard": "LANDSLIDE", "slope_steepness": "HIGH", "soil_type": "CLAY_LOAM"}'::jsonb, ST_Multi(ST_GeomFromText('POLYGON((36.85 6.15, 37.05 6.15, 37.05 6.35, 36.85 6.35, 36.85 6.15))', 4326))),
('44444444-4444-4444-4444-444444444402', '33333333-3333-3333-3333-333333333302', 'W-AWASH-FENTALE', 'Awash Fentale', 'አዋሽ ፈንታሌ', '{"primary_hazard": "RIVER_FLOOD", "river_basin": "AWASH", "flood_frequency": "ANNUAL"}'::jsonb, ST_Multi(ST_GeomFromText('POLYGON((39.85 8.90, 40.15 8.90, 40.15 9.15, 39.85 9.15, 39.85 8.90))', 4326))),
('44444444-4444-4444-4444-444444444403', '33333333-3333-3333-3333-333333333303', 'W-YABELO', 'Yabelo', 'ያቤሎ', '{"primary_hazard": "DROUGHT", "livestock_density": "HIGH", "pastoralist_dependency": "CRITICAL"}'::jsonb, ST_Multi(ST_GeomFromText('POLYGON((38.00 4.80, 38.30 4.80, 38.30 5.10, 38.00 5.10, 38.00 4.80))', 4326))),
('44444444-4444-4444-4444-444444444404', '33333333-3333-3333-3333-333333333304', 'W-DINSHO', 'Dinsho (Bale)', 'ዲንሾ (ባሌ)', '{"primary_hazard": "WILDFIRE", "forest_coverage": "HEATHLAND", "endemic_species": "ETHIOPIAN_WOLF"}'::jsonb, ST_Multi(ST_GeomFromText('POLYGON((39.75 6.90, 40.05 6.90, 40.05 7.15, 39.75 7.15, 39.75 6.90))', 4326))),
('44444444-4444-4444-4444-444444444405', '33333333-3333-3333-3333-333333333305', 'W-MERCATO', 'Woreda 01 (Mercato)', 'ወረዳ 01 (መርካቶ)', '{"primary_hazard": "URBAN_FIRE", "commercial_density": "EXTREME", "water_hydrant_access": "LIMITED"}'::jsonb, ST_Multi(ST_GeomFromText('POLYGON((38.73 9.02, 38.75 9.02, 38.75 9.04, 38.73 9.04, 38.73 9.02))', 4326)));

-- 5. Kebeles
INSERT INTO kebeles (kebele_id, woreda_id, code, name_en, name_am, emergency_contact_phone, population, geom) VALUES
('55555555-5555-5555-5555-555555555501', '44444444-4444-4444-4444-444444444401', 'K-KENCHO-SHACHA', 'Kencho Shacha Gozdi', 'ከንቾ ሻቻ ጎዝዲ', '+251911223344', 4500, ST_Multi(ST_GeomFromText('POLYGON((36.90 6.20, 36.95 6.20, 36.95 6.25, 36.90 6.25, 36.90 6.20))', 4326))),
('55555555-5555-5555-5555-555555555502', '44444444-4444-4444-4444-444444444402', 'K-SABURE', 'Sabure Kebele', 'ሳቡሬ ቀበሌ', '+251922334455', 6800, ST_Multi(ST_GeomFromText('POLYGON((39.95 8.95, 40.05 8.95, 40.05 9.05, 39.95 9.05, 39.95 8.95))', 4326))),
('55555555-5555-5555-5555-555555555503', '44444444-4444-4444-4444-444444444405', 'K-SHEMA-TERA', 'Shema Tera Kebele', 'ሸማ ተራ ቀበሌ', '+251933445566', 22000, ST_Multi(ST_GeomFromText('POLYGON((38.735 9.025, 38.745 9.025, 38.745 9.035, 38.735 9.035, 38.735 9.025))', 4326)));

-- 6. Hazard Types
INSERT INTO hazards (hazard_type_id, code, name_en, name_am, category, description_en, description_am, icon_name, color_hex) VALUES
('66666666-6666-6666-6666-666666666601', 'HAZ-FLOOD', 'Riverine & Flash Flood', 'የወንዝ እና ድንገተኛ ጎርፍ', 'HYDROLOGICAL', 'Overflow of river banks and rapid surface runoff inundating villages and farmland', 'የወንዞች መሙላትና ከመጠን ያለፈ የውሃ ፍሰት ሰብልና መንደሮችን የሚያጥለቀልቅ አደጋ', 'water-outline', '#0284c7'),
('66666666-6666-6666-6666-666666666602', 'HAZ-LANDSLIDE', 'Debris Flow & Landslide', 'የመሬት መንሸራተት እና ናዳ', 'GEOPHYSICAL', 'Mass movement of soil and rock debris triggered by prolonged rainfall and slope saturation', 'በከባድ ዝናብ ሳቢያ የተራራ ቁልቁለት አፈርና ድንጋይ መደርመስ የሚያስከትለው አደጋ', 'terrain-outline', '#ea580c'),
('66666666-6666-6666-6666-666666666603', 'HAZ-DROUGHT', 'Severe Agricultural Drought', 'ከባድ የግብርና እና የግጦሽ ድርቅ', 'CLIMATOLOGICAL', 'Prolonged deficit of rainfall leading to pasture depletion, crop failure, and livestock death', 'የዝናብ እጥረት በሰብልና በከብቶች እርባታ ላይ የሚያደርሰው የረሃብና የውሃ እጥረት አደጋ', 'sunny-outline', '#d97706'),
('66666666-6666-6666-6666-666666666604', 'HAZ-WILDFIRE', 'Forest & Bush Fire', 'የደን እና የሰደድ እሳት', 'CLIMATOLOGICAL', 'Uncontrolled fire spreading rapidly through national parks, woodlands, and grazing ranges', 'በተፈጥሮ ደኖች እና ብሔራዊ ፓርኮች ውስጥ በፍጥነት የሚዛመት አጥፊ እሳት', 'flame-outline', '#dc2626'),
('66666666-6666-6666-6666-666666666605', 'HAZ-URBAN-FIRE', 'High-Density Urban Fire', 'የከተማ እና የገበያ እሳት አደጋ', 'URBAN', 'Rapid-spreading conflagration in commercial centers, warehouses, and informal settlements', 'በንግድ ስፍራዎችና በመኖሪያ ሰፈሮች የሚከሰት ፈጣን የቃጠሎ አደጋ', 'business-outline', '#b91c1c'),
('66666666-6666-6666-6666-666666666606', 'HAZ-SEVERE-STORM', 'Hailstorm & Gale Winds', 'ኃይለኛ የበረዶ ዝናብ እና አውሎ ንፋስ', 'HYDROLOGICAL', 'Violent atmospheric storms damaging roofs, electrical grids, and ready-to-harvest crops', 'ጣሪያና የኤሌክትሪክ መስመሮችን የሚሰብር ብርቱ ንፋስና በረዶ የተቀላቀለበት ዝናብ', 'thunderstorm-outline', '#7c3aed');

-- 7. Users
INSERT INTO users (user_id, username, email, phone_number, password_hash, full_name, role_id, assigned_woreda_id, preferred_language, badge_number, is_active, is_phone_verified, trust_score) VALUES
('77777777-7777-7777-7777-777777777701', 'admin.national', 'admin@resilience.gov.et', '+251911000001', 'pbkdf2_sha256$600000$ethSec$saltedhash123', 'Abebe Tadesse Bekele', '11111111-1111-1111-1111-111111111101', NULL, 'am', 'EDRMC-ADM-001', TRUE, TRUE, 5.00),
('77777777-7777-7777-7777-777777777702', 'commander.edrmc', 'commander@edrmc.gov.et', '+251911000002', 'pbkdf2_sha256$600000$ethSec$saltedhash456', 'Dr. Senait Hailemariam', '11111111-1111-1111-1111-111111111102', NULL, 'am', 'EDRMC-CMD-009', TRUE, TRUE, 5.00),
('77777777-7777-7777-7777-777777777703', 'gofa.focal', 'focal.gofa@resilience.gov.et', '+251911000003', 'pbkdf2_sha256$600000$ethSec$saltedhash789', 'Mulugeta Woldeyes', '11111111-1111-1111-1111-111111111104', '44444444-4444-4444-4444-444444444401', 'am', 'SZ-GOFA-042', TRUE, TRUE, 4.80),
('77777777-7777-7777-7777-777777777704', 'citizen.kencho', 'reporter1@gmail.com', '+251922114477', 'pbkdf2_sha256$600000$ethSec$saltedhash012', 'Chala Benti Gemechu', '11111111-1111-1111-1111-111111111107', '44444444-4444-4444-4444-444444444401', 'am', NULL, TRUE, TRUE, 4.20);

-- 8. Incidents
INSERT INTO incidents (incident_id, incident_number, reporter_user_id, hazard_type_id, kebele_id, title_en, title_am, description_raw, description_summary_ai, location, status, verification_status, severity_level, estimated_affected_people, casualties_count, reported_at, verified_at, verified_by_user_id, verification_notes) VALUES
('88888888-8888-8888-8888-888888888801', 'INC-2026-00412', '77777777-7777-7777-7777-777777777704', '66666666-6666-6666-6666-666666666602', '55555555-5555-5555-5555-555555555501', 
'Massive Landslide on Hillside Slope - Kencho Shacha', 
'በከንቾ ሻቻ ተራራማ ቁልቁለት ላይ የተከሰተ ከባድ የመሬት ናዳ', 
'ከ3 ቀናት ተከታታይ ከባድ ዝናብ በኋላ የተራራው አፈር ተደርምሶ 18 ቤቶችን ሙሉ በሙሉ አጥለቅልቋል። ተጨማሪ ናዳ የመከሰት ከፍተኛ ስጋት አለ። ህዝቡ በአስቸኳይ መውጣት አለበት።', 
'ከባድ ዝናብ ተከትሎ በተከሰተ የመሬት መንሸራተት 18 ቤቶች ተደርምሰዋል፤ ተጨማሪ የመሬት መንቀጥቀጥና ናዳ ስጋት ስላለ ፈጣን የማስወጣት ስራ ያስፈልጋል።', 
ST_GeomFromText('POINT(36.9214 6.2241)', 4326), 'RESPONDING', 'OFFICIALLY_VERIFIED', 'LEVEL_4_CRITICAL', 250, 4, CURRENT_TIMESTAMP - INTERVAL '3 hours', CURRENT_TIMESTAMP - INTERVAL '2 hours', '77777777-7777-7777-7777-777777777703', 'Ground inspection confirmed severe fissure widening. Immediate evacuation ordered.'),

('88888888-8888-8888-8888-888888888802', 'INC-2026-00413', NULL, '66666666-6666-6666-6666-666666666601', '55555555-5555-5555-5555-555555555502', 
'Awash River Bank Breach Near Sabure Agricultural Village', 
'በሳቡሬ እርሻ መንደር አቅራቢያ የአዋሽ ወንዝ ዳርቻ መጣስ', 
'የአዋሽ ወንዝ ሞልቶ ግድቡን ሰብሮ ወደ ሰብል ማሳዎችና ወደ መንደሩ ጎርፉ እየገባ ነው። ወደ 400 የሚጠጉ አባወራዎች ከብቶቻቸውን ይዘው ወደ ኮረብታ እየሸሹ ነው።', 
'የአዋሽ ወንዝ ሙላት የገጠር እርሻዎችንና ቤቶችን እያጥለቀለቀ ነው፤ ወደ 400 አባወራዎች ተፈናቅለዋል።', 
ST_GeomFromText('POINT(40.0125 9.0142)', 4326), 'VERIFIED', 'OFFICIALLY_VERIFIED', 'LEVEL_3_HIGH', 1200, 0, CURRENT_TIMESTAMP - INTERVAL '5 hours', CURRENT_TIMESTAMP - INTERVAL '4 hours', '77777777-7777-7777-7777-777777777702', 'Water gauge at Sabure reached 4.8m exceeding emergency threshold.');

-- 9. AI Risk Predictions
INSERT INTO ai_predictions (prediction_id, model_name, model_version, hazard_type_id, target_woreda_id, target_kebele_id, target_geometry, predicted_severity, risk_probability, uncertainty_lower, uncertainty_upper, feature_importance_weights, input_features_digest, valid_until, is_reviewed_by_human, review_status) VALUES
('99999999-9999-9999-9999-999999999901', 'ETH-GEO-SLOPE-RISK-XGB', 'v2.4.1', '66666666-6666-6666-6666-666666666602', '44444444-4444-4444-4444-444444444401', '55555555-5555-5555-5555-555555555501', 
ST_GeomFromText('POLYGON((36.90 6.20, 36.95 6.20, 36.95 6.25, 36.90 6.25, 36.90 6.20))', 4326), 'LEVEL_4_CRITICAL', 0.912, 0.865, 0.948, 
'{"72h_antecedent_rainfall_mm": 0.42, "slope_gradient_degrees": 0.28, "soil_saturation_index": 0.18, "deforestation_rate": 0.12}'::jsonb, 
'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', CURRENT_TIMESTAMP + INTERVAL '24 hours', TRUE, 'ACCEPTED');

-- 10. Official Human-Approved Alert (Safety Invariant Demonstration)
INSERT INTO alerts (alert_id, alert_code, hazard_type_id, severity_level, status, title_en, title_am, message_en, message_am, affected_polygon, evacuation_order_issued, ai_prediction_id, drafted_by_user_id, approved_by_officer_id, approval_timestamp, officer_digital_signature, approval_reasoning, valid_from, valid_until) VALUES
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'ALT-ETH-2026-089', '66666666-6666-6666-6666-666666666602', 'LEVEL_4_CRITICAL', 'APPROVED_BY_OFFICER', 
'CRITICAL EVACUATION ORDER: Gofa Zone Mountain Slopes', 
'አስቸኳይ የመልቀቂያ ትዕዛዝ፡ በጎፋ ዞን ከንቾ ሻቻ ተራራማ መንደሮች', 
'EXTREME LANDSLIDE RISK: High saturation and ground fissures detected. All residents of Kencho Shacha must evacuate immediately to the designated high-ground school compound.', 
'ከፍተኛ የመሬት መንሸራተት አደጋ፡ በከንቾ ሻቻና አካባቢው የሚገኙ ነዋሪዎች ተጨማሪ ናዳ ከመከሰቱ በፊት በአስቸኳይ አካባቢውን ለቀው ወደ ተዘጋጀው አስተማማኝ መጠለያ እንዲሄዱ በጥብቅ እናሳስባለን።', 
ST_Multi(ST_GeomFromText('POLYGON((36.88 6.18, 36.97 6.18, 36.97 6.27, 36.88 6.27, 36.88 6.18))', 4326)), 
TRUE, '99999999-9999-9999-9999-999999999901', '77777777-7777-7777-7777-777777777703', '77777777-7777-7777-7777-777777777702', CURRENT_TIMESTAMP - INTERVAL '1 hour', 
'SHA256:ECDSA:9f8a83d47b1e5...EDRMC-HAILMARIAM-AUTH', 
'AI slope stability model confirmed critical threshold (P=0.91) corroborated by on-the-ground woreda officer visual evidence.', 
CURRENT_TIMESTAMP - INTERVAL '1 hour', CURRENT_TIMESTAMP + INTERVAL '48 hours');

-- 11. Response Teams
INSERT INTO response_teams (team_id, code, name, organization_type, base_woreda_id, leader_name, leader_phone, personnel_count, current_status, current_location) VALUES
('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbb01', 'RT-RED-CROSS-01', 'Ethiopian Red Cross Rapid Disaster Unit', 'ETHIOPIAN_RED_CROSS', '44444444-4444-4444-4444-444444444401', 'Sister Almaz Kebede', '+251911448822', 14, 'ON_MISSION', ST_GeomFromText('POINT(36.9200 6.2200)', 4326)),
('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbb02', 'RT-EDRMC-RESCUE-04', 'EDRMC Southern Heavy Rescue Battalion', 'EDRMC', '44444444-4444-4444-4444-444444444401', 'Commander Daniel Bekele', '+251911559933', 25, 'MOBILIZING', ST_GeomFromText('POINT(36.8900 6.2100)', 4326)),
('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbb03', 'RT-AA-FIRE-MERCATO', 'Mercato Fire Brigade Station 3', 'FIRE_AND_EMERGENCY', '44444444-4444-4444-4444-444444444405', 'Capt. Kassahun Ayalew', '+251911660044', 18, 'STANDBY', ST_GeomFromText('POINT(38.7400 9.0300)', 4326));

-- 12. Response Tasks
INSERT INTO response_tasks (task_id, incident_id, alert_id, team_id, task_code, task_type, priority, status, instructions_en, instructions_am, target_location, assigned_by_user_id) VALUES
('cccccccc-cccc-cccc-cccc-cccccccccccc', '88888888-8888-8888-8888-888888888801', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbb01', 'TSK-2026-0091', 'SEARCH_AND_RESCUE', 'LEVEL_4_CRITICAL', 'ON_SCENE', 
'Deploy search canine units and acoustic sensors to Sector B debris zone. Triage survivors to Sawla General Hospital.', 
'የአደጋ ፍለጋና ማዳን ቡድኑ በሴክተር ቢ ፍርስራሽ ውስጥ ህይወት ያላቸውን ሰዎች እንዲፈልግና ለተጎዱት የመጀመሪያ የህክምና እርዳታ እንዲሰጥ።', 
ST_GeomFromText('POINT(36.9220 6.2250)', 4326), '77777777-7777-7777-7777-777777777703');

-- 13. Audit Log Sample
INSERT INTO audit_logs (audit_id, actor_user_id, action_type, entity_table, entity_id, client_ip, user_agent, new_state, cryptographic_hash) VALUES
('dddddddd-dddd-dddd-dddd-dddddddddddd', '77777777-7777-7777-7777-777777777702', 'ALERT_OFFICIALLY_APPROVED', 'alerts', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '196.188.42.10', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) EDRMC-Portal/2.1', 
'{"status": "APPROVED_BY_OFFICER", "approver": "Dr. Senait Hailemariam", "level": "LEVEL_4_CRITICAL"}'::jsonb, 
'7d4a2cf5a134b22f6e917d2a8b30ef1d3e8a719c2a68e8b09312dcfa56291a0c');
