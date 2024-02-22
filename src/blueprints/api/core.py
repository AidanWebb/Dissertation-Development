from . import api
from flask import request, jsonify
from processing.auth import requires_auth
import database.user as user_db
from classes.status import Status

@api.route('/add-friend', methods=['POST'])
@requires_auth
def add_friend(username):
    data = request.get_json()
    user_db.add_friend(username, data['username'])
    return jsonify(Status.dict(Status.SUCCESS))

@api.route('/delete-friend', methods=['POST'])
@requires_auth
def delete_friend(username):
    data = request.get_json()
    user_db.delete_friend(username, data['username'])
    return jsonify(Status.dict(Status.SUCCESS))