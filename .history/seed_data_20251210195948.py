
import os
from datetime import date
from dotenv import load_dotenv
from app import app, db
from models import Project, Feedback, RegionBudget, ProjectSectorBudget, AnnualBudget, Region, ProjectSector, ReportType, UserRole

# Load environment variables
load_dotenv()

def seed_data():
    """Insert sample data into the database"""
    
    with app.app_context():
        try:
            # Create all tables if they don't exist
            print("Creating database tables...")
            db.create_all()
            print("✓ Tables created/verified")
            
            # Clear existing data (optional) - order matters due to FK constraints
            print("Clearing existing data...")
            Project.query.delete()
            Feedback.query.delete()
            RegionBudget.query.delete()
            ProjectSectorBudget.query.delete()
            AnnualBudget.query.delete()
            Region.query.delete()
            ProjectSector.query.delete()
            ReportType.query.delete()
            UserRole.query.delete()
            db.session.commit()
            
            # Insert User Roles
            print("Inserting user roles...")
            user_roles = [
                UserRole(role_name='admin'),
                UserRole(role_name='staff'),
                UserRole(role_name='viewer'),
            ]
            db.session.add_all(user_roles)
            db.session.commit()
            print(f"✓ Inserted {len(user_roles)} user roles")
            
            # Insert Report Types
            print("Inserting report types...")
            report_types = [
                ReportType(type_name='General'),
                ReportType(type_name='Issue'),
                ReportType(type_name='Concern'),
                ReportType(type_name='Suggestion'),
            ]
            db.session.add_all(report_types)
            db.session.commit()
            print(f"✓ Inserted {len(report_types)} report types")
            
            # Insert Regions
            print("Inserting regions...")
            regions_list = [
                'National Capital Region',
                'Cordillera Administrative Region',
                'Region I',
                'Region II',
                'Region III',
                'Region IV-A',
                'Region IV-B',
                'Region V',
                'Region VI',
                'Region VII',
                'Region VIII',
                'Region IX',
                'Region X',
                'Region XI',
                'Region XII',
                'Caraga',
                'BARMM',
            ]
            regions = [Region(region_name=name) for name in regions_list]
            db.session.add_all(regions)
            db.session.commit()
            print(f"✓ Inserted {len(regions)} regions")
            
            # Create region lookup dict
            region_lookup = {r.region_name: r.region_id for r in Region.query.all()}
            
            # Insert Project Sectors
            print("Inserting project sectors...")
            sectors_list = [
                'Road Infrastructure',
                'Bridge Infrastructure',
                'Flood Control and Drainage',
                'Public Buildings',
                'Water Resources and Irrigation',
                'Special Infrastructure Projects',
                'Disaster Response and Rehabilitation',
                'Local Infrastructure Support',
            ]
            sectors = [ProjectSector(sector_name=name) for name in sectors_list]
            db.session.add_all(sectors)
            db.session.commit()
            print(f"✓ Inserted {len(sectors)} project sectors")
            
            # Create sector lookup dict
            sector_lookup = {s.sector_name: s.sector_id for s in ProjectSector.query.all()}
            
            # Insert sample projects
            print("Inserting sample projects...")
            projects = [
                Project(
                    project_name='Road Rehabilitation - Barangay A',
                    sector_id=sector_lookup['Road Infrastructure'],
                    project_description='Rehab of 3km barangay road',
                    allocated_budget=5000000,
                    budget_spent=3500000,
                    project_status='Ongoing',
                    region_id=region_lookup['Region I'],
                    start_date=date(2024, 5, 1),
                    end_date=None
                ),
                Project(
                    project_name='Public Building Construction',
                    sector_id=sector_lookup['Public Buildings'],
                    project_description='Government office building',
                    allocated_budget=2000000,
                    budget_spent=2000000,
                    project_status='Completed',
                    region_id=region_lookup['Region II'],
                    start_date=date(2023, 10, 1),
                    end_date=date(2024, 4, 15)
                ),
                Project(
                    project_name='Bridge Repair and Maintenance',
                    sector_id=sector_lookup['Bridge Infrastructure'],
                    project_description='Structural repair of aging bridge',
                    allocated_budget=3000000,
                    budget_spent=1500000,
                    project_status='Ongoing',
                    region_id=region_lookup['Region III'],
                    start_date=date(2024, 1, 10),
                    end_date=None
                ),
                Project(
                    project_name='Irrigation System Project',
                    sector_id=sector_lookup['Water Resources and Irrigation'],
                    project_description='Small-scale irrigation facility',_
                    allocated_budget=1500000,
                    budget_spent=200000,
                    project_status='Planned',
                    region_id=region_lookup['Region IV-A'],
                    start_date=None,
                    end_date=None
                ),
            ]
            db.session.add_all(projects)
            db.session.commit()
            print(f"✓ Inserted {len(projects)} projects")
            
            # Insert sample feedback
            print("Inserting sample feedback...")
            feedback = [
                Feedback(
                    name='Juan Dela Cruz',
                    email='juan@example.com',
                    message='Please update the road project timeline.'
                ),
                Feedback(
                    name='Maria Santos',
                    email='maria@example.com',
                    message='Great initiative — more regional breakdown needed.'
                ),
            ]
            db.session.add_all(feedback)
            db.session.commit()
            print(f"✓ Inserted {len(feedback)} feedback entries")
            
            # Regional Budget Data for 2023
            print("Inserting regional budget data...")
            region_budgets_2023 = [
                RegionBudget(region_id=region_lookup['National Capital Region'], year=2023, region_budget=887000000000),
                RegionBudget(region_id=region_lookup['Cordillera Administrative Region'], year=2023, region_budget=98500000000),
                RegionBudget(region_id=region_lookup['Region I'], year=2023, region_budget=169900000000),
                RegionBudget(region_id=region_lookup['Region II'], year=2023, region_budget=144700000000),
                RegionBudget(region_id=region_lookup['Region III'], year=2023, region_budget=321100000000),
                RegionBudget(region_id=region_lookup['Region IV-A'], year=2023, region_budget=318700000000),
                RegionBudget(region_id=region_lookup['Region IV-B'], year=2023, region_budget=134200000000),
                RegionBudget(region_id=region_lookup['Region V'], year=2023, region_budget=212800000000),
                RegionBudget(region_id=region_lookup['Region VI'], year=2023, region_budget=203500000000),
                RegionBudget(region_id=region_lookup['Region VII'], year=2023, region_budget=212000000000),
                RegionBudget(region_id=region_lookup['Region VIII'], year=2023, region_budget=177400000000),
                RegionBudget(region_id=region_lookup['Region IX'], year=2023, region_budget=126800000000),
                RegionBudget(region_id=region_lookup['Region X'], year=2023, region_budget=175000000000),
                RegionBudget(region_id=region_lookup['Region XI'], year=2023, region_budget=149100000000),
                RegionBudget(region_id=region_lookup['Region XII'], year=2023, region_budget=116400000000),
                RegionBudget(region_id=region_lookup['Caraga'], year=2023, region_budget=109300000000),
                RegionBudget(region_id=region_lookup['BARMM'], year=2023, region_budget=130300000000),
            ]
            db.session.add_all(region_budgets_2023)
            
            # Regional Budget Data for 2024
            region_budgets_2024 = [
                RegionBudget(region_id=region_lookup['National Capital Region'], year=2024, region_budget=532008065000),
                RegionBudget(region_id=region_lookup['Cordillera Administrative Region'], year=2024, region_budget=867228911000),
                RegionBudget(region_id=region_lookup['Region I'], year=2024, region_budget=180565920000),
                RegionBudget(region_id=region_lookup['Region II'], year=2024, region_budget=97668044000),
                RegionBudget(region_id=region_lookup['Region III'], year=2024, region_budget=160174535000),
                RegionBudget(region_id=region_lookup['Region IV-A'], year=2024, region_budget=369230365000),
                RegionBudget(region_id=region_lookup['Region IV-B'], year=2024, region_budget=341101910000),
                RegionBudget(region_id=region_lookup['Region V'], year=2024, region_budget=234040470000),
                RegionBudget(region_id=region_lookup['Region VI'], year=2024, region_budget=222399947000),
                RegionBudget(region_id=region_lookup['Region VII'], year=2024, region_budget=228181764000),
                RegionBudget(region_id=region_lookup['Region VIII'], year=2024, region_budget=205946394000),
                RegionBudget(region_id=region_lookup['Region IX'], year=2024, region_budget=140072215000),
                RegionBudget(region_id=region_lookup['Region X'], year=2024, region_budget=190071333000),
                RegionBudget(region_id=region_lookup['Region XI'], year=2024, region_budget=162666370000),
                RegionBudget(region_id=region_lookup['Region XII'], year=2024, region_budget=127046390000),
                RegionBudget(region_id=region_lookup['Caraga'], year=2024, region_budget=124270792000),
                RegionBudget(region_id=region_lookup['BARMM'], year=2024, region_budget=149440406000),
            ]
            db.session.add_all(region_budgets_2024)
            
            # Regional Budget Data for 2025
            region_budgets_2025 = [
                RegionBudget(region_id=region_lookup['National Capital Region'], year=2025, region_budget=834600000000),
                RegionBudget(region_id=region_lookup['Cordillera Administrative Region'], year=2025, region_budget=106000000000),
                RegionBudget(region_id=region_lookup['Region I'], year=2025, region_budget=198700000000),
                RegionBudget(region_id=region_lookup['Region II'], year=2025, region_budget=175000000000),
                RegionBudget(region_id=region_lookup['Region III'], year=2025, region_budget=420600000000),
                RegionBudget(region_id=region_lookup['Region IV-A'], year=2025, region_budget=395600000000),
                RegionBudget(region_id=region_lookup['Region IV-B'], year=2025, region_budget=184600000000),
                RegionBudget(region_id=region_lookup['Region V'], year=2025, region_budget=257300000000),
                RegionBudget(region_id=region_lookup['Region VI'], year=2025, region_budget=236100000000),
                RegionBudget(region_id=region_lookup['Region VII'], year=2025, region_budget=255900000000),
                RegionBudget(region_id=region_lookup['Region VIII'], year=2025, region_budget=209400000000),
                RegionBudget(region_id=region_lookup['Region IX'], year=2025, region_budget=149300000000),
                RegionBudget(region_id=region_lookup['Region X'], year=2025, region_budget=195700000000),
                RegionBudget(region_id=region_lookup['Region XI'], year=2025, region_budget=172500000000),
                RegionBudget(region_id=region_lookup['Region XII'], year=2025, region_budget=137800000000),
                RegionBudget(region_id=region_lookup['Caraga'], year=2025, region_budget=138900000000),
                RegionBudget(region_id=region_lookup['BARMM'], year=2025, region_budget=172400000000),
            ]
            db.session.add_all(region_budgets_2025)
            db.session.commit()
            print(f"✓ Inserted {len(region_budgets_2023) + len(region_budgets_2024) + len(region_budgets_2025)} regional budget entries")
            
            # Project Sector Budget Data for 2023
            print("Inserting project sector budget data...")
            sector_budgets_2023 = [
                ProjectSectorBudget(sector_id=sector_lookup['Road Infrastructure'], year=2023, sector_budget=116252873000),
                ProjectSectorBudget(sector_id=sector_lookup['Bridge Infrastructure'], year=2023, sector_budget=29333447000),
                ProjectSectorBudget(sector_id=sector_lookup['Flood Control and Drainage'], year=2023, sector_budget=182989695000),
                ProjectSectorBudget(sector_id=sector_lookup['Public Buildings'], year=2023, sector_budget=79409974000),
                ProjectSectorBudget(sector_id=sector_lookup['Water Resources and Irrigation'], year=2023, sector_budget=15413692000),
                ProjectSectorBudget(sector_id=sector_lookup['Special Infrastructure Projects'], year=2023, sector_budget=388286983000),
                ProjectSectorBudget(sector_id=sector_lookup['Disaster Response and Rehabilitation'], year=2023, sector_budget=11000000000),
                ProjectSectorBudget(sector_id=sector_lookup['Local Infrastructure Support'], year=2023, sector_budget=37285405000),
            ]
            db.session.add_all(sector_budgets_2023)
            
            # Project Sector Budget Data for 2024
            sector_budgets_2024 = [
                ProjectSectorBudget(sector_id=sector_lookup['Road Infrastructure'], year=2024, sector_budget=132328352000),
                ProjectSectorBudget(sector_id=sector_lookup['Bridge Infrastructure'], year=2024, sector_budget=24755275000),
                ProjectSectorBudget(sector_id=sector_lookup['Flood Control and Drainage'], year=2024, sector_budget=244577911000),
                ProjectSectorBudget(sector_id=sector_lookup['Public Buildings'], year=2024, sector_budget=100214102000),
                ProjectSectorBudget(sector_id=sector_lookup['Water Resources and Irrigation'], year=2024, sector_budget=74903429000),
                ProjectSectorBudget(sector_id=sector_lookup['Special Infrastructure Projects'], year=2024, sector_budget=410991162000),
                ProjectSectorBudget(sector_id=sector_lookup['Disaster Response and Rehabilitation'], year=2024, sector_budget=1000000000),
                ProjectSectorBudget(sector_id=sector_lookup['Local Infrastructure Support'], year=2024, sector_budget=39343250000),
            ]
            db.session.add_all(sector_budgets_2024)
            
            # Project Sector Budget Data for 2025
            sector_budgets_2025 = [
                ProjectSectorBudget(sector_id=sector_lookup['Road Infrastructure'], year=2025, sector_budget=541980000000),
                ProjectSectorBudget(sector_id=sector_lookup['Bridge Infrastructure'], year=2025, sector_budget=38000000000),
                ProjectSectorBudget(sector_id=sector_lookup['Flood Control and Drainage'], year=2025, sector_budget=257060000000),
                ProjectSectorBudget(sector_id=sector_lookup['Public Buildings'], year=2025, sector_budget=113522058000),
                ProjectSectorBudget(sector_id=sector_lookup['Water Resources and Irrigation'], year=2025, sector_budget=42570000000),
                ProjectSectorBudget(sector_id=sector_lookup['Special Infrastructure Projects'], year=2025, sector_budget=330000000000),
                ProjectSectorBudget(sector_id=sector_lookup['Disaster Response and Rehabilitation'], year=2025, sector_budget=10000000000),
                ProjectSectorBudget(sector_id=sector_lookup['Local Infrastructure Support'], year=2025, sector_budget=25000000000),
            ]
            db.session.add_all(sector_budgets_2025)
            db.session.commit()
            print(f"✓ Inserted {len(sector_budgets_2023) + len(sector_budgets_2024) + len(sector_budgets_2025)} project sector budget entries")
            
            # Insert Annual Budget
            print("Inserting annual budget data...")
            annual_budgets = [
                AnnualBudget(year=2023, total_budget=5278700000000),
                AnnualBudget(year=2024, total_budget=5705700000000),
                AnnualBudget(year=2025, total_budget=6095900000000),
            ]
            db.session.add_all(annual_budgets)
            db.session.commit()
            print(f"✓ Inserted {len(annual_budgets)} annual budget entries")
            
            print("\n✅ All sample data inserted successfully!")
            
        except Exception as e:
            print(f"❌ Error inserting data: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    seed_data()
