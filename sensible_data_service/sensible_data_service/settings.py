# Django settings for sensible_data_service project.

import os
import LOCAL_SETTINGS

DEBUG = True
TEMPLATE_DEBUG = DEBUG
MAINTENANCE_MODE = False


ADMINS = (
     ('Dude', 'dude@rug.com'),
)

MANAGERS = ADMINS
BASE_DIR = LOCAL_SETTINGS.BASE_DIR
ROOT_DIR = LOCAL_SETTINGS.ROOT_DIR
ROOT_URL = LOCAL_SETTINGS.ROOT_URL
BASE_URL = LOCAL_SETTINGS.BASE_URL
DATA_DATABASE = LOCAL_SETTINGS.DATA_DATABASE
DATA_DATABASE_SQL = LOCAL_SETTINGS.DATA_DATABASE_SQL
FILESYSTEM_DATABASE = LOCAL_SETTINGS.FILESYSTEM_DATABASE
AUDIT_DATABASE = LOCAL_SETTINGS.AUDIT_DATABASE
DATA_BASE_DIR = LOCAL_SETTINGS.DATA_BASE_DIR
DATA_LOG_DIR = LOCAL_SETTINGS.DATA_LOG_DIR
DATA_BACKUP_DIR = LOCAL_SETTINGS.DATA_BACKUP_DIR
DATABASES = LOCAL_SETTINGS.DATABASES
PLATFORM = LOCAL_SETTINGS.PLATFORM
CONNECTORS = LOCAL_SETTINGS.CONNECTORS
SERVICE_NAME = LOCAL_SETTINGS.SERVICE_NAME
LOGGING = LOCAL_SETTINGS.LOGGING

# Make this unique, and don't share it with anybody.
SECRET_KEY = LOCAL_SETTINGS.SECRET_KEY


LOGIN_URL = ROOT_URL+'openid/login/'
LOGIN_REDIRECT_URL = ROOT_URL
OPENID_SSO_SERVER_URL = LOCAL_SETTINGS.OPENID_SSO_SERVER_URL
OPENID_USE_EMAIL_FOR_USERNAME = False
AUTHENTICATION_BACKENDS = (
            'django_openid_auth.auth.OpenIDBackend',
            'django.contrib.auth.backends.ModelBackend',
        )

OPENID_CREATE_USERS = True
OPENID_UPDATE_DETAILS_FROM_SREG = False

DATABASE_ROUTERS = ['questions.router.QuestionsDatabaseRouter']
def failure_handler_function(request, message, status=None, template_name=None, exception=None):
	from django.shortcuts import redirect
	from django.http import HttpResponse
	registration = request.REQUEST.get('registration', False)
	next = request.REQUEST.get('next', '')
	if registration: return redirect(next)
	#return redirect('openid_failed')
    	return HttpResponse(message)

OPENID_RENDER_FAILURE = failure_handler_function

MAINTENANCE_IGNORE_URLS = (
		    r'^.*/admin/$',
)

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['54.229.13.160']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Copenhagen'

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
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ROOT_DIR+'static_root'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = ROOT_URL+'static/'

# Additional locations of static files
STATICFILES_DIRS = (
	ROOT_DIR + 'static',
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
	'maintenancemode.middleware.MaintenanceModeMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
        'django.core.context_processors.static',
        'django.contrib.auth.context_processors.auth',
        'sensible_data_service.context_processors.service',
)

ROOT_URLCONF = 'sensible_data_service.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'sensible_data_service.wsgi.application'

TEMPLATE_DIRS = (
	ROOT_DIR+'templates',
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django_openid_auth',
    'bootstrap_toolkit',
    'uni_form',
    'south',
    'connectors',
    'utils',
    'authorization_manager',
    'application_manager',
    'accounts',
    'platform_manager',
    'testing',
    'connectors.connector_funf',
    'connectors.connector_questionnaire',
    'connectors.connector_facebook',
    'connectors.connector_raw',
    'connectors.connector_answer',
    'anonymizer',
    'oauth2app',
    'documents',
    'render',
    'backup',
	'djcelery',
	'questions',
	'sensible_audit',
	'db_access',
	'django_nose',
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
    'formatters': {
        'verbose': {
            'format': '%(levelname)s|%(asctime)s|%(module)s| %(message)s',
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 0,
            'filename': os.path.join(LOCAL_SETTINGS.DATA_LOG_DIR, 'log'),
            'formatter': 'verbose',
        },
        'fluentd_audit': {
            'level': 'INFO',
            'class': 'fluent.handler.FluentHandler',
            'tag': 'sensible.audit',
            'host': LOGGING['host'],
            'port': LOGGING['port']
        },
        'fluentd_log': {
            'level': 'INFO',
            'class': 'fluent.handler.FluentHandler',
            'tag': 'sensible.log',
            'host': LOGGING['host'],
            'port': LOGGING['port']
        },
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            }
    },
    'loggers': LOCAL_SETTINGS.LOGGING['loggers'],
}

CACHES = {
	'default': {
		'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
		'LOCATION': '/var/tmp/django_cache',
	},

	'memory': {
		'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
		'LOCATION': 'query_paging',
		'TIMEOUT': 60,
		'OPTIONS': {
			'MAX_ENTRIES': 1000
		}
	}
}

import hashlib
SESSION_COOKIE_NAME = str(hashlib.sha1(SECRET_KEY).hexdigest())

import djcelery
import djcelery.schedulers
djcelery.setup_loader()

CELERYBEAT_SCHEDULER = djcelery.schedulers.DatabaseScheduler

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
