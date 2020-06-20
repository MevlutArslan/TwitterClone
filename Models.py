from main import db


class User(db.Model):
    __tablename__ = 'user'

    userHandle = db.Column(db.String(15), unique=True, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    tweets = db.relationship('Tweet', backref="owner")
    # profilePictureUrl = Column(String(200), nullable=True)


class Tweet(db.Model):
    __tablename__ = 'tweet'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    tweetOwnerHandle = db.Column(db.String(15), db.ForeignKey('user.userHandle'))
    text = db.Column(db.String(140), nullable=False)
    likes = db.Column(db.Integer)
