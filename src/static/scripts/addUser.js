$(document).ready(function() {
    // Function to toggle search bar
    function toggleSearchBar() {
        $("#searchBar").toggle();
    }


    function searchUser() {
        var searchInput = $("#searchInput").val().trim();


        if (searchInput === "") {

            console.log('Please enter a username.');
            return;
        }


        $.ajax({
            type: 'POST',
            url: '/search_user',
            data: { username: searchInput },
            success: function(response) {
                console.log('Search successful:', response);
            },
            error: function(xhr, status, error) {
                console.error('Error searching for user:', error);
            }
        });
    }

    // Bind click event to add button
    $("#addButton").click(function() {
        toggleSearchBar();
    });

    // Bind click event to search button
    $("#searchButton").click(function() {
        searchUser();
    });
});
