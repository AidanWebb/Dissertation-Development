from flask import Flask
from flask_socketio import SocketIO, join_room, leave_room
import os

import processing.middleware as middleware
from blueprints.api import api
from blueprints.error_handlers import error_handlers
from blueprints.website import website
from processing import filters
from database.chatRooms import sendMessage, receiveMessages


# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY']

# Register blueprints
app.register_blueprint(website)
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(error_handlers)

# Middleware
app.before_request(middleware.before_request)
app.after_request(middleware.apply_content_version)

# Initialize Flask-SocketIO
socketio = SocketIO(app)


# WebSocket event handlers
@socketio.on('connect')
def handle_connect():
    print('User connected')


@socketio.on('disconnect')
def handle_disconnect():
    print('User disconnected')


@socketio.on('join_conversation')
def on_join(data):
    room = data['room']
    join_room(room)

    chat_history = receiveMessages(room)
    socketio.emit('chat_history', {'history': chat_history}, room=room)



@socketio.on('leave_conversation')
def on_leave(data):
    try:
        room = data['room']
        leave_room(room)
        print(f'User left room: {room}')
    except Exception as e:
        print(f'Error leaving room: {str(e)}')


@socketio.on('send_message')
def handle_send_message(data):
    try:
        room = data['room']
        sender = data.get('sender')
        message = data.get('message')

        # Store the message in DynamoDB
        sendMessage(room, sender, message)  # Assuming room acts as the receiver or unique identifier for the chat session

        # Debugging log
        print(f'Sending message from {sender} to room {room}: {message}')

        # Emit the message to other clients in the room
        socketio.emit('receive_message', {'sender': sender, 'message': message}, room=room)
    except Exception as e:
        print(f'Error sending message: {str(e)}')


# Serve the app
if __name__ == '__main__':
    socketio.run(app)
