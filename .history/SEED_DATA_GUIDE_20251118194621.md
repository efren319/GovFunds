# How to Populate Data on Railway

The sample data has been successfully inserted locally! Now you have two options to get data into Railway:

## Option 1: Using Railway's Shell/CLI (Recommended)

1. Go to https://railway.app
2. Click your **GovFunds** project
3. Click the **app service**
4. Click the **Shell** or **Terminal** tab
5. Run this command:
   ```bash
   python seed_data.py
   ```
6. Wait for it to complete - you should see:
   ```
   ✅ All sample data inserted successfully!
   ```

## Option 2: Using pgAdmin (Database GUI)

If Railway doesn't have a shell tab, you can use pgAdmin:

1. Go to https://pgadmin.railway.app
2. Connect to your Railway PostgreSQL database
3. Copy the SQL commands from `sample_data.txt`
4. Paste and execute in pgAdmin

## Option 3: Python Script (CLI)

Connect to Railway using SSH and run:
```bash
cd /app
python -m pip install -r requirements.txt
python seed_data.py
```

---

## What Gets Inserted

The `seed_data.py` script inserts:

- **4 Sample Projects**
  - Road Rehabilitation
  - School Building Construction
  - Health Center Upgrade
  - Irrigation System Project

- **2 Sample Feedback entries** from citizens

- **51 Regional Budget entries** (2023, 2024, 2025)
  - All 17 regions with budget allocations

- **59 Department Budget entries** (2023, 2024, 2025)
  - All government departments

- **3 Annual Budget entries**
  - Total budgets for 2023, 2024, 2025

---

## Testing Locally First

You already ran `python seed_data.py` locally and it worked! ✅

The data is in your local database. To verify it works with your local app:

1. Start your app: `python app.py`
2. Visit http://localhost:5000
3. Click on **Projects** - should see 4 sample projects
4. Click on **Budget** - should see regional and department budgets
5. Click on **Feedback** - should see 2 sample feedback entries

---

## Verifying Data on Railway

After running `seed_data.py` on Railway, check:

1. **Home Page** - Shows project count, total allocated, total spent
2. **Projects Page** - Lists all 4 sample projects
3. **Budget Page** - Shows interactive charts with budget data
4. **Feedback Page** - Shows recent feedback from citizens

---

## Clearing Data (if needed)

If you want to clear all data and start fresh:

1. In Railway shell, run:
   ```bash
   python
   ```
2. Then:
   ```python
   from app import app, db
   with app.app_context():
       db.drop_all()
       db.create_all()
   exit()
   ```
3. Then run `python seed_data.py` again

---

## Adding More Data

To add more projects/data through the web interface:

1. Log in to Admin: `/login`
2. Use credentials:
   - Username: `admin`
   - Password: `admin123`
3. Go to `/admin`
4. Add new projects using the form

---

**Ready to populate Railway? Go to your Railway dashboard and run the seed script!** 🚀
