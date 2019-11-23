from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

from api import create_user, create_chunk, read_chunk
from exceptions import UserExistsError

bob = {'name':'bob','email':'bob@gmail.com','password':'pass'}
tom = {'name':'tom','email':'tomgmail.com','password':''}
dick = {'name':'dick','email':'dick@gmail','password':'!@#$%'}
hairy = {'name':'hairy','email':'hairy@gmail.com','password':';'}
zonenhoogstanges = {'name':'epheseus','email':'usidor@gmail.com','password':'you shall not pass'}

usertable = [bob,tom,dick,hairy,zonenhoogstanges]

def testuserinput(user):
    try:
        create_user(name=user['name'],
                    password=user['password'],
                    email=user['email']
        )
    except UniqueViolation as err:
        print(err)

def testsuite():
    for i in usertable:
        testuserinput(i)
    
