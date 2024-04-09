import logging
from . import api
from flask import request, jsonify
from processing.auth import requires_auth
import database.user as user_db
from classes.status import Status
from database.user import fetch_public_key

@api.route('/add-friend', methods=['POST'])
@requires_auth
def add_friend(username):
    data = request.get_json()
    friend_username = data['username']

    user_db.add_friend(username, friend_username)

    public_key = fetch_public_key(friend_username)
    if public_key:
        logging.info(f"Public key for {friend_username} retrieved successfully during friend addition.")
        return jsonify({'status': 'success', 'public_key': public_key})
    else:
        logging.warning(f"Failed to retrieve public key for {friend_username} during friend addition.")
        return jsonify({'status': 'success', 'message': 'Friend added, but public key not found.'}), 200


@api.route('/delete-friend', methods=['POST'])
@requires_auth
def delete_friend(username):
    data = request.get_json()
    user_db.delete_friend(username, data['username'])
    return jsonify(Status.dict(Status.SUCCESS))

