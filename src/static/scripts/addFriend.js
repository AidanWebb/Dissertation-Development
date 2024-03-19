$(document).ready(function () {
    // Function to toggle search bar
    function toggleSearchBar() {
        $("#friendBar").toggle();
    }

    function addFriend() {
        let username = $("#userInput").val().trim();
        let json = {"username": username};

        console.log(`Adding friend: ${username}`); // Log adding friend attempt
        $.ajax("/api/add-friend", {
            type: "POST",
            data: JSON.stringify(json),
            contentType: "application/json",
            dataType: "json",
            success: function (data) {
                if (data.status === 'success') {
                    console.log(`${username} added successfully. Public key:`, data.public_key); // Log successful friend addition and public key

                    // Store the public key in local storage
                    localStorage.setItem(`publicKey_${username}`, data.public_key);
                    console.log(`Public key for ${username} stored successfully.`); // Log successful storage

                    // Dynamically update the sidebar with the new friend
                    $(".user-list").append(`<div class="user" data-username="${username}">${username}<button class="delete-button">Delete</button></div>`);
                    console.log(`Sidebar updated with new friend: ${username}.`); // Log sidebar update

                } else {
                    console.error(`Failed to add ${username} as a friend. Response:`, data); // Log failure to add friend with response data
                }
            },
            error: function (xhr, status, error) {
                console.error(`Error occurred when trying to add ${username} as a friend.`, error); // Log error on friend addition
            }
        });
    }


    // Bind click event to add button
    $("#addButton").click(function () {
        toggleSearchBar();
    });

    // Bind click event to search button
    $("#userAddButton").click(function () {
        addFriend();
    });
});
