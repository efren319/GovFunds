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
