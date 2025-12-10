from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ---------------- USER ROLE TABLE ----------------
class UserRole(db.Model):
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(20), unique=True, nullable=False)


# ---------------- USER TABLE ----------------
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    
    role_id = db.Column(db.Integer, db.ForeignKey('user_role.role_id'), nullable=False)
    role = db.relationship('UserRole')


# ---------------- REGION TABLE ----------------
class Region(db.Model):
    region_id = db.Column(db.Integer, primary_key=True)
    region_name = db.Column(db.String(100), unique=True, nullable=False)


# ---------------- PROJECT SECTOR TABLE ----------------
class ProjectSector(db.Model):
    sector_id = db.Column(db.Integer, primary_key=True)
    sector_name = db.Column(db.String(100), unique=True, nullable=False)


# ---------------- PROJECT TABLE ----------------
class Project(db.Model):
    project_id = db.Column(db.Integer, primary_key=True)
    
    project_name = db.Column(db.String(100), nullable=False)
    project_description = db.Column(db.Text)

    allocated_budget = db.Column(db.Float, default=0)
    budget_spent = db.Column(db.Float, default=0)

    project_status = db.Column(db.String(20), default='Planned')
    project_address = db.Column(db.String(200))

    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    # Foreign Keys
    region_id = db.Column(db.Integer, db.ForeignKey('region.region_id'))
    region = db.relationship('Region')

    sector_id = db.Column(db.Integer, db.ForeignKey('project_sector.sector_id'))
    sector = db.relationship('ProjectSector')

    # Relationship to reports
    reports = db.relationship('ProjectReport', backref='project', lazy=True, cascade='all, delete-orphan')


# ---------------- FEEDBACK TABLE ----------------
class Feedback(db.Model):
    feedback_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------- REPORT TYPE TABLE ----------------
class ReportType(db.Model):
    report_type_id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(50), unique=True, nullable=False)


# ---------------- PROJECT REPORT TABLE ----------------
class ProjectReport(db.Model):
    report_id = db.Column(db.Integer, primary_key=True)
    
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), nullable=False)

    reporter_name = db.Column(db.String(100))
    reporter_email = db.Column(db.String(100))
    
    report_subject = db.Column(db.String(200), nullable=False)
    report_message = db.Column(db.Text, nullable=False)

    report_type_id = db.Column(db.Integer, db.ForeignKey('report_type.report_type_id'))
    report_type = db.relationship('ReportType')

    is_resolved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------- REGION ANNUAL BUDGET TABLE ----------------
class RegionBudget(db.Model):
    region_budget_id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)

    region_id = db.Column(db.Integer, db.ForeignKey('region.region_id'), nullable=False)
    region = db.relationship('Region')

    region_budget = db.Column(db.Float, nullable=False)

    __table_args__ = (db.UniqueConstraint('region_id', 'year', name='unique_region_year'),)


# ---------------- PROJECT SECTOR BUDGET TABLE ----------------
class ProjectSectorBudget(db.Model):
    sector_budget_id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)

    sector_id = db.Column(db.Integer, db.ForeignKey('project_sector.sector_id'), nullable=False)
    sector = db.relationship('ProjectSector')

    sector_budget = db.Column(db.Float, nullable=False)


# ---------------- ANNUAL NATIONAL BUDGET TABLE ----------------
class AnnualBudget(db.Model):
    annual_budget_id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, unique=True, nullable=False)
    total_budget = db.Column(db.Float, nullable=False)