from app.model.TaiexModel import Taiex
from app import db
from sqlalchemy import desc
from app.utils.crawler import Crawler

def get_taiex():
    return Taiex.query.order_by(desc(Taiex.StartDate)).limit(5).all()

def update_taiex():
    taiex_new = Crawler().taiex_content
    print(taiex_new)
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