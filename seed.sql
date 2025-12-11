-- GovFunds Database Schema and Seed Data
-- PostgreSQL Database: govfunds
-- Generated from models.py and seed_data.py

-- ============================================
-- DROP EXISTING TABLES (if they exist)
-- ============================================
DROP TABLE IF EXISTS project_report CASCADE;
DROP TABLE IF EXISTS feedback CASCADE;
DROP TABLE IF EXISTS project CASCADE;

-- ============================================
-- CREATE TABLES
-- ============================================

-- PROJECT TABLE
CREATE TABLE project (
    project_id SERIAL PRIMARY KEY,
    project_name VARCHAR(100) NOT NULL,
    project_description TEXT,
    project_image VARCHAR(255),
    allocated_budget FLOAT DEFAULT 0,
    budget_spent FLOAT DEFAULT 0,
    project_status VARCHAR(20) DEFAULT 'Planned',
    project_address VARCHAR(200),
    start_date DATE,
    end_date DATE,
    region_name VARCHAR(100),
    sector_name VARCHAR(100)
);

-- FEEDBACK TABLE
CREATE TABLE feedback (
    feedback_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- PROJECT REPORT TABLE
CREATE TABLE project_report (
    report_id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES project(project_id) ON DELETE CASCADE,
    reporter_name VARCHAR(100),
    reporter_email VARCHAR(100),
    report_subject VARCHAR(200) NOT NULL,
    report_message TEXT NOT NULL,
    report_type VARCHAR(50) DEFAULT 'General',
    is_resolved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- SEED DATA
-- ============================================

-- Insert Projects
-- Note: project_image NULL means the app will use default sector image
INSERT INTO project (project_name, sector_name, project_description, allocated_budget, budget_spent, project_status, region_name, start_date, end_date, project_image) VALUES
('Road Rehabilitation - Barangay A', 'Road Infrastructure', 'Rehab of 3km barangay road', 5000000, 3500000, 'Ongoing', 'Region I', '2024-05-01', NULL, NULL),
('Public Building Construction', 'Public Buildings', 'Government office building', 2000000, 2000000, 'Completed', 'Region II', '2023-10-01', '2024-04-15', NULL),
('Bridge Repair and Maintenance', 'Bridge Infrastructure', 'Structural repair of aging bridge', 3000000, 1500000, 'Ongoing', 'Region III', '2024-01-10', NULL, NULL),
('Irrigation System Project', 'Water Resources and Irrigation', 'Small-scale irrigation facility', 1500000, 200000, 'Planned', 'Region IV-A', NULL, NULL, NULL),
('Flood Control System - NCR', 'Flood Control and Drainage', 'Drainage system improvement in Metro Manila', 8000000, 4000000, 'Ongoing', 'National Capital Region', '2024-03-15', NULL, 'images/projects/project1.webp'),
('Disaster Relief Center', 'Disaster Response and Rehabilitation', 'Emergency response facility construction', 4500000, 0, 'Planned', 'Region VIII', NULL, NULL, NULL);

-- Insert Feedback
INSERT INTO feedback (name, email, message) VALUES
('Juan Dela Cruz', 'juan@example.com', 'Please update the road project timeline.'),
('Maria Santos', 'maria@example.com', 'Great initiative — more regional breakdown needed.'),
('Pedro Reyes', 'pedro@example.com', 'Excellent transparency on budget spending!');

-- ============================================
-- USAGE INSTRUCTIONS
-- ============================================
-- To use this file:
-- 1. Create the database if it doesn't exist:
--    CREATE DATABASE govfunds;
-- 
-- 2. Connect to the database:
--    \c govfunds
--
-- 3. Run this script:
--    \i seed.sql
--
-- Or from command line:
--    psql -U postgres -d govfunds -f seed.sql
--
-- Or on Windows PowerShell:
--    psql -U postgres -d govfunds -f "path\to\seed.sql"
-- ============================================
