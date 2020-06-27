from app import db
from app.model.YieldRateModel import YieldRate
from flask import session
import json
from ast import literal_eval
import requests

def callback(contents):
    url = r'http://zhix6842.ga:5000/api/insertHighDividendStock'
    contents = literal_eval(contents)    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "api-key": session['cookie']
    }

    data = {
        "stockCode": contents["StockCode"],
        "stockName": contents["StockName"],
        "dividendMoney": contents["DividendMoney"],
        "dividendStock": contents["DividendStock"],
        "dividendYield": contents["DividendYield"],
        "upType": contents["UpType"]
    }
    
    res = requests.post(url, json=data, headers=headers)
    res_msg = json.loads(res.text)['message']   
    return res_msg
        
