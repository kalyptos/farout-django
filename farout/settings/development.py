"""
Development-specific Django settings.
"""
from .base import *

DEBUG = True

# Development-specific apps
INSTALLED_APPS += [
    'django_extensions',
    'debug_toolbar',
]

MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

# Internal IPs for debug toolbar
INTERNAL_IPS = ['127.0.0.1', 'localhost']

# Allow all hosts in development
ALLOWED_HOSTS = ['*']

# Disable CSP in development
CSP_ENABLED = False

# Email backend for development (console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Simplified static files for development
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
