from flask import jsonify, request, session
from classes.status import Status
from classes.errors import OKException
import database.user as user_db
from . import api

@api.route('/auth/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if data['password'] != data['confirm_password']:
        raise OKException(Status.PASSWORD_CONFIRMATION_FAILED)
    user_db.add_user(data['email'], data['password'], data['username'])
    return jsonify(Status.dict(Status.SUCCESS))


@api.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = user_db.get_user(data['email'])
    if user['password'] != data['password']:
        raise OKException(Status.INCORRECT_PASSWORD)
    session['user'] = user['email']
    return jsonify(Status.dict(Status.SUCCESS))
