import os
import shutil
import subprocess
from datetime import datetime

# --- CONFIG ---
TEMP_HTML = 'UFL/UFLWTmp.htm'

def get_current_week():
    # UFL 2026 Start: March 27
    start_date = datetime(2026, 3, 27)
    days_since = (datetime.now() - start_date).days
    return (days_since // 7) + 1

def archive_previous_week(week_num):
    target = f'UFL/UFLWk{week_num}.htm'
    if os.path.exists(TEMP_HTML):
        shutil.copy(TEMP_HTML, target)
        print(f"✅ Archived {TEMP_HTML} to {target}")

if __name__ == "__main__":
    current_wk = get_current_week()
    
    # 1. Archive the old issue first
    archive_previous_week(current_wk)
    
    # 2. Run the Scraper (updates ufl-data.csv)
    print("🚀 Running Scraper...")
    subprocess.run(["python", "UFL/ufl-datascraper.py"], check=True)

    
    # 3. Run the Projections (reads ufl-data.csv -> writes UFLWTmp.htm)
    print(f"📊 Generating projections for Week {current_wk + 1}...")
    subprocess.run(["python", "UFL/generate_projections.py"])
    
    print("✨ Weekly Update Complete.")
