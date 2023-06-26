$(document).ready(function() {
    // send message on form submit
    $('#chat-form').submit(function(event) {
        event.preventDefault(); // prevent default form submission behavior
        var user_input = document.getElementById('chat-input').value;
        var profile = document.getElementById('profile-pic').value;
        $('#chatbox').append("<div class=\"msg right-msg\">" +
            "                    <div class=\"msg-img\" style=\"background-image: url('/static/profile_pics/" + profile + "')\"></div>" +
            "                    <div class=\"msg-bubble\">" +
            "                        <div class=\"msg-text\">"
                                           + user_input +
            "                        </div>" +
            "                    </div>" +
            "                </div>");
        $.ajax({
            type: "POST",
            url: "/process_message/",
            data: new FormData($('#chat-form')[0]), // send form data as a FormData object
            processData: false,
            contentType: false,
            success: function(response) {
                console.log(data);
                $('#chatbox').append("<div class=\"msg left-msg\"><div class=\"msg-img\" style=\"background-image: url('/static/profile_pics/bot.jpg')\"></div>" +
                    "                    <div class=\"msg-bubble\"><div class=\"msg-text\">" + response.bot_response + "</div></div></div>");
                $('#chatbox').scrollTop($('#chatbox')[0].scrollHeight);
                $('#chat-input').val('');
            }
        });
    });
});
