from . import db
from flask_login import UserMixin
from datetime import datetime


followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    user_handle = db.Column(db.String(15), unique=True)
    display_name = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    profile_picture_url = db.Column(db.String(100), nullable=True, default="./static/user_media/default_egg.png")
    # profile_description = db.Column(db.String(140), nullable=True)
    tweets = db.relationship('Tweet', backref="owner")

    # relationships
    liked = db.relationship('LikeTweet', foreign_keys="LikeTweet.liked_by",
                            backref="user", lazy="dynamic")

    def like_tweet(self, tweet):
        if not self.has_liked_tweet(tweet):
            like = LikeTweet(liked_by=self.id, liked_tweet=tweet.id)
            db.session.add(like)

    def unlike_tweet(self, tweet):
        if self.has_liked_tweet(tweet):
            LikeTweet.query.filter_by(
                liked_by=self.id,
                liked_tweet=tweet.id).delete()

    def has_liked_tweet(self, tweet):
        return LikeTweet.query.filter(
            LikeTweet.liked_by == self.id,
            LikeTweet.liked_tweet == tweet.id).count() > 0

    followed = db.relationship('User', secondary=followers,
                            primaryjoin=(followers.c.follower_id == id),
                            secondaryjoin=(followers.c.followed_id == id),
                            backref=db.backref('followers', lazy='dynamic'),
                            lazy='dynamic')

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0


class Tweet(db.Model):
    __tablename__ = 'tweet'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    tweet_owner_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    text = db.Column(db.String(140), nullable=False)
    likes = db.relationship('LikeTweet', backref='tweet', lazy='dynamic')
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class LikeTweet(db.Model):
    __tablename__ = 'like'

    id = db.Column(db.Integer, primary_key=True)
    liked_by = db.Column(db.Integer(), db.ForeignKey('user.id'))
    liked_tweet = db.Column(db.Integer(), db.ForeignKey('tweet.id'))


