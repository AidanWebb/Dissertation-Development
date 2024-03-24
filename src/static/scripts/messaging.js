$(document).ready(function () {
    var chatLogs = $('#chatLogs');
    var sender = $('#sender').val();
    var receiver = null;

    // Retrieve the user's private key from the hidden input field
    var privateKeyPem = $('#userPrivateKey').val();
    var privateKey = forge.pki.privateKeyFromPem(privateKeyPem);

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // Function to append messages to chat logs
    function appendMessage(username, message) {
        var messageElement = $('<div>').addClass('message').text(`${username}: ${message}`);
        chatLogs.append(messageElement);
        chatLogs.scrollTop(chatLogs.prop('scrollHeight'));
    }

    $('.user').click(function () {
        $('#chatLogs').empty();
        receiver = $(this).data('username');
        $('#headerText').text("Chatting with " + receiver);
        socket.emit('join_conversation', {'room': [sender, receiver].sort().join('_')});

        // Load chat history for the selected user
        // This is a pseudo-code function, replace it with your actual implementation
        //loadChatHistory(receiver, function (history) {
            //history.forEach(function (messageData) {
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

        // Optimistically append the message to the chat log
        appendMessage(sender, message);
        $('#messageInput').val('');
    });

    socket.on('receive_message', function (data) {
        try {
            var encryptedMessageBytes = forge.util.decode64(data.message);
            var decryptedMessage = forge.util.decodeUtf8(privateKey.decrypt(encryptedMessageBytes, 'RSA-OAEP'));
            appendMessage(data.sender, decryptedMessage);
        } catch (error) {
            console.error('Decryption error:', error);
        }
    });

    socket.on('connect', function () {
        console.log('Connected to WebSocket server');
    });
});
