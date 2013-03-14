import settings
import os

# ======================================
# Mandatory settings
# ======================================

# Key used by Django for Cryptographic signing
SECRET_KEY = 'CHANGE_THIS_STRING'

# Keys used for Stripe processing
STRIPE_SECRET = "YOUR_STRIPE_SECRET_KEY"
STRIPE_PUBLISHABLE = "YOUR_STRIPE_PUBLIC_KEY"

# Mailchimp API Key
MAILCHIMP_API_KEY = ''

# Mailchimp list ID
MAILCHIMP_LIST_ID = ''

# Database
# Set this to the appropriate engine and auth settings
# likely mysql, or cloudsql if you decide to use AppEngine
DATABASES = {

}

# ======================================
# Optional settings
# ======================================

# Debug settings (include if testing, omit in production)
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Location of static files
# Set these to static content location if you collect static content and host on CDN
# (these default to the values below even if you delete this block)
STATIC_URL = "/static/"
ADMIN_MEDIA_PREFIX = "/static/admin/"

