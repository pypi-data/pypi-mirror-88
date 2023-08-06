import os
import random
import string

import dj_database_url
import django_cache_url

from .base import *  # noqa: F403

DEBUG = os.getenv('DJANGO_DEBUG', 'off') == 'on'

# DJANGO_SECRET_KEY *should* be specified in the environment. If it's not, generate an ephemeral key.
if 'DJANGO_SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
else:
    # Use if/else rather than a default value to avoid calculating this if we don't need it
    print("WARNING: DJANGO_SECRET_KEY not found in os.environ. Generating ephemeral SECRET_KEY.")
    SECRET_KEY = ''.join([random.SystemRandom().choice(string.printable) for i in range(50)])

# Make sure Django can detect a secure connection properly on Heroku:
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Redirect all requests to HTTPS
SECURE_SSL_REDIRECT = os.getenv('DJANGO_SECURE_SSL_REDIRECT', 'off') == 'on'

# Accept all hostnames, since we don't know in advance which hostname will be used for any given Heroku instance.
# IMPORTANT: Set this to a real hostname when using this in production!
# See https://docs.djangoproject.com/en/1.10/ref/settings/#allowed-hosts
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '*').split(';')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# BASE_URL required for notification emails
BASE_URL = 'http://localhost:8000'

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# configure CACHES from CACHE_URL environment variable (defaults to locmem if no CACHE_URL is set)
CACHES = {'default': django_cache_url.config()}

# Configure Elasticsearch, if present in os.environ
COUCHDB_URL = os.getenv('COUCHDB_URL', '')

if COUCHDB_URL:
    pass

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

