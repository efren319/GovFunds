# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from sqlalchemy import func, text  # type: ignore
from functools import wraps
import hashlib
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename
from models import db, Project, Feedback, ProjectReport

# File upload configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'images', 'projects')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# PostgreSQL Configuration for Local Development
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'govfunds'

app = Flask(__name__)
app.secret_key = 'sikreto ni aldred'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 hours

# Protected routes that require login
PROTECTED_ROUTES = ['/admin']

@app.before_request
def check_admin_access():
    """Check if user is trying to access protected routes"""
    if request.path == '/admin':
        if 'admin_user' not in session or not session.get('admin_user'):
            flash('Please log in to access the admin panel.', 'warning')
            return redirect(url_for('login'))

# SQLAlchemy Configuration for PostgreSQL
DB_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Validate database URI
try:
    from urllib.parse import urlparse
    parsed = urlparse(DB_URI)
    if not parsed.hostname:
        raise ValueError("Invalid database URL")
except Exception as e:
    print(f"Warning: Invalid database URI: {e}")
    print(f"Database URI: {DB_URI}")

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Initialize database on startup
def init_db():
    """Initialize database tables and seed data if empty"""
    with app.app_context():
        try:
            db.create_all()
            print("✓ Database tables created/verified")
            
            # Check if database is empty
            project_count = Project.query.count()
            
            if project_count == 0:
                print("→ Database is empty. Seeding from seed.sql...")
                seed_from_sql()
                print("✓ Database seeded successfully")
                
                # Export to JSON after seeding
                sync_to_json()
                print("✓ Data exported to JSON files")
            else:
                print(f"✓ Database already populated with {project_count} projects")
        except Exception as e:
            print(f"Error during database initialization: {e}")

def seed_from_sql():
    """Execute seed.sql to populate database"""
    try:
        seed_sql_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'seed.sql')
        
        if not os.path.exists(seed_sql_path):
            print(f"Warning: seed.sql not found at {seed_sql_path}")
            return
        
        with open(seed_sql_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Execute SQL
        db.session.execute(text(sql_content))
        db.session.commit()
        print("✓ Seed SQL executed successfully")
    except Exception as e:
        db.session.rollback()
        print(f"Error executing seed.sql: {e}")
        raise

def sync_to_json():
    """Export all database records to JSON files"""
    try:
        data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        os.makedirs(data_folder, exist_ok=True)
        
        # Export projects
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
                'start_date': p.start_date.isoformat() if p.start_date else None,
                'end_date': p.end_date.isoformat() if p.end_date else None,
                'region_name': p.region_name,
                'sector_name': p.sector_name
            })
        
        projects_path = os.path.join(data_folder, 'projects.json')
        with open(projects_path, 'w', encoding='utf-8') as f:
            json.dump(projects_data, f, ensure_ascii=False, indent=2)
        
        # Export feedback
        feedback_list = Feedback.query.all()
        feedback_data = []
        for fb in feedback_list:
            feedback_data.append({
                'feedback_id': fb.feedback_id,
                'name': fb.name,
                'email': fb.email,
                'message': fb.message,
                'created_at': fb.created_at.isoformat() if fb.created_at else None
            })
        
        feedback_path = os.path.join(data_folder, 'feedback.json')
        with open(feedback_path, 'w', encoding='utf-8') as f:
            json.dump(feedback_data, f, ensure_ascii=False, indent=2)
        
        # Export reports
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
                'report_image': r.report_image,
                'is_resolved': r.is_resolved,
                'created_at': r.created_at.isoformat() if r.created_at else None
            })
        
        reports_path = os.path.join(data_folder, 'reports.json')
        with open(reports_path, 'w', encoding='utf-8') as f:
            json.dump(reports_data, f, ensure_ascii=False, indent=2)
        
        print("✓ Data synced to JSON files")
    except Exception as e:
        print(f"Error syncing to JSON: {e}")

# Run initialization when app starts
init_db()

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_user' not in session or not session.get('admin_user'):
            flash('Please log in to access this feature.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Hash password for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Admin credentials
ADMIN_CREDENTIALS = {
    'admin': hash_password('admin123'),
    'staff': hash_password('staff123')
}

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            return render_template('login.html', error='Username and password are required.')
        
        # Check credentials
        hashed_password = hash_password(password)
        if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == hashed_password:
            session.permanent = True
            session['admin_user'] = username
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error='Invalid username or password.')
    
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

# Home
@app.route('/')
def home():
    try:
        # Use ORM to query projects
        projects = Project.query.all()
        projects_count = len(projects)
        total_alloc = sum(p.allocated_budget for p in projects) if projects else 0
        total_spent = sum(p.budget_spent for p in projects) if projects else 0
        
        # Get recent feedback for carousel
        recent_feedback = Feedback.query.order_by(Feedback.created_at.desc()).limit(20).all()
        
        return render_template('home.html',
                               projects_count=projects_count,
                               total_alloc=total_alloc,
                               total_spent=total_spent,
                               recent_feedback=recent_feedback)
    except Exception as e:
        print(f"Error in home route: {e}")
        return render_template('home.html',
                               projects_count=0,
                               total_alloc=0,
                               total_spent=0,
                               recent_feedback=[])

@app.route('/budget')
def budget():
    try:
        projects = Project.query.all()
        return render_template('budget.html', projects=projects)
    except Exception as e:
        print(f"Error in budget route: {e}")
        return render_template('budget.html', projects=[])


# API endpoint for budget data (used by Chart.js)
@app.route('/api/budget_data')
def budget_data():
    try:
        result = db.session.query(
            Project.sector_name,
            func.sum(Project.allocated_budget).label('allocated'),
            func.sum(Project.budget_spent).label('spent')
        ).group_by(Project.sector_name).all()

        rows = [{'sector': row[0], 'allocated': row[1] or 0, 'spent': row[2] or 0} for row in result]
        return jsonify(rows)
    except Exception as e:
        print(f"Error in budget_data: {e}")
        return jsonify([])

# Hardcoded lists for dropdowns
REGIONS_LIST = [
    'National Capital Region', 'Cordillera Administrative Region', 'Region I', 'Region II',
    'Region III', 'Region IV-A', 'Region IV-B', 'Region V', 'Region VI', 'Region VII',
    'Region VIII', 'Region IX', 'Region X', 'Region XI', 'Region XII', 'Caraga', 'BARMM'
]

SECTORS_LIST = [
    'Road Infrastructure', 'Bridge Infrastructure', 'Flood Control and Drainage',
    'Public Buildings', 'Water Resources and Irrigation', 'Special Infrastructure Projects',
    'Disaster Response and Rehabilitation', 'Local Infrastructure Support'
]

# Projects listing
@app.route('/projects')
def projects():
    try:
        projects_list = Project.query.order_by(Project.project_id.desc()).all()
        
        # Count projects by status
        total_count = len(projects_list)
        planned_count = sum(1 for p in projects_list if p.project_status == 'Planned')
        ongoing_count = sum(1 for p in projects_list if p.project_status == 'Ongoing')
        completed_count = sum(1 for p in projects_list if p.project_status == 'Completed')
        
        return render_template('projects.html', 
                               projects=projects_list, 
                               regions_list=REGIONS_LIST,
                               sectors_list=SECTORS_LIST,
                               total_count=total_count,
                               planned_count=planned_count,
                               ongoing_count=ongoing_count,
                               completed_count=completed_count)
    except Exception as e:
        print(f"Error in projects route: {e}")
        return render_template('projects.html', projects=[], regions_list=[], sectors_list=[],
                               total_count=0, planned_count=0, ongoing_count=0, completed_count=0)

# Project detail
@app.route('/project/<int:pid>')
def project_detail(pid):
    try:
        project = Project.query.get(pid)
        if not project:
            flash('Project not found', 'warning')
            return redirect(url_for('projects'))
        
        # Get reports for this project
        reports = ProjectReport.query.filter_by(project_id=pid).order_by(ProjectReport.created_at.desc()).all()
        
        return render_template('project_details.html', project=project, reports=reports)
    except Exception as e:
        print(f"Error in project_detail: {e}")
        flash('Error loading project', 'danger')
        return redirect(url_for('projects'))

# Get project data for editing (API endpoint)
@app.route('/api/project/<int:pid>')
def get_project_data(pid):
    if 'admin_user' not in session or not session.get('admin_user'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        project = Project.query.get(pid)
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        
        return jsonify({
            'id': project.project_id,
            'name': project.project_name,
            'project_sector': project.sector_name or '',
            'region': project.region_name or '',
            'status': project.project_status,
            'allocated_budget': project.allocated_budget or 0,
            'spent': project.budget_spent or 0,
            'description': project.project_description or '',
            'project_image': project.project_image or ''
        })
    except Exception as e:
        print(f"Error in get_project_data: {e}")
        return jsonify({'error': 'Error fetching project'}), 500

# Edit project (admin only)
@app.route('/project/<int:pid>/edit', methods=['GET', 'POST'])
def edit_project(pid):
    if 'admin_user' not in session or not session.get('admin_user'):
        flash('You must be logged in as admin to edit projects', 'danger')
        return redirect(url_for('login'))
    
    try:
        project = Project.query.get(pid)
        if not project:
            flash('Project not found', 'warning')
            return redirect(url_for('projects'))
        
        if request.method == 'POST':
            project.project_name = request.form.get('name', '').strip()
            project.sector_name = request.form.get('project_sector', '').strip()
            project.region_name = request.form.get('region', '').strip()
            project.project_status = request.form.get('status', 'Planned')
            project.allocated_budget = float(request.form.get('allocated_budget') or 0)
            project.budget_spent = float(request.form.get('spent') or 0)
            project.project_description = request.form.get('description', '').strip()
            
            # Handle image upload
            if 'project_image' in request.files:
                file = request.files['project_image']
                if file and file.filename and allowed_file(file.filename):
                    # Ensure upload directory exists
                    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                    filename = secure_filename(file.filename)
                    # Add timestamp to avoid duplicates
                    import time
                    filename = f"{int(time.time())}_{filename}"
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    project.project_image = f"images/projects/{filename}"
            
            db.session.commit()
            
            # Sync to JSON
            sync_to_json()
            
            flash('Project updated successfully', 'success')
            return redirect(url_for('project_detail', pid=pid))
        
        return redirect(url_for('projects'))
    except Exception as e:
        db.session.rollback()
        print(f"Error in edit_project: {e}")
        flash('Error updating project', 'danger')
        return redirect(url_for('projects'))

# Delete project (admin only)
@app.route('/project/<int:pid>/delete', methods=['POST'])
def delete_project(pid):
    if 'admin_user' not in session or not session.get('admin_user'):
        flash('You must be logged in as admin to delete projects', 'danger')
        return redirect(url_for('login'))
    
    try:
        project = Project.query.get(pid)
        if not project:
            flash('Project not found', 'warning')
            return redirect(url_for('projects'))
        
        # Delete associated reports first
        ProjectReport.query.filter_by(project_id=pid).delete()
        
        # Delete project image file if exists
        if project.project_image:
            image_path = os.path.join(app.static_folder, project.project_image)
            if os.path.exists(image_path):
                try:
                    os.remove(image_path)
                except Exception as img_err:
                    print(f"Error deleting image file: {img_err}")
        
        # Delete the project
        db.session.delete(project)
        db.session.commit()
        flash('Project deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Error in delete_project: {e}")
        flash('Error deleting project', 'danger')
    
    return redirect(url_for('projects'))

# Feedback form
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        feedback_type = request.form.get('feedback_type', 'general')
        
        if feedback_type == 'report':
            # Handle project report
            project_id = request.form.get('project_id', '').strip()
            reporter_name = request.form.get('reporter_name', '').strip()
            reporter_email = request.form.get('reporter_email', '').strip()
            report_subject = request.form.get('report_subject', '').strip()
            report_message = request.form.get('report_message', '').strip()
            report_type = request.form.get('report_type', 'General')
            
            if not project_id or not report_subject or not report_message:
                flash('Please fill in all required fields', 'danger')
                return redirect(url_for('feedback'))
            
            try:
                project_id = int(project_id)
                
                # Handle file upload
                image_file = None
                if 'report_image' in request.files:
                    file = request.files['report_image']
                    if file and file.filename and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        # Add timestamp to avoid filename conflicts
                        import time
                        timestamp = int(time.time())
                        filename = f"report_{timestamp}_{filename}"
                        file.save(os.path.join(UPLOAD_FOLDER, filename))
                        image_file = filename
                    elif file and file.filename:
                        flash('Invalid file type. Please use PNG, JPG, JPEG, GIF, or WebP.', 'danger')
                        return redirect(url_for('feedback'))
                
                new_report = ProjectReport(
                    project_id=project_id,
                    reporter_name=reporter_name,
                    reporter_email=reporter_email,
                    report_subject=report_subject,
                    report_message=report_message,
                    report_type=report_type,
                    report_image=image_file
                )
                db.session.add(new_report)
                db.session.commit()
                
                # Sync to JSON
                sync_to_json()
                
                flash('Thank you — your project report has been submitted.', 'success')
                return redirect(url_for('project_detail', pid=project_id))
            except (ValueError, Exception) as e:
                db.session.rollback()
                flash('Error submitting report. Please try again.', 'danger')
                return redirect(url_for('feedback'))
        else:
            # Handle general feedback
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            message = request.form.get('message', '').strip()
            if not message:
                flash('Please enter a message', 'danger')
                return redirect(url_for('feedback'))
            
            new_feedback = Feedback(name=name, email=email, message=message)
            db.session.add(new_feedback)
            db.session.commit()
            
            # Sync to JSON
            sync_to_json()
            
            flash('Thank you — your feedback has been submitted.', 'success')
        
        return redirect(url_for('feedback'))
    
    # Get projects for report dropdown
    projects_list = Project.query.order_by(Project.project_name).all()
    
    # Get recent feedback
    recent = Feedback.query.order_by(Feedback.created_at.desc()).limit(10).all()
    
    return render_template('feedback.html', recent=recent, projects=projects_list)

# About
@app.route('/about')
def about():
    return render_template('about.html')

# Contact
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        if not email or not message:
            flash('Please enter your email and message', 'danger')
            return redirect(url_for('contact'))
        # In production, send email here
        flash('Thank you for contacting us. We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

# Mark report as resolved
@login_required
@app.route('/admin/resolve-report/<int:report_id>', methods=['POST'])
def resolve_report(report_id):
    try:
        report = ProjectReport.query.filter_by(report_id=report_id).first()
        if report:
            report.is_resolved = True
            db.session.commit()
            
            # Sync to JSON
            sync_to_json()
            
            flash('Report marked as resolved.', 'success')
        else:
            flash('Report not found.', 'danger')
    except Exception as e:
        db.session.rollback()
        flash('Error updating report.', 'danger')
    return redirect(url_for('admin'))

# Simple admin to add projects (demo only — protect in production)
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        action = request.form.get('action', 'add_project')
        
        if action == 'add_project':
            try:
                name = request.form.get('name','').strip()
                sector_name = request.form.get('project_sector','').strip()
                desc = request.form.get('description','').strip()
                allocated = float(request.form.get('allocated_budget') or 0)
                spent = float(request.form.get('spent') or 0)
                status = request.form.get('status') or 'Planned'
                region_name = request.form.get('region','').strip()
                
                # Handle image upload
                project_image = None
                if 'project_image' in request.files:
                    file = request.files['project_image']
                    if file and file.filename and allowed_file(file.filename):
                        # Ensure upload directory exists
                        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                        filename = secure_filename(file.filename)
                        # Add timestamp to avoid duplicates
                        import time
                        filename = f"{int(time.time())}_{filename}"
                        file.save(os.path.join(UPLOAD_FOLDER, filename))
                        project_image = f"images/projects/{filename}"
                
                new_project = Project(
                    project_name=name,
                    sector_name=sector_name,
                    project_description=desc,
                    allocated_budget=allocated,
                    budget_spent=spent,
                    project_status=status,
                    region_name=region_name,
                    project_image=project_image
                )
                db.session.add(new_project)
                db.session.commit()
                flash('Project added.', 'success')
            except Exception as e:
                db.session.rollback()
                flash('Error adding project.', 'danger')
        
        return redirect(url_for('admin'))
    
    try:
        # Get projects
        projects = Project.query.order_by(Project.project_id.desc()).limit(50).all()
        
        # Add unresolved report count to each project
        projects_with_reports = []
        for project in projects:
            unresolved_count = ProjectReport.query.filter_by(
                project_id=project.project_id,
                is_resolved=False
            ).count()
            
            project_dict = {
                'id': project.project_id,
                'name': project.project_name,
                'project_sector': project.sector_name or '',
                'description': project.project_description,
                'allocated_budget': project.allocated_budget,
                'spent': project.budget_spent,
                'status': project.project_status,
                'region': project.region_name or '',
                'project_image': project.project_image or '',
                'unresolved_reports': unresolved_count
            }
            projects_with_reports.append(project_dict)
        
        # Get all unresolved reports with project info
        unresolved_reports = ProjectReport.query.filter_by(is_resolved=False).order_by(ProjectReport.created_at.desc()).all()
        
        # Convert reports to dictionaries with project names
        reports_with_project_names = []
        for report in unresolved_reports:
            project = Project.query.get(report.project_id)
            report_dict = {
                'id': report.report_id,
                'project_id': report.project_id,
                'project_name': project.project_name if project else 'Unknown Project',
                'reporter_name': report.reporter_name,
                'reporter_email': report.reporter_email,
                'report_subject': report.report_subject,
                'report_message': report.report_message,
                'report_type': report.report_type or 'General',
                'report_image': report.report_image,
                'is_resolved': report.is_resolved,
                'created_at': report.created_at.strftime('%Y-%m-%d %H:%M') if report.created_at else ''
            }
            reports_with_project_names.append(report_dict)
        
        # Hardcoded infrastructure departments
        departments = SECTORS_LIST
        
        # Use hardcoded regions
        regions = REGIONS_LIST
    except Exception as e:
        projects_with_reports = []
        reports_with_project_names = []
        departments = []
        regions = []
        print(f"Admin query error: {e}")
    
    return render_template('admin.html', projects=projects_with_reports, unresolved_reports=reports_with_project_names, departments=departments, regions=regions)

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Warning: Could not create tables: {e}")
    
    app.run(host='127.0.0.1', port=5000, debug=True)
