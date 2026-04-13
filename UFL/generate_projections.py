import os
import math
import csv
import sys

# Testing Multipliers
P_M = {
    "1.0":  2.375,
    "0.75": 2.314,
    "0.5":  2.131,
    "0.25": 2.031,
    "0.0":  1.935
}
M_D = 2.0 

def get_dynamic_pp4v(pf, pa, gp):
    if float(gp) == 0: return "0.5"
    win_pct = pf / (pf + pa) if (pf + pa) > 0 else 0.5
    if win_pct >= 0.8: return "1.0"
    if win_pct >= 0.6: return "0.75"
    if win_pct >= 0.4: return "0.5"
    if win_pct >= 0.2: return "0.25"
    return "0.0"

def c_pags(pf, pa, gp4, pp4v, v_pf, v_pa, vgp4):
    t_q = (pf / gp4) / 4
    v_q = (v_pa / vgp4) / 4
    p_c = P_M.get(str(pp4v))
    b_v = (t_q + v_q) * p_c
    pp4v_f = float(pp4v)
    if pp4v_f >= 0.75:
        res = math.ceil(b_v + M_D)
    elif pp4v_f <= 0.25:
        res = math.floor(b_v - M_D)
    else:
        res = round(b_v)
    return res

def generate_html(rows, week):
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
body {{ background-color: #000000; color: #ffffff; font-family: sans-serif; margin: 0; padding: 15px; text-align: center; }}
.f {{ max-width: 750px; margin: auto; border: 2px solid #00205B; padding: 30px; background-color: #050505; box-shadow: 0 0 20px rgba(191, 10, 48, 0.4); }}
header {{ border-bottom: 2px solid #BF0A30; margin-bottom: 25px; padding-bottom: 15px; }}
h1 {{ font-size: 1.8em; text-transform: uppercase; letter-spacing: 4px; margin: 0; }}
table {{ width: 100%; border-collapse: collapse; margin-top: 20px; background-color: #080808; }}
th {{ background-color: #00205B; color: #ffffff; padding: 12px; font-size: 0.75em; text-transform: uppercase; }}
td {{ padding: 15px; border-bottom: 1px solid #1a1a1a; font-size: 0.95em; }}
.w {{ color: #BF0A30; font-weight: bold; }}
</style>
</head>
<body>
<div class="f">
<header><h1>PanaGeoTech - WEEK {week}</h1></header>
<table>
<thead><tr><th>Matchup</th><th>PAGS Projection</th></tr></thead>
<tbody>{rows}</tbody>
</table>
</div>
</body>
</html>"""

if __name__ == "__main__":
    standings_file = 'UFL/ufl-data.csv'
    schedule_file = 'UFL/ufl-schedule.csv'
    output_file = 'UFL/UFLWTmp.htm'
    rows_html = ""
    
    try:
        # Load standings into a lookup dictionary
        with open(standings_file, mode='r') as f:
            standings = {row['name']: row for row in csv.DictReader(f)}
        
        # Process matchups for Week 3
        with open(schedule_file, mode='r') as f:
            matchups = list(csv.DictReader(f))
            current_week = matchups[0]['week']
            
            for m in matchups:
                home = standings[m['home']]
                away = standings[m['away']]
                
                # Dynamic power for Home team
                calc_pp4v = get_dynamic_pp4v(float(home['pf']), float(home['pa']), float(home['gp']))
                
                p_v = c_pags(
                    float(home['pf']), float(home['pa']), float(home['gp']), 
                    calc_pp4v, 
                    float(away['pf']), float(away['pa']), float(away['gp'])
                )
                rows_html += f"<tr><td>{m['away']} @ {m['home']}</td><td class='w'>{p_v}</td></tr>"
        
        with open(output_file, "w") as f:
            f.write(generate_html(rows_html, current_week))
        print(f"Success: Week {current_week} Projections Generated.")
    except Exception as e:
        print(f"Error: {e}")
