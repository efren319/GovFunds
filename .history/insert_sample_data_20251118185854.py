#!/usr/bin/env python
# Script to insert sample data into govfunds database

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db
from models import DepartmentBudget, RegionBudget, AnnualBudget, Project, Feedback

def insert_data():
    with app.app_context():
        try:
            # Clear existing data
            print("Clearing existing data...")
            db.session.query(DepartmentBudget).delete()
            db.session.query(RegionBudget).delete()
            db.session.query(AnnualBudget).delete()
            db.session.commit()
            
            # Insert Department Budget Data for 2025
            print("Inserting department budgets...")
            depts = [
                DepartmentBudget(department='Department of Education', year=2025, budget=500000000),
                DepartmentBudget(department='Department of Health', year=2025, budget=400000000),
                DepartmentBudget(department='Department of Infrastructure', year=2025, budget=600000000),
                DepartmentBudget(department='Department of Defense', year=2025, budget=350000000),
                DepartmentBudget(department='Department of Social Services', year=2025, budget=250000000),
                DepartmentBudget(department='Department of Environment', year=2025, budget=180000000),
                DepartmentBudget(department='Department of Agriculture', year=2025, budget=220000000),
                DepartmentBudget(department='Department of Transportation', year=2025, budget=300000000),
            ]
            for dept in depts:
                db.session.add(dept)
            
            # Insert Region Budget Data for 2025
            print("Inserting region budgets...")
            regions = [
                RegionBudget(region='Region 1 - Ilocos Region', year=2025, budget=280000000),
                RegionBudget(region='Region 2 - Cagayan Valley', year=2025, budget=250000000),
                RegionBudget(region='Region 3 - Central Luzon', year=2025, budget=350000000),
                RegionBudget(region='Region 4A - CALABARZON', year=2025, budget=420000000),
                RegionBudget(region='Region 4B - MIMAROPA', year=2025, budget=180000000),
                RegionBudget(region='Region 5 - Bicol Region', year=2025, budget=220000000),
                RegionBudget(region='Region 6 - Western Visayas', year=2025, budget=280000000),
                RegionBudget(region='Region 7 - Central Visayas', year=2025, budget=310000000),
                RegionBudget(region='Region 8 - Eastern Visayas', year=2025, budget=190000000),
                RegionBudget(region='Region 9 - Zamboanga Peninsula', year=2025, budget=210000000),
                RegionBudget(region='Region 10 - Northern Mindanao', year=2025, budget=240000000),
                RegionBudget(region='Region 11 - Davao Region', year=2025, budget=300000000),
                RegionBudget(region='Region 12 - SOCCSKSARGEN', year=2025, budget=270000000),
                RegionBudget(region='Region 13 - Caraga', year=2025, budget=160000000),
                RegionBudget(region='NCR - National Capital Region', year=2025, budget=500000000),
            ]
            for region in regions:
                db.session.add(region)
            
            # Insert Annual Budget for 2025
            print("Inserting annual budget...")
            annual = AnnualBudget(year=2025, total_budget=4130000000)
            db.session.add(annual)
            
            # Insert Sample Projects
            print("Inserting sample projects...")
            projects = [
                Project(name='Build New School', department='Department of Education', 
                       description='Construction of 10 new schools in rural areas', 
                       allocated_budget=50000000, spent=15000000, status='Ongoing', 
                       region='Region 1 - Ilocos Region'),
                Project(name='Health Center Renovation', department='Department of Health',
                       description='Renovation of 20 health centers nationwide',
                       allocated_budget=40000000, spent=10000000, status='Ongoing',
                       region='Region 3 - Central Luzon'),
                Project(name='Road Infrastructure Project', department='Department of Infrastructure',
                       description='Construction of 100 km highway',
                       allocated_budget=100000000, spent=45000000, status='Ongoing',
                       region='Region 4A - CALABARZON'),
                Project(name='Bridge Construction', department='Department of Infrastructure',
                       description='Building 5 new bridges in key locations',
                       allocated_budget=75000000, spent=20000000, status='Planned',
                       region='Region 2 - Cagayan Valley'),
                Project(name='Agricultural Training Centers', department='Department of Agriculture',
                       description='Establishment of 15 training centers',
                       allocated_budget=30000000, spent=8000000, status='Ongoing',
                       region='Region 5 - Bicol Region'),
            ]
            for project in projects:
                db.session.add(project)
            
            db.session.commit()
            print("✅ All data inserted successfully!")
            
            # Verify
            dept_count = db.session.query(DepartmentBudget).count()
            region_count = db.session.query(RegionBudget).count()
            print(f"✅ Departments: {dept_count}")
            print(f"✅ Regions: {region_count}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()

if __name__ == '__main__':
    insert_data()
