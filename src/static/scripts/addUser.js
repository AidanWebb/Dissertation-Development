 $(document).ready(function() {
            // Function to toggle search bar
            function toggleSearchBar() {
                $("#searchBar").toggle();
            }

            // Bind click event to add button
            $("#addButton").click(toggleSearchBar);
        });