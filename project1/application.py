import os
import sys
import logging
import calendar
import time

from flask import Flask, render_template, request, session, redirect, url_for
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

# @app.route("/",methods=["GET", "POST"])
# def index():
#     return "hello!"



@app.route("/register", methods=["GET","POST"])
@app.route("register/<int:parameter>",methods=["GET","POST"])
def response(parameter=None):
    if request.method == "POST":
        id = request.form.get("email")
        if "." not in id:
            return render_template("register.html",headline="Enter a valid email address")
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
        s = ""
        if parameter == 1:
            s = "You entered wrong credentials"
        elif parameter == 2:
            s = "Not registered. Please register"
        return render_template("register.html",headline=s)

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

@app.route("/auth", methods=["POST"])
def authentication():
    name = request.form.get("email")
    psd = request.form.get("password")
    gen = request.form.get("gender")
    ag = request.form.get("age")
    add = request.form.get("address")
    check = USER.query.filter_by(email=name).first()
    if check is None:
        return redirect(url_for('response',parameter=2))
    
    if name == check.email and psd == check.password:
        if session.get(name) is None:
            session[name] = psd
        return redirect(url_for('foo',param=name))
    else:
        return redirect(url_for('response',parameter=1))

@app.route("/home/<param>", methods=["GET","POST"])
def foo(param):
    if request.method == "GET":
        if session.get(param) is not None:
            return render_template("home.html",headline=param)
        else:
            return "<h3>Login to contintue</h3>"


@app.route("/logout/<param>", methods=["POST"])
def logout(param):
    session[param] = None
    return redirect(url_for('response'))





