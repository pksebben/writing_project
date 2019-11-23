import datetime as dt

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError


import config
from model import User, UserAuth, UserProfile, Chunk
from exceptions import UserExistsError

meta = MetaData()
engine = create_engine(config.db_string)
Session = sessionmaker(bind=engine)
session = Session()

def create_user(email, password, name):
    try:
        user = User(created=dt.datetime.now())
        user.auth = UserAuth(name=name, password=password, email=email)
        session.add(user)
        session.commit()
    except IntegrityError as err:
        session.rollback()
        raise err.orig

def create_chunk(author, text, parent=None, children=None):
    try:
        chunk  = Chunk(text=text,author=author, parent=parent) # should author be author.id?
        session.add(chunk)
        session.commit()
        print("am I a dumbass?")
        print(chunk.id)
        return chunk.id
    except IntegrityError as err:
        session.rollback()
        raise err.orig

    
def read_chunk(chunkid):
    try:
        chunktext = session.query(Chunk).get(chunkid).text
        return chunktext
    except Exception:
        raise
