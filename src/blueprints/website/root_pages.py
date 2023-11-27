from flask import render_template

from . import website


@website.route('/')
def home():
    """
    Returns the homepage for Project.
    """
    return render_template('index.html')

@website.route('/login')
def login():
    """
    Returns the login page for project where existing users can sign in.
    """
    return render_template('login.html')
@website.route('/signup')
def signup():
    """
    Returns the sign up page for new users to create an account.
    """
    return render_template('signup.html')
