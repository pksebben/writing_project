from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, Table, Text, FetchedValue
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

import config



Base = declarative_base()



# The base class for users that relate user data to other tables
class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    created = Column(String, nullable=False)
    auth = relationship("UserAuth", backref=backref("user", uselist=False), uselist=False)
    profile = relationship("UserProfile", backref=backref("user", uselist=False), uselist=False)

    
# The auth data for users
class UserAuth(Base):
    __tablename__ = 'user_auth'
    
    id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    name = Column(String(80), unique=False, nullable=False)
    password = Column(String(80), unique=False, nullable=False)
    email = Column(String(80), unique=True, nullable=False)


# All the data for a user.  Things that will be on their profile
class UserProfile(Base):
    __tablename__ = 'user_profile'
    
    id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    about = Column(String(2500))
    avatar = Column(String(80))
    birthday = Column(String(12))
    location = Column(String(20))


# Every story chunk will be stored here.  
class Chunk(Base):
    __tablename__ = "chunk"

    id = Column(Integer, primary_key=True, server_default=FetchedValue())
    title = Column(String)
    text = Column(Text, nullable=False)
    author = Column(Integer, ForeignKey("user.id"), nullable=False)
    parent = Column(Integer, ForeignKey("chunk.id"), nullable=True)
    children = relationship("Chunk")
    
    
#TODO: Factor out the engine connection string, present here and in db.py
engine = create_engine(config.db_string)

Base.metadata.create_all(engine)
