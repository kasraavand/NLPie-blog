function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function subscribe() {
    var email = document.getElementById('newsletter').value;
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        dataType: "json",
        url : "subscribe/", // the endpoint
        type : "POST", // http method
        data : { 'email' : email,
                 'csrfmiddlewaretoken': csrftoken }, // data sent with the post request

        // handle a successful response
        success : function(response) {
            alert("Thanks for subscription.");
        },

        // handle a non-successful response
        error : function(xhr, errmsg, err) { 
            console.log(xhr.status + ": " + xhr.responseText);
    }
});
        $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
};

(function (window, document, undefined){
    'use strict';
    var form        = '.newsletter',
        className   = 'newsletter--active',
        email       = 'input[type="email"]',

        addEventListener = function( element, event, handler )
        {
            element.addEventListener ? element.addEventListener( event, handler ) : element.attachEvent( 'on' + event, function(){ handler.call( element ); });
        },
        forEach = function( elements, fn )
        {
            for( var i = 0; i < elements.length; i++ ) fn( elements[ i ], i );
        },
        addClass = function( element, className )
        {
            element.classList ? element.classList.add( className ) : element.className += ' ' + className;
        },
        removeClass = function( element, className )
        {
            element.classList ? element.classList.remove( className ) : element.className += element.className.replace( new RegExp( '(^|\\b)' + className.split( ' ' ).join( '|' ) + '(\\b|$)', 'gi' ), ' ' );
        };

    forEach( document.querySelectorAll( form ), function( $form )
    {
        var $email = $form.querySelectorAll( email );

        if( $email.length )
        {
            $email = $email[ 0 ];
            addEventListener( $email, 'keyup', function()
            {
                $email.value != '' && /^([\w-\.]+@([\w-]+\.)+[\w-]{2,12})?$/.test( $email.value ) ? addClass( $form, className ) : removeClass( $form, className );
            });
        }
    });
})(window, document);