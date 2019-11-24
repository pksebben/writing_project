import datetime as dt

from flask import session as sess
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

import config
import exceptions
from model import User, UserAuth, UserProfile, Chunk



meta = MetaData()
engine = create_engine(config.db_string)
Session = sessionmaker(bind=engine)
session = Session()

def signin(email, password):
    try:
        userauth =  session.query(UserAuth).filter_by(email=email).one()
        assert password == userauth.password
        sess['userid'] = userauth.user.id
    except AssertionError:
        raise exceptions.IncorrectPasswordErr
    except IntegrityError as err:
        raise err.orig

def create_user(email, password, name):
    try:
        user = User(created=dt.datetime.now())
        user.auth = UserAuth(name=name, password=password, email=email)
        session.add(user)
        session.commit()
    except IntegrityError as err:
        session.rollback()
        raise err.orig

"""create a story chunk.  On success, returns the id of the chunk."""
def create_chunk(author, text, parentid=None , children=None):
    if parentid == 'None':
        parentid = None
    try:
        chunk  = Chunk(text=text, author=author) # should author be author.id?
        chunk.parent = session.query(Chunk).get(parentid).id
        session.add(chunk)
        session.commit()
        return chunk.id
    except IntegrityError as err:
        session.rollback()
        raise err.orig

    
def read_chunk(chunkid):
    try:
        chunk = session.query(Chunk).get(chunkid)
        return chunk
    except Exception:
        raise
