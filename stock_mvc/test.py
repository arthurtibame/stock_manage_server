import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "Referer": "https://stock.pchome.com.tw/set_cookie.php"
}

url = f'https://pchome.megatime.com.tw/stock/sid=0051.html'
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'lxml')
companyCategory = soup.find("span", {"class":"companyCategory"}).span.text.split()[1]
print(companyCategory)
