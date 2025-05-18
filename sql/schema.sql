-- Crear tablas para el proyecto

CREATE TABLE IF NOT EXISTS raw_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    source VARCHAR(100) NOT NULL,
    data JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS processed_data (
    id SERIAL PRIMARY KEY,
    raw_data_id INTEGER REFERENCES raw_data(id),
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS final_data (
    id SERIAL PRIMARY KEY,
    processed_data_id INTEGER REFERENCES processed_data(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metrics JSONB NOT NULL,
    insights TEXT
);

-- Índices para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_raw_data_timestamp ON raw_data(timestamp);
CREATE INDEX IF NOT EXISTS idx_raw_data_source ON raw_data(source);
CREATE INDEX IF NOT EXISTS idx_processed_data_processed_at ON processed_data(processed_at);
CREATE INDEX IF NOT EXISTS idx_final_data_created_at ON final_data(created_at);
