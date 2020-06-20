from sqlalchemy import Integer, String, Column, Model


class User(Model):
    __tablename__ = 'user'

    userHandle = Column(String(15), unique=True, primary_key=True)
    username = Column(String(30), nullable=False)
    password = Column(String(20), nullable=False)
    # profilePictureUrl = Column(String(200), nullable=True)
    
    
class Tweet(Model):
    __tablename__ = 'tweet'

    id = Column(Integer, unique=True, primary_key=True)
    text = Column(String(140), nullable=False)
    likes = Column(Integer)
    
