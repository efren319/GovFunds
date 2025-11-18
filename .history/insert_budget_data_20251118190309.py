#!/usr/bin/env python3
"""Force insert budget data into the database"""

from app import db, app, DepartmentBudget, RegionBudget, AnnualBudget

def insert_data():
    with app.app_context():
        try:
            # First, clear existing data
            db.session.query(DepartmentBudget).delete()
            db.session.query(RegionBudget).delete()
            db.session.query(AnnualBudget).delete()
            db.session.commit()
            print("✅ Cleared existing data")
            
            # Insert Department Budgets
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
            print("✅ Added 8 departments")
            
            # Insert Regions
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
            print("✅ Added 15 regions")
            
            # Insert Annual Budget
            annual = AnnualBudget(year=2025, total_budget=4130000000)
            db.session.add(annual)
            print("✅ Added annual budget")
            
            db.session.commit()
            print("✅ All data inserted successfully!")
            
            # Verify
            dept_count = db.session.query(DepartmentBudget).count()
            region_count = db.session.query(RegionBudget).count()
            annual_count = db.session.query(AnnualBudget).count()
            print(f"\n📊 Database Status:")
            print(f"   DepartmentBudget: {dept_count} records")
            print(f"   RegionBudget: {region_count} records")
            print(f"   AnnualBudget: {annual_count} records")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    insert_data()
