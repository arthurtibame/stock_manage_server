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
        shortTermStrongStockUrl = r'https://tw.screener.finance.yahoo.net/screener/ws?PickID=100042,100043,100213,1213,1214&PickCount=20&f=j&519'
        
        result_list = list()
        res = requests.post(shortTermStrongStockUrl)#, headers=headers, data=data)
        #soup = BeautifulSoup(res.text, 'lxml')
        json_list = json.loads(res.text)['items']
        for f in json_list:
            tmp_dict = dict()
            tmp_dict['StockCode'] = f['symid']
            tmp_dict['StockName'] =f['symname'] 
            tmp_dict['ClosingPrice'] =f['close_price']
            tmp_dict['PriceSpread'] =f['updn']
            tmp_dict['PriceSpreadRate'] =f['updn_rate']
            tmp_dict['DailyKvalue'] =f['B5']
            tmp_dict['UpType'] = self.__chkConpamyCategory(tmp_dict['StockCode'])

            result_list.append(tmp_dict)
        return result_list


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