#!/usr/bin/env python
"""Check and verify database tables"""

from app import app, db
from models import Project
from sqlalchemy import inspect

with app.app_context():
    # Create all tables if they don't exist
    db.create_all()
    print("✅ Tables created/verified successfully!")
    
    # Get inspector
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"\n📊 Tables in database ({len(tables)}):")
    for table in sorted(tables):
        print(f"  - {table}")
    
    # Check project count
    count = db.session.query(Project).count()
    print(f"\n✅ Projects in database: {count}")
