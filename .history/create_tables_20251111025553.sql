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

CREATE TABLE IF NOT EXISTS project_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    reporter_name TEXT,
    reporter_email TEXT,
    report_subject TEXT NOT NULL,
    report_message TEXT NOT NULL,
    report_type TEXT DEFAULT 'General', -- General, Issue, Concern, Suggestion
    created_at TEXT DEFAULT (datetime('now','localtime')),
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

CREATE TABLE IF NOT EXISTS region_budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    region TEXT NOT NULL,
    year INTEGER NOT NULL,
    budget REAL NOT NULL,
    UNIQUE(region, year)
);

CREATE TABLE IF NOT EXISTS department_budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department TEXT NOT NULL,
    year INTEGER NOT NULL,
    budget REAL NOT NULL,
    UNIQUE(department, year)
);

-- sample projects
INSERT INTO projects (name, department, description, allocated_budget, spent, status, region, start_date, end_date)
VALUES
('Road Rehabilitation - Barangay A', 'Department of Public Works and Highways', 'Rehab of 3km barangay road', 5000000, 3500000, 'Ongoing', 'Region I', '2024-05-01', NULL),
('School Building Construction', 'Department of Education', '2-classroom building', 2000000, 2000000, 'Completed', 'Region II', '2023-10-01', '2024-04-15'),
('Health Center Upgrade', 'Department of Health', 'Medical equipment and building upgrade', 3000000, 1500000, 'Ongoing', 'Region III', '2024-01-10', NULL),
('Irrigation System Project', 'Department of Agriculture', 'Small-scale irrigation', 1500000, 200000, 'Planned', 'Region IV', NULL, NULL);

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

-- Department Budget Data for 2023
INSERT INTO department_budgets (department, year, budget) VALUES
('Department of Education', 2023, 678317321000),
('Department of Health', 2023, 209624216000),
('Department of Public Works and Highways', 2023, 893121040000),
('Department of the Interior and Local Government', 2023, 253404249000),
('Department of National Defense', 2023, 204566332000),
('Department of Social Welfare and Development', 2023, 199256638000),
('Department of Agriculture', 2023, 98864397000),
('Department of Budget and Management', 2023, 1737629000),
('Department of Justice', 2023, 36228754000),
('Department of Labor and Employment', 2023, 46631922000),
('Department of Energy', 2023, 1320735000),
('Department of Finance', 2023, 23927302000),
('Department of Foreign Affairs', 2023, 20621463000),
('Department of Information and Communications Technology', 2023, 8289778000),
('Department of Tourism', 2023, 3731984000),
('Department of Trade and Industry', 2023, 6327029000),
('Department of Transportation', 2023, 105530385000),
('National Economic and Development Authority', 2023, 12961084000),
('Civil Service Commission', 2023, 2045591000),
('Commission on Audit', 2023, 13318049000),
('Commission on Elections', 2023, 5737340000),
('Office of the Ombudsman', 2023, 4721331000),
('Commission on Human Rights', 2023, 993921000),
('Special Purpose Funds', 2023, 1825624983000);

-- Department Budget Data for 2024
INSERT INTO department_budgets (department, year, budget) VALUES
('Department of Education', 2024, 717663478000),
('Department of Health', 2024, 241602813000),
('Department of Public Works and Highways', 2024, 996791684000),
('Department of the Interior and Local Government', 2024, 263649999000),
('Department of National Defense', 2024, 238356544000),
('Department of Social Welfare and Development', 2024, 247848341000),
('Department of Agriculture', 2024, 111687758000),
('Department of Budget and Management', 2024, 2501145000),
('Department of Justice', 2024, 36228754000),
('Department of Labor and Employment', 2024, 61268468000),
('Department of Energy', 2024, 1662160000),
('Department of Finance', 2024, 23927302000),
('Department of Foreign Affairs', 2024, 24591198000),
('Department of Tourism', 2024, 3439715000),
('Department of Trade and Industry', 2024, 8638218000),
('Department of Transportation', 2024, 73330669000),
('Special Purpose Funds', 2024, 2169133613000);

-- Department Budget Data for 2025
INSERT INTO department_budgets (department, year, budget) VALUES
('Department of Education', 2025, 793177297000),
('Department of Health', 2025, 223188973000),
('Department of Public Works and Highways', 2025, 900000000000),
('Department of the Interior and Local Government', 2025, 281320865000),
('Department of National Defense', 2025, 258164910000),
('Department of Social Welfare and Development', 2025, 230057270000),
('Department of Agriculture', 2025, 129001585000),
('Department of Budget and Management', 2025, 3191835000),
('Department of Justice', 2025, 40584630000),
('Department of Labor and Employment', 2025, 45833958000),
('Department of Migrant Workers', 2025, 8503912000),
('National Economic and Development Authority', 2025, 12575395000),
('Department of Transportation', 2025, 180893888000),
('Department of Trade and Industry', 2025, 8598332000),
('Commission on Audit', 2025, 13417340000),
('Commission on Elections', 2025, 35470671000),
('Office of the Ombudsman', 2025, 5824154000),
('Special Purpose Funds', 2025, 2740481084000);
