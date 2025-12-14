-- GovFunds Database Schema
-- This file defines the database structure for the GovFunds application
-- Tables: project, feedback, project_report

-- ============================================
-- PROJECT TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS project (
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

-- ============================================
-- FEEDBACK TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS feedback (
    feedback_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- PROJECT REPORT TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS project_report (
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

-- ============================================
-- INDEXES
-- ============================================
CREATE INDEX IF NOT EXISTS idx_project_status ON project(project_status);
CREATE INDEX IF NOT EXISTS idx_project_region ON project(region_name);
CREATE INDEX IF NOT EXISTS idx_project_sector ON project(sector_name);
CREATE INDEX IF NOT EXISTS idx_feedback_created ON feedback(created_at);
CREATE INDEX IF NOT EXISTS idx_report_project ON project_report(project_id);
CREATE INDEX IF NOT EXISTS idx_report_resolved ON project_report(is_resolved);
CREATE INDEX IF NOT EXISTS idx_report_created ON project_report(created_at);
