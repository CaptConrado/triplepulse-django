import mailchimp
from TriplePulse.settings import MAILCHIMP_API_KEY, MAILCHIMP_LIST_ID
from ecommerce.views import json_response


def subscribe_email(request):
    try:
        list = mailchimp.utils.get_connection().get_list_by_id(MAILCHIMP_LIST_ID)
    except:
        return_data = {'error' : 'Could not get list'}
        return json_response(return_data)
    if request.POST.get('email') and request.POST.get('first_name') and request.POST.get('last_name'):
        email = request.POST.get('email')
        first_name = request.POST.get('first')
        last_name = request.POST.get('last')
        try:
            list.subscribe(email, {'EMAIL': email, 'FNAME': first_name, 'LNAME': last_name})
        except:
            return_data = {'error' : 'Could not subscribe to list'}
            return json_response(return_data)
        return_data = {'success' : True}
        return json_response(return_data)
    elif request.POST.get('email'):
        email = request.POST.get('email')
        try:
            list.subscribe(email, {'EMAIL': email})
        except:
            return_data = {'error' : 'Could not subscribe to list'}
            return json_response(return_data)
        return_data = {'success' : True}
        return json_response(return_data)
    else:
        return_data = {'error' : 'Valid email is required'}
        return json_response(return_data)