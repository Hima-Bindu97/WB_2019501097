from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db=SQLAlchemy()
class data(db.Model):
    __tablename__="data"
    Name=db.Column(db.String,primary_key=True,nullable=False)
    email=db.Column(db.String,nullable=False)
    password=db.Column(db.String,nullable=False)
    creationtimestamp=db.Column(db.DateTime(timezone=True),nullable=False)

    def __init__(self,Name,email,password):
        self.Name=Name
        self.email=email
        self.password=password
        self.creationtimestamp=datetime.now()