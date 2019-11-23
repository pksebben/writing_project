from flask import Blueprint, render_template, abort, redirect, request

from sqlalchemy.exc import IntegrityError

from api import create_user, create_chunk, read_chunk
from exceptions import UserExistsError
from testing import testsuite

views = Blueprint('views', __name__,
                template_folder='templates')

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/about')
def about():
    return render_template('about.html')

@views.route('/signup')
def signup():
    return render_template('signup.html')

@views.route('/signup/userexists')
def signupagain():
    return render_template('signupagain.html')

@views.route('/newuser', methods=['POST'])
def newuser():
    try:
        create_user(name=request.form['name'],
                    password=request.form['password'],
                    email=request.form['email']
        )
        return redirect('/')
    except IntegrityError as err:
        print(err.orig)
        return redirect('/signup/userexists')

@views.route('/write')
def writesomething():
    return render_template('writesomething.html')

@views.route('/read/<chunkid>')
@views.route('/read')
def readsomething(chunkid):
    chunktext = read_chunk(chunkid)
    print(chunktext)
    return render_template('readsomething.html', chunktext=chunktext)
    
@views.route('/submitchunk', methods=['POST'])
def submitchunk():
    try:
        chunkid = create_chunk(author=1,
                    text=request.form['chunkbody']
        )
        addstring = '/read/' + str(chunkid)
        return redirect(addstring)
    except IntegrityError as err:
        print(err.orig)
        return redirect('/write')



# ##################################################
# This is a testing route to make things quicker

@views.route('/testdb')
def testdb():
    testsuite()
    return redirect('/')
