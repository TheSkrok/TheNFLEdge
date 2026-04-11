import requests
from bs4 import BeautifulSoup
import csv

def scrape_ufl_to_csv():
    url = "https://www.theufl.com/standings"
    
    # Advanced headers to mimic a real browser session
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://google.com',
        'Connection': 'keep-alive'
    }

    session = requests.Session()
    
    try:
        response = session.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        teams_data = {}
        # The site may use a specific class or id; we'll try to find any table
        table = soup.find('table')

        if table:
            rows = table.find_all('tr')[1:] # Skip header
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 6:
                    name = cols[0].get_text(strip=True)
                    w = int(cols[1].get_text(strip=True) or 0)
                    l = int(cols[2].get_text(strip=True) or 0)
                    pf = cols[4].get_text(strip=True) or "0"
                    pa = cols[5].get_text(strip=True) or "0"
                    
                    teams_data[name] = {
                        'pf': pf,
                        'pa': pa,
                        'gp': str(w + l)
                    }
        else:
            # If still failing, the site is likely purely JavaScript-driven
            print("Table not found. The site may requires JavaScript execution.")
            return

        if teams_data:
            with open('ufl-data.csv', mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['name', 'pf', 'pa', 'gp'])
                for name, stats in teams_data.items():
                    writer.writerow([name, stats['pf'], stats['pa'], stats['gp']])
            print("Scrape complete. ufl-data.csv updated.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_ufl_to_csv()
