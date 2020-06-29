from app import db
from datetime import datetime

class ChooseShortTermStrongStock(db.Model):
    __tablename__ = 'TodayStock'
    # Manual added cols
    id = db.Column(db.Integer,primary_key=True)
    StockCode = db.Column(db.Integer)
    StockName = db.Column(db.String(20))
    StartDate = db.Column(db.DateTime)
    EndDate  = db.Column(db.DateTime)
    OpeningPrice = db.Column(db.Float)
    ClosingPrice = db.Column(db.Float)
    DayHighPrice = db.Column(db.Float)
    DayLowPrice = db.Column(db.Float)
    PriceSpread = db.Column(db.Float)
    TradeQuantity = db.Column(db.Integer)
    TradeAmount = db.Column(db.Integer)
    StockType = db.Column(db.Integer)
    VolumeIncrease = db.Column(db.Float) 
    PreLegalBuy = db.Column(db.Float) 
    # Auto added cols
    CreateTime = db.Column(db.DateTime, default=datetime.utcnow)
    ModifyTime = db.Column(db.DateTime, default=datetime.utcnow)

    def __inti__(self, StockCode, StockName, OpeningPrice, ClosingPrice, DayHighPrice, DayLowPrice, PriceSpread, TradeQuantity, TradeAmount, StockType, StartDate, EndDate, VolumeIncrease, PreLegalBuy):
        self.StockCode = StockCode
        self.StockName = StockName
        self.OpeningPrice = OpeningPrice
        self.ClosingPrice = ClosingPrice
        self.DayHighPrice = DayHighPrice 
        self.DayLowPrice = DayLowPrice
        self.PriceSpread = PriceSpread
        self.TradeQuantity = TradeQuantity
        self.TradeAmount = TradeAmount
        self.StockType = StockType       
        
        self.VolumeIncrease =  VolumeIncrease
        self.PreLegalBuy = PreLegalBuy

        self.StartDate = StartDate
        self.EndDate = EndDate