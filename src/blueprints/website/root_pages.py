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
def auth_test(username):
    """
    Tests to see if a user is logged in
    """
    return username


@website.route('/chat_page')
@requires_auth
def chat_page(username):
    """
    Returns the chat page for the logged-in user.
    """
    user = user_db.get_user(username)
    if not user:
        return "User not found", 404

    private_key = user_db.fetch_private_key(username)

    # Explicitly decode the private_key if it's a bytes object
    if isinstance(private_key, bytes):
        private_key = private_key.decode('utf-8')

    # Now private_key should be a string, safe to print
    print(private_key)

    contacts_public_keys = {}
    for friend_username in user.get('friends', []):
        public_key = user_db.fetch_public_key(friend_username)
        if public_key:
            contacts_public_keys[friend_username] = public_key

    return render_template('chat_page.html', user=user, private_key=private_key,
                           contacts_public_keys=contacts_public_keys)


@website.route('/user/<email>', methods=['GET'])
def get_user_info(username):
    user_info = user_db.get_user(username)
    if user_info:
        return jsonify(user_info)
    else:
        return jsonify({'error': 'User not found'}), 404


@website.route('/test/user/<email>')
def test_user_get(username):
    return jsonify(user_db.get_user(username))


@website.route('/test/user', methods=['POST'])
def test_user_insert():
    user_info = request.get_json()
    user = user_db.add_user(user_info['email'], user_info['age'], user_info['name'])
    return jsonify(user)
