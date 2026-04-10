import pandas as pd
import os

def scrape_ufl_stats():
    # Target URL for UFL Standings/Stats
    url = "https://foxsports.com"
    
    try:
        # read_html returns a list of all tables on the page
        tables = pd.read_html(url)
        # Usually, the main standings table is index 0 or 1
        df = tables[0] 
        
        # Mapping the scraped data to your required fields: 
        # team, opp, pf, pa, gp4, pp4v, v_pf, v_pa, vgp4
        # (Note: You'll need to define 'opp' based on the weekly schedule)
        
        output_path = 'UFL/ufl-data.csv'
        df.to_csv(output_path, index=False)
        print(f"Successfully updated {output_path}")
    except Exception as e:
        print(f"Error scraping data: {e}")

if __name__ == "__main__":
    scrape_ufl_stats()
