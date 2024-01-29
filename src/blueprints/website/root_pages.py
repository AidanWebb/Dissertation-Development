from flask import render_template, request, jsonify, redirect, url_for, session

from database import user as user_db
from processing.auth import requires_auth
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
    Returns the signup page for project where new users can sign up.
    """
    return render_template('signup.html')

@website.route('/auth-test')
@requires_auth
def auth_test(email):
    """
    Tests to see if a user is logged in
    """
    return email


@website.route('/chat_page')
@requires_auth
def chat_page(user):
    """
    Returns the page for logged in users or users who have finished signing up
    """
    return render_template('chat_page.html', user=user)

@website.route('/search_user', methods=['POST'])
@requires_auth
def searchUser():
    username = request.form['username']
    user_info = user_db.get_user_by_username(username)
    if user_info:
        return jsonify(user_info)
    else:
        return jsonify({"error": "User not found"}), 404

@website.route('/user/<email>', methods = ['GET'])
def get_user_info(email):
    user_info = user_db.get_user(email)
    if user_info:
        return jsonify(user_info)
    else:
        return jsonify({'error': 'User not found'}), 404


@website.route('/test/user/<email>')
def test_user_get(email):

    return jsonify(user_db.get_user(email))


@website.route('/test/user', methods=['POST'])
def test_user_insert():
    user_info = request.get_json()
    user = user_db.add_user(user_info['email'], user_info['age'], user_info['name'])
    return jsonify(user)
