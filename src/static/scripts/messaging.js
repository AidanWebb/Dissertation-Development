$(document).ready(function () {
    var chatLogs = $('#chatLogs');
    var sender = $('#sender').val();
    var receiver = null;

    var privateKeyPem = $('#userPrivateKey').val();
    var privateKey = forge.pki.privateKeyFromPem(privateKeyPem);

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    function appendMessage(username, message, type) {
        var existingMessages = $('.message').filter(function () {
            return $(this).text() === `${username}: ${message}` && $(this).hasClass(type);
        });

        if (existingMessages.length === 0) {
            var messageElement = $('<div>').addClass('message').addClass(type).text(`${username}: ${message}`);
            chatLogs.append(messageElement);
            chatLogs.scrollTop(chatLogs.prop('scrollHeight'));
        }
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
        var publicKeyPemReceiver = $(`.contactPublicKey[data-username="${receiver}"]`).val();
        var publicKeyReceiver = forge.pki.publicKeyFromPem(publicKeyPemReceiver);
        var encryptedMessageForReceiver = forge.util.encode64(publicKeyReceiver.encrypt(forge.util.encodeUtf8(message), 'RSA-OAEP'));

        var publicKeyPemSender = $('#userPublicKey').val();
        var publicKeySender = forge.pki.publicKeyFromPem(publicKeyPemSender);
        var encryptedMessageForSender = forge.util.encode64(publicKeySender.encrypt(forge.util.encodeUtf8(message), 'RSA-OAEP'));

        socket.emit('send_message', {
            'sender': sender,
            'message_receiver': encryptedMessageForReceiver,
            'message_sender': encryptedMessageForSender,
            'receiver': receiver,
            'room': [sender, receiver].sort().join('_')
        });

        appendMessage(sender, message, 'sent');
        $('#messageInput').val('');
    });

    socket.on('receive_message', function (data) {
        try {
            var encryptedMessageBytes = forge.util.decode64(data.message);
            var decryptedMessage = forge.util.decodeUtf8(privateKey.decrypt(encryptedMessageBytes, 'RSA-OAEP'));

            appendMessage(data.sender, decryptedMessage, 'received');
        } catch (error) {
            console.error('Decryption error:', error);
        }
    });

    socket.on('chat_history', function (data) {
        console.log(data);
        data.history.forEach(function (historyItem) {
            try {
                var encryptedMessageBytes;
                var decryptedMessage;

                if (historyItem.sender === sender) {
                    encryptedMessageBytes = forge.util.decode64(historyItem.message_sender);
                    decryptedMessage = forge.util.decodeUtf8(privateKey.decrypt(encryptedMessageBytes, 'RSA-OAEP'));
                    appendMessage(historyItem.sender, decryptedMessage, 'sent');
                } else {

                    encryptedMessageBytes = forge.util.decode64(historyItem.message_receiver);
                    decryptedMessage = forge.util.decodeUtf8(privateKey.decrypt(encryptedMessageBytes, 'RSA-OAEP'));
                    appendMessage(historyItem.sender, decryptedMessage, 'received');
                }
            } catch (error) {
                console.error('Decryption error in chat history:', error);
            }
        });
    });


    socket.on('connect', function () {
        console.log('Connected to WebSocket server');
    });
});