#!/usr/bin/env python
"""Load sample data into PostgreSQL database"""

from app import app, db
from models import Project, Feedback, ProjectReport, RegionBudget, DepartmentBudget, AnnualBudget
from datetime import datetime

def load_data():
    with app.app_context():
        # Clear existing data
        db.session.query(ProjectReport).delete()
        db.session.query(Project).delete()
        db.session.query(Feedback).delete()
        db.session.query(RegionBudget).delete()
        db.session.query(DepartmentBudget).delete()
        db.session.query(AnnualBudget).delete()
        db.session.commit()
        print("✅ Cleared existing data")
        
        # Load sample projects
        projects_data = [
            {
                'name': 'Road Rehabilitation - Barangay A',
                'department': 'Department of Public Works and Highways',
                'description': 'Rehab of 3km barangay road',
                'allocated_budget': 5000000,
                'spent': 3500000,
                'status': 'Ongoing',
                'region': 'Region I',
                'start_date': '2024-05-01',
                'end_date': None
            },
            {
                'name': 'School Building Construction',
                'department': 'Department of Education',
                'description': '2-classroom building',
                'allocated_budget': 2000000,
                'spent': 2000000,
                'status': 'Completed',
                'region': 'Region II',
                'start_date': '2023-10-01',
                'end_date': '2024-04-15'
            },
            {
                'name': 'Health Center Upgrade',
                'department': 'Department of Health',
                'description': 'Medical equipment and building upgrade',
                'allocated_budget': 3000000,
                'spent': 1500000,
                'status': 'Ongoing',
                'region': 'Region III',
                'start_date': '2024-01-10',
                'end_date': None
            },
            {
                'name': 'Irrigation System Project',
                'department': 'Department of Agriculture',
                'description': 'Small-scale irrigation',
                'allocated_budget': 1500000,
                'spent': 200000,
                'status': 'Planned',
                'region': 'Region IV',
                'start_date': None,
                'end_date': None
            }
        ]
        
        for proj_data in projects_data:
            project = Project(**proj_data)
            db.session.add(project)
        db.session.commit()
        print(f"✅ Loaded {len(projects_data)} projects")
        
        # Load sample feedback
        feedback_data = [
            {'name': 'Juan Dela Cruz', 'email': 'juan@example.com', 'message': 'Please update the road project timeline.'},
            {'name': 'Maria Santos', 'email': 'maria@example.com', 'message': 'Great initiative — more regional breakdown needed.'},
        ]
        
        for fb_data in feedback_data:
            feedback = Feedback(**fb_data)
            db.session.add(feedback)
        db.session.commit()
        print(f"✅ Loaded {len(feedback_data)} feedback entries")
        
        # Load annual budgets
        annual_budgets = [
            {'year': 2023, 'total_budget': 5268000000000},
            {'year': 2024, 'total_budget': 5768000000000},
            {'year': 2025, 'total_budget': 6326000000000},
        ]
        
        for ab_data in annual_budgets:
            annual_budget = AnnualBudget(**ab_data)
            db.session.add(annual_budget)
        db.session.commit()
        print(f"✅ Loaded {len(annual_budgets)} annual budgets")
        
        # Load regional budgets for 2023
        regional_2023 = [
            ('National Capital Region', 2023, 887000000000),
            ('Cordillera Administrative Region', 2023, 98500000000),
            ('Region I', 2023, 169900000000),
            ('Region II', 2023, 144700000000),
            ('Region III', 2023, 321100000000),
            ('Region IV-A', 2023, 318700000000),
            ('Region IV-B', 2023, 134200000000),
            ('Region V', 2023, 212800000000),
            ('Region VI', 2023, 203500000000),
            ('Region VII', 2023, 212000000000),
            ('Region VIII', 2023, 177400000000),
            ('Region IX', 2023, 126800000000),
            ('Region X', 2023, 175000000000),
            ('Region XI', 2023, 149100000000),
            ('Region XII', 2023, 116400000000),
            ('Caraga', 2023, 109300000000),
            ('BARMM', 2023, 130300000000),
        ]
        
        for region, year, budget in regional_2023:
            rb = RegionBudget(region=region, year=year, budget=budget)
            db.session.add(rb)
        
        # Load regional budgets for 2024
        regional_2024 = [
            ('National Capital Region', 2024, 532008065000),
            ('Cordillera Administrative Region', 2024, 867228911000),
            ('Region I', 2024, 180565920000),
            ('Region II', 2024, 97668044000),
            ('Region III', 2024, 160174535000),
            ('Region IV-A', 2024, 369230365000),
            ('Region IV-B', 2024, 341101910000),
            ('Region V', 2024, 234040470000),
            ('Region VI', 2024, 222399947000),
            ('Region VII', 2024, 228181764000),
            ('Region VIII', 2024, 205946394000),
            ('Region IX', 2024, 140072215000),
            ('Region X', 2024, 190071333000),
            ('Region XI', 2024, 162666370000),
            ('Region XII', 2024, 127046390000),
            ('Caraga', 2024, 124270792000),
            ('BARMM', 2024, 149440406000),
        ]
        
        for region, year, budget in regional_2024:
            rb = RegionBudget(region=region, year=year, budget=budget)
            db.session.add(rb)
        
        # Load regional budgets for 2025
        regional_2025 = [
            ('National Capital Region', 2025, 834600000000),
            ('Cordillera Administrative Region', 2025, 106000000000),
            ('Region I', 2025, 198700000000),
            ('Region II', 2025, 175000000000),
            ('Region III', 2025, 420600000000),
            ('Region IV-A', 2025, 395600000000),
            ('Region IV-B', 2025, 184600000000),
            ('Region V', 2025, 257300000000),
            ('Region VI', 2025, 236100000000),
            ('Region VII', 2025, 255900000000),
            ('Region VIII', 2025, 209400000000),
            ('Region IX', 2025, 149300000000),
            ('Region X', 2025, 195700000000),
            ('Region XI', 2025, 172500000000),
            ('Region XII', 2025, 137800000000),
            ('Caraga', 2025, 138900000000),
            ('BARMM', 2025, 172400000000),
        ]
        
        for region, year, budget in regional_2025:
            rb = RegionBudget(region=region, year=year, budget=budget)
            db.session.add(rb)
        
        db.session.commit()
        print(f"✅ Loaded {len(regional_2023) + len(regional_2024) + len(regional_2025)} regional budgets")
        
        # Load department budgets for 2023
        dept_2023 = [
            ('Department of Education', 2023, 678317321000),
            ('Department of Health', 2023, 209624216000),
            ('Department of Public Works and Highways', 2023, 893121040000),
            ('Department of the Interior and Local Government', 2023, 253404249000),
            ('Department of National Defense', 2023, 204566332000),
            ('Department of Social Welfare and Development', 2023, 199256638000),
            ('Department of Agriculture', 2023, 98864397000),
            ('Department of Budget and Management', 2023, 1737629000),
            ('Department of Justice', 2023, 36228754000),
            ('Department of Labor and Employment', 2023, 46631922000),
            ('Department of Energy', 2023, 1320735000),
            ('Department of Finance', 2023, 23927302000),
            ('Department of Foreign Affairs', 2023, 20621463000),
            ('Department of Information and Communications Technology', 2023, 8289778000),
            ('Department of Tourism', 2023, 3731984000),
            ('Department of Trade and Industry', 2023, 6327029000),
            ('Department of Transportation', 2023, 105530385000),
            ('National Economic and Development Authority', 2023, 12961084000),
            ('Civil Service Commission', 2023, 2045591000),
            ('Commission on Audit', 2023, 13318049000),
            ('Commission on Elections', 2023, 5737340000),
            ('Office of the Ombudsman', 2023, 4721331000),
            ('Commission on Human Rights', 2023, 993921000),
            ('Special Purpose Funds', 2023, 1825624983000),
        ]
        
        for dept, year, budget in dept_2023:
            db_obj = DepartmentBudget(department=dept, year=year, budget=budget)
            db.session.add(db_obj)
        
        # Load department budgets for 2024
        dept_2024 = [
            ('Department of Education', 2024, 717663478000),
            ('Department of Health', 2024, 241602813000),
            ('Department of Public Works and Highways', 2024, 996791684000),
            ('Department of the Interior and Local Government', 2024, 263649999000),
            ('Department of National Defense', 2024, 238356544000),
            ('Department of Social Welfare and Development', 2024, 247848341000),
            ('Department of Agriculture', 2024, 111687758000),
            ('Department of Budget and Management', 2024, 2501145000),
            ('Department of Justice', 2024, 36228754000),
            ('Department of Labor and Employment', 2024, 61268468000),
            ('Department of Energy', 2024, 1662160000),
            ('Department of Finance', 2024, 23927302000),
            ('Department of Foreign Affairs', 2024, 24591198000),
            ('Department of Tourism', 2024, 3439715000),
            ('Department of Trade and Industry', 2024, 8638218000),
            ('Department of Transportation', 2024, 73330669000),
            ('Special Purpose Funds', 2024, 2169133613000),
        ]
        
        for dept, year, budget in dept_2024:
            db_obj = DepartmentBudget(department=dept, year=year, budget=budget)
            db.session.add(db_obj)
        
        # Load department budgets for 2025
        dept_2025 = [
            ('Department of Education', 2025, 793177297000),
            ('Department of Health', 2025, 223188973000),
            ('Department of Public Works and Highways', 2025, 900000000000),
            ('Department of the Interior and Local Government', 2025, 281320865000),
            ('Department of National Defense', 2025, 258164910000),
            ('Department of Social Welfare and Development', 2025, 230057270000),
            ('Department of Agriculture', 2025, 129001585000),
            ('Department of Budget and Management', 2025, 3191835000),
            ('Department of Justice', 2025, 40584630000),
            ('Department of Labor and Employment', 2025, 45833958000),
            ('Department of Migrant Workers', 2025, 8503912000),
            ('National Economic and Development Authority', 2025, 12575395000),
            ('Department of Transportation', 2025, 180893888000),
            ('Department of Trade and Industry', 2025, 8598332000),
            ('Commission on Audit', 2025, 13417340000),
            ('Commission on Elections', 2025, 35470671000),
            ('Office of the Ombudsman', 2025, 5824154000),
            ('Special Purpose Funds', 2025, 2740481084000),
        ]
        
        for dept, year, budget in dept_2025:
            db_obj = DepartmentBudget(department=dept, year=year, budget=budget)
            db.session.add(db_obj)
        
        db.session.commit()
        print(f"✅ Loaded {len(dept_2023) + len(dept_2024) + len(dept_2025)} department budgets")
        
        # Verify data
        print("\n📊 Data Summary:")
        print(f"  Projects: {db.session.query(Project).count()}")
        print(f"  Feedback: {db.session.query(Feedback).count()}")
        print(f"  Regional Budgets: {db.session.query(RegionBudget).count()}")
        print(f"  Department Budgets: {db.session.query(DepartmentBudget).count()}")
        print(f"  Annual Budgets: {db.session.query(AnnualBudget).count()}")
        print("\n✅ All data loaded successfully!")

if __name__ == '__main__':
    load_data()
