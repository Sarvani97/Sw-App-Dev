import os
import sys
import logging
import calendar
import time

from flask import Flask, render_template, request, session
from flask_session import Session
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import scoped_session, sessionmaker
#from sqlalchemy.ext.declarative import declarative_base
import models
from models import *

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

logging.basicConfig(filename='logger.log',level=logging.DEBUG)
# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db_session = scoped_session(sessionmaker(bind=engine))
db.query = db_session.query_property()
logging.debug("database sessions created")


app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def init_db():
    db.metadata.create_all(bind=engine)
init_db()

@app.route("/",methods=["GET", "POST"])
def index():
    return "hello!"

# @app.route("/")
# def index():
#     return "Project 1: TODO"

@app.route("/register", methods=["GET","POST"])
def response():
    if request.method == "POST":
        id = request.form.get("email")
        #print(id, file=sys.stdout)
        pwd = request.form.get("password")
        g = request.form.get("gender")
        a = request.form.get("age")
        addr = request.form.get("address")
        ch = USER.query.filter_by(email=id).first()
        if ch is not None:
            return render_template("register.html", headline=id+" Registered already. Login.")
        info = USER(email=id,password=pwd,gender=g,age=a,address=addr,timestamp=calendar.timegm(time.gmtime()))
        db.session.add(info)
        db.session.commit()
        if len(id) == 0:
            id += "Please enter the details"
        else:
            id += "Registered. Please login."
        return render_template("register.html",headline=id)
    elif request.method == "GET":
        return render_template("register.html",headline="")

<<<<<<< HEAD
=======
@app.route("/admin")
def database():
    users = USER.query.order_by(USER.timestamp).all()
    emails = []
    pwd = []
    gen = []
    ag = []
    ad = []
    stamps = []
    for i in users:
        emails.append(i.email)
        pwd.append(i.password)
        gen.append(i.gender)
        ag.append(i.age)
        ad.append(i.address)
        stamps.append(time.ctime(i.timestamp))
    return render_template("userlist.html", emails=emails,pwd=pwd,gen=gen,ag=ag,ad=ad,stamps=stamps,length=len(emails))
    




>>>>>>> 68f048244d387577fc9302c769f5db1cdc03974b

