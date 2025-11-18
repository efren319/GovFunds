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
    return render_template('home.html',
                           projects_count=projects_count,
                           total_alloc=total_alloc,
                           total_spent=total_spent)

@app.route('/budget')
def budget():
    db = get_db()
    projects = db.execute("SELECT * FROM projects ORDER BY id DESC").fetchall()

    # Map projects to regions (example mapping)
    region_map = {
        "Ilocos Region": ["Ilocos Norte", "Ilocos Sur", "La Union", "Pangasinan"],
        "Cagayan Valley": ["Batanes", "Cagayan", "Isabela", "Nueva Vizcaya", "Quirino"],
        "Central Luzon": ["Aurora","Bataan","Bulacan","Nueva Ecija","Pampanga","Tarlac","Zambales"],
        # Add remaining regions here...
        "NCR": ["Manila","Quezon City","Makati","Pasig","Taguig"]
    }

    # Aggregate budget per region
    region_labels = []
    region_data = []
    for region, provinces in region_map.items():
        total = sum(p['allocated_budget'] for p in projects if p['department'] in provinces)
        region_labels.append(region)
        region_data.append(total)

    return render_template(
        'budget.html',
        projects=projects,
        region_labels=region_labels,
        region_data=region_data
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
    return render_template('project_detail.html', project=project)

# Feedback form
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    db = get_db()
    if request.method == 'POST':
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
    cur = db.execute("SELECT * FROM feedback ORDER BY created_at DESC LIMIT 10")
    recent = cur.fetchall()
    return render_template('feedback.html', recent=recent)

# About
@app.route('/about')
def about():
    team = [
        {'name': 'Diola, Christan Micael V.', 'role': 'Frontend Developer / UI Designer'},
        {'name': 'Feliciano, Francine May L.', 'role': 'Content and Research Manager'},
        {'name': 'Mangurali, Efren C.', 'role': 'Backend Developer / Data Handler'},
        {'name': 'Olan, Aldred C.', 'role': 'Project Coordinator / System Analyst'}
    ]
    return render_template('about.html', team=team)

# Simple admin to add projects (demo only — protect in production)
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    db = get_db()
    if request.method == 'POST':
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
    cur = db.execute("SELECT * FROM projects ORDER BY id DESC LIMIT 50")
    projects = cur.fetchall()
    return render_template('admin.html', projects=projects)

if __name__ == '__main__':
    app.run(debug=True)
