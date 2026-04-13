-- ============================================================
-- BRAJ SAHAYAK
-- PostgreSQL schema aligned with app/db/models.py
-- ============================================================

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE temples (
    id               SERIAL PRIMARY KEY,
    code             VARCHAR(60) UNIQUE NOT NULL,
    name_en          VARCHAR(200) NOT NULL,
    name_hi          VARCHAR(200),
    name_bn          VARCHAR(200),
    name_ta          VARCHAR(200),
    area             VARCHAR(120),
    city             VARCHAR(80) DEFAULT 'Vrindavan',
    latitude         DECIMAL(9, 6),
    longitude        DECIMAL(9, 6),
    notes            TEXT,
    source_url       TEXT,
    source_type      VARCHAR(30),
    confidence_level VARCHAR(20),
    entry_fee_note   TEXT,
    footwear_note_en TEXT,
    mobile_note_en   TEXT,
    dress_code_en    TEXT,
    is_active        BOOLEAN NOT NULL DEFAULT TRUE,
    created_at       TIMESTAMP DEFAULT NOW(),
    updated_at       TIMESTAMP DEFAULT NOW()
);

CREATE TABLE schedules (
    id             SERIAL PRIMARY KEY,
    temple_id      INT REFERENCES temples(id) ON DELETE CASCADE,
    season         VARCHAR(30),
    open_morning   TIME,
    close_morning  TIME,
    bhog_start     TIME,
    bhog_end       TIME,
    open_evening   TIME,
    close_evening  TIME,
    notes_en       TEXT,
    notes_hi       TEXT,
    source_url     TEXT,
    verified_by    VARCHAR(100),
    verified_at    TIMESTAMP,
    is_current     BOOLEAN NOT NULL DEFAULT TRUE,
    created_at     TIMESTAMP DEFAULT NOW()
);

CREATE TABLE festival_overrides (
    id             SERIAL PRIMARY KEY,
    temple_id      INT REFERENCES temples(id) ON DELETE CASCADE,
    festival_name  VARCHAR(120),
    date_from      DATE NOT NULL,
    date_to        DATE NOT NULL,
    open_morning   TIME,
    close_morning  TIME,
    open_evening   TIME,
    close_evening  TIME,
    notice_text_en TEXT,
    notice_text_hi TEXT,
    is_active      BOOLEAN NOT NULL DEFAULT TRUE,
    created_at     TIMESTAMP DEFAULT NOW()
);

CREATE TABLE temple_advisories (
    id            SERIAL PRIMARY KEY,
    temple_id     INT REFERENCES temples(id) ON DELETE CASCADE,
    advisory_type VARCHAR(50),
    message_en    TEXT NOT NULL,
    message_hi    TEXT,
    message_bn    TEXT,
    message_ta    TEXT,
    priority      INT NOT NULL DEFAULT 1,
    is_active     BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE route_points (
    id         SERIAL PRIMARY KEY,
    code       VARCHAR(60) UNIQUE NOT NULL,
    name_en    VARCHAR(150) NOT NULL,
    name_hi    VARCHAR(150),
    name_bn    VARCHAR(150),
    name_ta    VARCHAR(150),
    area       VARCHAR(120),
    city       VARCHAR(80),
    point_type VARCHAR(40),
    latitude   DECIMAL(9, 6),
    longitude  DECIMAL(9, 6)
);

CREATE TABLE routes (
    id               SERIAL PRIMARY KEY,
    from_point_id    INT REFERENCES route_points(id),
    temple_id        INT REFERENCES temples(id),
    mode             VARCHAR(30),
    duration_min_est INT,
    fare_min         INT,
    fare_max         INT,
    fare_currency    VARCHAR(5) DEFAULT 'INR',
    route_text_en    TEXT NOT NULL,
    route_text_hi    TEXT,
    route_text_bn    TEXT,
    route_text_ta    TEXT,
    map_link         TEXT,
    last_mile_note   TEXT,
    is_active        BOOLEAN NOT NULL DEFAULT TRUE,
    is_verified      BOOLEAN NOT NULL DEFAULT FALSE,
    verified_at      TIMESTAMP
);

CREATE TABLE fare_guides (
    id           SERIAL PRIMARY KEY,
    from_label   VARCHAR(120),
    to_label     VARCHAR(120),
    service_type VARCHAR(60),
    fare_min     INT,
    fare_max     INT,
    currency     VARCHAR(5) DEFAULT 'INR',
    fare_note_en TEXT,
    is_official  BOOLEAN NOT NULL DEFAULT FALSE,
    source_label VARCHAR(100),
    verified_at  TIMESTAMP
);

CREATE TABLE partner_categories (
    id             SERIAL PRIMARY KEY,
    code           VARCHAR(60) UNIQUE NOT NULL,
    name           VARCHAR(80) NOT NULL,
    name_en        VARCHAR(80),
    name_hi        VARCHAR(80),
    icon_emoji     VARCHAR(16),
    slug           VARCHAR(60) UNIQUE NOT NULL,
    priority_order INT NOT NULL DEFAULT 10
);

CREATE TABLE partners (
    id               SERIAL PRIMARY KEY,
    category_id      INT REFERENCES partner_categories(id),
    name             VARCHAR(200) NOT NULL,
    phone            VARCHAR(30),
    whatsapp         VARCHAR(30),
    area             VARCHAR(120),
    temple_focus     VARCHAR(80),
    short_desc_en    TEXT,
    price_note       TEXT,
    verified         BOOLEAN NOT NULL DEFAULT FALSE,
    verified_by      VARCHAR(100),
    verified_at      TIMESTAMP,
    plan_type        VARCHAR(20),
    monthly_fee      INT,
    subscription_end DATE,
    is_active        BOOLEAN NOT NULL DEFAULT TRUE,
    created_at       TIMESTAMP DEFAULT NOW()
);

CREATE TABLE user_sessions (
    id                  SERIAL PRIMARY KEY,
    wa_number           VARCHAR(30) UNIQUE NOT NULL,
    language_code       VARCHAR(10) NOT NULL DEFAULT 'en',
    current_state       VARCHAR(60) NOT NULL DEFAULT 'language_select',
    prev_state          VARCHAR(60),
    last_intent         VARCHAR(60),
    last_entity         VARCHAR(80),
    selected_temple     VARCHAR(60),
    selected_route_from VARCHAR(60),
    pending_action      VARCHAR(20),
    selected_area       VARCHAR(50),
    message_count       INT NOT NULL DEFAULT 0,
    updated_at          TIMESTAMP DEFAULT NOW(),
    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE TABLE support_requests (
    id            SERIAL PRIMARY KEY,
    wa_number     VARCHAR(30),
    language_code VARCHAR(10),
    request_type  VARCHAR(60),
    temple_id     INT REFERENCES temples(id),
    message_text  TEXT,
    status        VARCHAR(30) NOT NULL DEFAULT 'open',
    assigned_to   VARCHAR(100),
    notes         TEXT,
    created_at    TIMESTAMP DEFAULT NOW(),
    resolved_at   TIMESTAMP
);

CREATE TABLE query_logs (
    id              SERIAL PRIMARY KEY,
    wa_number       VARCHAR(30),
    language_code   VARCHAR(10),
    incoming_text   TEXT,
    detected_state  VARCHAR(60),
    detected_intent VARCHAR(60),
    detected_entity VARCHAR(80),
    response_status VARCHAR(30) NOT NULL DEFAULT 'ok',
    processing_ms   INT,
    created_at      TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_schedules_temple_current ON schedules(temple_id, is_current, season);
CREATE INDEX idx_festival_overrides_dates ON festival_overrides(temple_id, date_from, date_to);
CREATE INDEX idx_routes_from_temple ON routes(from_point_id, temple_id, mode);
CREATE INDEX idx_partners_category_active ON partners(category_id, is_active, plan_type);
CREATE INDEX idx_query_logs_created ON query_logs(created_at DESC);
CREATE INDEX idx_user_sessions_number ON user_sessions(wa_number);
