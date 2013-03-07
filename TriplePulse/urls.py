from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from pinboard.views import pinboard_posts
from blog.views import blog_index
from ecommerce.views import create_and_subscribe_stripe_user, signup, login_user, signup_form, logout_user, stripe_webhook
from django.views.generic.simple import redirect_to

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    url(r'^pinboard/posts/?$', pinboard_posts),
    url(r'^signup/?$', signup_form),
    url(r'^signup/stripe/?$', create_and_subscribe_stripe_user),
    url(r'^signup/account/?$', signup),
    url(r'^login/?$', login_user),
    url(r'^logout/?$', logout_user),
    url(r'^account/?', include('ecommerce.urls')),
    url(r'^account/?$', redirect_to, {'url': '/account/profile/'}),
    url(r'^blog/(?P<page_number>\d+)/?$', blog_index),
    url(r'^blog/?$', redirect_to, {'url': '/blog/1'}),
    url(r'^webhooks/stripe?$', stripe_webhook),

    url(r'^' + settings.POSTS_ROOT, include('cms.urls')),

)

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'direct_to_template', {'template': 'index.html'}),
    (r'^channel$', 'direct_to_template', {'template': 'channel.html'}),
    (r'^pinboard/?$', 'direct_to_template', {'template': 'pinboard.html'}),
    (r'^thankyou/?$', 'direct_to_template', {'template': 'thankyou.html'}),
    (r'^stacks/?$', 'direct_to_template', {'template': 'stacks.html'}),
    (r'^admin/', include(admin.site.urls)),
) + urlpatterns


if settings.DEBUG:
    urlpatterns = patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'', include('django.contrib.staticfiles.urls')),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
             {'document_root': settings.STATIC_ROOT}),
) + urlpatterns