-- שמות מבצעי האירוע
CREATE TABLE terrorist_organizations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);
-- סוגי הנשק/התקפות
CREATE TABLE weapon_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);
-- סוג מטרה
CREATE TABLE target_types (
    id SERIAL PRIMARY KEY,
    type VARCHAR(255) UNIQUE
);

CREATE TABLE motive (
    id SERIAL PRIMARY KEY,
    motive VARCHAR(255) UNIQUE
);
-- תאריך
CREATE TABLE dates (
    id SERIAL PRIMARY KEY,
    day INTEGER,
    month INTEGER,
    year INTEGER NOT NULL,
    UNIQUE(day, month, year)
);
-- מיקום שמי
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    city VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL,
    region VARCHAR(255) NOT NULL,
    UNIQUE(city, country, region)
);
-- מיקום קווי אורך ורוחב
CREATE TABLE coordinate(
    id SERIAL PRIMARY KEY,
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    UNIQUE (latitude, longitude)
                       );
-- טבלת אירועים (טבלה ראשית\מקשרת)
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    date_id INTEGER REFERENCES dates(id),
    location_id INTEGER REFERENCES locations(id),
    coordinate_id INTEGER REFERENCES coordinate(id),
    organization_id INTEGER REFERENCES terrorist_organizations(id),
    weapon_id INTEGER REFERENCES weapon_types(id),
    target_id INTEGER REFERENCES target_types(id),
    motive_id INTEGER REFERENCES motive(id)
    nperps INTEGER,
    casualties INTEGER DEFAULT 0,
    injuries INTEGER DEFAULT 0,
    source VARCHAR(255),
    description TEXT
);


-- אינדקסים לטבלת מיקומים
CREATE INDEX idx_locations_region ON locations(region);
CREATE INDEX idx_locations_country ON locations(country);
CREATE INDEX idx_locations_composite ON locations(region, country, city);

-- אינדקסים לטבלת תאריכים
CREATE INDEX idx_dates_year ON dates(year);
CREATE INDEX idx_dates_year_month ON dates(year, month);

-- אינדקס מרחבי לקואורדינטות
CREATE INDEX idx_coordinate_spatial ON coordinate USING GIST (
    ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)
);

-- אינדקס לחיפוש טקסטואלי
CREATE INDEX idx_events_description_gin ON events USING GIN (to_tsvector('english', description));

-- לחישובי קטלניות ונפגעים
CREATE INDEX idx_events_casualties ON events(casualties, injuries);

-- לניתוח לפי סוג התקפה
CREATE INDEX idx_events_weapon_casualties ON events(weapon_id, casualties, injuries);

-- לניתוח לפי ארגון
CREATE INDEX idx_events_organization_region ON events(organization_id, location_id);

-- לניתוח טמפורלי
CREATE INDEX idx_events_date_location ON events(date_id, location_id);

-- לניתוח מגמות וקורלציות
CREATE INDEX idx_events_target_weapon ON events(target_id, weapon_id);
CREATE INDEX idx_events_nperps_casualties ON events(nperps, casualties, injuries);

-- לניתוח גיאוגרפי
CREATE INDEX idx_events_location_time ON events(location_id, date_id);

-- לניתוח קבוצות ומטרות
CREATE INDEX idx_events_org_target ON events(organization_id, target_id);

-- חיפוש מקורות
CREATE INDEX idx_events_source ON events(source);

-- חיפוש טקסט מלא
CREATE INDEX idx_events_full_text ON events USING GIN (
    to_tsvector('english',
        coalesce(description,'') || ' ' ||
        coalesce(source,'')
    )
);

-- לסינון לפי תאריך עדכון
CREATE INDEX idx_events_created_at ON events(created_at);

-- לסינון לפי סוג מידע (היסטורי/זמן אמת)
CREATE INDEX idx_events_type ON events(event_type);