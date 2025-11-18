#!/usr/bin/env python
"""Force recreate all tables in the govfunds database"""

from app import app, db
from models import Project, Feedback, ProjectReport, RegionBudget, DepartmentBudget, AnnualBudget, User

with app.app_context():
    print("🔄 Dropping all existing tables...")
    db.drop_all()
    print("✅ All tables dropped")
    
    print("\n🆕 Creating new tables...")
    db.create_all()
    print("✅ All tables created")
    
    print("\n📊 Verifying tables...")
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"✅ Tables in database ({len(tables)}):")
    for table in sorted(tables):
        print(f"   - {table}")
    
    print("\n✅ Database ready for pgAdmin!")
    print("\nNow:")
    print("1. Open pgAdmin")
    print("2. Refresh your server (F5)")
    print("3. Navigate to: Servers → PostgreSQL 18 → Databases → govfunds → Schemas → public → Tables")
    print("4. Right-click any table → View/Edit Data → All Rows")
