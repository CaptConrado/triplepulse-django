
var pages = {
	1 : 'type',
	2 : 'level',
	3 : 'plans',
	4 : 'billing',
	5 : 'account'
}

var curPage = 1;
paymentValidated=false;
formValidated=false;

function advanceSlide(subClass){
	$('.game .' + pages[curPage]).hide();
	$('.breadcrumbs .' + pages[curPage]).removeClass('active').addClass('completed');
	$('.breadcrumbs .' + pages[curPage] + ' .checkmark').fadeIn();
	curPage ++;
	$('.breadcrumbs .' + pages[curPage]).addClass('active');
	if (subClass){
		var slide = pages[curPage] + '.' + subClass;
	}else{
		var slide = pages[curPage];
	}
	$('.game .' + slide).fadeIn();
}

$(document).ready(function(){
    Stripe.setPublishableKey($('#stripe_publishable').val());
    $('#accountForm').h5Validate();

    $('.game .type a').click(function(event){
		event.preventDefault();
		if ($(this).hasClass('race')){
			advanceSlide('race');
			$('.game > h3').html('What\'s your experience level?');
		}else if ($(this).hasClass('cardio')){
			advanceSlide('cardio');
			$('.game > h3').html('How often do you train?');	
		}
	})
	$('.game .level a').click(function(event){
		event.preventDefault();
		advanceSlide();
		$('.game > h3').html('Subscription structure');	
	})
	$('.game .plans a').click(function(event){
		event.preventDefault();
		advanceSlide();
		$('.game > h3').hide();
		planID = $(this).children('.planID').val(); // planID is the variable to post to the checkout
		$('.selectedPlan .yourSubscription').html($(this).children('.planName').val());
		$('.selectedPlan .price').html($(this).children('.planCost').val());
	})
	$('.game .billing .proceed').click(function(event){
		event.preventDefault();

        if ($('#name').val().length>0 && $('#email').val().length>0){
            advanceSlide();
            $('#username').focus()
            //Prevent submit until we have token
            $('.slide.account .proceed').attr('disabled', 'disabled');

            //Get Stripe Token
            Stripe.createToken({
                number: $('#card').val(),
                cvc: $('#cvc').val(),
                exp_month: $('#expMonth').val(),
                exp_year: $('#expYear').val(),
                adress_zip : $('#billingZIP').val(),
                name : $('#name').val(),
                adress_line1 : $('#billingLine1').val()
            }, stripeResponseHandler);

            $('#shippingLine1').val($('#billingLine1').val());
            $('#shippingLine2').val($('#billingLine2').val());
            $('#shippingCity').val($('#billingCity').val());
            $('#shippingState').val($('#billingState').val());
            $('#shippingZIP').val($('#billingZIP').val());
        }else{
            paymentError('Name and email are required');
        }
    })

	$('.game .billing .back').click(function(event){
		event.preventDefault();
		curPage--;
		$('.slide.billing').hide();
		$('.slide.plans').fadeIn();
		$('.game > h3').html('Subscription structure').fadeIn();	
	})
	$('.game .account .back').click(function(event){
		event.preventDefault();
		curPage--;
		$('.slide.account').hide();
		$('.slide.billing').fadeIn();
	})

    $('#accountForm input').keyup(function(event){
        var validated = true;
        $('#accountForm input[required]').each(function(){
            if ($(this).val().length<1){
                validated = false;
                }
            });
        if (validated==true){
            formValidated =true;
        }else{
            formValidated =false;
        }
        checkSubmissionDisable();
    });
    $('.row.submit').mouseover(function(){
        highlightMissingFields();
    })
    $('#accountForm').submit(function(event){
        event.preventDefault();

        if (formValidated){
            $('.slide.account .proceed').attr('disabled', 'disabled');

            $.ajax({
                url : '/signup/account',
                data : $(this).serialize(),
                type : 'POST',
                success : function(response){
                    if (response.success && response.url){
                        window.location.href = response.url
                    }else if (response.error){
                        accountError(response.error)
                    }
                    $('.slide.account .proceed').removeAttr('disabled');

                },
                error : function(){
                    accountError("There was an error processing your registration")
                    $('.slide.account .proceed').removeAttr('disabled');

                }

            });
        }else{
            highlightMissingFields();
        }
    })
});

function stripeResponseHandler(status, response) {
    if (response.error) {
        // Show the errors on the form
        paymentError(response.error.message);

    } else {
        var token = response.id;
        subscribe(token, planID, $('#email').val(), $('#name').val());
    }
}

function subscribe(token, plan, email, description){
    $.ajax({
        url : '/signup/stripe',
        type : 'POST',
        data : {
            'token' : token,
            'plan' : plan,
            'email' : email,
            'description' : description
            },
        success : function (response) {
            if (response.success == true){
                paymentValidated=true;
                checkSubmissionDisable();
                $('#stripe_id').val(response.stripe_id)
            }else if (response.message){
                paymentError(response.message)
                }
            },
        error :  function (jqXHR){
                paymentError('There was an error processing your payment');
            }
        })
}

function checkSubmissionDisable(){
    if (formValidated==true && paymentValidated==true){
        $('.slide.account .proceed').removeAttr('disabled');
    }else{
        $('.slide.account .proceed').attr('disabled', 'disabled');
    }
}

function scrollToTop(){
    $( 'html, body' ).animate( {
        scrollTop: 0
    }, 500 );
}

function paymentError(message){
    $('.paymentErrors').html(errorHtml(message));
    curPage=4;
    $('.slide.account').hide();
    $('.slide.billing').fadeIn();
    scrollToTop();
}

function accountError(message){
    $('.accountErrors').html(errorHtml(message));
    scrollToTop();
}

function highlightMissingFields(){
    $('#accountForm input[required]').each(function(){
        if ($(this).val().length<1){
            $(this).addClass('ui-state-error')
        }
    });
}