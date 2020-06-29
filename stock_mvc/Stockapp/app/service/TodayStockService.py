from app.model.TodayStockModel import TodayStock
from app import db
from sqlalchemy import desc,text

def get_today_stock():
    sql = text('SELECT * FROM TodayStock WHERE StockType = "0" AND EndDate = (SELECT MAX(EndDate) FROM TodayStock WHERE StockType = "0")')
    result = db.engine.execute(sql)
    return result
    

    #return Taiex.query.order_by(desc(Taiex.StartDate)).limit(5).all()