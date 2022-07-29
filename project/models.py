from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kool.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
   id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
   data = db.Column(db.String(2000))
