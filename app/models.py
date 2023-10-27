from app import db
from datetime import datetime

class User(db.Model):
    userID = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    birthday = db.Column(db.DateTime)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.userName}>'