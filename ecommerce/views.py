from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils import simplejson
from models import UserProfile, Shipment
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render
import stripe
from TriplePulse.settings import STRIPE_SECRET, SIGNUP_SUCCESS_URL, STRIPE_PLANS, LOGIN_SUCCESS_URL, STRIPE_PUBLISHABLE
import datetime
from django.db  import IntegrityError
import forms
from django.http import HttpResponseRedirect
import json
from django.http import HttpRequest

def json_response(content, status_code=200):
    response = simplejson.dumps(content)
    response = HttpResponse(response, content_type="application/json")
    response.status_code=status_code
    return response

@ensure_csrf_cookie
def signup_form(request):
    context = {'stripe_publishable' : STRIPE_PUBLISHABLE}
    return render(request, 'signup.html', context)


@require_http_methods(["POST"])
def create_and_subscribe_stripe_user(request):

    stripe.api_key = STRIPE_SECRET

    if request.POST.get('token') and request.POST.get('email') and request.POST.get('plan') :
        try:
            stripe_customer = stripe.Customer.create(
                description=request.POST.get('name'),
                card=request.POST.get('token'),
                email=request.POST.get('email'),
                coupon=request.POST.get('coupon'),
                plan=request.POST.get('plan')
            )
        except stripe.CardError, e:
            body = e.json_body
            return_data  = body['error']
            return json_response(return_data)
        except stripe.InvalidRequestError, e:
            return_data = {
                'error' : "Invalid payment request"
            }
            return json_response(return_data)
        except stripe.AuthenticationError, e:
            return_data = {
                'error' : "Could not authenticate with our payment processor"
            }
            return json_response(return_data)
        except stripe.StripeError, e:
            return_data = {
                'error' : "Sorry, we're having issues with our payment processor"
            }
            return json_response(return_data)

        return_data = {'success' : True, 'stripe_id' : stripe_customer.id}
        return json_response(return_data)
    else:
        return_data = {
            'error' : "Stripe token, plan, and email required"
        }
        return json_response(return_data)

@require_http_methods(["POST"])
def signup(request):
    stripe.api_key = STRIPE_SECRET
    if request.POST.get('stripe_id') and request.POST.get('username') and request.POST.get('email') and request.POST.get('password') and request.POST.get('street1') and request.POST.get('zip'):
        try:
            stripe_customer = stripe.Customer.retrieve(request.POST.get('stripe_id'))
        except (stripe.CardError, stripe.InvalidRequestError, stripe.AuthenticationError, stripe.APIConnectionError, stripe.StripeError) as e:
            return_data = {
                'error' : "Could not validate Stripe customer"
            }
            return json_response(return_data)

        try:
            user = User.objects.create_user(request.POST.get('username'), request.POST.get('email'), request.POST.get('password'))
        except IntegrityError:
            return_data = {
                'error' : 'Username "' + request.POST.get('username') + '" already exists'
            }
            return json_response(return_data)

        user.first_name = request.POST.get('name')
        user.save()

        user_profile = UserProfile(
            user = user,
            street1 = request.POST.get('street1'),
            street2 = request.POST.get('street2', ''),
            city = request.POST.get('city', ''),
            state = request.POST.get('state', ''),
            zip = request.POST.get('zip'),
            stripe_id = stripe_customer.id,
        )
        user_profile.save()

        plan = stripe_customer.subscription.plan.id

        create_shipments(user, plan)

        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        login(request, user)

        return_data = {'success' : True, 'url' : SIGNUP_SUCCESS_URL }
        return json_response(return_data)
    else:
        return_data = {'error' : 'Required fields missing'}
        return json_response(return_data)

@require_http_methods(["POST"])
def login_user(request):
    if request.POST.get('username') and request.POST.get('password'):
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                # User is good. Log them in.
                login(request, user)
                return_data = {
                    'success' : True,
                    'url' : LOGIN_SUCCESS_URL
                }
                return json_response(return_data)
            else:
                # User is disabled
                return_data = {
                    'error' : 'Account disabled'
                }
                return json_response(return_data)
        else:
            # User does not exist or password is incorrect
            return_data = {
                'error' : 'Username or password is incorrect'
            }
            return json_response(return_data)
    else:
        return_data = {
            'error' : 'Username and password are required'
        }
    return json_response(return_data)

@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")

@login_required
def update_account(request):
    if request.method == 'POST': # If the form has been submitted...
        form = forms.UserForm(data=request.POST, instance=request.user) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            return render(request, 'settings.html', {
                'form': form,
                'updated' : True,
                'active_page' : 'shipping'

            })

    else:
        form = forms.UserForm(instance=request.user) # An unbound form
    return render(request, 'settings.html', {
        'form': form,
        'updated' : False,
        'active_page' : 'profile'
        })

@login_required
def update_shipping(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect("/account/profile")
    if request.method == 'POST': # If the form has been submitted...
        form = forms.ShippingForm(data=request.POST, instance=user_profile) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            update_future_orders(request.user)
            return render(request, 'settings.html', {
                'form': form,
                'updated' : True,
                'active_page' : 'shipping'

            })
    else:
        form = forms.ShippingForm(instance=user_profile) # An unbound form
    return render(request, 'settings.html', {
        'form': form,
        'updated' : False,
        'active_page' : 'shipping'
    })

@login_required
def update_billing(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect("/account/profile")

    form = forms.BillingForm()
    return render(request, 'billing.html', {
        'form': form,
        'updated' : False,
        'active_page' : 'billing',
        'stripe_publishable' : STRIPE_PUBLISHABLE
    })

@login_required
def update_subscription(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect("/account/profile")
    return_data = {
        'error' : 'Not implemented'
    }
    return json_response(return_data)

@login_required
def attach_new_card(request):
    if request.POST.get('token'):
        stripe_id = request.user.get_profile().stripe_id
        try:
            stripe_customer = stripe.Customer.retrieve(stripe_id)
        except (stripe.CardError, stripe.InvalidRequestError, stripe.AuthenticationError, stripe.APIConnectionError, stripe.StripeError) as e:
            return_data = {
                'error' : "Could not validate Stripe customer"
            }
            return json_response(return_data)

        try:
            stripe_customer.card = request.POST.get('token')
            stripe_customer.save()
        except stripe.CardError, e:
            body = e.json_body
            return_data  = body['error']
            return json_response(return_data)
        except stripe.InvalidRequestError, e:
            return_data = {
                'error' : "Invalid payment request"
            }
            return json_response(return_data)
        except stripe.AuthenticationError, e:
            return_data = {
               'error' : "Could not authenticate with our payment processor"
            }
            return json_response(return_data)
        except stripe.StripeError, e:
            return_data = {
                'error' : "Sorry, we're having issues with our payment processor"
            }
            return json_response(return_data)

        return_data = {'success' : True}
        return json_response(return_data)
    else:
        return_data = {
        'error' : "Stripe token required"
        }
        return json_response(return_data)

def stripe_webhook(request):
    stripe.api_key = STRIPE_SECRET
    event_json = json.loads(HttpRequest.body)
    if event_json.get('type') == 'invoice.payment_succeeded':
        stripe_customer = event_json['data']['object']['customer']
        user_profile = UserProfile.objects.get(stripe_id=stripe_customer)
        user = user_profile.user
        for subscription in event_json['data']['object']['lines']['subcriptions']:
            plan = subscription['plan']
            create_shipments(user, plan)
    return_data = {'success' : True}
    return json_response(return_data)

def create_shipments(user, plan):
    user_profile = user.get_profile()
    months = STRIPE_PLANS[plan]['months']
    startDay = datetime.date.today() + datetime.timedelta(days=3)
    for month in range(0, (months)):
        ship_date = startDay + datetime.timedelta(days=(31*month))
        user.shipment_set.create(
            date = ship_date,
            shipped = False,
            name = user.first_name,
            street1 = user_profile.street1,
            street2 = user_profile.street2,
            city = user_profile.city,
            state = user_profile.state,
            zip = user_profile.zip,
        )
    return True

def update_future_orders(user):
    user_profile = user.get_profile()
    Shipment.objects.filter(user=user, shipped=False).update(
        name = user.first_name,
        street1 = user_profile.street1,
        street2 = user_profile.street2,
        city = user_profile.city,
        state = user_profile.state,
        zip = user_profile.zip,
    )
