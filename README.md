# GovFunds - Government Project Budget Tracker

A Flask-based web application for tracking government infrastructure projects, budgets, and citizen feedback with an admin dashboard for project management.

## Features

- 📊 Dashboard with project statistics and budget overview
- 💰 Budget tracking by department/sector and region
- 📋 Project listing with filtering and sorting
- 📈 Budget comparison visualizations with Chart.js
- 📝 Citizen feedback and project reporting system
- 🔐 Admin panel for project and report management
- 🖼️ Project image management with fallback sector-based defaults
- 📱 Responsive design with Bootstrap

## Tech Stack

- **Backend**: Flask 2.3.3, SQLAlchemy 2.0.44
- **Database**: PostgreSQL 12+
- **ORM**: Flask-SQLAlchemy 3.1.1
- **Frontend**: HTML5, CSS3, JavaScript (ES6)
- **Charts**: Chart.js
- **Package Manager**: pip

## Prerequisites

- Python 3.8+
- PostgreSQL 12+ (local installation)
- pip
- Git

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/efren319/GovFunds.git
cd GovFunds
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database

Update `app.py` with your PostgreSQL credentials (lines 20-24):

```python
DB_USER = 'postgres'
DB_PASSWORD = 'your_password'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'govfunds'
```

Alternatively, copy and edit `.env.example`:

```bash
cp .env.example .env
# Edit .env with your database credentials
```

### 5. Create PostgreSQL Database

```bash
createdb govfunds
```

### 6. Start the Application

```bash
python app.py
```

The app will automatically:
- Create database tables from models
- Check if database is empty
- Seed with sample data from `seed.sql`
- Export data to JSON files (`data/` folder)

Visit: `http://localhost:5000`

## Database Auto-Initialization

The application includes automatic database initialization in `app.py`:

- **On first run**: Creates tables, seeds 60 sample records (20 projects, 20 feedback, 20 reports)
- **On subsequent runs**: Verifies tables exist and skips seeding
- **Data sync**: Any changes (add/edit feedback/reports) automatically update JSON backups

## Project Structure

```
GovFunds/
├── app.py                    # Flask app + auto-init + data sync
├── models.py                 # SQLAlchemy models (Project, Feedback, ProjectReport)
├── reset_db.py              # Database reset utility
├── seed.sql                 # SQL insert statements for sample data
├── seed_backup.sql          # Backup copy of seed.sql with schema
├── schema.sql               # Database schema reference
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
├── README.md                # This file
├── data/                    # JSON exports (auto-generated)
│   ├── projects.json
│   ├── feedback.json
│   └── reports.json
├── static/                  # Assets
│   ├── style.css            # Main styles + responsive design
│   ├── script.js            # Carousel + general JS
│   ├── budget.js            # Budget page + Chart.js
│   ├── projects.js          # Projects filtering & sorting
│   ├── confirm.js           # Confirmation dialogs
│   └── images/
│       └── projects/        # Project images
└── templates/               # Jinja2 templates
    ├── base.html            # Base template + navigation
    ├── home.html            # Landing page with carousel
    ├── projects.html        # Projects listing with filters & sorts
    ├── project_details.html # Project detail view + reports
    ├── budget.html          # Budget dashboard with charts
    ├── feedback.html        # Feedback & report submission forms
    ├── contact.html         # Contact form
    ├── about.html           # About page
    ├── admin.html           # Admin dashboard + project/report tables
    └── login.html           # Admin login
```

## Key Features

### Projects Management
- View all 20 sample projects
- Filter by status (Planned/Ongoing/Completed), region, sector
- Sort by name, date, budget, spent amount, report count
- View project details with associated reports
- Admin: Add, edit, delete projects with image uploads

### Budget Dashboard
- Allocated vs. spent budget by sector
- Interactive Chart.js visualizations
- Real-time calculations from database

### Citizen Feedback
- General feedback submission
- Project-specific reports with images
- Admin reports tracking with resolution status

### Admin Features
- Login with credentials (admin/admin123 or staff/staff123)
- Add/edit/delete projects
- Manage project images with fallback defaults
- Track unresolved project reports
- Mark reports as resolved

## Database Models

### Project
- `project_id`: Primary key
- `project_name`: Title (required)
- `project_description`: Details
- `project_image`: Image path (null = use sector default)
- `allocated_budget`, `budget_spent`: Financial tracking
- `project_status`: Planned/Ongoing/Completed
- `region_name`, `sector_name`: Classification
- Relationships: Many reports per project

### Feedback
- `feedback_id`: Primary key
- `name`, `email`: User info
- `message`: Feedback text (required)
- `created_at`: Timestamp

### ProjectReport
- `report_id`: Primary key
- `project_id`: Foreign key to Project
- `reporter_name`, `reporter_email`: Submitter info
- `report_subject`, `report_message`: Report content
- `report_type`: General/Issue/Concern
- `report_image`: Optional image
- `is_resolved`: Status flag
- `created_at`: Timestamp

## API Endpoints

### Public Routes
- `GET /` – Home page with carousel
- `GET /projects` – Projects listing
- `GET /project/<id>` – Project details + reports
- `GET /budget` – Budget dashboard with charts
- `GET /feedback` – Feedback form
- `POST /feedback` – Submit feedback or project report
- `GET /contact` – Contact page
- `POST /contact` – Submit contact message
- `GET /about` – About page

### Admin Routes
- `GET /login` – Login page
- `POST /login` – Authenticate
- `GET /logout` – Clear session
- `GET /admin` – Dashboard (projects table + unresolved reports)
- `POST /admin` – Add project
- `POST /admin/resolve-report/<id>` – Mark report as resolved
- `POST /project/<id>/edit` – Update project
- `POST /project/<id>/delete` – Remove project

### API Endpoints
- `GET /api/budget_data` – JSON budget data for Chart.js
- `GET /api/project/<id>` – JSON project details (admin only)

## Admin Credentials

```
Username: admin    Password: admin123
Username: staff    Password: staff123
```

## Configuration

### Image Management
- Supported formats: PNG, JPG, JPEG, GIF, WebP
- Projects without images use sector-based defaults
- Report images are optional
- Uploads stored in `static/images/projects/`

### Responsive Design
- Mobile-first approach
- Tablet & desktop optimizations
- Scrollable data tables (admin)
- Touch-friendly buttons

### Sessions & Security
- Session cookies marked HttpOnly
- 24-hour session timeout
- Password hashing with SHA-256
- CSRF protection on forms

## Data Files

- `seed.sql` – 60 sample records (INSERT statements only)
- `seed_backup.sql` – Complete schema + data backup
- `schema.sql` – Schema reference
- `data/*.json` – Auto-exported from database

## Troubleshooting

### Database Connection Error
Check PostgreSQL is running and credentials in `app.py` are correct

### Port 5000 Already in Use
```bash
python app.py --port 5001
```

### Module Not Found
```bash
pip install -r requirements.txt
```

### Reset Database
```bash
python reset_db.py
```
Then restart the app to reseed.

## Development Notes

- Database initialization is automatic on app startup
- Models defined in `models.py`, routes in `app.py`
- No separate seed scripts needed—all in `app.py`
- JSON exports happen automatically on data changes
- Admin section scrollable for large datasets

## License

Open source project for government transparency

## Author

Created by efren319
