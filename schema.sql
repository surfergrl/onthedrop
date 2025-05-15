-- schema.sql for PostgreSQL
CREATE TABLE IF NOT EXISTS beaches (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    spot_type TEXT,
    wave TEXT,
    offshore TEXT,
    tide TEXT,
    level TEXT
);