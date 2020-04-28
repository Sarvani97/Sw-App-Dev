from flask_sqlalchemy import SQLAlchemy
<<<<<<< HEAD

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    name = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)

class Book(db.Model):
    __tablename__ = "books"
    isbn = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)

class Review(db.Model):
    __tablename__ = "reviews"
    isbn = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String, nullable=False)
=======
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

class Book(db.Model):
    __tablename__ = "book"
    isbn = Column(String(25), primary_key=True)
    bname = Column(String(50))
    author = Column(String(50))
    year = Column(Integer)

>>>>>>> c0e12bf948f38e0c7dc173ad9853596c20e40672
