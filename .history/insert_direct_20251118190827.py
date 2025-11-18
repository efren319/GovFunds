#!/usr/bin/env python3
"""Direct database insertion using psycopg2"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    # Connect to database
    conn = psycopg2.connect(
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432',
        database='govfunds'
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    
    print("Connected to database!")
    
    # Clear existing data
    cur.execute("DELETE FROM department_budget;")
    cur.execute("DELETE FROM region_budget;")
    cur.execute("DELETE FROM annual_budget;")
    print("Cleared existing data")
    
    # Insert departments
    depts = [
        ('Department of Education', 2025, 500000000),
        ('Department of Health', 2025, 400000000),
        ('Department of Infrastructure', 2025, 600000000),
        ('Department of Defense', 2025, 350000000),
        ('Department of Social Services', 2025, 250000000),
        ('Department of Environment', 2025, 180000000),
        ('Department of Agriculture', 2025, 220000000),
        ('Department of Transportation', 2025, 300000000),
    ]
    
    for dept_name, year, budget in depts:
        cur.execute(
            "INSERT INTO department_budget (department, year, budget) VALUES (%s, %s, %s)",
            (dept_name, year, budget)
        )
    print(f"Inserted {len(depts)} departments")
    
    # Insert regions
    regions = [
        ('Region 1 - Ilocos Region', 2025, 280000000),
        ('Region 2 - Cagayan Valley', 2025, 250000000),
        ('Region 3 - Central Luzon', 2025, 350000000),
        ('Region 4A - CALABARZON', 2025, 420000000),
        ('Region 4B - MIMAROPA', 2025, 180000000),
        ('Region 5 - Bicol Region', 2025, 220000000),
        ('Region 6 - Western Visayas', 2025, 280000000),
        ('Region 7 - Central Visayas', 2025, 310000000),
        ('Region 8 - Eastern Visayas', 2025, 190000000),
        ('Region 9 - Zamboanga Peninsula', 2025, 210000000),
        ('Region 10 - Northern Mindanao', 2025, 240000000),
        ('Region 11 - Davao Region', 2025, 300000000),
        ('Region 12 - SOCCSKSARGEN', 2025, 270000000),
        ('Region 13 - Caraga', 2025, 160000000),
        ('NCR - National Capital Region', 2025, 500000000),
    ]
    
    for region_name, year, budget in regions:
        cur.execute(
            "INSERT INTO region_budget (region, year, budget) VALUES (%s, %s, %s)",
            (region_name, year, budget)
        )
    print(f"Inserted {len(regions)} regions")
    
    # Insert annual budget
    cur.execute("INSERT INTO annual_budget (year, total_budget) VALUES (%s, %s)", (2025, 4130000000))
    print("Inserted annual budget")
    
    cur.close()
    conn.close()
    print("[SUCCESS] All data inserted!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
