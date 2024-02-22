$(document).ready(function() {
    // Function to delete a friend
    function deleteFriend(username) {
        // Prepare the JSON to send to the API
        let json = {
            "username": username
        };

        // Send AJAX request to delete friend
        $.ajax("/api/delete-friend", {
            type: "POST",
            data: JSON.stringify(json),
            contentType: "application/json",
            dataType: "json",
            success: function (data) {
                // Check if friend was deleted successfully
                if (data.status === 0) {
                    // Remove friend from the UI
                    $(`div.user[data-username='${username}']`).remove();
                } else {
                    // Handle failure
                    console.log("Failed to delete friend:", data.message);
                }
            },
            error: function (xhr, status, error) {
                // Handle error
                console.error("Error deleting friend:", error);
            }
        });
    }

    // Bind click event to delete button
    $('.user-list').on('click', '.delete-button', function () {
        var username = $(this).closest('.user').attr('data-username');
        deleteFriend(username);
    });
});
