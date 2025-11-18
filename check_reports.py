from app import app, db
from models import Project, ProjectReport

with app.app_context():
    # Find unresolved reports
    unresolved = ProjectReport.query.filter_by(is_resolved=False).all()
    print(f'Unresolved reports: {len(unresolved)}')
    
    for report in unresolved:
        project = Project.query.get(report.project_id)
        proj_name = project.name if project else 'Unknown'
        print(f'Report {report.id}: Project {report.project_id} ({proj_name})')
        print(f'  Subject: {report.report_subject}')
        print(f'  Type: {report.report_type}')
        print(f'  Resolved: {report.is_resolved}')
        print()
    
    # Test the admin page logic
    print("Testing admin page report count logic:")
    projects = Project.query.all()
    for project in projects[:5]:
        count = ProjectReport.query.filter_by(project_id=project.id, is_resolved=False).count()
        print(f'Project {project.id} ({project.name}): {count} unresolved')
