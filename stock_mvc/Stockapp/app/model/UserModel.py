from app import db

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(10),unique=True)
    password = db.Column(db.String(16))

    def __init__(self,username,password):
        self.username  = username
        self.password = password
        
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

    