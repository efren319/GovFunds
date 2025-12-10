# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from sqlalchemy import func, text  # type: ignore
from functools import wraps
import hashlib
from models import db, User, UserRole, Project, Feedback, ProjectReport, RegionBudget, ProjectSectorBudget, AnnualBudget, Region, ProjectSector, ReportType

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

# Auto-seed database on startup if empty
def init_db_with_data():
    """Initialize database with sample data if empty"""
    with app.app_context():
        try:
            db.create_all()
            
            # Check if database is empty
            if Project.query.first() is None:
                print("Database is empty. Seeding with sample data...")
                from seed_data import seed_data
                seed_data()
        except Exception as e:
            print(f"Error during database initialization: {e}")

# Run initialization when app starts
init_db_with_data()

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

        # Get selected year from query parameter (default to 2025)
        selected_year = request.args.get('year', 2025, type=int)

        # Get ALL available years from database
        available_years_query = db.session.query(RegionBudget.year).distinct().order_by(RegionBudget.year.desc()).all()
        years = [row[0] for row in available_years_query] if available_years_query else [2025]
        
        # If selected year doesn't exist in available years, use the first available
        if years and selected_year not in years:
            selected_year = years[0]

        # Get project sector budget data with sector names
        sector_budgets = db.session.query(ProjectSectorBudget, ProjectSector).join(
            ProjectSector, ProjectSectorBudget.sector_id == ProjectSector.sector_id
        ).filter(ProjectSectorBudget.year == selected_year).order_by(ProjectSectorBudget.sector_budget.desc()).all()
        dept_labels = [s.sector_name for psb, s in sector_budgets]
        dept_data = [psb.sector_budget for psb, s in sector_budgets]

        # Get regional budget data with region names
        regional_budgets = db.session.query(RegionBudget, Region).join(
            Region, RegionBudget.region_id == Region.region_id
        ).filter(RegionBudget.year == selected_year).order_by(Region.region_name).all()
        region_labels = [r.region_name for rb, r in regional_budgets]
        region_data = [rb.region_budget for rb, r in regional_budgets]
        
        # Get annual budget
        annual_budget_row = AnnualBudget.query.filter_by(year=selected_year).first()
        annual_budget_obj = annual_budget_row.total_budget if annual_budget_row else 0

        # Convert sector_budgets to dictionaries for JSON serialization
        sector_budgets_list = [
            {'sector': s.sector_name, 'budget': psb.sector_budget, 'year': psb.year}
            for psb, s in sector_budgets
        ]

        return render_template(
            'budget.html',
            projects=projects,
            dept_labels=dept_labels,
            dept_data=dept_data,
            region_labels=region_labels,
            region_data=region_data,
            selected_year=selected_year,
            available_years=years,
            annual_budget=annual_budget_obj,
            sector_budgets_list=sector_budgets_list
        )
    except Exception as e:
        print(f"Error in budget route: {e}")
        import traceback
        traceback.print_exc()
        return render_template('budget.html', projects=[], dept_labels=[], dept_data=[], region_labels=[], region_data=[], selected_year=2025, available_years=[], annual_budget=0, sector_budgets_list=[])


# API endpoint for budget data (used by Chart.js)
@app.route('/api/budget_data')
def budget_data():
    try:
        result = db.session.query(
            ProjectSector.sector_name,
            func.sum(Project.allocated_budget).label('allocated'),
            func.sum(Project.budget_spent).label('spent')
        ).join(ProjectSector, Project.sector_id == ProjectSector.sector_id
        ).group_by(ProjectSector.sector_name).all()

        rows = [{'sector': row[0], 'allocated': row[1] or 0, 'spent': row[2] or 0} for row in result]
        return jsonify(rows)
    except Exception as e:
        print(f"Error in budget_data: {e}")
        return jsonify([])

# Projects listing
@app.route('/projects')
def projects():
    try:
        projects_list = Project.query.order_by(Project.project_id.desc()).all()
        # Get all regions for the modal
        regions = Region.query.order_by(Region.region_name).all()
        regions = [r.region_name for r in regions]
        return render_template('projects.html', projects=projects_list, regions_list=regions)
    except Exception as e:
        print(f"Error in projects route: {e}")
        return render_template('projects.html', projects=[])

# Project detail
@app.route('/project/<int:pid>')
def project_detail(pid):
    try:
        project = Project.query.get(pid)
        if not project:
            flash('Project not found', 'warning')
            return redirect(url_for('projects'))
        
        # Get reports for this project with report type names
        reports = db.session.query(ProjectReport, ReportType).outerjoin(
            ReportType, ProjectReport.report_type_id == ReportType.report_type_id
        ).filter(ProjectReport.project_id == pid).order_by(ProjectReport.created_at.desc()).all()
        
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
        
        # Get sector and region names
        sector_name = project.sector.sector_name if project.sector else ''
        region_name = project.region.region_name if project.region else ''
        
        return jsonify({
            'id': project.project_id,
            'name': project.project_name,
            'project_sector': sector_name,
            'sector_id': project.sector_id,
            'region': region_name,
            'region_id': project.region_id,
            'status': project.project_status,
            'allocated_budget': project.allocated_budget or 0,
            'spent': project.budget_spent or 0,
            'description': project.project_description or ''
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
            
            # Handle sector - look up or create
            sector_name = request.form.get('project_sector', '').strip()
            if sector_name:
                sector = ProjectSector.query.filter_by(sector_name=sector_name).first()
                if sector:
                    project.sector_id = sector.sector_id
            
            # Handle region - look up or create
            region_name = request.form.get('region', '').strip()
            if region_name:
                region = Region.query.filter_by(region_name=region_name).first()
                if region:
                    project.region_id = region.region_id
            
            project.project_status = request.form.get('status', 'Planned')
            project.allocated_budget = float(request.form.get('allocated_budget') or 0)
            project.budget_spent = float(request.form.get('spent') or 0)
            project.project_description = request.form.get('description', '').strip()
            
            db.session.commit()
            flash('Project updated successfully', 'success')
            return redirect(url_for('project_detail', pid=pid))
        
        return redirect(url_for('projects'))
    except Exception as e:
        db.session.rollback()
        print(f"Error in edit_project: {e}")
        flash('Error updating project', 'danger')
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
                
                # Look up report type
                report_type_obj = ReportType.query.filter_by(type_name=report_type).first()
                report_type_id = report_type_obj.report_type_id if report_type_obj else None
                
                new_report = ProjectReport(
                    project_id=project_id,
                    reporter_name=reporter_name,
                    reporter_email=reporter_email,
                    report_subject=report_subject,
                    report_message=report_message,
                    report_type_id=report_type_id
                )
                db.session.add(new_report)
                db.session.commit()
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
                
                # Look up sector_id
                sector = ProjectSector.query.filter_by(sector_name=sector_name).first()
                sector_id = sector.sector_id if sector else None
                
                # Look up region_id
                region = Region.query.filter_by(region_name=region_name).first()
                region_id = region.region_id if region else None
                
                new_project = Project(
                    project_name=name,
                    sector_id=sector_id,
                    project_description=desc,
                    allocated_budget=allocated,
                    budget_spent=spent,
                    project_status=status,
                    region_id=region_id
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
            
            # Get sector and region names
            sector_name = project.sector.sector_name if project.sector else ''
            region_name = project.region.region_name if project.region else ''
            
            project_dict = {
                'id': project.project_id,
                'name': project.project_name,
                'project_sector': sector_name,
                'description': project.project_description,
                'allocated_budget': project.allocated_budget,
                'spent': project.budget_spent,
                'status': project.project_status,
                'region': region_name,
                'unresolved_reports': unresolved_count
            }
            projects_with_reports.append(project_dict)
        
        # Get all unresolved reports with project info
        unresolved_reports = ProjectReport.query.filter_by(is_resolved=False).order_by(ProjectReport.created_at.desc()).all()
        
        # Convert reports to dictionaries with project names
        reports_with_project_names = []
        for report in unresolved_reports:
            project = Project.query.get(report.project_id)
            report_type_name = report.report_type.type_name if report.report_type else 'General'
            report_dict = {
                'id': report.report_id,
                'project_id': report.project_id,
                'project_name': project.project_name if project else 'Unknown Project',
                'reporter_name': report.reporter_name,
                'reporter_email': report.reporter_email,
                'report_subject': report.report_subject,
                'report_message': report.report_message,
                'report_type': report_type_name,
                'is_resolved': report.is_resolved,
                'created_at': report.created_at.strftime('%Y-%m-%d %H:%M') if report.created_at else ''
            }
            reports_with_project_names.append(report_dict)
        
        # Hardcoded infrastructure departments
        departments = [
            'Road Infrastructure',
            'Bridge Infrastructure',
            'Flood Control and Drainage',
            'Public Buildings',
            'Water Resources and Irrigation',
            'Special Infrastructure Projects',
            'Disaster Response and Rehabilitation',
            'Local Infrastructure Support'
        ]
        
        # Get all unique regions
        regions = Region.query.order_by(Region.region_name).all()
        regions = [r.region_name for r in regions]
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
