# models.py
# ---------------- IMPORTS ----------------
# These tools help us define tables for our database and track time
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the database object
db = SQLAlchemy()


# ---------------- USER TABLE ----------------
# This table stores all users (admin and viewers)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each user
    username = db.Column(db.String(50), unique=True, nullable=False)  
    # username must be unique and cannot be empty
    password = db.Column(db.String(200), nullable=False)  
    # store hashed passwords, cannot be empty
    role = db.Column(db.String(10), nullable=False)  
    # user role: 'admin' or 'staff' or 'viewer'


# ---------------- PROJECT TABLE ----------------
# This table stores government projects
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each project
    name = db.Column(db.String(100), nullable=False)  # Project name, cannot be empty
    project_sector = db.Column(db.String(100), nullable=False)  # Project sector managing project
    description = db.Column(db.Text)  # Optional description of the project
    allocated_budget = db.Column(db.Float, default=0)  # Budget allocated
    spent = db.Column(db.Float, default=0)  # Amount spent so far
    status = db.Column(db.String(20), default='Planned')  # Planned, Ongoing, Completed
    region = db.Column(db.String(50))  # Region where project is located
    start_date = db.Column(db.String(50))  # Project start date
    end_date = db.Column(db.String(50))  # Project end date
    
    # Relationship to project reports
    reports = db.relationship('ProjectReport', backref='project', lazy=True, cascade='all, delete-orphan')


# ---------------- FEEDBACK TABLE ----------------
# This table stores general feedback from citizens
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each feedback
    name = db.Column(db.String(100))  # Name of person giving feedback
    email = db.Column(db.String(100))  # Email of person giving feedback
    message = db.Column(db.Text, nullable=False)  # Feedback message, cannot be empty
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  
    # Automatically store the time when feedback was created


# ---------------- PROJECT REPORT TABLE ----------------
# This table stores reports/complaints about specific projects
class ProjectReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each report
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)  
    # Links to the project being reported
    reporter_name = db.Column(db.String(100))  # Name of person filing report
    reporter_email = db.Column(db.String(100))  # Email of reporter
    report_subject = db.Column(db.String(200), nullable=False)  # Subject of report
    report_message = db.Column(db.Text, nullable=False)  # Detailed message, cannot be empty
    report_type = db.Column(db.String(50), default='General')  # General, Issue, Concern, Suggestion
    is_resolved = db.Column(db.Boolean, default=False)  # Whether report has been resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  
    # Automatically store the time when report was created


# ---------------- REGION BUDGET TABLE ----------------
# This table stores budget allocations for each region
class RegionBudget(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID
    region = db.Column(db.String(100), nullable=False)  # Region name, cannot be empty
    year = db.Column(db.Integer, nullable=False)  # Budget year
    budget = db.Column(db.Float, nullable=False)  # Amount allocated for that year
    
    # Ensure each region has only one budget per year
    __table_args__ = (db.UniqueConstraint('region', 'year', name='unique_region_year'),)


# ---------------- PROJECT SECTOR BUDGET TABLE ----------------
# This table stores budget allocations for each project sector
class ProjectSectorBudget(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID
    sector = db.Column(db.String(100), nullable=False)  # Project sector name, cannot be empty
    year = db.Column(db.Integer, nullable=False)  # Budget year
    budget = db.Column(db.Float, nullable=False)  # Amount allocated for that year
    


# ---------------- ANNUAL BUDGET TABLE ----------------
# This table stores total annual budget allocations
class AnnualBudget(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID
    year = db.Column(db.Integer, unique=True, nullable=False)  # Budget year, must be unique
    total_budget = db.Column(db.Float, nullable=False)  # Total budget for that year
