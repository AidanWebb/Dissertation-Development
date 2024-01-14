$(document).ready(function () {

    // Submit the form when submit button is pressed
    $("#loginForm").submit(function (event) {
        event.preventDefault();
        submitForm();
    });

    function submitForm() {
        // Disable the submit button to ensure groups are not duplicated
        let submitButton = $('#login');
        submitButton.attr('disabled', true);
        submitButton.html("Logging In...");

        // Prepare the JSON that you want to send to the API here...
        let json = {
            "email": $("#email").val(),
            "password": $("#password").val()
        };

        // Post the JSON
        $.ajax("/api/auth/login", {
            type: "POST",
            data: JSON.stringify(json),
            contentType: "application/json",
            dataType: "json",
            success: function (data) {
                if (data.status === 0) {
                    window.location.href = "/chat_page";
                } else {
                    raise_failure();
                }
            },
            error: function () {
                raise_failure();
            }
        });
    }

    // Shows error alert
    function raise_failure() {
        // Maybe show a log message here...
        reset_submit_button();
    }

    // Re-enables the form submission button
    function reset_submit_button() {
        let submit_button = $('#signup');
        submit_button.attr('disabled', false);
        submit_button.html("Login");
    }
});