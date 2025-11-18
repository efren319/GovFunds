# GitHub & Railway Deployment Guide

## ✅ What's Ready for Deployment

Your GovFunds project has been prepared with:

1. **`.gitignore`** - Excludes unnecessary files from Git
2. **`Procfile`** - Railway configuration to run the app
3. **`.env.example`** - Template for environment variables
4. **`README.md`** - Complete project documentation
5. **`requirements.txt`** - Updated with `gunicorn` for production
6. **`app.py`** - Updated for production-ready deployment
7. **Initial Git commit** - All files committed locally

---

## 📤 Step 1: Create a GitHub Repository

1. Go to https://github.com/new
2. Create a new repository:
   - **Repository name**: `govfunds` (or your preferred name)
   - **Description**: "Government Project Budget Tracker with citizen feedback"
   - **Visibility**: Public (for Railway to access)
   - **DO NOT** initialize with README (we already have one)
3. Click "Create repository"

---

## 🔗 Step 2: Push Code to GitHub

Run these commands in PowerShell in your project directory:

```powershell
cd C:\Users\efren\Downloads\GovFunds

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/govfunds.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

---

## 🚀 Step 3: Deploy to Railway

### 3.1 Create Railway Account
1. Go to https://railway.app
2. Sign up with GitHub (click "Sign in with GitHub")
3. Authorize Railway to access your GitHub account

### 3.2 Create New Project
1. Click **"New Project"** button
2. Select **"Deploy from GitHub repo"**
3. Select **"Configure GitHub App"**
4. Authorize and select your `govfunds` repository

### 3.3 Add PostgreSQL Database
1. In your project dashboard, click **"Add Service"**
2. Select **"PostgreSQL"**
3. Railway will automatically create the database

### 3.4 Set Environment Variables
1. In Railway dashboard, click on your app service
2. Go to **Variables** tab
3. Add these variables:

```
FLASK_ENV = production
DB_USER = postgres
DB_PASSWORD = [Copy from PostgreSQL service]
DB_HOST = [Copy from PostgreSQL service]
DB_PORT = 5432
DB_NAME = railway
SECRET_KEY = [Generate a random secure string - e.g., use Python: python -c "import secrets; print(secrets.token_hex(32))"]
```

To get PostgreSQL credentials:
- Click on the PostgreSQL service in your project
- Go to the **Variables** tab
- Find: `PGUSER`, `PGPASSWORD`, `PGHOST`

### 3.5 Deploy
- Railway automatically deploys when you push to GitHub
- Monitor the build in the **Deployments** tab
- Your app URL will be shown when deployment is complete (e.g., `https://govfunds-production.railway.app`)

---

## 🔐 Important Security Notes for Railway

### Before Going Live:

1. **Change Admin Credentials** (in app.py)
   - Update the hardcoded `ADMIN_CREDENTIALS` dictionary
   - Better: Move to database with hashed passwords

2. **Update SECRET_KEY**
   - Generate a strong random key:
   ```powershell
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   - Set this as `SECRET_KEY` environment variable in Railway

3. **Database Backups**
   - Railway provides automatic backups
   - Check Railway dashboard for backup settings

4. **Monitor Logs**
   - Go to Railway dashboard → Your app → Logs
   - Monitor for errors and issues

---

## 📝 Local Testing Before Deployment

1. **Create local .env file**:
   ```
   cp .env.example .env
   ```

2. **Update .env** with your local PostgreSQL credentials

3. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

4. **Run locally**:
   ```powershell
   python app.py
   ```

5. **Test the app** at `http://localhost:5000`

---

## 🐛 Troubleshooting

### App won't deploy
- Check Railway Deployment logs for errors
- Verify all environment variables are set
- Ensure `Procfile` exists and is correct

### Database connection errors
- Verify `DB_*` environment variables match PostgreSQL service
- Check PostgreSQL service is running in Railway
- Test connection string format

### Admin login not working
- Clear session cookies (browser settings)
- Verify `SECRET_KEY` is set
- Check admin credentials in app.py

### Static files not loading
- Files should be in `static/` folder (already done)
- Flask serves static files automatically

---

## 📊 After Deployment

### First Steps:
1. Visit your app URL
2. Test all pages work (Home, Projects, Budget, Feedback, etc.)
3. Test admin login (`admin` / `admin123`)
4. Add sample projects from admin panel
5. Test feedback submission

### Ongoing Maintenance:
- Monitor logs regularly
- Keep dependencies updated (update requirements.txt)
- Make changes locally, commit to Git, push to GitHub
- Railway auto-deploys on push to main branch

---

## 🆘 Need Help?

- **Railway Docs**: https://docs.railway.app
- **Flask Docs**: https://flask.palletsprojects.com
- **PostgreSQL on Railway**: https://docs.railway.app/guides/databases

---

**You're all set! Your GovFunds app is ready for the world! 🚀**
