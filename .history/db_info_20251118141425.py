#!/usr/bin/env python
"""Export database structure and data for pgAdmin viewing"""

from app import app, db
from models import Project, Feedback, ProjectReport, RegionBudget, DepartmentBudget, AnnualBudget
from sqlalchemy import inspect
import json

with app.app_context():
    print("=" * 60)
    print("🗄️  DATABASE INFORMATION FOR PGADMIN")
    print("=" * 60)
    
    # Get inspector
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    
    print(f"\n📊 Tables exist in PostgreSQL ({len(tables)}):")
    for table in sorted(tables):
        print(f"  ✅ {table}")
    
    print("\n" + "=" * 60)
    print("📋 DATA IN EACH TABLE")
    print("=" * 60)
    
    # Projects
    projects = db.session.query(Project).all()
    print(f"\n🏗️  PROJECTS ({len(projects)} records):")
    if projects:
        for p in projects:
            print(f"  ID: {p.id} | {p.name} | Status: {p.status} | Region: {p.region}")
    else:
        print("  (No projects found)")
    
    # Feedback
    feedbacks = db.session.query(Feedback).all()
    print(f"\n💬 FEEDBACK ({len(feedbacks)} records):")
    if feedbacks:
        for f in feedbacks:
            print(f"  ID: {f.id} | {f.name} ({f.email}) | {f.message[:50]}...")
    else:
        print("  (No feedback found)")
    
    # Regional Budgets
    regions = db.session.query(RegionBudget).all()
    print(f"\n🌍 REGIONAL BUDGETS ({len(regions)} records):")
    if regions:
        region_summary = {}
        for r in regions:
            if r.year not in region_summary:
                region_summary[r.year] = 0
            region_summary[r.year] += 1
        for year, count in sorted(region_summary.items()):
            print(f"  Year {year}: {count} regions")
    else:
        print("  (No regional budgets found)")
    
    # Department Budgets
    depts = db.session.query(DepartmentBudget).all()
    print(f"\n🏢 DEPARTMENT BUDGETS ({len(depts)} records):")
    if depts:
        dept_summary = {}
        for d in depts:
            if d.year not in dept_summary:
                dept_summary[d.year] = 0
            dept_summary[d.year] += 1
        for year, count in sorted(dept_summary.items()):
            print(f"  Year {year}: {count} departments")
    else:
        print("  (No department budgets found)")
    
    # Annual Budgets
    annual = db.session.query(AnnualBudget).all()
    print(f"\n💰 ANNUAL BUDGETS ({len(annual)} records):")
    if annual:
        for a in annual:
            print(f"  Year {a.year}: ₱{a.total_budget:,}")
    else:
        print("  (No annual budgets found)")
    
    print("\n" + "=" * 60)
    print("🔗 TO VIEW IN PGADMIN:")
    print("=" * 60)
    print("""
1. Open pgAdmin: http://localhost:5050
2. Login with your pgAdmin credentials
3. Navigate: Servers → PostgreSQL 18 → Databases → govfunds
4. Expand the database
5. In the left panel, you'll see all tables:
   - annual_budgets
   - department_budgets
   - feedback
   - project_reports
   - projects
   - region_budgets
   - users

6. Right-click any table → View/Edit Data → All Rows

7. To run SQL queries:
   - Right-click govfunds → Query Tool
   - Run: SELECT * FROM projects;
    """)
    print("=" * 60)
