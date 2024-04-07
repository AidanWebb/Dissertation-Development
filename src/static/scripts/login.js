$(document).ready(function () {
    $("#loginForm").submit(function (event) {
        event.preventDefault();
        submitForm();
    });

    function submitForm() {

        let submitButton = $('#login');
        submitButton.attr('disabled', true);
        submitButton.html("Logging In...");

        let json = {
            "username": $("#username").val(),
            "password": $("#password").val()
        };


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


    function raise_failure() {
        // Maybe show a log message here...
        reset_submit_button();
    }


    function reset_submit_button() {
        let submit_button = $('#login');
        submit_button.attr('disabled', false);
        submit_button.html("Login");
    }
});