$(document).ready(function() {
    // Function to toggle search bar
    function toggleSearchBar() {
        $("#friendBar").toggle();
    }


    function addFriend() {
        // Prepare the JSON that you want to send to the API here...
        let json = {
            "username": $("#userInput").val().trim()
        };

        // Post the JSON
        $.ajax("/api/add-friend", {
            type: "POST",
            data: JSON.stringify(json),
            contentType: "application/json",
            dataType: "json",
            success: function (data) {
                if (data.status === 0) {
                    window.location.href = "/chat_page";
                } else {
                    // Do something for failure maybe...
                }
            },
            error: function () {
                // also do something for this kind of failure...
            }
        });
    }

    // Bind click event to add button
    $("#addButton").click(function() {
        toggleSearchBar();
    });

    // Bind click event to search button
    $("#userAddButton").click(function() {
        addFriend();
    });
});
