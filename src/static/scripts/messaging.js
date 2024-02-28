var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

function determineRoomIdentifier(clickedUsername) {
    var currentUserUsername = $('h1').text().replace('Welcome back ', '').trim();
    var usernames = [currentUserUsername, clickedUsername].sort();
    return usernames.join('_');
}

$(document).ready(function () {
    $('.user').click(function() {
        var clickedUsername = $(this).attr('data-username');
        $('#headerText').text("Chatting with " + clickedUsername);

        var room = determineRoomIdentifier(clickedUsername);
        socket.emit('join_conversation', { room: room });
    });

    $('#send-button').click(function() {
        var messageInput = $('#messageInput');
        var message = messageInput.val();
        var receiver = $('#headerText').text().replace('Chatting with ', '');
        var sender = $('h1').text().replace('Welcome back ', '').trim();
        var room = determineRoomIdentifier(receiver);

        // Emit the message to the server with sender information
        socket.emit('send_message', {sender: sender, message: message, receiver: receiver, room: room});
        messageInput.val(''); // Clear the input after sending
    });

    socket.on('receive_message', function(data) {
        var chatLogs = $('#chatLogs');
        var messageElement = $('<div>').addClass('message').text(`${data.sender}: ${data.message}`);
        chatLogs.append(messageElement);

        chatLogs.scrollTop(chatLogs.prop('scrollHeight'));
    });

    socket.on('connect', function () {
        console.log('Connected to the WebSocket server');
    });
});
