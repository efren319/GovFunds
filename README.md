# GovFunds - Government Project Budget Tracker

A Flask-based web application for tracking government projects, budgets, and regional allocations with citizen feedback capabilities.

## Features

- 📊 Dashboard with project overview and statistics
- 💰 Budget tracking by department and region
- 📋 Project management and details
- 📝 Citizen feedback and project reporting system
- 🔐 Admin panel for project management
- 📈 Interactive charts and visualizations

## Tech Stack

- **Backend**: Flask 2.3.3
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Railway

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip

## Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/govfunds.git
   cd govfunds
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

   The app will be available at `http://localhost:5000`

## Deployment to Railway

### Prerequisites
- Railway account (https://railway.app)
- GitHub repository with your code

### Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Connect Railway to GitHub**
   - Go to https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub"
   - Authorize and select your repository

3. **Set Environment Variables on Railway**
   - Go to your project settings
   - Add the following variables:
     - `DB_USER`: Your PostgreSQL username
     - `DB_PASSWORD`: Your PostgreSQL password
     - `DB_HOST`: Your PostgreSQL host
     - `DB_PORT`: 5432
     - `DB_NAME`: govfunds
     - `SECRET_KEY`: A secure random string

4. **Add PostgreSQL Database**
   - In your Railway project, click "Add"
   - Select "PostgreSQL"
   - The `DATABASE_URL` will be set automatically

5. **Deploy**
   - Railway will automatically deploy when you push to GitHub
   - Monitor deployment in the Railway dashboard

## Project Structure

```
├── app.py                 # Main Flask application
├── models.py             # Database models
├── requirements.txt      # Python dependencies
├── Procfile             # Railway configuration
├── .env.example         # Example environment variables
├── static/
│   ├── style.css        # Main stylesheet
│   ├── script.js        # Frontend logic
│   ├── budget.js        # Budget visualization
│   ├── carousel.js      # Feedback carousel
│   └── images/          # Static images
└── templates/
    ├── base.html        # Base template
    ├── home.html        # Home page
    ├── projects.html    # Projects listing
    ├── project_details.html # Project details
    ├── budget.html      # Budget dashboard
    ├── feedback.html    # Feedback form
    ├── contact.html     # Contact form
    ├── about.html       # About page
    ├── admin.html       # Admin panel
    └── login.html       # Login page
```

## Admin Login

**Default Credentials** (change in production):
- Username: `admin`
- Password: `admin123`

Alternative:
- Username: `staff`
- Password: `staff123`

## Database Models

### Project
- id, name, department, description, allocated_budget, spent, status, region, start_date, end_date

### Feedback
- id, name, email, message, created_at

### ProjectReport
- id, project_id, reporter_name, reporter_email, report_subject, report_message, report_type, is_resolved, created_at

### RegionBudget
- id, region, year, budget

### DepartmentBudget
- id, department, year, budget

### AnnualBudget
- id, year, total_budget

## API Endpoints

### Public Routes
- `GET /` - Home page
- `GET /projects` - Projects listing
- `GET /project/<id>` - Project details
- `GET /budget` - Budget dashboard
- `GET /feedback` - Feedback page
- `POST /feedback` - Submit feedback
- `GET /contact` - Contact page
- `POST /contact` - Submit contact form
- `GET /about` - About page

### Admin Routes
- `GET /login` - Login page
- `POST /login` - Submit login
- `GET /logout` - Logout
- `GET /admin` - Admin dashboard
- `POST /admin` - Add project
- `POST /admin/resolve-report/<id>` - Mark report as resolved

### API Endpoints
- `GET /api/budget_data` - Budget data for charts

## Security Notes

⚠️ **Before deploying to production:**
1. Change the `SECRET_KEY` in `app.py`
2. Update `ADMIN_CREDENTIALS` - use a database with hashed passwords
3. Set `SESSION_COOKIE_SECURE = True` for HTTPS
4. Store credentials securely (never in code)
5. Use environment variables for all sensitive data
6. Implement proper input validation and SQL injection prevention
7. Add rate limiting for API endpoints
8. Enable HTTPS/SSL

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License

## Support

For issues and questions, please open an issue on GitHub.

---

**Built with ❤️ for government transparency and public accountability**
