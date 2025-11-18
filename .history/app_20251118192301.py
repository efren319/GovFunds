# app.py
from flask import Flask, render_template, g, request, redirect, url_for, jsonify, flash, session
from sqlalchemy import func  # type: ignore
import os
from functools import wraps
import hashlib
from dotenv import load_dotenv
from models import db, User, Project, Feedback, ProjectReport, RegionBudget, DepartmentBudget, AnnualBudget

# Load environment variables from .env file
load_dotenv()

# PostgreSQL Configuration from environment variables
# Default to localhost for development
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'govfunds')

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'sikreto ni aldred')  # Use env variable in production
app.config['SESSION_COOKIE_SECURE'] = os.getenv('FLASK_ENV') == 'production'
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
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Authentication decorator (for resolve-report)
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

# Admin credentials (in production, store in database with proper security)
ADMIN_CREDENTIALS = {
    'admin': hash_password('admin123'),  # Change this in production!
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
        total_spent = sum(p.spent for p in projects) if projects else 0
        
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

        # Get department budget data
        department_budgets = DepartmentBudget.query.filter_by(year=selected_year).order_by(DepartmentBudget.budget.desc()).all()
        dept_labels = [d.department for d in department_budgets]
        dept_data = [d.budget for d in department_budgets]

        # Get regional budget data
        regional_budgets = RegionBudget.query.filter_by(year=selected_year).order_by(RegionBudget.region).all()
        region_labels = [r.region for r in regional_budgets]
        region_data = [r.budget for r in regional_budgets]
        
        # Get annual budget
        annual_budget_row = AnnualBudget.query.filter_by(year=selected_year).first()
        annual_budget_obj = annual_budget_row.total_budget if annual_budget_row else 0

        # Convert department_budgets to dictionaries for JSON serialization
        department_budgets_list = [
            {'department': d.department, 'budget': d.budget, 'year': d.year}
            for d in department_budgets
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
            department_budgets_list=department_budgets_list
        )
    except Exception as e:
        print(f"Error in budget route: {e}")
        import traceback
        traceback.print_exc()
        return render_template('budget.html', projects=[], dept_labels=[], dept_data=[], region_labels=[], region_data=[], selected_year=2025, available_years=[], annual_budget=0, department_budgets_list=[])


# API endpoint for budget data (used by Chart.js)
@app.route('/api/budget_data')
def budget_data():
    try:
        result = db.session.query(
            Project.department,
            func.sum(Project.allocated_budget).label('allocated'),
            func.sum(Project.spent).label('spent')
        ).group_by(Project.department).all()
        
        rows = [{'department': row[0], 'allocated': row[1] or 0, 'spent': row[2] or 0} for row in result]
        return jsonify(rows)
    except Exception as e:
        print(f"Error in budget_data: {e}")
        return jsonify([])

# Projects listing
@app.route('/projects')
def projects():
    try:
        projects_list = Project.query.order_by(Project.id.desc()).all()
        return render_template('projects.html', projects=projects_list)
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
        
        # Get reports for this project
        reports = ProjectReport.query.filter_by(project_id=pid).order_by(ProjectReport.created_at.desc()).all()
        
        return render_template('project_details.html', project=project, reports=reports)
    except Exception as e:
        print(f"Error in project_detail: {e}")
        flash('Error loading project', 'danger')
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
                new_report = ProjectReport(
                    project_id=project_id,
                    reporter_name=reporter_name,
                    reporter_email=reporter_email,
                    report_subject=report_subject,
                    report_message=report_message,
                    report_type=report_type
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
    projects_list = Project.query.order_by(Project.name).all()
    
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
        report = ProjectReport.query.get(report_id)
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
                dept = request.form.get('department','').strip()
                desc = request.form.get('description','').strip()
                allocated = float(request.form.get('allocated_budget') or 0)
                spent = float(request.form.get('spent') or 0)
                status = request.form.get('status') or 'Planned'
                region = request.form.get('region','').strip()
                
                new_project = Project(
                    name=name,
                    department=dept,
                    description=desc,
                    allocated_budget=allocated,
                    spent=spent,
                    status=status,
                    region=region
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
        projects = Project.query.order_by(Project.id.desc()).limit(50).all()
        
        # Get all unresolved reports with project info
        unresolved_reports = ProjectReport.query.filter_by(is_resolved=False).order_by(ProjectReport.created_at.desc()).all()
        
        # Get all unique departments
        departments = db.session.query(DepartmentBudget.department).distinct().order_by(DepartmentBudget.department).all()
        departments = [d[0] for d in departments]
        
        # Get all unique regions
        regions = db.session.query(RegionBudget.region).distinct().order_by(RegionBudget.region).all()
        regions = [r[0] for r in regions]
    except Exception as e:
        projects = []
        unresolved_reports = []
        departments = []
        regions = []
        print(f"Admin query error: {e}")
    
    return render_template('admin.html', projects=projects, unresolved_reports=unresolved_reports, departments=departments, regions=regions)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)
