document.querySelector('.img__btn').addEventListener('click', function() {
    document.querySelector('.cont').classList.toggle('s--signup');
});

$(document).ready(function() {
    // send message on form submit
    $('#signInForm').submit(function(event) {
        event.preventDefault(); // prevent default form submission behavior
        $.ajax({
            type: "POST",
            url: "/signin/",
            data: new FormData($('#signInForm')[0]), // send form data as a FormData object
            processData: false,
            contentType: false,
            success: function(response) {
                if (typeof response === 'object' && response.prob) {
                  // If the response is a JSON object with the "prob" property
                  $('#errors').append("<p>" + response.prob + "</p>");
                } else {
                  // Default behavior when the response is not the expected JSON object
                  // This code can be replaced with your desired actions
                  window.location.href = "/stella"
                }
            }
        });
    });
});

$(document).ready(function() {
    // send message on form submit
    $('#passwordForm').submit(function(event) {
        event.preventDefault(); // prevent default form submission behavior
        $.ajax({
            type: "POST",
            url: "/signup/",
            data: new FormData($('#passwordForm')[0]), // send form data as a FormData object
            processData: false,
            contentType: false,
            success: function(response) {
                if (typeof response === 'object' && response.prob) {
                    // If the response is a JSON object with the "prob" property
                    for (var i = 0; i < response.prob.length; i++) {
                        $('#errors').append("<p class='errors'>" + response.prob[i] + "</p>");
                    }
                } else {
                  // Default behavior when the response is not the expected JSON object
                  // This code can be replaced with your desired actions
                  window.location.href = "/upload/"
                }
            }
        });
    });
});

function emptyDiv() {
  var div = document.getElementById("errors");
  div.innerHTML = ""; // Set the innerHTML of the div to an empty string
}