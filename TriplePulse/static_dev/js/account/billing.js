
$(document).ready(function(){
    Stripe.setPublishableKey($('#stripe_publishable').val());
	$('#paymentForm').submit(function(event){
		event.preventDefault();

        //Prevent submit until we have token
        $('#paymentForm input[type="submit"]').attr('disabled', 'disabled');

        //Get Stripe Token
        Stripe.createToken({
            number: $('#id_card').val(),
            cvc: $('#id_cvc').val(),
            exp_month: $('#id_exp_month').val(),
            exp_year: $('#id_exp_year').val(),
			adress_zip : $('#id_zip').val(),
			name : $('#id_name').val(),
        }, stripeResponseHandler);

    })

});

function stripeResponseHandler(status, response) {
    if (response.error) {
        // Show the errors on the form
        paymentError(response.error.message);
        $('#paymentForm input[type="submit"]').removeAttr('disabled');

    } else {
        var token = response.id;
        updateCard(token);
    }
}

function updateCard(token){
    $.ajax({
        url : '/account/billing/stripe',
        type : 'POST',
        data : {
            'token' : token,
            },
        success : function (response) {
            if (response.success == true){
				$('.paymentErrors').html('<div class="alert alert-success"><button type="button" class="close" data-dismiss="alert">&times;</button>Card sucessfully upated</div>')
				scrollToTop();
            }else if (response.message){
                paymentError(response.message)
            }
	        $('#paymentForm input[type="submit"]').removeAttr('disabled');
        },
        error :  function (jqXHR){
                paymentError('There was an error processing your payment');
		        $('#paymentForm input[type="submit"]').removeAttr('disabled');

            }
        })
}

function paymentError(message){
    $('.paymentErrors').html(errorHtml(message));
	scrollToTop();
}


function scrollToTop(){
    $( 'html, body' ).animate( {
        scrollTop: 0
    }, 500 );
}