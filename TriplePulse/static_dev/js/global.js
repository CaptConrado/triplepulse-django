FACEBOOK_APP_ID = 'YOUR APP ID GOES HERE'
GOOGLE_ANALYTICS_TRACKING_ID = 'YOUR TRACKING ID GOES HERE'

var _gaq = _gaq || [];
_gaq.push(['_setAccount', GOOGLE_ANALYTICS_TRACKING_ID]);
_gaq.push(['_trackPageview']);

(function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
})();


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
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}


$(document).ready(function(){
    //CSRF Token for Django Security
    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    //Header interactions
    $('a.login').click(function(event){
		event.preventDefault();
		$('.modal.login').modal('show');
	});
	$('a.newsletter').click(function(event){
		event.preventDefault();
		$('.modal.newsletter').modal('show');
	});
	$('.modal.newsletter form').submit(function(event){
		event.preventDefault();
        var email = $(this).find('.email').val();
        subscribeNewsletter({'email' : email})
	})

    //AJAX Login
    $('#loginForm').submit(function(event){
        event.preventDefault();
        $('#loginForm input[type=submit]').attr('disabled', 'disabled')
        $.post('/login', $(this).serialize(), function(response){
            if (response.success && response.url){
                window.location.href = response.url
            }else if (response.error){
                $('.loginErrors').html(errorHtml(response.error))
            }
            $('#loginForm input[type=submit]').removeAttr('disabled')
        }, 'json')
    })

//    Social newsletter login
    $('a.fbNewsletter').click(function(event){
        event.preventDefault();
        facebookLogin();
    })
})

function errorHtml(message){
    return '<div class="alert"><button type="button" class="close" data-dismiss="alert">&times;</button>' + message + '</div>'
}


window.fbAsyncInit = function() {
    // init the FB JS SDK
    FB.init({
        appId      : FACEBOOK_APP_ID, // App ID from the App Dashboard
        status     : true, // check the login status upon init?
        cookie     : true, // set sessions cookies to allow your server to access the session?
        xfbml      : true  // parse XFBML tags on this page?
});

// Additional initialization code such as adding Event Listeners goes here

};

// Load the SDK's source Asynchronously
// Note that the debug version is being actively developed and might
// contain some type checks that are overly strict.
// Please report such bugs using the bugs tool.
(function(d, debug){
    var js, id = 'facebook-jssdk', ref = d.getElementsByTagName('script')[0];
    if (d.getElementById(id)) {return;}
js = d.createElement('script'); js.id = id; js.async = true;
js.src = "//connect.facebook.net/en_US/all" + (debug ? "/debug" : "") + ".js";
ref.parentNode.insertBefore(js, ref);
}(document, /*debug*/ false));

function facebookLogin(){
    FB.login(function(response) {
        if (response.authResponse) {
            FB.api('/me', function(response) {
                postdata = {
                    'email' : response.email,
                    'first' : response.first_name,
                    'last' : response.last_name
                }

                subscribeNewsletter(postdata)
            });
        }
    }, {scope: 'email'});
}

function subscribeNewsletter(postdata){
    $.post('/newsletter/subscribe/', postdata, function(response){
        if (response.success){
            $('.newsletterSignup').hide();
            $('.newsletterConfirm').fadeIn();
        }else if(response.error){
            $('.newsletterErrors').html(errorHtml(response.error));
        }
    }, 'json')

}