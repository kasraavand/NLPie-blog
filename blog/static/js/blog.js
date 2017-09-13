function subscribe() {
    var email = document.getElementById('newsletter').value;
    $.ajax({
        dataType: "json",
        url : "subscribe", // the endpoint
        type : "POST", // http method
        data : { 'email' : email}, // data sent with the post request

        // handle a successful response
        success : function(response) {
            alert("Thanks for subscription.");
        },

        // handle a non-successful response
        error : function(xhr, errmsg, err) { 
            console.log(xhr.status + ": " + xhr.responseText);
    }
});
};