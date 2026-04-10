import pandas as pd
import requests

def scrape_ufl_data():
    # 1. Scrape Standings for Stats (PF, PA, GP)
    standings_url = "https://foxsports.com"
    try:
        tables = pd.read_html(standings_url)
        stats_df = tables[0] # Assuming first table is standings
        
        # Clean Team names (Fox adds ranks like "1 DC Defenders")
        stats_df['team_clean'] = stats_df['TEAMS'].str.replace(r'^\d+\s+', '', regex=True).str.strip()
        stats_df = stats_df.rename(columns={'PF': 'pf', 'PA': 'pa', 'W': 'gp4'})
        stats_map = stats_df.set_index('team_clean')[['pf', 'pa', 'gp4']].to_dict('index')
    except Exception as e:
        print(f"Error scraping standings: {e}")
        return

    # 2. Matchup Data for Week 4 (Hardcoded for accuracy as schedule pages vary)
    # We will automate this fully once the season settles, but for Week 4:
    week_4_matchups = [
        {"team": "Louisville Kings", "opp": "Houston Gamblers"},
        {"team": "Dallas Renegades", "opp": "Columbus Aviators"},
        {"team": "St. Louis Battlehawks", "opp": "DC Defenders"},
        {"team": "Orlando Storm", "opp": "Birmingham Stallions"}
    ]

    # 3. Merge Stats into Matchups
    final_rows = []
    for m in week_4_matchups:
        team_stats = stats_map.get(m['team'], {'pf': 0, 'pa': 0, 'gp4': 1})
        opp_stats = stats_map.get(m['opp'], {'pf': 0, 'pa': 0, 'gp4': 1})
        
        row = {
            "team": m['team'],
            "opp": m['opp'],
            "pf": team_stats['pf'],
            "pa": team_stats['pa'],
            "gp4": team_stats['gp4'],
            "pp4v": 0.5, # Default variance
            "v_pf": opp_stats['pf'],
            "v_pa": opp_stats['pa'],
            "vgp4": opp_stats['gp4']
        }
        final_rows.append(row)

    # 4. Save to ufl-data.csv
    pd.DataFrame(final_rows).to_csv('UFL/ufl-data.csv', index=False)
    print("✅ ufl-data.csv updated with Week 4 matchups and season stats.")

if __name__ == "__main__":
    scrape_ufl_data()
