from . import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    user_handle = db.Column(db.String(15), unique=True)
    display_name = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    profile_picture_url = db.Column(db.String(100), nullable=True, default="./static/user_media/default_egg.png")
    tweets = db.relationship('Tweet', backref="owner")


class Tweet(db.Model):
    __tablename__ = 'tweet'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    tweet_owner_id = db.Column(db.String(15), db.ForeignKey('user.id'))
    # tweet_owner_handle = db.relationship('User')
    text = db.Column(db.String(140), nullable=False)
    likes = db.Column(db.Integer)
