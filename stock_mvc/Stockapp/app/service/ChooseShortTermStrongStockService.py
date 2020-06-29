from app.model.ChooseShortTermStrongStockModel import ChooseShortTermStrongStock
from app import db
from sqlalchemy import desc, text
from datetime import datetime, timedelta
from app.utils.TimeDealer import TheTime
import requests
import json
import ast 

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
}


def insert_short_term_strong_stock(content):#content=dict()):
    """
    參數帶選取強勢股內容, 這邊利用爬蟲處理 其餘資料
    先判斷上市上櫃 判斷完成且資料已更新的話新增到db       
    """        
    content = ast.literal_eval(content) 
    print("GOT SERVICE:  ", type(content))
    final_result = FromDict2StockCode(content)
    if type(final_result) == type(dict()):
        print(final_result)
        try:
            newShortTermStrongStock = ChooseShortTermStrongStock(                                
                StockCode = final_result["StockCode"],
                StockName = final_result["StockName"],
                StartDate = final_result['StartDate'],
                EndDate = final_result['EndDate'],
                OpeningPrice = final_result['OpeningPrice'],
                ClosingPrice = final_result['ClosingPrice'],
                DayHighPrice = final_result['DayHighPrice'],
                DayLowPrice = final_result['DayLowPrice'],
                PriceSpread = final_result['PriceSpread'],
                TradeQuantity = final_result['TradeQuantity'],
                TradeAmount = final_result['TradeAmount'],
                StockType = final_result['StockType'],
                VolumeIncrease = final_result['VolumeIncrease'],
                PreLegalBuy = final_result['PreLegalBuy']                                                 
                )
            db.session.add(newShortTermStrongStock)
            db.session.commit()            
        except:
            return "db error"
        return 'successfully'
    else:
        return "There is no data updated today "

def FromDict2StockCode(content=dict()): 
    """
    # 處理回傳來的dictionary 擷取股票代馬
    # 再去 call OTCcompany or PublicCompany
    # 如果 result 回傳 None 回傳 尚未更新的訊息
    """
    
    print("=======================================================")    
    UpType = content['UpType']
    
    print(UpType)
    if  UpType == "上櫃":
        result = OTCcompany(content['StockCode'])
        if result != False:
            return MergeResult(content, result)

    elif UpType == "上市":
        result = PublicCompany(content['StockCode'])
        if result != False:
            return MergeResult(content, result)    

    return False


def OTCcompany(StockCode):  # 上櫃公司
    """
    這邊處理上櫃公司資料, 回傳其餘資料是 
    PChome 那邊沒有的到 insert_short_term_strong_stock
    """
    now_date = datetime.now().date()
    year = str(now_date.year - 1911)
    if len(list(str(now_date.month))) == 1:
        month = f"0{str(now_date.month)}"
    else:
        month = f"{str(now_date.month)}"
    chinese_date = f"{year}/{month}"
    
    global headers
    OTCcompanyUrl = f'https://www.tpex.org.tw/web/stock/aftertrading/daily_trading_info/st43_result.php?l=zh-tw&d={chinese_date}&stkno={str(StockCode)}&_=1593153458642'
    res = requests.post(OTCcompanyUrl, headers=headers)
    latest_data_date = json.loads(res.text)['aaData'][-1][0]
    # check the data updated or not
    callback_result =  ChkUpdateDate(latest_data_date)
    if callback_result == True:
        json_content = json.loads(res.text)['aaData'][-1][1:]
        result = list()
        i = 0
        for f in json_content:
            if i<2:
                result.append(num(f)*1000)
            else:
                result.append(num(f))
            i+=1
        return result
    else:
        return False

def PublicCompany(StockCode):  # 上市公司
    """
    這邊處理上市公司資料 回傳其餘資料是 
    PChome 那邊沒有的到 insert_short_term_strong_stock
    """
    today_date = datetime.now().date().strftime("%Y%m%d")
    global headers
    PublicCompanyUrl = f'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={today_date}&stockNo={str(StockCode)}'
    res = requests.post(PublicCompanyUrl, headers=headers)
    
    latest_data_date = json.loads(res.text)['data'][-1][0]
    # check the data updated or not
    callback_result =  ChkUpdateDate(latest_data_date)
    if callback_result == True:
        json_content = json.loads(res.text)['data'][-1][1:-1]
        result = [num(f) for f in json_content]
        return result
    else: 
        return False

def ChkUpdateDate(latest_data_date): # 檢查資料是否更新
    def transform_date(date):   #民國轉西元
        y, m, d = date.split('/')
        return str(int(y)+1911) + '/' + m  + '/' + d
    
    latest_data_date = datetime.strptime(transform_date(latest_data_date) ,"%Y/%m/%d").date()
    if latest_data_date == datetime.now().date():
        return True
    else:
        return False
    

def MergeResult(content=dict(), result=list()):
    
    content['TradeQuantity'] = result[0]
    content['TradeAmount'] = result[1]
    content['OpeningPrice'] = result[2]
    content['DayHighPrice'] = result[3]
    content['DayLowPrice'] = result[4]
    content['ClosingPrice'] = result[5]
    content['PriceSpread'] = result[6]
    content['StockType'] = 1
    content['StartDate'] = TheTime().start_date_time
    content['EndDate'] = TheTime().end_date_time
    return content

def num(s):
    try:
        return int(s.replace(",",""))
    except ValueError:
        return float(s)
