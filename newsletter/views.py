import mailchimp
from TriplePulse.settings import MAILCHIMP_API_KEY, MAILCHIMP_LIST_ID
from ecommerce.views import json_response

def subscribe(email, first_name, last_name):
    list = mailchimp.utils.get_connection().get_list_by_id(MAILCHIMP_LIST_ID)
    list.subscribe(email, {'EMAIL': email, 'FNAME': first_name, 'LNAME': last_name})

def subscribe_email(request):
    if request.POST.get('email') and request.POST.get('first_name') and request.POST.get('last_name'):
        subscribe(request.POST.get('email'), request.POST.get('first_name'), request.POST.get('last_name'))
        return_data = {'success' : True}
        json_response(return_data)
    else:
        return_data = {'error' : 'Email, first name and last name are required'}
        json_response(return_data)