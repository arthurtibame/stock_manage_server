import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import json
from flask import session
from urllib.parse import quote, unquote
import pandas as pd
from app.utils.TimeDealer import TheTime


class Crawler(object):

    def __init__(self):

        self.taiex_content = self.__taiex_crawler()  # return list
        self.yield_rate = self.__yield_rate_crawler()
        self.short_term_strong_stock = self.__short_term_strong_stock_crawler()

    def __yield_rate_crawler(self):

        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/5\
                    37.36 (KHTML,like Gecko) Chrome/83.0.4103.116 Safari/537.36",
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            "qry[]": ["dv", "money", "stock", "yield", "uptype"],
            "id[]": ["dv", "money", "stock", "yield", "uptype"],
            "val[]": ["0;12000", "0;100", "0;5", "5;100", "-0;-0"]
        }
        YieldRateUrl = r'https://stock.wespai.com/pick/choice'
        res = requests.post(YieldRateUrl, headers=headers, data=data)
        try:
            json_list = json.loads(res.text)
            json_content = self.__yield_rate_to_dict(json_list)
            return json_content
        except:
            return dict()

    def __yield_rate_to_dict(self, json_list):
        """
        原本是大list 包 小list
        轉為 大list 包 dict
        """
        Keys = ["StockCode", "StockName", "StockPrice",
                "DividendMoney", "DividendStock", "DividendYield", "UpType"]
        df = pd.DataFrame(json_list, index=None, columns=Keys).to_dict(orient='records')                
        return [dict(zip(Keys, content)) for content in json_list]

    def __taiex_crawler(self):
        """
        大盤爬蟲
        """

        NOW = datetime.now().date()
        TaiexUrl = f'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date={NOW.strftime("%Y%m%d")}&type=IND'
        #TaiexUrl = f'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date={str(20200514)}&type=IND'
        res = requests.post(TaiexUrl)

        try:
            json_content = json.loads(res.text)['data1'][1]
            closing_index = json_content[1].replace(',', '')
            index_spread = json_content[2][-5] + json_content[3]

            return [closing_index, index_spread, TheTime().start_date_time, TheTime().end_date_time]

        except:
            return list()
   
    def __short_term_strong_stock_crawler(self):    
        
        """
        短線強勢股爬蟲資料(成交量大於5日均量10% 3大法人買超量大): POST
        欄位名稱: 
            col_names = ['StockName', 'StockCode', 'ClosingPrice', "PriceSpread", "TradeQuantity", \
            "VolumeIncrease", "PreLegalBuy"]        
        """
        shortTermStrongStockUrl = r'https://pchome.megatime.com.tw/get_qranklist.php'
        
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/5\
                    37.36 (KHTML,like Gecko) Chrome/83.0.4103.116 Safari/537.36",
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest'
        }

        data = {
            "area_item1[]" : ["1_3", "5_1"],
            "item2[]" : ["1", "1"],
            "item3[]" : ["10", "1"],
            "page1" : "1"
        }

        res = requests.post(shortTermStrongStockUrl, headers=headers, data=data)
        soup = BeautifulSoup(res.text, 'lxml')
        uls = soup.find_all('ul', {"class":"ul_stock"})
        result = list()
        for ul in uls:
            counter = 0
            a = list()
            for li in ul.find_all('li'):
                if counter == 1 : # deal with second tag <li></li>
                    stockCode = li.a['href'][-9:-5]
                    stockName = li.a.text[:-6]
                    nameDealer = stockName.split()
                    if len(nameDealer) == 2:
                        stockName = nameDealer[0] + nameDealer[1]
                        a.append(stockName)    
                    else:
                        a.append(stockName)
                    # check check company category 
                    companyCategory = self.__chkConpamyCategory(stockCode)                    
                    a.append(stockCode)                   
                    a.append(companyCategory)
                elif counter !=7:
                    a.append(li.text)   
                counter+=1
            a = self.__StrongStock2dict(a[1:])            
            result.append(a)
        return result

    def __chkConpamyCategory(self, stock_id):
        
        """
        判斷上市上櫃回傳 "上市" or "上櫃" 至
        PChome Crawler
        """
        #這邊要帶 referer 才能爬取
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
            "Referer": "https://stock.pchome.com.tw/set_cookie.php"
        }
        
        url = f'https://pchome.megatime.com.tw/stock/sid{stock_id}.html'
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')
        companyCategory = soup.find("span", {"class":"companyCategory"}).span.text.split()[1]
        return companyCategory

    
    def __StrongStock2dict(self, content=list()):
        col_names = ['StockName', 'StockCode', 'UpType' , 'ClosingPrice', "PriceSpread", "TradeQuantity", \
            "VolumeIncrease", "PreLegalBuy"
            ]
        return dict(zip(col_names, content))

        
    

if __name__ == "__main__":
    from datetime import datetime, timedelta
    start_time = datetime.now()
    a = Crawler()
    #a.test
    #print(a.taiex_content)
    #print(a.yield_rate)
    b = a.shortTermStrongStock
    end_time = datetime.now()
    
    print((end_time - start_time).seconds)
    print(b)
    
