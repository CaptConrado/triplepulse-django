from django.conf.urls.defaults import *
from views import update_account, update_shipping, update_billing, attach_new_card

urlpatterns = patterns('',
    url(r'^profile/?$', update_account),
    url(r'shipping/?$', update_shipping),
    url(r'billing/?$', update_billing),
    url(r'billing/stripe/?$', attach_new_card),

)
