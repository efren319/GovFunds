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
 500000, 200000, 'Completed',
 'National Capital Region',
 '2025-01-10', '2026-12-31', 'images/projects/project1.webp'),

-- 2
('San Miguel Road Repair', 'Special Infrastructure Projects',
 'Road resurfacing and pothole repairs',
 750000, 400000, 'Planned',
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
 450000, 220000, 'Completed',
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
 400000, 180000, 'Planned',
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
 800000, 500000, 'Completed',
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
 450000, 200000, 'Planned',
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
 400000, 180000, 'Completed',
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
 300000, 120000, 'Planned',
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
 200000, 100000, 'Completed',
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
 300000, 150000, 'Planned',
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
 700000, 400000, 'Completed',
 'Cordillera Administrative Region',
 '2025-03-15', '2026-12-15', 'images/projects/project1.webp');




INSERT INTO feedback (name, email, message, created_at) VALUES
('Juan Dela Cruz', 'juan@email.com', 'Some project details lack complete budget breakdown.', '2025-11-18 14:32:15'),
('Maria Santos', 'maria@email.com', 'Please include status updates for delayed projects.', '2025-12-02 09:15:42'),
('Pedro Reyes', 'pedro@email.com', 'It would be helpful to upload proof-of-work photos monthly.', '2025-11-25 16:48:20'),
('Ana Lopez', 'ana@email.com', 'Some project locations are incorrect on the map.', '2025-12-05 11:22:38'),
('Carlo Tan', 'carlo@email.com', 'Additional filters like barangay or phase would improve reports.', '2025-11-30 13:45:10'),
('Liza Cruz', 'liza@email.com', 'The project timelines are not always updated.', '2025-12-08 08:30:55'),
('Mark Lim', 'mark@email.com', 'Add a feature to compare planned vs. actual spending.', '2025-11-22 15:18:33'),
('Susan Reyes', 'susan@email.com', 'Some uploaded project receipts are blurry or unreadable.', '2025-12-03 10:05:47'),
('Jose Santos', 'jose@email.com', 'Please add a category for urgent community concerns.', '2025-11-27 17:20:12'),
('Carla Tan', 'carla@email.com', 'Some reports take too long before being marked resolved.', '2025-12-06 12:40:25'),
('Daniel Lim', 'daniel@email.com', 'The dashboard charts should reflect real-time financial data.', '2025-11-20 14:10:18'),
('Rosa Cruz', 'rosa@email.com', 'Notifications for project updates would help citizens stay informed.', '2025-12-01 09:50:30'),
('Miguel Reyes', 'miguel@email.com', 'Add clearer labeling for completed vs. ongoing projects.', '2025-11-28 16:35:22'),
('Patricia Lopez', 'patricia@email.com', 'Some project reports have missing contractor details.', '2025-12-04 13:25:48'),
('Henry Tan', 'henry@email.com', 'Good initiative but needs more transparency on project bidding.', '2025-11-23 11:15:40'),
('Grace Santos', 'grace@email.com', 'Include documents such as contracts and purchase orders.', '2025-12-07 15:42:08'),
('Ramon Lim', 'ramon@email.com', 'Tracking report history would help verify consistent follow-ups.', '2025-11-21 10:28:55'),
('Lucia Cruz', 'lucia@email.com', 'Add an option for citizens to rate government response quality.', '2025-12-02 14:18:36'),
('Erik Reyes', 'erik@email.com', 'Some hazard-related reports lack proper prioritization tags.', '2025-11-26 12:05:19'),
('Jenny Tan', 'jenny@email.com', 'Project descriptions should include the responsible agency and budget.', '2025-12-05 16:50:42');



INSERT INTO project_report (
    project_id,
    reporter_name,
    reporter_email,
    report_subject,
    report_message,
    report_type,
    report_image,
    is_resolved,
    created_at
) VALUES
(1, 'Juan Dela Cruz', 'juan@email.com', 'Roof Problem', 'Roofing work not completed on Barangay Hall', 'General Feedback', 'images/projects/project1.webp', FALSE, '2025-11-19 09:15:20'),
(2, 'Maria Santos', 'maria@email.com', 'Potholes', 'Potholes still visible on San Miguel Road', 'Issue/Problem', 'images/projects/project1.webp', FALSE, '2025-11-23 14:42:35'),
(3, 'Pedro Reyes', 'pedro@email.com', 'Playground Issue', 'Playground equipment not installed in Public Park', 'Concern', 'images/projects/project1.webp', FALSE, '2025-11-27 10:28:18'),
(4, 'Ana Lopez', 'ana@email.com', 'Library Incomplete', 'Library rooms still incomplete and unfinished', 'General Feedback', 'images/projects/project1.webp', FALSE, '2025-12-01 15:50:42'),
(5, 'Carlo Tan', 'carlo@email.com', 'Pump Delay', 'Water pump installation has been delayed', 'Issue/Problem', 'images/projects/project1.webp', FALSE, '2025-11-21 11:35:55'),
(6, 'Liza Cruz', 'liza@email.com', 'Broken Streetlights', 'Some streetlights not functioning properly', 'General Feedback', 'images/projects/project1.webp', FALSE, '2025-12-04 16:20:38'),
(7, 'Mark Lim', 'mark@email.com', 'Riverbank Erosion', 'Riverbank erosion continues despite reinforcement work', 'Concern', 'images/projects/project1.webp', FALSE, '2025-11-25 12:05:22'),
(8, 'Susan Reyes', 'susan@email.com', 'Trees Not Planted', 'Many trees not fully planted in reforestation area', 'General Feedback', 'images/projects/project1.webp', FALSE, '2025-11-22 13:18:47'),
(9, 'Jose Santos', 'jose@email.com', 'Chemical Leaking', 'Chemical waste leaking from containment area', 'Issue/Problem', 'images/projects/project1.webp', FALSE, '2025-12-03 09:40:15'),
(10, 'Carla Tan', 'carla@email.com', 'Drainage Blocked', 'Drainage system still blocked with debris', 'Issue/Problem', 'images/projects/project1.webp', FALSE, '2025-11-28 14:25:30'),
(11, 'Daniel Lim', 'daniel@email.com', 'Flood Barriers', 'Flood barriers incomplete and need repairs', 'General Feedback', 'images/projects/project1.webp', FALSE, '2025-12-02 10:55:48'),
(12, 'Rosa Cruz', 'rosa@email.com', 'Garbage Bins Insufficient', 'Number of garbage bins insufficient for area', 'Concern', 'images/projects/project1.webp', FALSE, '2025-11-30 15:12:26'),
(13, 'Miguel Reyes', 'miguel@email.com', 'Vehicle Still Present', 'Abandoned vehicle still blocking the road', 'Issue/Problem', 'images/projects/project1.webp', FALSE, '2025-12-05 11:38:50'),
(14, 'Patricia Lopez', 'patricia@email.com', 'Unsafe Wiring', 'Electrical wiring remains unsafe in public areas', 'General Feedback', 'images/projects/project1.webp', FALSE, '2025-11-24 13:45:23'),
(15, 'Henry Tan', 'henry@email.com', 'Air Pollution High', 'Air pollution levels still high near factories', 'Concern', 'images/projects/project1.webp', FALSE, '2025-12-06 16:30:42'),
(1, 'Grace Santos', 'grace@email.com', 'Security System Needed', 'CCTV cameras and security system needed for Hall', 'General Feedback', 'images/projects/project1.webp', FALSE, '2025-11-26 10:15:35'),
(2, 'Ramon Lim', 'ramon@email.com', 'Road Signs Missing', 'Road signage missing on San Miguel Road repairs', 'Issue/Problem', 'images/projects/project1.webp', FALSE, '2025-12-04 14:20:18'),
(18, 'Lucia Cruz', 'lucia@email.com', 'Stagnant Water', 'Stagnant water breeding mosquito in area', 'Concern', 'images/projects/project1.webp', FALSE, '2025-11-29 12:35:55'),
(19, 'Erik Reyes', 'erik@email.com', 'Illegal Logging Observed', 'Illegal logging still observed in protected forest', 'General Feedback', 'images/projects/project1.webp', FALSE, '2025-12-01 09:50:26'),
(20, 'Jenny Tan', 'jenny@email.com', 'Potholes Reappearing', 'Potholes reappearing on main road repairs', 'Issue/Problem', 'images/projects/project1.webp', FALSE, '2025-11-20 15:25:40');