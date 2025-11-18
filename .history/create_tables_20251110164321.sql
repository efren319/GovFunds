-- create_tables.sql
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    description TEXT,
    allocated_budget REAL NOT NULL DEFAULT 0,
    spent REAL NOT NULL DEFAULT 0,
    status TEXT DEFAULT 'Planned', -- Planned, Ongoing, Completed
    region TEXT,
    start_date TEXT,
    end_date TEXT
);

CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    message TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now','localtime'))
);

CREATE TABLE IF NOT EXISTS region_budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    region TEXT NOT NULL,
    year INTEGER NOT NULL,
    budget REAL NOT NULL,
    UNIQUE(region, year)
);

-- sample projects
INSERT INTO projects (name, department, description, allocated_budget, spent, status, region, start_date, end_date)
VALUES
('Road Rehabilitation - Barangay A', 'Public Works', 'Rehab of 3km barangay road', 5000000, 3500000, 'Ongoing', 'Region I', '2024-05-01', NULL),
('School Building Construction', 'Education', '2-classroom building', 2000000, 2000000, 'Completed', 'Region II', '2023-10-01', '2024-04-15'),
('Health Center Upgrade', 'Health', 'Medical equipment and building upgrade', 3000000, 1500000, 'Ongoing', 'Region III', '2024-01-10', NULL),
('Irrigation System Project', 'Agriculture', 'Small-scale irrigation', 1500000, 200000, 'Planned', 'Region IV', NULL, NULL);

-- sample feedback
INSERT INTO feedback (name, email, message) VALUES
('Juan Dela Cruz', 'juan@example.com', 'Please update the road project timeline.'),
('Maria Santos', 'maria@example.com', 'Great initiative — more regional breakdown needed.');

-- Regional Budget Data for 2023
INSERT INTO region_budgets (region, year, budget) VALUES
('National Capital Region', 2023, 887000000000),
('Cordillera Administrative Region', 2023, 98500000000),
('Region I', 2023, 169900000000),
('Region II', 2023, 144700000000),
('Region III', 2023, 321100000000),
('Region IV-A', 2023, 318700000000),
('Region IV-B', 2023, 134200000000),
('Region V', 2023, 212800000000),
('Region VI', 2023, 203500000000),
('Region VII', 2023, 212000000000),
('Region VIII', 2023, 177400000000),
('Region IX', 2023, 126800000000),
('Region X', 2023, 175000000000),
('Region XI', 2023, 149100000000),
('Region XII', 2023, 116400000000),
('Caraga', 2023, 109300000000),
('BARMM', 2023, 130300000000);

-- Regional Budget Data for 2024
INSERT INTO region_budgets (region, year, budget) VALUES
('National Capital Region', 2024, 532008065000),
('Cordillera Administrative Region', 2024, 867228911000),
('Region I', 2024, 180565920000),
('Region II', 2024, 97668044000),
('Region III', 2024, 160174535000),
('Region IV-A', 2024, 369230365000),
('Region IV-B', 2024, 341101910000),
('Region V', 2024, 234040470000),
('Region VI', 2024, 222399947000),
('Region VII', 2024, 228181764000),
('Region VIII', 2024, 205946394000),
('Region IX', 2024, 140072215000),
('Region X', 2024, 190071333000),
('Region XI', 2024, 162666370000),
('Region XII', 2024, 127046390000),
('Caraga', 2024, 124270792000),
('BARMM', 2024, 149440406000);

-- Regional Budget Data for 2025
INSERT INTO region_budgets (region, year, budget) VALUES
('National Capital Region', 2025, 834600000000),
('Cordillera Administrative Region', 2025, 106000000000),
('Region I', 2025, 198700000000),
('Region II', 2025, 175000000000),
('Region III', 2025, 420600000000),
('Region IV-A', 2025, 395600000000),
('Region IV-B', 2025, 184600000000),
('Region V', 2025, 257300000000),
('Region VI', 2025, 236100000000),
('Region VII', 2025, 255900000000),
('Region VIII', 2025, 209400000000),
('Region IX', 2025, 149300000000),
('Region X', 2025, 195700000000),
('Region XI', 2025, 172500000000),
('Region XII', 2025, 137800000000),
('Caraga', 2025, 138900000000),
('BARMM', 2025, 172400000000);
