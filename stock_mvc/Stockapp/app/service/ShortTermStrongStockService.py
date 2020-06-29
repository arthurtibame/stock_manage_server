from app.model.TodayStockModel import TodayStock
from app import db
from sqlalchemy import desc,text

def get_short_term_strong_stock():
    sql = text('SELECT * FROM TodayStock WHERE StockType = "1" AND EndDate = (SELECT MAX(EndDate) FROM TodayStock)')
    result = db.engine.execute(sql)
    return result

