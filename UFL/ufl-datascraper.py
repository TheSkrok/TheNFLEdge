import pandas as pd

def scrape_ufl_data():
    # Focused UFL URL
    url = "https://foxsports.com"
    
    try:
        # Instead of a team name, we match on a column header unique to football standings
        tables = pd.read_html(url, match='PF') 
        df = tables[0]
        
        # Identify the Team column (usually the first one) and stats columns
        # Fox often names the first column 'TEAMS' or 'TEAM'
        team_col = [c for c in df.columns if 'TEAM' in str(c).upper()][0]
        
        # Map stats into a dictionary
        stats_map = {}
        for _, row in df.iterrows():
            # Strip ranking numbers (e.g., "1 Renegades" -> "Renegades")
            name = str(row[team_col]).replace(r'^\d+\s+', '', regex=True).strip()
            stats_map[name] = {
                'pf': row.get('PF', 0),
                'pa': row.get('PA', 0),
                'gp4': row.get('W', 0) + row.get('L', 0) # Games Played
            }
        print(f"✅ Successfully mapped {len(stats_map)} UFL teams.")
        
    except Exception as e:
        print(f"❌ Brittle check failed: {e}")
        return

    # Matchup Logic (Week 4)
    week_4_matchups = [
        {"team": "Louisville Kings", "opp": "Houston Gamblers"},
        {"team": "Dallas Renegades", "opp": "Columbus Aviators"},
        {"team": "St. Louis Battlehawks", "opp": "DC Defenders"},
        {"team": "Orlando Storm", "opp": "Birmingham Stallions"}
    ]

    final_rows = []
    for m in week_4_matchups:
        t_s = stats_map.get(m['team'], {'pf': 0, 'pa': 0, 'gp4': 1})
        o_s = stats_map.get(m['opp'], {'pf': 0, 'pa': 0, 'gp4': 1})
        
        final_rows.append({
            "team": m['team'], "opp": m['opp'],
            "pf": t_s['pf'], "pa": t_s['pa'], "gp4": t_s['gp4'],
            "pp4v": 0.5,
            "v_pf": o_s['pf'], "v_pa": o_s['pa'], "vgp4": o_s['gp4']
        })

    pd.DataFrame(final_rows).to_csv('UFL/ufl-data.csv', index=False)
    print("✅ ufl-data.csv updated with robust header-matching.")

if __name__ == "__main__":
    scrape_ufl_data()
