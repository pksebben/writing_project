import datetime as dt

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app_config
from model import User, UserAuth, UserProfile, Chunk
from exceptions import UserExistsError

engine = create_engine(app_config.db_string)
Session = sessionmaker(bind=engine)
session = Session()

def create_user(email, password, name):
    q = session.query(UserAuth).filter_by(email=email)
    if session.query(q.exists()).scalar():
        raise UserExistsError
    else:
        user = User(created=dt.datetime.now())
        user.auth = UserAuth(name=name, password=password, email=email)
        session.add(user)
        session.commit()

def create_chunk(author, text, parent=None, children=None):
    chunk  = Chunk(text=text,author=author, parent=parent)
    session.add(chunk)
    session.commit()

def read_chunk(chunkid):
    raise NotImplementedError
