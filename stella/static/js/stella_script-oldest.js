$(document).ready(function() {
    // send message on form submit
    $('#chat-form').submit(function(event) {
        event.preventDefault(); // prevent default form submission behavior
        var user_input = document.getElementById('chat-input').value;
        $('#chatbox').append("<div class='user-message'><p><span class='before-element'></span>" + user_input + "</p><span class='after-element-user'></span></div>");
        $.ajax({
            type: "POST",
            url: "/process_message/",
            data: new FormData($('#chat-form')[0]), // send form data as a FormData object
            processData: false,
            contentType: false,
            success: function(response) {
                $('#chatbox').append("<div class='bot-message'><p><span class='before-element'></span>" + response.bot_response + "</p><span class='after-element-bot'></span></div>");
                $('#chatbox').scrollTop($('#chatbox')[0].scrollHeight);
                $('#chat-input').val('');
            }
        });
    });
});
