triplepulse-django
==================

Triplepulse's full Django application. Django CMS is used for the social pinboard, blog and basic pages.

Deploying
----------
1.) Use pip to install the packages listed in requirement.txt. To do this, run "pip install -r requirements.txt"

2.) Create a local_settings.py file. local_settings_example.py should be a good reference. This file defines your API keys,
crypto keys, database connections, and debugging settings. It will be omitted from GitHub for security reasons.

3.) Make sure the database you linked to in local_settings.py is running, then run "python manage.py
syndcb," then "python manage.py migrate"

4.) If fixtures weren't loaded in by syncb, run "python manage.py loaddata TriplePulse/fixtures/initial_data.json" to import
pages that are stored in Django CMS (like terms, about, etc.)

5.) Create a first superuser by running "python manage.py createsuperuser"

6.) For static files, you may want to use a cdn. Use "python manage.py collectstatic" to collect the static files in the
static root. Copy these to a CDN, then set the static root to the CDN address. For more info:
https://docs.djangoproject.com/en/dev/howto/static-files/#staticfiles-production

7.) Run whatever webserver you choose (App Engine makes this easy, or Nginx with Gunicorn is easy to setup)

You're done!

Adding CMS Content and Managing the Site
-----------------------------------------
To add pinboard posts, create a page in the CMS admin panel (most likely, these will be children of the pinboard page,
but they don't have to be). Then use then pinboard admin panel to upload a thumbnail image and set other information
used for pinboard display.

To add a blog post, us the CMS admin panel to add a page that is subsidiary to the Blog page. Make sure it's published.

To see upcoming shipments, click on shipments in the admin panel. Mark when you ship, and add tracking info.

You can use the User and Auth admin tools to update password and other basic user info.

Payment changes can be handled directly in Stripe. Stripe webhooks will schedule new shipments when each payment clears.

To update text pages like Mission, FAQ, etc, simply edit the page in the CMS admin.