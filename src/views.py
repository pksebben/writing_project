from flask import Blueprint, render_template, abort, redirect, request, session

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from psycopg2.errors import UniqueViolation, ProgrammingError

import api
import exceptions
from testing import testsuite

views = Blueprint('views', __name__,
                template_folder='templates')

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/about')
def about():
    return render_template('about.html')

@views.route('/signup/<failure>')
@views.route('/signup')
def signup(failure=None):
    return render_template('signup.html',failure=failure)

@views.route('/signin', methods=['POST'])
def signin():
    try:
        api.signin(email=request.form['email'], password=request.form['password'])
        return redirect('/')
    except exceptions.IncorrectPasswordErr:
        return redirect('/login/passwordfailure')
    except NoResultFound:
        return redirect('/login/nouserfailure')

@views.route('/login/<failure>')
@views.route('/login')
def login(failure=None):
    return render_template('/login.html',failure=failure)

@views.route('/newuser', methods=['POST'])
def newuser():
    try:
        api.create_user(name=request.form['name'],
                    password=request.form['password'],
                    email=request.form['email']
        )
        return redirect('/')
    except UniqueViolation as err:
        print(err)
        return redirect('/signup/userexists')

@views.route('/write/<parentchunkid>')
@views.route('/write')
def writesomething(parentchunkid = 0):
    if parentchunkid == 0:
        print('title required')
        requiretitle = True
    else:
        print('no title req')
        requiretitle = False
    if session['userid']:
        return render_template('writesomething.html', parent=api.read_chunk(parentchunkid), requiretitle=requiretitle)
    else:
        return redirect('/login/signinbeforewriting')

@views.route('/read/<chunkid>')
@views.route('/read')
def readsomething(chunkid):
    chunk = api.read_chunk(chunkid)
    print(chunk.text)
    return render_template('readsomething.html', chunk=chunk)
    
@views.route('/submitchunk', methods=['POST'])
def submitchunk():
    print("submitting")
    print(request.form)
    try:
        chunkid = api.create_chunk(author=session['userid'],
                                   text=request.form['chunkbody'],
                                   parentid=request.form['parentid'],
                                   title=request.form['title']
        )
        addstring = '/read/' + str(chunkid)
        return redirect(addstring)
    except IntegrityError as err:
        print(err.orig)
        return redirect('/write')
    except ProgrammingError as err:
        raise(err.orig)

@views.route('/browse')
def browse():
    firstchapters = api.get_index()
    return render_template('browse.html', index=firstchapters)

# ##################################################
# This is a testing route to make things quicker

@views.route('/testdb')
def testdb():
    testsuite()
    return redirect('/')
