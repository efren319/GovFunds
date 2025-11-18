# Database Maintenance Guide

## 🛠️ Regular Maintenance Tasks

### 1. Backup Your Database

**On Railway:**
1. Go to https://railway.app
2. Click your **GovFunds** project
3. Click **PostgreSQL** service
4. Go to **Backups** tab
5. Railway automatically creates backups
6. You can manually trigger a backup anytime

**Manual Backup (using pg_dump):**
```bash
# Download PostgreSQL tools first, then run:
pg_dump -h [PGHOST] -U [PGUSER] -d [PGDATABASE] > backup.sql
# Enter password when prompted
```

---

### 2. Monitor Database Size

**Check database size:**
```sql
SELECT 
    datname as database,
    pg_size_pretty(pg_database_size(datname)) as size
FROM pg_database
ORDER BY pg_database_size(datname) DESC;
```

Run this in pgAdmin Query Tool to see how large your database is.

---

### 3. Vacuum & Analyze (Clean Up)

**Run maintenance:**
```sql
-- Vacuum removes dead data and optimizes storage
VACUUM ANALYZE;

-- For specific table:
VACUUM ANALYZE project;
VACUUM ANALYZE feedback;
```

This should run automatically, but you can run it manually to free up space.

---

### 4. Check Database Health

**View active connections:**
```sql
SELECT datname, count(*) as connections
FROM pg_stat_activity
GROUP BY datname;
```

**Kill stuck connections (if needed):**
```sql
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'railway' AND pid <> pg_backend_pid();
```

---

### 5. Index Maintenance

**View all indexes:**
```sql
SELECT indexname, tablename 
FROM pg_indexes 
WHERE schemaname = 'public';
```

**Create indexes for faster queries:**
```sql
-- Speed up project lookups
CREATE INDEX idx_project_department ON project(department);
CREATE INDEX idx_project_status ON project(status);

-- Speed up feedback searches
CREATE INDEX idx_feedback_created_at ON feedback(created_at DESC);

-- Speed up budget queries
CREATE INDEX idx_region_budget_year ON region_budget(year);
CREATE INDEX idx_dept_budget_year ON department_budget(year);
```

---

## 🔄 Data Maintenance

### Reset/Clear All Data

**If you want to start fresh:**

**Option 1: Using Python**
```python
from app import app, db
from models import Project, Feedback, ProjectReport, RegionBudget, DepartmentBudget, AnnualBudget

with app.app_context():
    # Delete all data
    Project.query.delete()
    Feedback.query.delete()
    ProjectReport.query.delete()
    RegionBudget.query.delete()
    DepartmentBudget.query.delete()
    AnnualBudget.query.delete()
    db.session.commit()
    print("All data cleared!")
```

**Option 2: SQL Commands**
```sql
DELETE FROM project_report;
DELETE FROM project;
DELETE FROM feedback;
DELETE FROM region_budget;
DELETE FROM department_budget;
DELETE FROM annual_budget;
```

### Re-seed Data

After clearing, run:
```bash
python seed_data.py
```

---

## 📊 Monitor Performance

### Check Slow Queries

**Enable slow query log (if available):**
```sql
-- View slow queries
SELECT query, calls, total_time, mean_time 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;
```

### Table Statistics

**Get table sizes:**
```sql
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

---

## 🔒 Security Maintenance

### Change Default Password

**Don't use default admin credentials in production!**

Update in `app.py`:
```python
# CHANGE THIS:
ADMIN_CREDENTIALS = {
    'admin': hash_password('admin123'),  # ❌ Not secure!
    'staff': hash_password('staff123')   # ❌ Not secure!
}

# Better: Use environment variables
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'change_this_in_production')
```

### Rotate Secrets

In Railway:
1. Go to Variables
2. Update `SECRET_KEY` with a new random string:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

---

## 📈 Scaling Considerations

### When to Upgrade Database:

- Database size > 5GB
- More than 1000 queries/second
- Response times slowing down
- High CPU/Memory usage

**Upgrade on Railway:**
1. Click PostgreSQL service
2. Go to Settings
3. Upgrade to larger plan if needed

---

## 🚨 Emergency Procedures

### Database Won't Connect

1. Check Railway dashboard - is PostgreSQL running?
2. Verify credentials in environment variables
3. Check firewall/network settings
4. Restart the PostgreSQL service

### Out of Disk Space

1. Check database size: `SELECT pg_database_size(current_database());`
2. Run VACUUM: `VACUUM FULL;`
3. Upgrade storage plan on Railway
4. Archive old data to another database

### Corrupted Data

1. **Restore from backup:**
   - Go to Railway PostgreSQL service
   - Click Backups
   - Choose previous backup
   - Click Restore

2. **Check table integrity:**
   ```sql
   REINDEX DATABASE railway;
   ```

---

## 📋 Maintenance Checklist

**Weekly:**
- ✅ Check database is running
- ✅ Verify backups are being created
- ✅ Monitor database size

**Monthly:**
- ✅ Run VACUUM ANALYZE
- ✅ Review slow queries
- ✅ Check disk space

**Quarterly:**
- ✅ Test backup restoration
- ✅ Review security settings
- ✅ Analyze table statistics
- ✅ Create missing indexes if needed

**Annually:**
- ✅ Archive old data
- ✅ Update passwords/secrets
- ✅ Review disaster recovery plan
- ✅ Consider database upgrade

---

## 🔗 Useful SQL Queries

**Count records by table:**
```sql
SELECT 
    'project' as table_name, COUNT(*) as count FROM project
UNION ALL SELECT 'feedback', COUNT(*) FROM feedback
UNION ALL SELECT 'project_report', COUNT(*) FROM project_report
UNION ALL SELECT 'region_budget', COUNT(*) FROM region_budget
UNION ALL SELECT 'department_budget', COUNT(*) FROM department_budget
UNION ALL SELECT 'annual_budget', COUNT(*) FROM annual_budget;
```

**Database info:**
```sql
SELECT 
    version(),
    current_database(),
    pg_database_size(current_database()) as size_bytes,
    pg_size_pretty(pg_database_size(current_database())) as size;
```

---

## 📞 Support

- **Railway Docs**: https://docs.railway.app/databases/postgresql
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **pgAdmin Help**: https://www.pgadmin.org/support/

---

**Your database is running smoothly! Keep these maintenance tasks in mind for long-term health! 🚀**
