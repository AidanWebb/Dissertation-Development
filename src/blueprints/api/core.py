import logging
from . import api
from flask import request, jsonify
from processing.auth import requires_auth
import database.user as user_db
import database.chatRooms as chatRoom_db
from classes.status import Status
from processing.crypto import encrypt_message
from database.user import fetch_public_key

@api.route('/add-friend', methods=['POST'])
@requires_auth
def add_friend(username):
    data = request.get_json()
    friend_username = data['username']

    # Add the friend to the user's friend list
    user_db.add_friend(username, friend_username)

    # Attempt to fetch the friend's public key
    public_key = fetch_public_key(friend_username)
    if public_key:
        logging.info(f"Public key for {friend_username} retrieved successfully during friend addition.")
        return jsonify({'status': 'success', 'public_key': public_key})
    else:
        logging.warning(f"Failed to retrieve public key for {friend_username} during friend addition.")
        # Decide on how you want to handle the scenario where a friend is added but their public key isn't found
        return jsonify({'status': 'success', 'message': 'Friend added, but public key not found.'}), 200


@api.route('/delete-friend', methods=['POST'])
@requires_auth
def delete_friend(username):
    data = request.get_json()
    user_db.delete_friend(username, data['username'])
    return jsonify(Status.dict(Status.SUCCESS))


@api.route('/send-message', methods=['POST'])
@requires_auth
def send_message():
    data = request.get_json()
    sender = data.get('sender')
    receiver = data.get('receiver')
    message = data.get('message')
    if not sender or not receiver or not message:
        return jsonify(Status.dict(Status.ERROR, message="Missing sender, receiver, or message"))

    # Encrypt the message before sending
    encrypted_message = encrypt_message(message)

    chatRoom_db.sendMessage(sender, receiver, encrypted_message)
    return jsonify(Status.dict(Status.SUCCESS))


@api.route('/receive_messages', methods=['GET'])
@requires_auth
def get_messages():
    sender = request.args.get('sender')
    receiver = request.args.get('receiver')
    if not sender or not receiver:
        return jsonify(Status.dict(Status.USER_NOT_FOUND, message="Missing sender or receiver"))
    messages = chatRoom_db.recieveMessages(sender, receiver)
    return jsonify(messages)