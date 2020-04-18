from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer
#from sqlalchemy.types import TIMESTAMP
#from sqlalchemy.ext.declarative import declarative_base
#from datetime import datetime

db = SQLAlchemy()
#base = declarative_base()

class USER(db.Model):
    __tablename__ = "USER"
    email = Column(String(50), primary_key=True)
    password = Column(String(50))
    gender = Column(String(25))
    age = Column(Integer)
    address = Column(String(120))
    timestamp = Column(Integer, nullable=False)

    # def __init__(self,email,password,gender,age,address,stamp):
    #     self.email = email
    #     self.password = password
    #     self.gender = gender
    #     self.age = age
    #     self.address = address
    #     self.stamp = stamp

    # def __repr__(self):
    #     return '<Registers %r>' %(self.email)

