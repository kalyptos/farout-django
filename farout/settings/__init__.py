"""
Django settings module selector.
Automatically imports the correct settings based on DJANGO_ENVIRONMENT.
Defaults to production settings for safety.
"""
import os

# Get the environment setting (defaults to production for safety)
ENVIRONMENT = os.getenv('DJANGO_ENVIRONMENT', 'production')

if ENVIRONMENT == 'development':
    from .development import *
elif ENVIRONMENT == 'production':
    from .production import *
else:
    # Default to production for any unknown environment
    from .production import *
