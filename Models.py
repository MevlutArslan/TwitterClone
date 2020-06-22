from . import db 
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    user_handle = db.Column(db.String(15), unique=True)
    display_name = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    tweets = db.relationship('Tweet', backref="owner")
    # profile_picture_url = Column(String(200), nullable=True)


class Tweet(db.Model):
    __tablename__ = 'tweet'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    tweet_owner_handle = db.Column(db.String(15), db.ForeignKey('user.id'))
    text = db.Column(db.String(140), nullable=False)
    likes = db.Column(db.Integer)
