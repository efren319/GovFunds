#!/usr/bin/env python3
"""Verify data is in database and appears in budget page"""

from app import db, app, DepartmentBudget, RegionBudget, AnnualBudget

with app.app_context():
    dept_count = db.session.query(DepartmentBudget).count()
    region_count = db.session.query(RegionBudget).count()
    annual_count = db.session.query(AnnualBudget).count()
    
    print("[BUDGET PAGE DATA VERIFICATION]")
    print(f"Departments: {dept_count}")
    print(f"Regions: {region_count}")
    print(f"Annual Budgets: {annual_count}")
    
    if dept_count == 8 and region_count == 15 and annual_count >= 1:
        print("\n[SUCCESS] Budget page should now display all data!")
        print("\nDepartment sample:")
        depts = db.session.query(DepartmentBudget).order_by(DepartmentBudget.budget.desc()).limit(3).all()
        for dept in depts:
            print(f"  {dept.department}: {dept.budget:,}")
        
        print("\nRegion sample:")
        regions = db.session.query(RegionBudget).order_by(RegionBudget.budget.desc()).limit(3).all()
        for region in regions:
            print(f"  {region.region}: {region.budget:,}")
    else:
        print(f"\n[WARNING] Expected 8 depts, 15 regions, 1+ annual - got {dept_count}, {region_count}, {annual_count}")
