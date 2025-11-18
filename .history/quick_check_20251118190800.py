#!/usr/bin/env python3
"""Quick check of database records without hanging"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

try:
    from app import db, app, DepartmentBudget, RegionBudget, AnnualBudget
    
    with app.app_context():
        dept_count = db.session.query(DepartmentBudget).count()
        region_count = db.session.query(RegionBudget).count()
        annual_count = db.session.query(AnnualBudget).count()
        
        print(f"DepartmentBudget: {dept_count}")
        print(f"RegionBudget: {region_count}")
        print(f"AnnualBudget: {annual_count}")
        
        if dept_count > 0:
            dept = db.session.query(DepartmentBudget).first()
            print(f"First dept: {dept.department} - {dept.budget}")
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
