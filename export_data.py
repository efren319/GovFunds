"""
Export database data to JSON files for sharing via Git.
Run this whenever you want to share your current data with others.

Usage: python export_data.py
Then: git add data/ && git commit -m "Update data" && git push
"""
import json
import os
from datetime import date, datetime
from app import app, db
from models import Project, Feedback, ProjectReport

def json_serial(obj):
    """JSON serializer for objects not serializable by default"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def export_data():
    """Export all database data to JSON files"""
    
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    with app.app_context():
        # Export Projects
        projects = Project.query.all()
        projects_data = []
        for p in projects:
            projects_data.append({
                'project_id': p.project_id,
                'project_name': p.project_name,
                'project_description': p.project_description,
                'project_image': p.project_image,
                'allocated_budget': p.allocated_budget,
                'budget_spent': p.budget_spent,
                'project_status': p.project_status,
                'start_date': p.start_date,
                'end_date': p.end_date,
                'region_name': p.region_name,
                'sector_name': p.sector_name
            })
        
        with open(os.path.join(data_dir, 'projects.json'), 'w', encoding='utf-8') as f:
            json.dump(projects_data, f, indent=2, default=json_serial, ensure_ascii=False)
        print(f"✓ Exported {len(projects_data)} projects")
        
        # Export Feedback
        feedbacks = Feedback.query.all()
        feedback_data = []
        for fb in feedbacks:
            feedback_data.append({
                'feedback_id': fb.feedback_id,
                'name': fb.name,
                'email': fb.email,
                'message': fb.message,
                'created_at': fb.created_at
            })
        
        with open(os.path.join(data_dir, 'feedback.json'), 'w', encoding='utf-8') as f:
            json.dump(feedback_data, f, indent=2, default=json_serial, ensure_ascii=False)
        print(f"✓ Exported {len(feedback_data)} feedback entries")
        
        # Export Project Reports
        reports = ProjectReport.query.all()
        reports_data = []
        for r in reports:
            reports_data.append({
                'report_id': r.report_id,
                'project_id': r.project_id,
                'reporter_name': r.reporter_name,
                'reporter_email': r.reporter_email,
                'report_subject': r.report_subject,
                'report_message': r.report_message,
                'report_type': r.report_type,
                'is_resolved': r.is_resolved,
                'created_at': r.created_at
            })
        
        with open(os.path.join(data_dir, 'reports.json'), 'w', encoding='utf-8') as f:
            json.dump(reports_data, f, indent=2, default=json_serial, ensure_ascii=False)
        print(f"✓ Exported {len(reports_data)} reports")
        
        print(f"\n✅ Data exported to 'data/' folder")
        print("Now run: git add data/ && git commit -m 'Update data' && git push")

if __name__ == '__main__':
    export_data()
