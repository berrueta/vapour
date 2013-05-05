import logging, os

# Must set this env var before importing any part of Django
# 'project' is the name of the project created with django-admin.py
os.environ['DJANGO_SETTINGS_MODULE'] = 'vapour.settings'

# Force Django to reload its settings.
from django.conf import settings
settings._target = None

from django.core.signals import got_request_exception
from django.db import _rollback_on_exception
import django

def log_exception(*args, **kwds):
    logging.exception('Exception in request:')

# Log errors.
django.dispatch.Signal.connect(
   django.core.signals.got_request_exception, log_exception)

# Unregister the rollback event handler.
django.dispatch.Signal.disconnect(
    django.core.signals.got_request_exception,
    django.db._rollback_on_exception)

import django.core.handlers.wsgi

# Create a Django application for WSGI.
application = django.core.handlers.wsgi.WSGIHandler()

# Google App Engine imports.
from google.appengine.ext.webapp import util

# Run the WSGI CGI handler with that application.
util.run_wsgi_app(application)
