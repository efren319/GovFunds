DROP TABLE IF EXISTS project_report CASCADE;
DROP TABLE IF EXISTS feedback CASCADE;
DROP TABLE IF EXISTS project CASCADE;

CREATE TABLE project (
    project_id SERIAL PRIMARY KEY,
    project_name VARCHAR(100) NOT NULL,
    project_description TEXT,
    project_image VARCHAR(255),
    allocated_budget FLOAT DEFAULT 0,
    budget_spent FLOAT DEFAULT 0,
    project_status VARCHAR(20) DEFAULT 'Planned',
    start_date DATE,
    end_date DATE,
    region_name VARCHAR(100),
    sector_name VARCHAR(100)
);

CREATE TABLE feedback (
    feedback_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE project_report (
    report_id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES project(project_id) ON DELETE CASCADE,
    reporter_name VARCHAR(100),
    reporter_email VARCHAR(100),
    report_subject VARCHAR(200) NOT NULL,
    report_message TEXT NOT NULL,
    report_type VARCHAR(50) DEFAULT 'General',
    report_image VARCHAR(255),
    is_resolved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO project (
    project_name,
    sector_name,
    project_description,
    allocated_budget,
    budget_spent,
    project_status,
    region_name,
    start_date,
    end_date,
    project_image
) VALUES
-- 1
('Barangay Hall Renovation', 'Road Infrastructure',
 'Renovation of the Barangay Hall including roofing and interiors',
 500000, 200000, 'Ongoing',
 'National Capital Region',
 '2025-01-10', '2026-12-31', 'images/projects/project1.webp'),

-- 2
('San Miguel Road Repair', 'Special Infrastructure Projects',
 'Road resurfacing and pothole repairs',
 750000, 400000, 'Ongoing',
 'Cordillera Administrative Region',
 '2025-03-15', '2026-11-30', 'images/projects/project1.webp'),

-- 3
('Public Park Landscaping', 'Local Infrastructure Support',
 'Landscaping and playground installation',
 300000, 150000, 'Ongoing',
 'Region I',
 '2025-02-01', '2026-10-30', 'images/projects/project1.webp'),

-- 4
('Barangay Library Expansion', 'Road Infrastructure',
 'Adding more rooms and bookshelves',
 450000, 220000, 'Ongoing',
 'National Capital Region',
 '2025-04-01', '2026-12-15', 'images/projects/project1.webp'),

-- 5
('Water Pump Installation', 'Disaster Response and Rehabilitation',
 'Installation of new water pumps',
 600000, 250000, 'Ongoing',
 'Region II',
 '2025-05-05', '2026-11-20', 'images/projects/project1.webp'),

-- 6
('Street Lighting Upgrade', 'Local Infrastructure Support',
 'Install new LED street lights',
 400000, 180000, 'Ongoing',
 'Region III',
 '2025-06-10', '2026-12-10', 'images/projects/project1.webp'),

-- 7
('Riverbank Reinforcement', 'Local Infrastructure Support',
 'Reinforce riverbanks to prevent erosion',
 650000, 320000, 'Ongoing',
 'Region IV-A',
 '2025-02-20', '2026-12-15', 'images/projects/project1.webp'),

-- 8
('Forest Reforestation Program', 'Local Infrastructure Support',
 'Planting trees in protected forest area',
 800000, 500000, 'Ongoing',
 'Region IV-A',
 '2025-03-01', '2026-12-31', 'images/projects/project1.webp'),

-- 9
('Chemical Waste Containment', 'Flood Control and Drainage',
 'Proper disposal and containment of chemical waste',
 550000, 300000, 'Ongoing',
 'Region IV-B',
 '2025-01-25', '2026-11-30', 'images/projects/project1.webp'),

-- 10
('Drainage System Improvement', 'Bridge Infrastructure',
 'Clearing and upgrading drainage',
 450000, 200000, 'Ongoing',
 'Region V',
 '2025-02-15', '2026-10-31', 'images/projects/project1.webp'),

-- 11
('Flood Control Project', 'Bridge Infrastructure',
 'Flood barriers and water diversion',
 950000, 600000, 'Ongoing',
 'Cordillera Administrative Region',
 '2025-01-05', '2026-12-15', 'images/projects/project1.webp'),

-- 12
('Garbage Collection Enhancement', 'Road Infrastructure',
 'Adding garbage trucks and bins',
 400000, 180000, 'Ongoing',
 'National Capital Region',
 '2025-03-01', '2026-12-31', 'images/projects/project1.webp'),

-- 13
('Abandoned Vehicle Removal', 'Special Infrastructure Projects',
 'Remove abandoned vehicles blocking roads',
 250000, 150000, 'Ongoing',
 'Region II',
 '2025-04-15', '2026-11-30', 'images/projects/project1.webp'),

-- 14
('Electrical Wiring Safety', 'Local Infrastructure Support',
 'Replace unsafe electrical wirings in public areas',
 300000, 120000, 'Ongoing',
 'Region III',
 '2025-05-10', '2026-10-31', 'images/projects/project1.webp'),

-- 15
('Air Pollution Monitoring', 'Flood Control and Drainage',
 'Monitoring pollution near factories',
 350000, 150000, 'Ongoing',
 'Region IV-B',
 '2025-03-20', '2026-12-15', 'images/projects/project1.webp'),

-- 16
('Barangay Hall Security Upgrade', 'Road Infrastructure',
 'CCTV cameras and security systems',
 200000, 100000, 'Ongoing',
 'National Capital Region',
 '2025-02-10', '2026-11-30', 'images/projects/project1.webp'),

-- 17
('Road Signage Installation', 'Special Infrastructure Projects',
 'Install traffic signs and markers',
 150000, 50000, 'Ongoing',
 'Cordillera Administrative Region',
 '2025-03-05', '2026-11-15', 'images/projects/project1.webp'),

-- 18
('Mosquito Control Program', 'Disaster Response and Rehabilitation',
 'Remove stagnant water and dengue breeding sites',
 300000, 150000, 'Ongoing',
 'Region II',
 '2025-01-20', '2026-12-01', 'images/projects/project1.webp'),

-- 19
('Forest Patrol Program', 'Local Infrastructure Support',
 'Protect forests from illegal logging',
 500000, 250000, 'Ongoing',
 'Region IV-A',
 '2025-02-10', '2026-12-31', 'images/projects/project1.webp'),

-- 20
('Road Repair and Maintenance', 'Special Infrastructure Projects',
 'Pothole filling and road leveling',
 700000, 400000, 'Ongoing',
 'Cordillera Administrative Region',
 '2025-03-15', '2026-12-15', 'images/projects/project1.webp');




INSERT INTO feedback (name, email, message) VALUES
('Juan Dela Cruz', 'juan@email.com', 'Some project details lack complete budget breakdown.'),
('Maria Santos', 'maria@email.com', 'Please include status updates for delayed projects.'),
('Pedro Reyes', 'pedro@email.com', 'It would be helpful to upload proof-of-work photos monthly.'),
('Ana Lopez', 'ana@email.com', 'Some project locations are incorrect on the map.'),
('Carlo Tan', 'carlo@email.com', 'Additional filters like barangay or phase would improve reports.'),
('Liza Cruz', 'liza@email.com', 'The project timelines are not always updated.'),
('Mark Lim', 'mark@email.com', 'Add a feature to compare planned vs. actual spending.'),
('Susan Reyes', 'susan@email.com', 'Some uploaded project receipts are blurry or unreadable.'),
('Jose Santos', 'jose@email.com', 'Please add a category for urgent community concerns.'),
('Carla Tan', 'carla@email.com', 'Some reports take too long before being marked resolved.'),
('Daniel Lim', 'daniel@email.com', 'The dashboard charts should reflect real-time financial data.'),
('Rosa Cruz', 'rosa@email.com', 'Notifications for project updates would help citizens stay informed.'),
('Miguel Reyes', 'miguel@email.com', 'Add clearer labeling for completed vs. ongoing projects.'),
('Patricia Lopez', 'patricia@email.com', 'Some project reports have missing contractor details.'),
('Henry Tan', 'henry@email.com', 'Good initiative but needs more transparency on project bidding.'),
('Grace Santos', 'grace@email.com', 'Include documents such as contracts and purchase orders.'),
('Ramon Lim', 'ramon@email.com', 'Tracking report history would help verify consistent follow-ups.'),
('Lucia Cruz', 'lucia@email.com', 'Add an option for citizens to rate government response quality.'),
('Erik Reyes', 'erik@email.com', 'Some hazard-related reports lack proper prioritization tags.'),
('Jenny Tan', 'jenny@email.com', 'Project descriptions should include the responsible agency and budget.');



INSERT INTO project_report (
    project_id,
    reporter_name,
    reporter_email,
    report_subject,
    report_message,
    report_type,
    report_image,
    is_resolved
) VALUES
(1, 'Juan Dela Cruz', 'juan@email.com', 'Roof Problem', 'Roofing work not completed', 'General Feedback', 'images/projects/project1.webp', FALSE),
(2, 'Maria Santos', 'maria@email.com', 'Potholes', 'Potholes still visible', 'Issue/Problem', 'images/projects/project1.webp', FALSE),
(3, 'Pedro Reyes', 'pedro@email.com', 'Playground', 'Playground not installed', 'Concern', 'images/projects/project1.webp', FALSE),
(4, 'Ana Lopez', 'ana@email.com', 'Incomplete Library', 'Library rooms incomplete', 'General Feedback', 'images/projects/project1.webp', FALSE),
(5, 'Carlo Tan', 'carlo@email.com', 'Pump Delay', 'Pump installation delayed', 'Issue/Problem', 'images/projects/project1.webp', FALSE),
(6, 'Liza Cruz', 'liza@email.com', 'Broken Streetlights', 'Some streetlights still broken', 'General Feedback', 'images/projects/project1.webp', FALSE),
(7, 'Mark Lim', 'mark@email.com', 'Riverbank Erosion', 'Riverbank erosion continues', 'Concern', 'images/projects/project1.webp', FALSE),
(8, 'Susan Reyes', 'susan@email.com', 'Unplanted Trees', 'Trees not fully planted', 'General Feedback', 'images/projects/project1.webp', FALSE),
(9, 'Jose Santos', 'jose@email.com', 'Leaking Chemicals', 'Chemicals leaking', 'Issue/Problem', 'images/projects/project1.webp', FALSE),
(10, 'Carla Tan', 'carla@email.com', 'Drainage', 'Drainage still blocked', 'Issue/Problem', 'images/projects/project1.webp', FALSE),
(11, 'Daniel Lim', 'daniel@email.com', 'Flood Control', 'Flood barriers incomplete', 'General Feedback', 'images/projects/project1.webp', FALSE),
(12, 'Rosa Cruz', 'rosa@email.com', 'Garbage Bins', 'Garbage bins insufficient', 'Concern', 'images/projects/project1.webp', FALSE),
(13, 'Miguel Reyes', 'miguel@email.com', 'Abandoned Vehicles', 'Abandoned vehicle still present', 'Issue/Problem', 'images/projects/project1.webp', FALSE),
(14, 'Patricia Lopez', 'patricia@email.com', 'Wires', 'Unsafe wiring', 'General Feedback', 'images/projects/project1.webp', FALSE),
(15, 'Henry Tan', 'henry@email.com', 'Air Pollution', 'Air pollution persists', 'Concern', 'images/projects/project1.webp', FALSE),
(16, 'Grace Santos', 'grace@email.com', 'CCTV', 'CCTV cameras not installed', 'General Feedback', 'images/projects/project1.webp', FALSE),
(17, 'Ramon Lim', 'ramon@email.com', 'Road Signs', 'Road signs missing', 'Issue/Problem', 'images/projects/project1.webp', FALSE),
(18, 'Lucia Cruz', 'lucia@email.com', 'Stagnant Water', 'Stagnant water problem', 'Concern', 'images/projects/project1.webp', FALSE),
(19, 'Erik Reyes', 'erik@email.com', 'Illegal Logging', 'Illegal logging observed', 'General Feedback', 'images/projects/project1.webp', FALSE),
(20, 'Jenny Tan', 'jenny@email.com', 'Potholes', 'Potholes reappearing', 'Issue/Problem', 'images/projects/project1.webp', FALSE);