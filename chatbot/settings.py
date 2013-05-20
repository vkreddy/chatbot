# Django settings for chatbot project.
from os import environ
from urlparse import urlparse
import os.path
import sys

#DEBUG = True
#TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '9zc8_hw&amp;5*u0wc0jn1uar3&amp;8)@2i0wepgxu5#vym*0qg5ebb%!'

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
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'chatbot.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'chatbot.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__),'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'kombu.transport.django',
    'djcelery',
    'django_hipchat',
    'bot'
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


#This is the URL that users get directed to for pages that use the @login_required decorator
LOGIN_URL = '/login/'

# This is used when the when the contrib.auth.login view gets no next parameter
LOGIN_REDIRECT_URL = '/'

#If you want this to work locally you need to set up a postgres database called
#gb on your computer - download postgres here: http://postgresapp.com
import dj_database_url
DATABASES = {
        'default':
                dj_database_url.config(default='postgres://karthik:vkr090@localhost:5432/gb')
}


FACEBOOK_SCOPE = ['offline_access']                   # application scopes
FACEBOOK_APP_ID = '526627504062453'                               # application ID
FACEBOOK_APP_SECRET = '717a266c7a394c229c46adc91bcb4e8c'                           # application secret key
FACEBOOK_ACCESS_TOKEN = 'CAACEdEose0cBAERLwUda5GoaD115u1ZC72rJtlRSxp36scVe8KEUy59aDZBruWjTAZAe7Tiqfg0nxpZCXPoG4At9wwWNFarkQAHC7H1qN9dmvSZAIzP20lEKovRbVmhFp0MxHUqaOj74qCnZCcZB4MKU4d6bMblksaa5ZClQV62vfQZDZD'

# HipChat credentials
HIPCHAT_MESSAGE_ROOM = 'Karthik Project'
HIPCHAT_AUTH_TOKEN = '2c637806f4c031e35006882b9f5240'
HIPCHAT_MESSAGE_FROM = 'Food Bot'

# Celery details
#BROKER_BACKEND = "djkombu.transport.DatabaseTransport"
#BROKER_BACKEND = "django"
BROKER_URL = "django://guest:guest@localhost:5672//"

from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    'add-every-morning': {
        'task': 'bot.tasks.update_database',
        'schedule': crontab(hour=7,minute=30)
    },
}


import djcelery
djcelery.setup_loader()

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
