# PostgreSQL Setup Guide for GovFunds Application

## Prerequisites

- PostgreSQL database server installed and running
- Python 3.7+
- Virtual environment activated

## Installation Steps

### 1. Install Required Packages

```bash
pip install -r requirements.txt
```

The `requirements.txt` file includes:
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- psycopg2-binary (PostgreSQL driver)
- python-dotenv (for environment variables)

### 2. Configure Database Connection

Edit the `.env` file with your PostgreSQL credentials:

```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=govfunds
```

### 3. Create PostgreSQL Database

Using psql or PgAdmin:

```sql
CREATE DATABASE govfunds;
```

### 4. Initialize Database Tables

The application will automatically create tables when you run it:

```bash
python app.py
```

The `db.create_all()` function in `app.py` creates all necessary tables on startup.

### 5. Load Sample Data (Optional)

To populate the database with sample data, run the SQL statements from `insert_data.sql`:

```bash
psql -U postgres -d govfunds -f insert_data.sql
```

Or in PgAdmin, open `insert_data.sql` and execute it.

## Running the Application

```bash
python app.py
```

The Flask development server will start at `http://127.0.0.1:5000`

## Default Credentials

- Username: `admin`
- Password: `admin123`

OR

- Username: `staff`
- Password: `staff123`

## Database Models

The application uses the following SQLAlchemy models:

- **User** - Admin users
- **Project** - Government projects
- **Feedback** - Public feedback
- **ProjectReport** - Project-specific reports/complaints
- **RegionBudget** - Regional budget allocations
- **DepartmentBudget** - Department budget allocations
- **AnnualBudget** - Total annual budget allocations

## Environment Variables

The `.env` file should contain:

```env
DB_USER=<postgres_username>
DB_PASSWORD=<postgres_password>
DB_HOST=<database_host>
DB_PORT=<database_port>
DB_NAME=<database_name>
```

## Migration from SQLite

If you were previously using SQLite:

1. All SQLite-specific code has been removed
2. The application now uses PostgreSQL via SQLAlchemy ORM
3. No manual migration needed - just ensure PostgreSQL is configured and the database exists

## Troubleshooting

### Connection Error
- Ensure PostgreSQL server is running
- Verify credentials in `.env` file
- Check that the database exists

### Import Error (psycopg2)
```bash
pip install psycopg2-binary
```

### Import Error (dotenv)
```bash
pip install python-dotenv
```

## Security Notes

⚠️ For production deployment:
- Store database credentials securely (use environment variables)
- Change the secret key in `app.secret_key`
- Enable HTTPS (set `SESSION_COOKIE_SECURE = True`)
- Use a production WSGI server (gunicorn, uWSGI, etc.)
- Use strong passwords for database users
