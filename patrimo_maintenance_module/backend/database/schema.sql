
CREATE TABLE properties (
    id SERIAL PRIMARY KEY,
    type VARCHAR(50),
    address TEXT,
    surface NUMERIC,
    year_built INTEGER
);

CREATE TABLE components (
    id SERIAL PRIMARY KEY,
    property_id INTEGER REFERENCES properties(id),
    ifc_global_id VARCHAR(255),
    name VARCHAR(255),
    category VARCHAR(100),
    installation_date DATE,
    useful_life_years INTEGER,
    replacement_cost NUMERIC,
    criticality INTEGER,
    maintenance_frequency_months INTEGER,
    maintenance_type VARCHAR(50),
    current_condition VARCHAR(50)
);

CREATE TABLE maintenance_history (
    id SERIAL PRIMARY KEY,
    component_id INTEGER REFERENCES components(id),
    date DATE,
    type VARCHAR(50),
    description TEXT,
    cost NUMERIC,
    provider VARCHAR(255)
);

CREATE TABLE inspections (
    id SERIAL PRIMARY KEY,
    component_id INTEGER REFERENCES components(id),
    date DATE,
    measured_variable VARCHAR(100),
    value NUMERIC,
    critical_threshold NUMERIC,
    result VARCHAR(50)
);
