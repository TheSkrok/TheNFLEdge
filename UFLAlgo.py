import math

# PanaGeo Constants
PG_PI = {
    "1.0": 2.31415,
    "0.75": 2.31415,
    "0.5": 2.131415,
    "0.25": 2.031415,
    "0.0": 1.97531415
}
MODIFIER = 0.7314

def calculate_pags(team_ppqf, opp_ppqa, win_ratio):
    # Tier I: PCPS Calculation
    pi = PG_PI[str(win_ratio)]
    pcps = (team_ppqf + opp_ppqa) * pi
    
    # Tier II: PAGS Calculation (The 1984 Weighted Logic)
    if win_ratio >= 0.75:
        pags = math.ceil(pcps + MODIFIER)
    elif win_ratio <= 0.25:
        pags = math.floor(pcps - MODIFIER)
    else: # 50% Win Ratio
        pags = round(pcps)
    
    return pags
