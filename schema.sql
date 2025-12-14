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