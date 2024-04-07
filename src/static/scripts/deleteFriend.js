$(document).ready(function() {

    function deleteFriend(username) {

        let json = {
            "username": username
        };

        $.ajax("/api/delete-friend", {
            type: "POST",
            data: JSON.stringify(json),
            contentType: "application/json",
            dataType: "json",
            success: function (data) {
                if (data.status === 0) {

                    $(`div.user[data-username='${username}']`).remove();

                    $('#headerText').text("Click a friend to start chatting");
                } else {
                    console.log("Failed to delete friend:", data.message);
                }
            },
            error: function (xhr, status, error) {
                console.error("Error deleting friend:", error);
            }
        });
    }

    $('.user-list').on('click', '.delete-button', function () {
        var username = $(this).closest('.user').attr('data-username');
        deleteFriend(username);
    });
});
