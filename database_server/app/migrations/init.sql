# שמות מבצעי האירוע
CREATE TABLE terrorist_organizations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);
# סוגי הנשק/התקפות
CREATE TABLE weapon_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);
# סוג מטרה
CREATE TABLE target_types (
    id SERIAL PRIMARY KEY,
    type VARCHAR(255) UNIQUE
);

CREATE TABLE motive (
    id SERIAL PRIMARY KEY,
    motive VARCHAR(255) UNIQUE
);
# תאריך
CREATE TABLE dates (
    id SERIAL PRIMARY KEY,
    day INTEGER,
    month INTEGER,
    year INTEGER NOT NULL,
    UNIQUE(day, month, year)
);
# מיקום שמי
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    city VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL,
    region VARCHAR(255) NOT NULL,
    UNIQUE(city, country, region)
);
# מיקום קווי אורך ורוחב
CREATE TABLE coordinate(
    id SERIAL PRIMARY KEY,
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    UNIQUE (latitude, longitude)
                       );
# טבלת אירועים (טבלה ראשית\מקשרת)
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