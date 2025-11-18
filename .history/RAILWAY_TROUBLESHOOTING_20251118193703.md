# Railway Deployment Troubleshooting

## 🔴 "Application failed to respond" Error

Your deployment has been fixed! Here's what was wrong and what I changed:

### Issues Fixed:

1. **Missing PORT Binding** ❌ → ✅
   - Railway provides a dynamic `PORT` environment variable
   - App was trying to run on default port 5000
   - **Fixed**: Now reads `PORT` from environment and binds to `0.0.0.0:PORT`

2. **Host Binding** ❌ → ✅
   - App was binding to localhost only (`127.0.0.1`)
   - Railway needs app to bind to all interfaces (`0.0.0.0`)
   - **Fixed**: Changed to `host='0.0.0.0'`

3. **Database Initialization Errors** ❌ → ✅
   - Database tables might fail to create on first deploy
   - App would crash instead of continuing
   - **Fixed**: Added try-except to handle gracefully

4. **Added Health Check Endpoint** ✅
   - `/health` endpoint for Railway to verify app is running
   - Tests database connection
   - Returns `200 OK` if healthy, `503` if database fails

---

## 📋 What You Need to Check on Railway

Go to https://railway.app and follow these steps:

### Step 1: Verify Environment Variables
1. Click your **GovFunds** project
2. Click the **app service** (not PostgreSQL)
3. Click **Variables** tab
4. Verify you have:
   - `FLASK_ENV` = `production`
   - `DB_USER` = `postgres`
   - `DB_PASSWORD` = [your password]
   - `DB_HOST` = [your host]
   - `DB_PORT` = `5432`
   - `DB_NAME` = `railway` (or whatever your database name is)
   - `SECRET_KEY` = [a strong random string]

❌ **If `DB_HOST` or `DB_PASSWORD` are missing**: Copy them from the PostgreSQL service:
- Click PostgreSQL service
- Go to Variables
- Find `PGHOST` → copy to `DB_HOST`
- Find `PGPASSWORD` → copy to `DB_PASSWORD`
- Find `PGPORT` → copy to `DB_PORT`

### Step 2: Check the Database Service
1. Click **PostgreSQL** service in your project
2. Verify it's in **Running** state (green)
3. Check the connection string is correct

### Step 3: Review Deployment Logs
1. Click your **app service**
2. Click **Deployments** tab
3. Click the latest deployment
4. Scroll through **Build Logs** and **Runtime Logs**
5. Look for:
   - ✅ `* Running on http://0.0.0.0:PORT`
   - ✅ `Successfully connected to PostgreSQL`
   - ❌ Any red error messages

### Step 4: Test the Health Endpoint
1. Copy your Railway app URL (e.g., `https://govfunds-production.railway.app`)
2. Visit: `https://govfunds-production.railway.app/health`
3. Expected response:
   ```json
   {"status": "healthy", "database": "connected"}
   ```
4. If you see this → Database connection is working! ✅

---

## 🔍 Common Issues & Solutions

### Issue: "connect: connection refused"
**Cause**: App can't connect to PostgreSQL
**Solution**:
1. Verify `DB_HOST`, `DB_PASSWORD` are correct
2. Check PostgreSQL service is running
3. Try redeploying: Click Redeploy in Railway

### Issue: "database does not exist"
**Cause**: Database name mismatch
**Solution**:
1. Check `DB_NAME` environment variable
2. If it's wrong, update it to match PostgreSQL
3. Redeploy

### Issue: "Address already in use"
**Cause**: Port conflict (shouldn't happen on Railway)
**Solution**:
1. Delete current deployment
2. Redeploy from Railway dashboard

### Issue: App starts but shows "Internal Server Error"
**Cause**: Database table creation failed
**Solution**:
1. Check /health endpoint
2. Review runtime logs
3. May need to manually create tables (see below)

---

## 🛠️ Manual Database Setup (if needed)

If tables weren't created automatically, you can create them manually:

1. Connect to PostgreSQL on Railway using a client (pgAdmin, DBeaver, etc.)
2. Run these SQL commands:

```sql
-- User table
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,
    role VARCHAR(10) NOT NULL
);

-- Project table
CREATE TABLE project (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    description TEXT,
    allocated_budget FLOAT DEFAULT 0,
    spent FLOAT DEFAULT 0,
    status VARCHAR(20) DEFAULT 'Planned',
    region VARCHAR(50),
    start_date VARCHAR(50),
    end_date VARCHAR(50)
);

-- Feedback table
CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ProjectReport table
CREATE TABLE project_report (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES project(id) ON DELETE CASCADE,
    reporter_name VARCHAR(100),
    reporter_email VARCHAR(100),
    report_subject VARCHAR(200) NOT NULL,
    report_message TEXT NOT NULL,
    report_type VARCHAR(50) DEFAULT 'General',
    is_resolved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- RegionBudget table
CREATE TABLE region_budget (
    id SERIAL PRIMARY KEY,
    region VARCHAR(100) NOT NULL,
    year INTEGER NOT NULL,
    budget FLOAT NOT NULL,
    UNIQUE(region, year)
);

-- DepartmentBudget table
CREATE TABLE department_budget (
    id SERIAL PRIMARY KEY,
    department VARCHAR(100) NOT NULL,
    year INTEGER NOT NULL,
    budget FLOAT NOT NULL
);

-- AnnualBudget table
CREATE TABLE annual_budget (
    id SERIAL PRIMARY KEY,
    year INTEGER UNIQUE NOT NULL,
    total_budget FLOAT NOT NULL
);
```

---

## ✅ Next Steps

1. **Wait for Railway to redeploy** (triggered by your git push)
   - Check Deployments tab for status
   - Usually takes 2-3 minutes

2. **Test the app**:
   - Visit your Railway app URL
   - Check `/health` endpoint
   - Try logging in with `admin` / `admin123`

3. **Monitor logs**:
   - Keep Railway dashboard open
   - Watch for any new errors

4. **If still failing**:
   - Take a screenshot of the error logs
   - Check environment variables
   - Try clearing Railway cache (Redeploy button)

---

## 📞 Getting Help

- **Railway Support**: https://docs.railway.app
- **Check your email** for Railway support contact info
- **GitHub Issues**: Document what you tried in a repo issue

---

**The fixes have been pushed! Railway should now redeploy automatically. Check your app in 2-3 minutes! 🚀**
