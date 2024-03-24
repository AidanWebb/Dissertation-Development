$(document).ready(function () {
    var chatLogs = $('#chatLogs');
    var sender = $('#sender').val();
    var receiver = null;

    // Retrieve the user's private key from the hidden input field
    var privateKeyPem = $('#userPrivateKey').val();
    var privateKey = forge.pki.privateKeyFromPem(privateKeyPem);

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // Updated function to append messages to chat logs with message type
    function appendMessage(username, message, type) {
        var messageElement = $('<div>').addClass('message').addClass(type).text(`${username}: ${message}`);
        chatLogs.append(messageElement);
        chatLogs.scrollTop(chatLogs.prop('scrollHeight'));
    }

    $('.user').click(function () {
        $('#chatLogs').empty();
        receiver = $(this).data('username');
        $('#headerText').text("Chatting with " + receiver);
        socket.emit('join_conversation', {'room': [sender, receiver].sort().join('_')});
    });

    $('#send-button').click(function () {
        var message = $('#messageInput').val();
        if (!receiver) {
            alert("Select a user to chat with.");
            return;
        }
        var publicKeyPem = $(`.contactPublicKey[data-username="${receiver}"]`).val();
        var publicKey = forge.pki.publicKeyFromPem(publicKeyPem);

        var encryptedMessage = forge.util.encode64(publicKey.encrypt(forge.util.encodeUtf8(message), 'RSA-OAEP'));
        socket.emit('send_message', {
            'sender': sender,
            'message': encryptedMessage,
            'receiver': receiver,
            'room': [sender, receiver].sort().join('_')
        });

        // Optimistically append the sent message to the chat log with 'sent' type
        appendMessage(sender, message, 'sent');
        $('#messageInput').val('');
    });

    socket.on('receive_message', function (data) {
        try {
            var encryptedMessageBytes = forge.util.decode64(data.message);
            var decryptedMessage = forge.util.decodeUtf8(privateKey.decrypt(encryptedMessageBytes, 'RSA-OAEP'));
            // Append the received message to the chat log with 'received' type
            appendMessage(data.sender, decryptedMessage, 'received');
        } catch (error) {
            console.error('Decryption error:', error);
        }
    });

    socket.on('connect', function () {
        console.log('Connected to WebSocket server');
    });
});
