import os
from datetime import date
from dotenv import load_dotenv
from app import app, db
from models import Project, Feedback, ProjectReport

# Load environment variables
load_dotenv()

def seed_data():
    """Insert sample data into the database"""
    
    with app.app_context():
        try:
            # Create all tables if they don't exist
            print("Creating database tables...")
            db.create_all()
            print("✓ Tables created/verified")
            
            # Clear existing data
            print("Clearing existing data...")
            ProjectReport.query.delete()
            Project.query.delete()
            Feedback.query.delete()
            db.session.commit()
            
            # Insert sample projects
            print("Inserting sample projects...")
            projects = [
                Project(
                    project_name='Road Rehabilitation - Barangay A',
                    sector_name='Road Infrastructure',
                    project_description='Rehab of 3km barangay road',
                    allocated_budget=5000000,
                    budget_spent=3500000,
                    project_status='Ongoing',
                    region_name='Region I',
                    start_date=date(2024, 5, 1),
                    end_date=None
                ),
                Project(
                    project_name='Public Building Construction',
                    sector_name='Public Buildings',
                    project_description='Government office building',
                    allocated_budget=2000000,
                    budget_spent=2000000,
                    project_status='Completed',
                    region_name='Region II',
                    start_date=date(2023, 10, 1),
                    end_date=date(2024, 4, 15)
                ),
                Project(
                    project_name='Bridge Repair and Maintenance',
                    sector_name='Bridge Infrastructure',
                    project_description='Structural repair of aging bridge',
                    allocated_budget=3000000,
                    budget_spent=1500000,
                    project_status='Ongoing',
                    region_name='Region III',
                    start_date=date(2024, 1, 10),
                    end_date=None
                ),
                Project(
                    project_name='Irrigation System Project',
                    sector_name='Water Resources and Irrigation',
                    project_description='Small-scale irrigation facility',
                    allocated_budget=1500000,
                    budget_spent=200000,
                    project_status='Planned',
                    region_name='Region IV-A',
                    start_date=None,
                    end_date=None
                ),
                Project(
                    project_name='Flood Control System - NCR',
                    sector_name='Flood Control and Drainage',
                    project_description='Drainage system improvement in Metro Manila',
                    allocated_budget=8000000,
                    budget_spent=4000000,
                    project_status='Ongoing',
                    region_name='National Capital Region',
                    start_date=date(2024, 3, 15),
                    end_date=None
                ),
                Project(
                    project_name='Disaster Relief Center',
                    sector_name='Disaster Response and Rehabilitation',
                    project_description='Emergency response facility construction',
                    allocated_budget=4500000,
                    budget_spent=0,
                    project_status='Planned',
                    region_name='Region VIII',
                    start_date=None,
                    end_date=None
                ),
            ]
            db.session.add_all(projects)
            db.session.commit()
            print(f"✓ Inserted {len(projects)} projects")
            
            # Insert sample feedback
            print("Inserting sample feedback...")
            feedback = [
                Feedback(
                    name='Juan Dela Cruz',
                    email='juan@example.com',
                    message='Please update the road project timeline.'
                ),
                Feedback(
                    name='Maria Santos',
                    email='maria@example.com',
                    message='Great initiative — more regional breakdown needed.'
                ),
                Feedback(
                    name='Pedro Reyes',
                    email='pedro@example.com',
                    message='Excellent transparency on budget spending!'
                ),
            ]
            db.session.add_all(feedback)
            db.session.commit()
            print(f"✓ Inserted {len(feedback)} feedback entries")
            
            print("\n✅ All sample data inserted successfully!")
            
        except Exception as e:
            print(f"❌ Error inserting data: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    seed_data()
