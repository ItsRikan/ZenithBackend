import requests
from bs4 import BeautifulSoup

URL = "https://svmcm.wb.gov.in/page/application_procedure.php"

async def get_svmcm_schedule():
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
        table = soup.find('table',class_="table table-bordered")
        rows = table.find('tbody').find_all('tr')
        headers =[]
        for th in table.find_all('th'):
            headers.append(th.text.strip())
        for row in rows:
            row_to_insert={}
            cells = row.find_all('td')
            for i,header in enumerate(headers):
                row_to_insert[header] = cells[i].text.strip()
            data.append(row_to_insert)


    except requests.exceptions.RequestException as e:
        data.append(f"An error occurred while fetching the URL ({URL}): {e}")
    except Exception as e:
        data.append(f"An error occurred during parsing: {e}")
    return data

