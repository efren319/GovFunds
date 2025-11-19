#!/usr/bin/env python3
"""
Script to insert sample data into the GovFunds database.
Run this after the app is deployed: python seed_data.py
"""

import os
from dotenv import load_dotenv
from app import app, db
from models import Project, Feedback, RegionBudget, DepartmentBudget, AnnualBudget

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
            
            # Clear existing data (optional)
            print("Clearing existing data...")
            Project.query.delete()
            Feedback.query.delete()
            RegionBudget.query.delete()
            DepartmentBudget.query.delete()
            AnnualBudget.query.delete()
            db.session.commit()
            
            # Insert sample projects
            print("Inserting sample projects...")
            projects = [
                Project(
                    name='Road Rehabilitation - Barangay A',
                    department='Road Infrastructure',
                    description='Rehab of 3km barangay road',
                    allocated_budget=5000000,
                    spent=3500000,
                    status='Ongoing',
                    region='Region I',
                    start_date='2024-05-01',
                    end_date=None
                ),
                Project(
                    name='Bridge Construction Project',
                    department='Bridge Infrastructure',
                    description='New bridge construction across river',
                    allocated_budget=2000000,
                    spent=2000000,
                    status='Completed',
                    region='Region II',
                    start_date='2023-10-01',
                    end_date='2024-04-15'
                ),
                Project(
                    name='Flood Control System',
                    department='Flood Control and Drainage',
                    description='Installation of flood control infrastructure',
                    allocated_budget=3000000,
                    spent=1500000,
                    status='Ongoing',
                    region='Region III',
                    start_date='2024-01-10',
                    end_date=None
                ),
                Project(
                    name='Irrigation System Project',
                    department='Water Resources and Irrigation',
                    description='Small-scale irrigation',
                    allocated_budget=1500000,
                    spent=200000,
                    status='Planned',
                    region='Region IV',
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
            ]
            db.session.add_all(feedback)
            db.session.commit()
            print(f"✓ Inserted {len(feedback)} feedback entries")
            
            # Regional Budget Data for 2023
            print("Inserting regional budget data...")
            region_budgets_2023 = [
                RegionBudget(region='National Capital Region', year=2023, budget=887000000000),
                RegionBudget(region='Cordillera Administrative Region', year=2023, budget=98500000000),
                RegionBudget(region='Region I', year=2023, budget=169900000000),
                RegionBudget(region='Region II', year=2023, budget=144700000000),
                RegionBudget(region='Region III', year=2023, budget=321100000000),
                RegionBudget(region='Region IV-A', year=2023, budget=318700000000),
                RegionBudget(region='Region IV-B', year=2023, budget=134200000000),
                RegionBudget(region='Region V', year=2023, budget=212800000000),
                RegionBudget(region='Region VI', year=2023, budget=203500000000),
                RegionBudget(region='Region VII', year=2023, budget=212000000000),
                RegionBudget(region='Region VIII', year=2023, budget=177400000000),
                RegionBudget(region='Region IX', year=2023, budget=126800000000),
                RegionBudget(region='Region X', year=2023, budget=175000000000),
                RegionBudget(region='Region XI', year=2023, budget=149100000000),
                RegionBudget(region='Region XII', year=2023, budget=116400000000),
                RegionBudget(region='Caraga', year=2023, budget=109300000000),
                RegionBudget(region='BARMM', year=2023, budget=130300000000),
            ]
            db.session.add_all(region_budgets_2023)
            
            # Regional Budget Data for 2024
            region_budgets_2024 = [
                RegionBudget(region='National Capital Region', year=2024, budget=532008065000),
                RegionBudget(region='Cordillera Administrative Region', year=2024, budget=867228911000),
                RegionBudget(region='Region I', year=2024, budget=180565920000),
                RegionBudget(region='Region II', year=2024, budget=97668044000),
                RegionBudget(region='Region III', year=2024, budget=160174535000),
                RegionBudget(region='Region IV-A', year=2024, budget=369230365000),
                RegionBudget(region='Region IV-B', year=2024, budget=341101910000),
                RegionBudget(region='Region V', year=2024, budget=234040470000),
                RegionBudget(region='Region VI', year=2024, budget=222399947000),
                RegionBudget(region='Region VII', year=2024, budget=228181764000),
                RegionBudget(region='Region VIII', year=2024, budget=205946394000),
                RegionBudget(region='Region IX', year=2024, budget=140072215000),
                RegionBudget(region='Region X', year=2024, budget=190071333000),
                RegionBudget(region='Region XI', year=2024, budget=162666370000),
                RegionBudget(region='Region XII', year=2024, budget=127046390000),
                RegionBudget(region='Caraga', year=2024, budget=124270792000),
                RegionBudget(region='BARMM', year=2024, budget=149440406000),
            ]
            db.session.add_all(region_budgets_2024)
            
            # Regional Budget Data for 2025
            region_budgets_2025 = [
                RegionBudget(region='National Capital Region', year=2025, budget=834600000000),
                RegionBudget(region='Cordillera Administrative Region', year=2025, budget=106000000000),
                RegionBudget(region='Region I', year=2025, budget=198700000000),
                RegionBudget(region='Region II', year=2025, budget=175000000000),
                RegionBudget(region='Region III', year=2025, budget=420600000000),
                RegionBudget(region='Region IV-A', year=2025, budget=395600000000),
                RegionBudget(region='Region IV-B', year=2025, budget=184600000000),
                RegionBudget(region='Region V', year=2025, budget=257300000000),
                RegionBudget(region='Region VI', year=2025, budget=236100000000),
                RegionBudget(region='Region VII', year=2025, budget=255900000000),
                RegionBudget(region='Region VIII', year=2025, budget=209400000000),
                RegionBudget(region='Region IX', year=2025, budget=149300000000),
                RegionBudget(region='Region X', year=2025, budget=195700000000),
                RegionBudget(region='Region XI', year=2025, budget=172500000000),
                RegionBudget(region='Region XII', year=2025, budget=137800000000),
                RegionBudget(region='Caraga', year=2025, budget=138900000000),
                RegionBudget(region='BARMM', year=2025, budget=172400000000),
            ]
            db.session.add_all(region_budgets_2025)
            db.session.commit()
            print(f"✓ Inserted {len(region_budgets_2023) + len(region_budgets_2024) + len(region_budgets_2025)} regional budget entries")
            
            # Department Budget Data for 2023
            print("Inserting department budget data...")
            dept_budgets_2023 = [
                DepartmentBudget(department='Road Infrastructure', year=2023, budget=116252873000),
                DepartmentBudget(department='Bridge Infrastructure', year=2023, budget=29333447000),
                DepartmentBudget(department='Flood Control and Drainage', year=2023, budget=182989695000),
                DepartmentBudget(department='Public Buildings', year=2023, budget=79409974000),
                DepartmentBudget(department='Water Resources and Irrigation', year=2023, budget=15413692000),
                DepartmentBudget(department='Special Infrastructure Projects', year=2023, budget=388286983000),
                DepartmentBudget(department='Disaster Response and Rehabilitation', year=2023, budget=11000000000),
                DepartmentBudget(department='Local Infrastructure Support', year=2023, budget=37285405000),
            ]
            db.session.add_all(dept_budgets_2023)
            
            # Department Budget Data for 2024
            dept_budgets_2024 = [
                DepartmentBudget(department='Road Infrastructure', year=2024, budget=132328352000),
                DepartmentBudget(department='Bridge Infrastructure', year=2024, budget=24755275000),
                DepartmentBudget(department='Flood Control and Drainage', year=2024, budget=244577911000),
                DepartmentBudget(department='Public Buildings', year=2024, budget=100214102000),
                DepartmentBudget(department='Water Resources and Irrigation', year=2024, budget=74903429000),
                DepartmentBudget(department='Special Infrastructure Projects', year=2024, budget=410991162000),
                DepartmentBudget(department='Disaster Response and Rehabilitation', year=2024, budget=1000000000),
                DepartmentBudget(department='Local Infrastructure Support', year=2024, budget=39343250000),
            ]
            db.session.add_all(dept_budgets_2024)
            
            # Department Budget Data for 2025
            dept_budgets_2025 = [
                DepartmentBudget(department='Road Infrastructure', year=2025, budget=541980000000),
                DepartmentBudget(department='Bridge Infrastructure', year=2025, budget=38000000000),
                DepartmentBudget(department='Flood Control and Drainage', year=2025, budget=257060000000),
                DepartmentBudget(department='Public Buildings', year=2025, budget=113522058000),
                DepartmentBudget(department='Water Resources and Irrigation', year=2025, budget=42570000000),
                DepartmentBudget(department='Special Infrastructure Projects', year=2025, budget=330000000000),
                DepartmentBudget(department='Disaster Response and Rehabilitation', year=2025, budget=10000000000),
                DepartmentBudget(department='Local Infrastructure Support', year=2025, budget=25000000000),
            ]
            db.session.add_all(dept_budgets_2025)
            db.session.commit()
            print(f"✓ Inserted {len(dept_budgets_2023) + len(dept_budgets_2024) + len(dept_budgets_2025)} department budget entries")
            
            # Insert Annual Budget
            print("Inserting annual budget data...")
            annual_budgets = [
                AnnualBudget(year=2023, total_budget=5278700000000),
                AnnualBudget(year=2024, total_budget=5705700000000),
                AnnualBudget(year=2025, total_budget=6095900000000),
            ]
            db.session.add_all(annual_budgets)
            db.session.commit()
            print(f"✓ Inserted {len(annual_budgets)} annual budget entries")
            
            print("\n✅ All sample data inserted successfully!")
            
        except Exception as e:
            print(f"❌ Error inserting data: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    seed_data()
