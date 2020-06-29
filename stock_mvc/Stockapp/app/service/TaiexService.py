from app.model.TaiexModel import Taiex
from app import db
from sqlalchemy import desc
from app.utils.crawler import Crawler
from datetime import datetime
def get_taiex():
    return Taiex.query.order_by(desc(Taiex.StartDate)).limit(5).all()

def update_taiex():
    # check latest data 一天只能新增一筆
    latest_record = Taiex.query.order_by(desc(Taiex.StartDate)).limit(1).all()
    
    if latest_record[0].StartDate.date() != datetime.now().date(): 
        taiex_new = Crawler().taiex_content    
        if taiex_new:

            newTaiex = Taiex(
                ClosingIndex=taiex_new[0],
                IndexSpread=taiex_new[1], 
                StartDate=taiex_new[2], 
                EndDate=taiex_new[3]
            )
            db.session.add(newTaiex)
            db.session.commit()            
            return "1"
        else:
            return None
    else:
        return "今日已更新"