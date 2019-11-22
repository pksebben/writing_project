from flask import Blueprint, render_template, abort, redirect, request

from api import create_user, create_chunk, read_chunk
from exceptions import UserExistsError

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
    except UserExistsError:
        return redirect('/signup/userexists')
