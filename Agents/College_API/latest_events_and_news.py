import requests
from bs4 import BeautifulSoup

URL = "https://www.bcrec.ac.in/"
async def get_news_and_events():
    data = {'source':URL}
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
        events_and_news = soup.find_all('div',class_="sec5-inner")
        for ean in events_and_news:
            info = []
            heading = ean.find('h4').text.strip()
            for i in ean.find_all('div',class_="sec5-inner-card"):
                title = i.find('a').text.strip()
                text = i.find('p').text.strip()
                info.append({'title':title,'text':text})
            data[heading]=info      
    except requests.exceptions.RequestException as e:
        data['error']=f"An error occurred while fetching the URL ({URL}): {e}"
    except Exception as e:
        data['error']=f"An error occurred during parsing: {e}"
    return data
