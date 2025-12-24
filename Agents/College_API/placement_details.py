import requests
from bs4 import BeautifulSoup

URL = "https://www.bcrec.ac.in/placements"
async def get_top_placement_records():
    data = []
    data.append({'source':URL})
    try:
        response = requests.get(URL, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',})
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table',class_="table-bordered")
        headers = []
        for th in table.find_all('th'):
            headers.append(th.text.strip())
        rows = table.find('tbody').find_all('tr')
        for row in rows:
            cells = row.find_all(['td'])
            if len(cells) > 0:
                    row_data = {}
                    for i, header in enumerate(headers):
                        if i < len(cells):
                            row_data[header] = cells[i].text.strip()
                    data.append(row_data)
                    if len(data)>=5:
                        break
    except requests.exceptions.RequestException as e:
        data.append(f"An error occurred while fetching the URL ({URL}): {e}")
    except Exception as e:
        data.append(f"An error occurred during parsing: {e}")
    return data
