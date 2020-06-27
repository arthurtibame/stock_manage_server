import requests
from datetime import datetime, timedelta
import json
from flask import session
from urllib.parse import quote, unquote
import pandas as pd

class Crawler(object):

    def __init__(self):

        self.taiex_content = self.__taiex_crawler()  # return list
        self.yield_rate = self.__yield_rate_crawler()

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

        NOW = datetime.now().date()
        TaiexUrl = f'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date={NOW.strftime("%Y%m%d")}&type=IND'
        #TaiexUrl = f'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date={str(20200514)}&type=IND'
        res = requests.post(TaiexUrl)

        try:
            json_content = json.loads(res.text)['data1'][1]
            closing_index = json_content[1].replace(',', '')
            index_spread = json_content[2][-5] + json_content[3]

            # date to string time
            str_start_date = self.__objdateConverter(NOW, case=1)
            str_end_date = self.__objdateConverter(NOW, case=2)

            # strftime 2 strptime --> type = datetime
            start_date_time = self.__strdateConverter(str_start_date)
            end_date_time = self.__strdateConverter(str_end_date)

            return [closing_index, index_spread, start_date_time, end_date_time]

        except:
            return list()

    def __objdateConverter(self, obj_date, case=1):
        """
        date 物件轉 strftime + 指定時間
        """
        if case == 1:
            return obj_date.strftime("%Y%m%d") + "14:00:00:00"
        elif case == 2:
            return (obj_date + timedelta(days=1)).strftime("%Y%m%d") + "13:59:59:00"
        else:
            return False

    def __strdateConverter(self, str_datetime):
        """
        strftime 轉 strptime 
        """
        return datetime.strptime(str_datetime, "%Y%m%d%H:%M:%S:%f")
