"""
Database seed script - resets and populates the database with JSON data
Run with: python seed_db.py
"""
import json
import os
from datetime import datetime
from app import app, db
from models import Project, Feedback, ProjectReport

def reset_database():
    """Drop all tables and recreate them"""
    with app.app_context():
        print("🔄 Resetting database...")
        db.drop_all()
        db.create_all()
        print("✓ Database tables created")

def seed_projects():
    """Load projects from JSON and add to database"""
    with app.app_context():
        json_file = os.path.join(os.path.dirname(__file__), 'data', 'projects.json')
        
        if not os.path.exists(json_file):
            print(f"❌ {json_file} not found")
            return
        
        with open(json_file, 'r', encoding='utf-8') as f:
            projects_data = json.load(f)
        
        print(f"📦 Loading {len(projects_data)} projects...")
        
        for proj_data in projects_data:
            # Skip the problematic project 7 if needed, or include it
            project = Project(
                project_name=proj_data.get('project_name'),
                project_description=proj_data.get('project_description'),
                project_image=proj_data.get('project_image'),
                allocated_budget=proj_data.get('allocated_budget', 0),
                budget_spent=proj_data.get('budget_spent', 0),
                project_status=proj_data.get('project_status', 'Planned'),
                start_date=datetime.fromisoformat(proj_data['start_date']).date() if proj_data.get('start_date') else None,
                end_date=datetime.fromisoformat(proj_data['end_date']).date() if proj_data.get('end_date') else None,
                region_name=proj_data.get('region_name'),
                sector_name=proj_data.get('sector_name')
            )
            db.session.add(project)
        
        db.session.commit()
        print(f"✓ Added {len(projects_data)} projects")

def seed_feedback():
    """Load feedback from JSON and add to database"""
    with app.app_context():
        json_file = os.path.join(os.path.dirname(__file__), 'data', 'feedback.json')
        
        if not os.path.exists(json_file):
            print(f"⚠️ {json_file} not found")
            return
        
        with open(json_file, 'r', encoding='utf-8') as f:
            feedback_data = json.load(f)
        
        print(f"📦 Loading {len(feedback_data)} feedback entries...")
        
        for fb_data in feedback_data:
            feedback = Feedback(
                name=fb_data.get('name'),
                email=fb_data.get('email'),
                message=fb_data.get('message'),
                created_at=datetime.fromisoformat(fb_data['created_at']) if fb_data.get('created_at') else datetime.utcnow()
            )
            db.session.add(feedback)
        
        db.session.commit()
        print(f"✓ Added {len(feedback_data)} feedback entries")

def seed_reports():
    """Load reports from JSON and add to database"""
    with app.app_context():
        json_file = os.path.join(os.path.dirname(__file__), 'data', 'reports.json')
        
        if not os.path.exists(json_file):
            print(f"⚠️ {json_file} not found")
            return
        
        with open(json_file, 'r', encoding='utf-8') as f:
            reports_data = json.load(f)
        
        print(f"📦 Loading {len(reports_data)} reports...")
        
        for report_data in reports_data:
            report = ProjectReport(
                project_id=report_data.get('project_id'),
                reporter_name=report_data.get('reporter_name'),
                reporter_email=report_data.get('reporter_email'),
                report_subject=report_data.get('report_subject'),
                report_message=report_data.get('report_message'),
                report_type=report_data.get('report_type', 'General'),
                report_image=report_data.get('report_image'),
                is_resolved=report_data.get('is_resolved', False),
                created_at=datetime.fromisoformat(report_data['created_at']) if report_data.get('created_at') else datetime.utcnow()
            )
            db.session.add(report)
        
        db.session.commit()
        print(f"✓ Added {len(reports_data)} reports")

def verify_data():
    """Verify data was loaded correctly"""
    with app.app_context():
        project_count = Project.query.count()
        feedback_count = Feedback.query.count()
        report_count = ProjectReport.query.count()
        
        print("\n📊 Database Verification:")
        print(f"  Projects: {project_count}")
        print(f"  Feedback: {feedback_count}")
        print(f"  Reports: {report_count}")
        
        if project_count > 0:
            print("\n✅ Sample project:")
            sample = Project.query.first()
            print(f"  - {sample.project_name} ({sample.region_name})")

if __name__ == '__main__':
    try:
        reset_database()
        seed_projects()
        seed_feedback()
        seed_reports()
        verify_data()
        print("\n✅ Database seeding complete!")
    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        import traceback
        traceback.print_exc()
