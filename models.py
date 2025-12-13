from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ---------------- PROJECT TABLE ----------------
class Project(db.Model):
    project_id = db.Column(db.Integer, primary_key=True)
    
    project_name = db.Column(db.String(100), nullable=False)
    project_description = db.Column(db.Text)
    project_image = db.Column(db.String(255))  # Image filename

    allocated_budget = db.Column(db.Float, default=0)
    budget_spent = db.Column(db.Float, default=0)

    project_status = db.Column(db.String(20), default='Planned')

    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    region_name = db.Column(db.String(100))
    sector_name = db.Column(db.String(100))
    
    # Relationship to reports
    reports = db.relationship('ProjectReport', backref='project', lazy=True, cascade='all, delete-orphan')


# ---------------- FEEDBACK TABLE ----------------
class Feedback(db.Model):
    feedback_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------- PROJECT REPORT TABLE ----------------
class ProjectReport(db.Model):
    report_id = db.Column(db.Integer, primary_key=True)
    
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), nullable=False)

    reporter_name = db.Column(db.String(100))
    reporter_email = db.Column(db.String(100))
    
    report_subject = db.Column(db.String(200), nullable=False)
    report_message = db.Column(db.Text, nullable=False)

    report_type = db.Column(db.String(50), default='General')
    
    report_image = db.Column(db.String(255))  # Image filename

    is_resolved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
