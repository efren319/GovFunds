# app.py
from flask import Flask, render_template, g, request, redirect, url_for, jsonify, flash
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'govfunds.db')
DATABASE = "govfunds.db"

app = Flask(__name__)
app.secret_key = 'replace-with-a-secure-key'  # change in production

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # <-- this is important
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Home
@app.route('/')
def home():
    db = get_db()
    cur = db.execute("SELECT COUNT(*) as cnt, SUM(allocated_budget) as total_alloc, SUM(spent) as total_spent FROM projects")
    stats = cur.fetchone()
    projects_count = stats['cnt'] or 0
    total_alloc = stats['total_alloc'] or 0
    total_spent = stats['total_spent'] or 0
    
    # Get recent feedback for carousel
    feedback_cur = db.execute("SELECT name, message, created_at FROM feedback ORDER BY created_at DESC LIMIT 20")
    recent_feedback = feedback_cur.fetchall()
    
    return render_template('home.html',
                           projects_count=projects_count,
                           total_alloc=total_alloc,
                           total_spent=total_spent,
                           recent_feedback=recent_feedback)

@app.route('/budget')
def budget():
    db = get_db()
    projects = db.execute("SELECT * FROM projects").fetchall()

    # Get selected year from query parameter (default to 2025)
    selected_year = request.args.get('year', 2025, type=int)

    # Annual budgets data
    annual_budgets = {
        2023: 5268000000000,
        2024: 5768000000000,
        2025: 6326000000000
    }

    # Get department budget data from database for selected year
    department_budgets = db.execute(
        "SELECT department, budget FROM department_budgets WHERE year = ? ORDER BY budget DESC",
        (selected_year,)
    ).fetchall()

    dept_labels = [d['department'] for d in department_budgets]
    dept_data = [d['budget'] for d in department_budgets]

    # Get regional budget data from database for selected year
    regional_budgets = db.execute(
        "SELECT region, budget FROM region_budgets WHERE year = ? ORDER BY region",
        (selected_year,)
    ).fetchall()

    region_labels = [r['region'] for r in regional_budgets]
    region_data = [r['budget'] for r in regional_budgets]

    # Get available years
    available_years = db.execute(
        "SELECT DISTINCT year FROM region_budgets ORDER BY year DESC"
    ).fetchall()
    years = [row['year'] for row in available_years]

    print("Department Labels:", dept_labels)
    print("Department Data:", dept_data)
    print("Region Labels:", region_labels)
    print("Region Data:", region_data)
    print("Selected Year:", selected_year)

    return render_template(
        'budget.html',
        projects=projects,
        dept_labels=dept_labels,
        dept_data=dept_data,
        region_labels=region_labels,
        region_data=region_data,
        selected_year=selected_year,
        available_years=years,
        annual_budget=annual_budgets.get(selected_year, 0),
        department_budgets_list=department_budgets
    )


# API endpoint for budget data (used by Chart.js)
@app.route('/api/budget_data')
def budget_data():
    db = get_db()
    cur = db.execute("SELECT department, SUM(allocated_budget) as allocated, SUM(spent) as spent FROM projects GROUP BY department")
    rows = [dict(r) for r in cur.fetchall()]
    return jsonify(rows)

# Projects listing
@app.route('/projects')
def projects():
    db = get_db()
    cur = db.execute("SELECT * FROM projects ORDER BY id DESC")
    projects = cur.fetchall()
    return render_template('projects.html', projects=projects)

# Project detail
@app.route('/project/<int:pid>')
def project_detail(pid):
    db = get_db()
    cur = db.execute("SELECT * FROM projects WHERE id = ?", (pid,))
    project = cur.fetchone()
    if not project:
        flash('Project not found', 'warning')
        return redirect(url_for('projects'))
    
    # Get reports for this project
    reports_cur = db.execute("SELECT * FROM project_reports WHERE project_id = ? ORDER BY created_at DESC", (pid,))
    reports = reports_cur.fetchall()
    
    return render_template('project_details.html', project=project, reports=reports)

# Feedback form
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    db = get_db()
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
                db.execute(
                    "INSERT INTO project_reports (project_id, reporter_name, reporter_email, report_subject, report_message, report_type) VALUES (?,?,?,?,?,?)",
                    (project_id, reporter_name, reporter_email, report_subject, report_message, report_type)
                )
                db.commit()
                flash('Thank you — your project report has been submitted.', 'success')
                # Redirect back to the project page instead of feedback
                return redirect(url_for('project_detail', pid=project_id))
            except (ValueError, Exception) as e:
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
            db.execute("INSERT INTO feedback (name,email,message) VALUES (?,?,?)", (name, email, message))
            db.commit()
            flash('Thank you — your feedback has been submitted.', 'success')
        
        return redirect(url_for('feedback'))
    
    # Get projects for report dropdown
    projects_cur = db.execute("SELECT id, name, department FROM projects ORDER BY name")
    projects = projects_cur.fetchall()
    
    # Get recent feedback
    cur = db.execute("SELECT * FROM feedback ORDER BY created_at DESC LIMIT 10")
    recent = cur.fetchall()
    
    return render_template('feedback.html', recent=recent, projects=projects)

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
@app.route('/admin/resolve-report/<int:report_id>', methods=['POST'])
def resolve_report(report_id):
    db = get_db()
    db.execute("UPDATE project_reports SET is_resolved = 1 WHERE id = ?", (report_id,))
    db.commit()
    flash('Report marked as resolved.', 'success')
    return redirect(url_for('admin'))

# Simple admin to add projects (demo only — protect in production)
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    db = get_db()
    if request.method == 'POST':
        action = request.form.get('action', 'add_project')
        
        if action == 'add_project':
            name = request.form.get('name','').strip()
            dept = request.form.get('department','').strip()
            desc = request.form.get('description','').strip()
            allocated = float(request.form.get('allocated_budget') or 0)
            spent = float(request.form.get('spent') or 0)
            status = request.form.get('status') or 'Planned'
            region = request.form.get('region','').strip()
            db.execute(
                "INSERT INTO projects (name, department, description, allocated_budget, spent, status, region) VALUES (?,?,?,?,?,?,?)",
                (name, dept, desc, allocated, spent, status, region)
            )
            db.commit()
            flash('Project added.', 'success')
        
        return redirect(url_for('admin'))
    
    try:
        # Get projects with unresolved report counts
        cur = db.execute("""
            SELECT p.*, 
                   COUNT(CASE WHEN pr.is_resolved = 0 THEN 1 END) as unresolved_reports
            FROM projects p
            LEFT JOIN project_reports pr ON p.id = pr.project_id
            GROUP BY p.id
            ORDER BY p.id DESC 
            LIMIT 50
        """)
        projects_raw = cur.fetchall()
        # Convert sqlite3.Row to dict for easier template handling
        projects = [dict(p) for p in projects_raw]
        
        # Get all unresolved reports with project info
        reports_cur = db.execute("""
            SELECT pr.*, p.name as project_name
            FROM project_reports pr
            JOIN projects p ON pr.project_id = p.id
            WHERE pr.is_resolved = 0
            ORDER BY pr.created_at DESC
        """)
        unresolved_reports_raw = reports_cur.fetchall()
        unresolved_reports = [dict(r) for r in unresolved_reports_raw]
        
        # Get all departments from department_budgets table
        dept_cur = db.execute("SELECT DISTINCT department FROM department_budgets ORDER BY department")
        departments = [dict(d)['department'] for d in dept_cur.fetchall()]
        
        # Get all regions from region_budgets table
        region_cur = db.execute("SELECT DISTINCT region FROM region_budgets ORDER BY region")
        regions = [dict(r)['region'] for r in region_cur.fetchall()]
    except Exception as e:
        # Fallback if there's an issue with the query - get projects without report counts
        try:
            projects_list = db.execute("SELECT * FROM projects ORDER BY id DESC LIMIT 50").fetchall()
            # Convert to dict and add unresolved_reports field with default 0
            projects = []
            for p in projects_list:
                p_dict = dict(p)
                p_dict['unresolved_reports'] = 0
                projects.append(p_dict)
        except:
            projects = []
        
        unresolved_reports = []
        departments = []
        regions = []
        print(f"Admin query error: {e}")
    
    return render_template('admin.html', projects=projects, unresolved_reports=unresolved_reports, departments=departments, regions=regions)

if __name__ == '__main__':
    app.run(debug=True)
