import requests
from bs4 import BeautifulSoup

URL = "https://svmcm.wb.gov.in/page/about.php"
DIRECTORATE = ["DTE","DTE&T","DME"]
headers= ['DIRECTORATE', 'COURSE', 'Eligibility Criteria', 'SCHOLARSHIP RATE PER MONTH (RS.)']
async def get_svmcm_about():
    data = []
    data.append({'source':URL})
    try:
        response = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'})
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        rows = soup.find_all(['tr'])
        for row in rows:
            cells = row.find_all(['td'])
            if len(cells) > 0:
                directorate_name = cells[0].text.strip()
                if directorate_name in ["DTE&T", "DME","DTE"]:
                    row_data = {}
                    for i, header in enumerate(headers):
                        if i < len(cells):
                            row_data[header] = cells[i].text.strip()
                    data.append(row_data)
    except requests.exceptions.RequestException as e:
        data.append(f"An error occurred while fetching the URL ({URL}): {e}")
    except Exception as e:
        data.append(f"An error occurred during parsing: {e}")
    return data


if __name__=="__main__":
    for i in get_svmcm_about():
        print(i)