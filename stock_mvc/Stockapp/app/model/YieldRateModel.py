from app.utils.crawler import Crawler

class YieldRate(object):
    
    def __init__(self):
        self.__list = Crawler().yield_rate
        self.StockPrice = self.__stock_price_list()
        self.StockName = self.__stock_name_list()
        self.DividendMoney  = self.__dividend_money_list()
        self.DividendStock  = self.__dividend_stock_list()
        self.DividendYield  = self.__dividend_yield_list()
        self.UpType = self.__up_type_list()
    def __stock_price_list(self):
        return [content['StockPrice'] for content in self.__list]        
        
    def __stock_name_list(self):
        return [content['StockName'] for content in self.__list]        
    
    def __dividend_money_list(self):
        return [content['DividendMoney'] for content in self.__list]        
    
    def __dividend_stock_list(self):
        return [content['DividendStock'] for content in self.__list]        
    
    def __dividend_yield_list(self):
        return [content['DividendYield'] for content in self.__list]        
    
    def __up_type_list(self):
        return [content['UpType'] for content in self.__list]        
