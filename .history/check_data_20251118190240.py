from app import db, app, DepartmentBudget, RegionBudget, AnnualBudget

with app.app_context():
    dept_count = db.session.query(DepartmentBudget).count()
    region_count = db.session.query(RegionBudget).count()
    annual_count = db.session.query(AnnualBudget).count()
    
    print(f"DepartmentBudget records: {dept_count}")
    print(f"RegionBudget records: {region_count}")
    print(f"AnnualBudget records: {annual_count}")
    
    if dept_count > 0:
        depts = DepartmentBudget.query.limit(3).all()
        for d in depts:
            print(f"  - {d.department} (Year {d.year}): {d.budget}")
    
    if region_count > 0:
        regions = RegionBudget.query.limit(3).all()
        for r in regions:
            print(f"  - {r.region} (Year {r.year}): {r.budget}")
