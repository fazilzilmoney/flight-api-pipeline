-- ==========================================================
-- CREATE DATABASE
-- ==========================================================

CREATE DATABASE flight_data;


-- ==========================================================
-- CONNECT TO flight_data
-- ==========================================================

\c flight_data


-- ==========================================================
-- CREATE AIRCRAFT POSITIONS TABLE
-- ==========================================================

CREATE TABLE aircraft_positions (
    id SERIAL PRIMARY KEY,

    aircraft_id VARCHAR(20),

    callsign VARCHAR(50),

    origin_country VARCHAR(100),

    time_position BIGINT,

    last_contact BIGINT,

    longitude DOUBLE PRECISION,

    latitude DOUBLE PRECISION,

    baro_altitude DOUBLE PRECISION,

    on_ground BOOLEAN,

    velocity DOUBLE PRECISION,

    true_track DOUBLE PRECISION,

    vertical_rate DOUBLE PRECISION,

    geo_altitude DOUBLE PRECISION,

    squawk VARCHAR(10),

    spi BOOLEAN,

    position_source INTEGER,

    collected_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    sensors TEXT
);


-- ==========================================================
-- PREVENT DUPLICATE AIRCRAFT OBSERVATIONS
-- ==========================================================

ALTER TABLE aircraft_positions
ADD CONSTRAINT unique_aircraft_last_contact
UNIQUE (aircraft_id, last_contact);


-- ==========================================================
-- CREATE PIPELINE RUN TRACKING TABLE
-- ==========================================================

CREATE TABLE pipeline_runs (
    run_id SERIAL PRIMARY KEY,

    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    completed_at TIMESTAMP,

    records_extracted INTEGER DEFAULT 0,

    records_inserted INTEGER DEFAULT 0,

    records_skipped INTEGER DEFAULT 0,

    records_failed INTEGER DEFAULT 0,

    status VARCHAR(20),

    error_message TEXT,

    duration_seconds NUMERIC
);