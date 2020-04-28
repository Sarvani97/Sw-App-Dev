<<<<<<< HEAD
import sys, os, time, calendar;
from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from sqlalchemy import and_
=======
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
>>>>>>> c0e12bf948f38e0c7dc173ad9853596c20e40672
from models import *

app = Flask(__name__)

<<<<<<< HEAD
# Tell Flask what SQLAlchemy database to use.
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Link the Flask app with the database (no Flask app is actually being run yet).
db.init_app(app)
=======
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
>>>>>>> c0e12bf948f38e0c7dc173ad9853596c20e40672

with app.app_context():
    db.create_all()

<<<<<<< HEAD
@app.route("/", methods=["GET"])
def initial():
    return redirect(url_for('index'))

@app.route("/register", methods=["GET", "POST"])
@app.route("/register/<int:parameter>", methods=["GET", "POST"])
def index(parameter=None):
    if request.method == "POST":
        var1 = request.form.get("email")
        if "." not in var1:
            return render_template("registration_form.html", headline="Please enter valid email address")
        var2 = request.form.get("pwd")
        check = User.query.filter_by(name=var1).first()
        if check is not None:
            return render_template("registration_form.html", headline=var1+" Already Registered. Please Login.")
        user = User(name=var1, password=var2, timestamp=calendar.timegm(time.gmtime()))
        db.session.add(user)
        db.session.commit()
        if len(var1) == 0:
            var1 += "Enter details"
        else:
            var1 += " successfully registered. Please Login."
        return render_template("registration_form.html", headline=var1)
    else:
        variable = ""
        if parameter == 1:
            variable = "You have entered wrong credentials."
        elif parameter == 2:
            variable = "You are not registered. Please Register."
        return render_template("registration_form.html", headline=variable)


@app.route("/admin", methods=["GET"])
def admin():
    users = User.query.order_by(User.timestamp).all()
    names = []
    pwds = []
    timest = []
    for user in users:
        names.append(user.name)
        pwds.append(user.password)
        timest.append(time.ctime(user.timestamp))
    return render_template("registered_users.html", names=names, pwds=pwds, timest=timest, length=len(names))

@app.route("/auth", methods=["POST"])
def authentication():
    mail = request.form.get("email")
    pwd = request.form.get("pwd")
    check = User.query.filter_by(name=mail).first()
    if check is None:
        return redirect(url_for('index', parameter=2))
    if mail == check.name and pwd == check.password:
        if session.get(mail) is None:
            session[mail] = pwd
        return redirect(url_for('func', param=mail))
    else:
        return redirect(url_for('index', parameter=1))

@app.route("/home/<param>", methods=["GET", "POST"])
def func(param):
    if request.method == "GET":
        if session.get(param) is not None:
            return render_template("search.html", headline=param)
        else:
            return "<h1>Please Login to Access</h1>"
    else:
        value = request.form.get('dropdown')
        search = request.form.get('box')
        if len(search) == 0:
            return redirect(url_for('func', param=param))
        list = []
        if value == "ISBN":
            list = Book.query.filter(Book.isbn.ilike("%"+search+"%")).all()
        elif value == "Title":
            list = Book.query.filter(Book.title.ilike("%"+search+"%")).all()
        else:
            list = Book.query.filter(Book.author.ilike("%"+search+"%")).all()
        isbns = []
        titles = []
        authors = []
        for i in list:
            isbns.append(i.isbn)
            titles.append(i.title)
            authors.append(i.author)
        return render_template("homepage.html", length=len(list), isbns=isbns, titles=titles, authors=authors, headline=param, search=search)

@app.route("/book/<param>/<arg>", methods=["GET", "POST"])
def page(param, arg):
    if request.method == "GET":
        if session.get(param) is not None:
            bookObj = Book.query.filter_by(isbn=arg).first()
            list = Review.query.filter_by(isbn=arg).all()
            if len(list) == 0:
                users = ["-"]
                ratings = [0]
                reviews = ["-"]
                return render_template("review.html", headline=param,isbnObj=bookObj,users=users,ratings=ratings,reviews=reviews,length=1)    
            obj = Review.query.filter(and_(Review.isbn == arg, Review.name == param)).first()
            users = []
            ratings = []
            reviews = []
            for i in list:
                users.append(i.name)
                ratings.append(i.rating)
                reviews.append(i.review)
            if obj is None:
                return render_template("review.html",headline=param,isbnObj=bookObj,users=users,ratings=ratings,reviews=reviews,length=len(list))
            else:
                return render_template("reviewed.html",headline=param,isbnObj=bookObj,users=users,ratings=ratings,reviews=reviews,length=len(list))
        else:
            return "<h1>Please Login to Access</h1>"
    else:
        rating = request.form.get('rate')
        review = request.form.get('textarea')
        if rating is None or len(review) == 0:
            return redirect(url_for('page', param=param, arg=arg))
        reviewObj = Review(isbn=arg,name=param,rating=rating,review=review)
        db.session.add(reviewObj)
        db.session.commit()
        bookObj = Book.query.filter_by(isbn=arg).first()
        list = Review.query.filter_by(isbn=arg).all()
        users = []
        ratings = []
        reviews = []
        for i in list:
            users.append(i.name)
            ratings.append(i.rating)
            reviews.append(i.review)
        return render_template("reviewed.html",headline=param,isbnObj=bookObj,users=users,ratings=ratings,reviews=reviews,length=len(list))   
=======

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




>>>>>>> c0e12bf948f38e0c7dc173ad9853596c20e40672

@app.route("/logout/<param>", methods=["POST"])
def logout(param):
    session[param] = None
    return redirect(url_for('index'))