$(document).ready(function () {
    var chatLogs = $('#chatLogs'); // Cache the selector

    var sender = $('#sender').val();
    var receiver = null;

    // Establish WebSocket connection globally
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    $('.user').click(function () {
        $('#chatLogs').empty();
        var clickedUsername = $(this).attr('data-username');
        $('#headerText').text("Chatting with " + clickedUsername);
        receiver = clickedUsername;
        var parties = [sender, receiver].sort();
        let room = parties.join('_');
        socket.emit('join_conversation', {'room': room});
    });

    $('#send-button').click(function () {
        var messageInput = $('#messageInput');
        var message = messageInput.val();
        var parties = [sender, receiver].sort();
        let room = parties.join('_');

        socket.emit('send_message', {'sender': sender, 'message': message, 'receiver': receiver, 'room': room});
        messageInput.val(''); // Clear the input after sending
    });


    socket.on('chat_history', function (data) {
        console.log(data);
        data.history.forEach(function (message) {
            var messageElement = $('<div>').addClass('message').text(`${message.sender}: ${message.message}`);  // Adjusted to use 'message' instead of 'content'
            chatLogs.append(messageElement);
        });
        chatLogs.scrollTop(chatLogs.prop('scrollHeight'));
    });


    socket.on('receive_message', function (data) {
        var messageElement = $('<div>').addClass('message').text(`${data.sender}: ${data.message}`);
        chatLogs.append(messageElement); // Use the cached selector
        chatLogs.scrollTop(chatLogs.prop('scrollHeight')); // Scroll to the bottom
    });

    // Handle connection event
    socket.on('connect', function () {
        console.log('Connected to the WebSocket server');
    });
});
