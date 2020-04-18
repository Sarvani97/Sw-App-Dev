import os
import sys

from flask import Flask, render_template, request, session
#from flask_session import Session
#from sqlalchemy import create_engine
#from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
#if not os.getenv("DATABASE_URL"):
    #raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
#app.config["SESSION_PERMANENT"] = False
#app.config["SESSION_TYPE"] = "filesystem"
#Session(app)

# Set up database
#engine = create_engine(os.getenv("DATABASE_URL"))
#db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return "Project 1: TODO"

@app.route("/register", methods=["GET","POST"])
def response():
    #if session.get("notes") is None:
        #session.notes = []
    if request.method == "POST":
        id = request.form.get("email")
        #session["notes"].append(note)
        print(id, file=sys.stdout)
        return render_template("register.html",headline="successfully registered "+id)
    elif request.method == "GET":
        return render_template("register.html",headline="")


