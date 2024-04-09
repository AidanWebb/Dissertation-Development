$(document).ready(function () {
    function toggleSearchBar() {
        $("#friendBar").toggle();
    }

    function addFriend() {
        let username = $("#userInput").val().trim();
        let json = {"username": username};

        console.log(`Adding friend: ${username}`);
        $.ajax("/api/add-friend", {
            type: "POST",
            data: JSON.stringify(json),
            contentType: "application/json",
            dataType: "json",
            success: function (data) {
                if (data.status === 'success') {
                    console.log(`${username} added successfully. Public key:`, data.public_key);


                    localStorage.setItem(`publicKey_${username}`, data.public_key);
                    console.log(`Public key for ${username} stored successfully.`);


                    $(".user-list").append(`<div class="user" data-username="${username}">${username}<button class="delete-button">Delete</button></div>`);
                    console.log(`Sidebar updated with new friend: ${username}.`);

                } else {
                    console.error(`Failed to add ${username} as a friend. Response:`, data);
                }
            },
            error: function (xhr, status, error) {
                console.error(`Error occurred when trying to add ${username} as a friend.`, error);
            }
        });
    }



    $("#addButton").click(function () {
        toggleSearchBar();
    });


    $("#userAddButton").click(function () {
        addFriend();
    });
});
