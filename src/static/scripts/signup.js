$(document).ready(function () {

    // Submit the form when submit button is pressed
    $("#signupForm").submit(function (event) {
        event.preventDefault();
        submitForm();
    });

    function submitForm() {
        // Disable the submit button to ensure groups are not duplicated
        let submitButton = $('#signup');
        submitButton.attr('disabled', true);
        submitButton.html("Signing Up...");

        // Prepare the JSON that you want to send to the API here...
        let json = {
            "email": $("#email").val(),
            "password": $("#password").val(),
            "confirm_password": $("#confirm_password").val()
        };

        // Post the JSON
        $.ajax("/api/auth/signup", {
            type: "POST",
            data: JSON.stringify(json),
            contentType: "application/json",
            dataType: "json",
            success: function (data) {
                if (data.status === 0) {
                    window.location.href = "/login";
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
        submit_button.html("Create your account now!");
    }
});