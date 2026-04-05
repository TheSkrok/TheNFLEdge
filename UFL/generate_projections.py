import os
import math
import csv
import sys

def g_s(k):
    v = os.getenv(k)
    if v is None:
        sys.exit(1)
    return float(v)

P_M = {
    "1.0":  g_s("PG_PI_X"),
    "0.75": g_s("PG_PI7"),
    "0.5":  g_s("PG_PPI5"),
    "0.25": g_s("PG_PI2"),
    "0.0":  g_s("PG_PI0")
}
M_D = g_s("PG_MD")

def c_pags(pf, pa, gp4, pp4v, v_pf, v_pa, vgp4):
    t_q = (pf / gp4) / 4
    v_q = (v_pa / vgp4) / 4
    p_c = P_M.get(str(pp4v))
    b_v = (t_q + v_q) * p_c
    if pp4v >= 0.75:
        res = math.ceil(b_v + M_D)
    elif pp4v <= 0.25:
        res = math.floor(b_v - M_D)
    else:
        res = round(b_v)
    return res

def generate_html(rows):
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
<header><h1>PanaGeoTech</h1></header>
<table>
<thead><tr><th>Matchup</th><th>PAGS</th></tr></thead>
<tbody>{rows}</tbody>
</table>
</div>
</body>
</html>"""

if __name__ == "__main__":
    d_f = 'UFL/stats.csv'
    o_f = 'UFL/panageo.htm'
    r_h = ""
    try:
        with open(d_f, mode='r') as f:
            reader = csv.DictReader(f)
            for r in reader:
                p_v = c_pags(
                    float(r['pf']), 
                    float(r['pa']), 
                    float(r['gp4']), 
                    float(r['pp4v']), 
                    float(r['v_pf']), 
                    float(r['v_pa']), 
                    float(r['vgp4'])
                )
                r_h += f"<tr><td>{r['team']} @ {r['opp']}</td><td class='w'>{p_v}</td></tr>"
        
        with open(o_f, "w") as f:
            f.write(generate_html(r_h))
        print("Success")
    except Exception as e:
        sys.exit(1)
