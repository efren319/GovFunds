from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ---------------- USER ROLE TABLE ----------------
class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(20), unique=True, nullable=False)


# ---------------- USER TABLE ----------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    
    role_id = db.Column(db.Integer, db.ForeignKey('user_role.id'), nullable=False)
    role = db.relationship('UserRole')


# ---------------- REGION TABLE ----------------
class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region_name = db.Column(db.String(100), unique=True, nullable=False)


# ---------------- PROJECT SECTOR TABLE ----------------
class ProjectSector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sector_name = db.Column(db.String(100), unique=True, nullable=False)


# ---------------- PROJECT TABLE ----------------
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    allocated_budget = db.Column(db.Float, default=0)
    spent = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='Planned')

    # Foreign Keys
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))
    region = db.relationship('Region')

    sector_id = db.Column(db.Integer, db.ForeignKey('project_sector.id'))
    sector = db.relationship('ProjectSector')

    location = db.Column(db.String(200))

    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    # Relationship to reports
    reports = db.relationship('ProjectReport', backref='project', lazy=True, cascade='all, delete-orphan')


# ---------------- FEEDBACK TABLE ----------------
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------- REPORT TYPE TABLE ----------------
class ReportType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(50), unique=True, nullable=False)


# ---------------- PROJECT REPORT TABLE ----------------
class ProjectReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    reporter_name = db.Column(db.String(100))
    reporter_email = db.Column(db.String(100))
    
    report_subject = db.Column(db.String(200), nullable=False)
    report_message = db.Column(db.Text, nullable=False)

    report_type_id = db.Column(db.Integer, db.ForeignKey('report_type.id'))
    report_type = db.relationship('ReportType')

    is_resolved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------- REGION ANNUAL BUDGET TABLE ----------------
class RegionBudget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)

    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    region = db.relationship('Region')

    budget = db.Column(db.Float, nullable=False)

    __table_args__ = (db.UniqueConstraint('region_id', 'year', name='unique_region_year'),)


# ---------------- PROJECT SECTOR BUDGET TABLE ----------------
class ProjectSectorBudget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)

    sector_id = db.Column(db.Integer, db.ForeignKey('project_sector.id'), nullable=False)
    sector = db.relationship('ProjectSector')

    budget = db.Column(db.Float, nullable=False)


# ---------------- ANNUAL NATIONAL BUDGET TABLE ----------------
class AnnualBudget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, unique=True, nullable=False)
    total_budget = db.Column(db.Float, nullable=False)