-- Insert Department Budget Data for 2025
INSERT INTO department_budget (department, year, budget) VALUES
('Department of Education', 2025, 500000000),
('Department of Health', 2025, 400000000),
('Department of Infrastructure', 2025, 600000000),
('Department of Defense', 2025, 350000000),
('Department of Social Services', 2025, 250000000),
('Department of Environment', 2025, 180000000),
('Department of Agriculture', 2025, 220000000),
('Department of Transportation', 2025, 300000000);

-- Insert Region Budget Data for 2025
INSERT INTO region_budget (region, year, budget) VALUES
('Region 1 - Ilocos Region', 2025, 280000000),
('Region 2 - Cagayan Valley', 2025, 250000000),
('Region 3 - Central Luzon', 2025, 350000000),
('Region 4A - CALABARZON', 2025, 420000000),
('Region 4B - MIMAROPA', 2025, 180000000),
('Region 5 - Bicol Region', 2025, 220000000),
('Region 6 - Western Visayas', 2025, 280000000),
('Region 7 - Central Visayas', 2025, 310000000),
('Region 8 - Eastern Visayas', 2025, 190000000),
('Region 9 - Zamboanga Peninsula', 2025, 210000000),
('Region 10 - Northern Mindanao', 2025, 240000000),
('Region 11 - Davao Region', 2025, 300000000),
('Region 12 - SOCCSKSARGEN', 2025, 270000000),
('Region 13 - Caraga', 2025, 160000000),
('NCR - National Capital Region', 2025, 500000000);

-- Insert Annual Budget for 2025
INSERT INTO annual_budget (year, total_budget) VALUES
(2025, 4130000000);

-- Insert Sample Projects
INSERT INTO project (name, department, description, allocated_budget, spent, status, region) VALUES
('Build New School', 'Department of Education', 'Construction of 10 new schools in rural areas', 50000000, 15000000, 'Ongoing', 'Region 1 - Ilocos Region'),
('Health Center Renovation', 'Department of Health', 'Renovation of 20 health centers nationwide', 40000000, 10000000, 'Ongoing', 'Region 3 - Central Luzon'),
('Road Infrastructure Project', 'Department of Infrastructure', 'Construction of 100 km highway', 100000000, 45000000, 'Ongoing', 'Region 4A - CALABARZON'),
('Bridge Construction', 'Department of Infrastructure', 'Building 5 new bridges in key locations', 75000000, 20000000, 'Planned', 'Region 2 - Cagayan Valley'),
('Agricultural Training Centers', 'Department of Agriculture', 'Establishment of 15 training centers', 30000000, 8000000, 'Ongoing', 'Region 5 - Bicol Region'),
('Environmental Conservation', 'Department of Environment', 'Mangrove reforestation project', 25000000, 5000000, 'Ongoing', 'Region 7 - Central Visayas'),
('Public Transportation System', 'Department of Transportation', 'Metro rail expansion project', 120000000, 60000000, 'Ongoing', 'NCR - National Capital Region'),
('Social Housing Program', 'Department of Social Services', 'Construction of 1000 housing units', 80000000, 25000000, 'Ongoing', 'Region 6 - Western Visayas'),
('Water Supply Project', 'Department of Infrastructure', 'Clean water system for 50 municipalities', 60000000, 18000000, 'Planned', 'Region 8 - Eastern Visayas'),
('Disaster Risk Reduction', 'Department of Defense', 'Early warning system installation', 35000000, 12000000, 'Ongoing', 'Region 9 - Zamboanga Peninsula');

-- Insert Sample Feedback
INSERT INTO feedback (name, email, message) VALUES
('Juan dela Cruz', 'juan@example.com', 'Great project on education! Keep up the good work.'),
('Maria Santos', 'maria@example.com', 'Please prioritize health center upgrades in rural areas.'),
('Carlos Reyes', 'carlos@example.com', 'The infrastructure projects are progressing well. Very satisfied!'),
('Ana Gonzales', 'ana@example.com', 'Hope to see more environmental programs soon.'),
('Luis Fernandez', 'luis@example.com', 'Transportation system improvements needed in our area.');
