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
                    department='Department of Public Works and Highways',
                    description='Rehab of 3km barangay road',
                    allocated_budget=5000000,
                    spent=3500000,
                    status='Ongoing',
                    region='Region I',
                    start_date='2024-05-01',
                    end_date=None
                ),
                Project(
                    name='School Building Construction',
                    department='Department of Education',
                    description='2-classroom building',
                    allocated_budget=2000000,
                    spent=2000000,
                    status='Completed',
                    region='Region II',
                    start_date='2023-10-01',
                    end_date='2024-04-15'
                ),
                Project(
                    name='Health Center Upgrade',
                    department='Department of Health',
                    description='Medical equipment and building upgrade',
                    allocated_budget=3000000,
                    spent=1500000,
                    status='Ongoing',
                    region='Region III',
                    start_date='2024-01-10',
                    end_date=None
                ),
                Project(
                    name='Irrigation System Project',
                    department='Department of Agriculture',
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
                DepartmentBudget(department='Department of Education', year=2023, budget=678317321000),
                DepartmentBudget(department='Department of Health', year=2023, budget=209624216000),
                DepartmentBudget(department='Department of Public Works and Highways', year=2023, budget=893121040000),
                DepartmentBudget(department='Department of the Interior and Local Government', year=2023, budget=253404249000),
                DepartmentBudget(department='Department of National Defense', year=2023, budget=204566332000),
                DepartmentBudget(department='Department of Social Welfare and Development', year=2023, budget=199256638000),
                DepartmentBudget(department='Department of Agriculture', year=2023, budget=98864397000),
                DepartmentBudget(department='Department of Budget and Management', year=2023, budget=1737629000),
                DepartmentBudget(department='Department of Justice', year=2023, budget=36228754000),
                DepartmentBudget(department='Department of Labor and Employment', year=2023, budget=46631922000),
                DepartmentBudget(department='Department of Energy', year=2023, budget=1320735000),
                DepartmentBudget(department='Department of Finance', year=2023, budget=23927302000),
                DepartmentBudget(department='Department of Foreign Affairs', year=2023, budget=20621463000),
                DepartmentBudget(department='Department of Information and Communications Technology', year=2023, budget=8289778000),
                DepartmentBudget(department='Department of Tourism', year=2023, budget=3731984000),
                DepartmentBudget(department='Department of Trade and Industry', year=2023, budget=6327029000),
                DepartmentBudget(department='Department of Transportation', year=2023, budget=105530385000),
                DepartmentBudget(department='National Economic and Development Authority', year=2023, budget=12961084000),
                DepartmentBudget(department='Civil Service Commission', year=2023, budget=2045591000),
                DepartmentBudget(department='Commission on Audit', year=2023, budget=13318049000),
                DepartmentBudget(department='Commission on Elections', year=2023, budget=5737340000),
                DepartmentBudget(department='Office of the Ombudsman', year=2023, budget=4721331000),
                DepartmentBudget(department='Commission on Human Rights', year=2023, budget=993921000),
                DepartmentBudget(department='Special Purpose Funds', year=2023, budget=1825624983000),
            ]
            db.session.add_all(dept_budgets_2023)
            
            # Department Budget Data for 2024
            dept_budgets_2024 = [
                DepartmentBudget(department='Department of Education', year=2024, budget=717663478000),
                DepartmentBudget(department='Department of Health', year=2024, budget=241602813000),
                DepartmentBudget(department='Department of Public Works and Highways', year=2024, budget=996791684000),
                DepartmentBudget(department='Department of the Interior and Local Government', year=2024, budget=263649999000),
                DepartmentBudget(department='Department of National Defense', year=2024, budget=238356544000),
                DepartmentBudget(department='Department of Social Welfare and Development', year=2024, budget=247848341000),
                DepartmentBudget(department='Department of Agriculture', year=2024, budget=111687758000),
                DepartmentBudget(department='Department of Budget and Management', year=2024, budget=2501145000),
                DepartmentBudget(department='Department of Justice', year=2024, budget=36228754000),
                DepartmentBudget(department='Department of Labor and Employment', year=2024, budget=61268468000),
                DepartmentBudget(department='Department of Energy', year=2024, budget=1662160000),
                DepartmentBudget(department='Department of Finance', year=2024, budget=23927302000),
                DepartmentBudget(department='Department of Foreign Affairs', year=2024, budget=24591198000),
                DepartmentBudget(department='Department of Tourism', year=2024, budget=3439715000),
                DepartmentBudget(department='Department of Trade and Industry', year=2024, budget=8638218000),
                DepartmentBudget(department='Department of Transportation', year=2024, budget=73330669000),
                DepartmentBudget(department='Special Purpose Funds', year=2024, budget=2169133613000),
            ]
            db.session.add_all(dept_budgets_2024)
            
            # Department Budget Data for 2025
            dept_budgets_2025 = [
                DepartmentBudget(department='Department of Education', year=2025, budget=793177297000),
                DepartmentBudget(department='Department of Health', year=2025, budget=223188973000),
                DepartmentBudget(department='Department of Public Works and Highways', year=2025, budget=900000000000),
                DepartmentBudget(department='Department of the Interior and Local Government', year=2025, budget=281320865000),
                DepartmentBudget(department='Department of National Defense', year=2025, budget=258164910000),
                DepartmentBudget(department='Department of Social Welfare and Development', year=2025, budget=230057270000),
                DepartmentBudget(department='Department of Agriculture', year=2025, budget=129001585000),
                DepartmentBudget(department='Department of Budget and Management', year=2025, budget=3191835000),
                DepartmentBudget(department='Department of Justice', year=2025, budget=40584630000),
                DepartmentBudget(department='Department of Labor and Employment', year=2025, budget=45833958000),
                DepartmentBudget(department='Department of Migrant Workers', year=2025, budget=8503912000),
                DepartmentBudget(department='National Economic and Development Authority', year=2025, budget=12575395000),
                DepartmentBudget(department='Department of Transportation', year=2025, budget=180893888000),
                DepartmentBudget(department='Department of Trade and Industry', year=2025, budget=8598332000),
                DepartmentBudget(department='Commission on Audit', year=2025, budget=13417340000),
                DepartmentBudget(department='Commission on Elections', year=2025, budget=35470671000),
                DepartmentBudget(department='Office of the Ombudsman', year=2025, budget=5824154000),
                DepartmentBudget(department='Special Purpose Funds', year=2025, budget=2740481084000),
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
