from app import db
from datetime import datetime

class Taiex(db.Model):
    __tablename__ = 'Taiex'
    id = db.Column(db.Integer,primary_key=True)
    ClosingIndex = db.Column(db.String(10))
    IndexSpread = db.Column(db.String(16))
    StartDate = db.Column(db.DateTime)
    EndDate  = db.Column(db.DateTime)
    CreateTime = db.Column(db.DateTime, default=datetime.utcnow)
    ModifyTime = db.Column(db.DateTime, default=datetime.utcnow)

    def __inti__(self, ClosingIndex, IndexSpread, StartDate, EndDate):
        self.ClosingIndex = ClosingIndex
        self.IndexSpread = IndexSpread
        self.StartDate = StartDate
        self.EndDate = EndDate