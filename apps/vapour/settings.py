# Django settings for vapour project.

import os
import sys

RUNNING_IN_GAE='SERVER_SOFTWARE' in os.environ and (os.environ['SERVER_SOFTWARE'].startswith('Development') or os.environ['SERVER_SOFTWARE'].startswith('Google App Engine'))

ROOT_PATH = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ("Sergio Fernandez", "sergio.fernandez@fundacionctic.org"),
     ("Diego Berrueta", "diego.berrueta@fundacionctic.org")
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'django.db.backends.'  # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'CET'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(ROOT_PATH, "..", "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/media/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(ROOT_PATH, "static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/resources/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(ROOT_PATH, "..", "static"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'd26h#_0*xdub&cj)v$67qu!*7*wl^nxg5j7a20%08)n*x1khsl'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = "vapour.urls"

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(ROOT_PATH, "templates'")
)

INSTALLED_APPS = (
     'django.contrib.staticfiles',
#    'django.contrib.auth',
#    'django.contrib.contenttypes',
#    'django.contrib.sessions',
#    'django.contrib.sites', 
     "vapour.common",   
     "vapour.cup",
     "vapour.strainer",
     "vapour.teapot",
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(filename)s:%(lineno)d %(levelname)s: %(message)s'
        },
        'verbose': {
            'format': '%(asctime)s %(filename)s:%(lineno)d %(process)d %(thread)d %(levelname)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level' : 'DEBUG',    # minimum level
            'class' : 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'vapour': {
            'handlers': [] if RUNNING_IN_GAE else ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': True
        }
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [".vapour-gae.appspot.com", "localhost", "127.0.0.1"]

#Custom stuff for vapour
REQ_BASE_URL = "http://validator.linkeddata.org/vapour#req"
PATH_RDF_FILES = os.path.join(ROOT_PATH, "..", "rdf")
PATH_TEMPLATES = os.path.join(ROOT_PATH, "strainer/templates/")
ALLOW_INTRANET = True

