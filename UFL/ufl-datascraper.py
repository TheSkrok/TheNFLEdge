import csv
import os
from playwright.sync_api import sync_playwright

def scrape_ufl_wikipedia_precise():
    # TARGET URL (Must be the specific template page)
    url = "https://en.wikipedia.org/wiki/Template:2026_UFL_standings"
    
    # Ensure local directory exists
    os.makedirs('ufl', exist_ok=True)
    output_path = os.path.join('ufl', 'ufl-data.csv')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print(f"Connecting to {url}...")
        page.goto(url, wait_until="load")
        
        # Locate the specific wikitable on the page
        table = page.query_selector("table.wikitable")
        if not table:
            print("FAILED: Could not find the wikitable on this page.")
            browser.close()
            return

        rows = table.query_selector_all("tr")
        teams_data = []
        
        for row in rows:
            # We only want data cells (td) to skip headers automatically
            cols = row.query_selector_all("td")
            
            # Requirement: Team Name(0), W(1), L(2), PCT(3), PF(8), PA(9)
            if len(cols) >= 10:
                texts = [c.inner_text().strip() for c in cols]
                
                try:
                    name_raw = texts[0]
                    w_val    = texts[1]
                    l_val    = texts[2]
                    pct_val  = texts[3]
                    pf_val   = texts[8]
                    pa_val   = texts[9]

                    # DATA CLEANING:
                    # Convert to float first to handle '1.000', then to int
                    wins_int = int(float(w_val))
                    loss_int = int(float(l_val))
                    gp = str(wins_int + loss_int)
                    
                    # Clean team name of Wikipedia citation brackets like [a]
                    name = name_raw.split('[')[0].strip()
                    
                    # Final CSV order: [name, pf, pa, gp, wins, pct]
                    teams_data.append([name, pf_val, pa_val, gp, str(wins_int), pct_val])
                except (ValueError, IndexError):
                    continue

        if teams_data:
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['name', 'pf', 'pa', 'gp', 'wins', 'pct'])
                writer.writerows(teams_data)
            print(f"SUCCESS! {output_path} updated with {len(teams_data)} teams.")
        else:
            print("FAILED: Found the table but no rows matched the index requirements.")

        browser.close()

if __name__ == "__main__":
    scrape_ufl_wikipedia_precise()
