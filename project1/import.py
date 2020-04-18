import os
import csv
import sys

from flask import Flask
from models import Book

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

def main():
    with app.app_context():
        db.create_all()
        f = open("books.csv")
        read = csv.reader(f)

        for isbn, bname, author, year in read:
            binfo = Book(isbn=isbn, bname=bname, author=author, year=year)
            db.session.add(binfo)
            db.session.commit()
        print("Successfully added", file=sys.stdout)

if __name__ == "__main__":
    main()