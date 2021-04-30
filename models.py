from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(256))
    email = db.Column(db.String(256))
    phone = db.Column(db.String(256))


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256))
    text = db.Column(db.String(256))


class Stats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(256))
    likes = db.Column(db.Integer)
    followers = db.Column(db.Integer)
    following = db.Column(db.Integer)
