"""Execute seed.sql file against the database"""
import os
from app import app, db

def execute_seed_sql():
    """Execute seed.sql file"""
    with app.app_context():
        sql_file = os.path.join(os.path.dirname(__file__), 'seed.sql')
        
        if not os.path.exists(sql_file):
            print(f"❌ {sql_file} not found")
            return
        
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        try:
            print("🔄 Executing seed.sql...")
            db.session.execute(db.text(sql_content))
            db.session.commit()
            print("✓ SQL executed successfully")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error executing SQL: {e}")
            raise

def verify_data():
    """Verify data was loaded"""
    with app.app_context():
        from models import Project, Feedback, ProjectReport
        
        project_count = Project.query.count()
        feedback_count = Feedback.query.count()
        report_count = ProjectReport.query.count()
        
        print("\n📊 Database Verification:")
        print(f"  Projects: {project_count}")
        print(f"  Feedback: {feedback_count}")
        print(f"  Reports: {report_count}")
        
        if project_count > 0:
            print("\n✅ Sample projects:")
            samples = Project.query.limit(3).all()
            for p in samples:
                print(f"  - {p.project_name} (₱{p.allocated_budget:,.0f})")

if __name__ == '__main__':
    try:
        execute_seed_sql()
        verify_data()
        print("\n✅ Database seeding complete!")
    except Exception as e:
        print(f"\n❌ Failed: {e}")
        import traceback
        traceback.print_exc()
