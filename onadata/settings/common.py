# vim: set fileencoding=utf-8
# this system uses structured settings as defined in
# http://www.slideshare.net/jacobian/the-best-and-worst-of-django
#
# this is the base settings.py -- which contains settings common to all
# implementations of ona: edit it at last resort
#
# local customizations should be done in several files each of which in turn
# imports this one.
# The local files should be used as the value for your DJANGO_SETTINGS_MODULE
# environment variable as needed.
import logging
import os
import socket
import subprocess  # noqa, used by included files
import sys
from imp import reload

from future.moves.urllib.parse import urljoin

from past.builtins import basestring

from django.core.exceptions import SuspiciousOperation
from django.utils.log import AdminEmailHandler

from celery.signals import after_setup_logger

from onadata.libs.utils.string import str2bool


# setting default encoding to utf-8
if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding("utf-8")

CURRENT_FILE = os.path.abspath(__file__)
PROJECT_ROOT = os.path.realpath(
    os.path.join(os.path.dirname(CURRENT_FILE), '../'))
BASE_DIR = os.path.dirname(PROJECT_ROOT)
PRINT_EXCEPTION = False

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(BASE_DIR, ".env"))
except ImportError:
    pass

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 's3cr3t-K3y')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = str2bool(os.environ.get('DEBUG', False))

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split()

TEMPLATED_EMAIL_TEMPLATE_DIR = 'templated_email/'

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS


DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@ona.io')
SHARE_PROJECT_SUBJECT = os.environ.get(
    'SHARE_PROJECT_SUBJECT', '{} Ona Project has been shared with you.')
SHARE_ORG_SUBJECT = os.environ.get(
    'SHARE_ORG_SUBJECT', '{}, You have been added to {} organisation.')
DEFAULT_SESSION_EXPIRY_TIME = int(os.environ.get(
    'DEFAULT_SESSION_EXPIRY_TIME', 21600))  # 6 hours by default
DEFAULT_TEMP_TOKEN_EXPIRY_TIME = int(os.environ.get(
    'DEFAULT_TEMP_TOKEN_EXPIRY_TIME', 21600))  # 6 hours by default

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = os.environ.get('TIME_ZONE', 'America/New_York')

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = os.environ.get('LANGUAGE_CODE', 'en-us')

LANGUAGES = (
    ('fr', u'Français'),
    ('en', u'English'),
    ('es', u'Español'),
    ('it', u'Italiano'),
    ('km', u'ភាសាខ្មែរ'),
    ('ne', u'नेपाली'),
    ('nl', u'Nederlands'),
    ('zh', u'中文'),
)

SITE_ID = int(os.environ.get('SITE_ID', 1))

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = str2bool(os.environ.get('USE_I18N', True))

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = str2bool(os.environ.get('USE_L10N', True))

# Media root
MEDIA_ROOT = os.environ.get('MEDIA_ROOT', os.path.join(BASE_DIR, 'media'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = os.environ.get('MEDIA_URL', 'http://localhost:8000/media/')

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.environ.get('STATIC_ROOT', os.path.join(BASE_DIR, 'static'))

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = os.environ.get('STATIC_URL', '/static/')

# Enketo URL
ENKETO_PROTOCOL = os.environ.get('ENKETO_PROTOCOL', 'https')
ENKETO_URL = os.environ.get('ENKETO_URL', 'https://enketo.ona.io/')
ENKETO_API_SURVEY_PATH = os.environ.get(
    'ENKETO_API_SURVEY_PATH', '/api_v2/survey')
ENKETO_API_INSTANCE_PATH = os.environ.get(
    'ENKETO_API_INSTANCE_PATH', '/api_v2/instance')
ENKETO_PREVIEW_URL = os.environ.get(
    'ENKETO_PREVIEW_URL',
    urljoin(ENKETO_URL, ENKETO_API_SURVEY_PATH + '/preview'))
ENKETO_API_TOKEN = os.environ.get('ENKETO_API_TOKEN', '')
ENKETO_API_INSTANCE_IFRAME_URL = os.environ.get(
    'ENKETO_API_INSTANCE_IFRAME_URL', ENKETO_URL + "api_v2/instance/iframe")
ENKETO_API_SALT = os.environ.get('ENKETO_API_SALT', 'secretsalt')
VERIFY_SSL = str2bool(os.environ.get('VERIFY_SSL', True))

TOUCHFORMS_URL = os.environ.get('TOUCHFORMS_URL', 'http://localhost:9000/')

# Login URLs
LOGIN_URL = os.environ.get('LOGIN_URL', '/accounts/login/')
LOGIN_REDIRECT_URL = os.environ.get('LOGIN_REDIRECT_URL', '/login_redirect/')

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = os.environ.get('ADMIN_MEDIA_PREFIX', '/static/admin/')

# Additional locations of static files
# Put strings here, like "/home/html/static" or "C:/www/django/static".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
STATICFILES_DIRS = os.environ.get('STATICFILES_DIRS', '').split()

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': os.environ.get('TEMPLATES_DIRS', '').split() or [
            os.path.join(PROJECT_ROOT, 'libs/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'onadata.apps.main.context_processors.google_analytics',
                'onadata.apps.main.context_processors.site_name',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DATABASES_DEFAULT_ENGINE',
                                 'django.contrib.gis.db.backends.postgis'),
        'NAME': os.environ.get('DATABASES_DEFAULT_NAME', 'onadata'),
        'USER': os.environ.get('DATABASES_DEFAULT_USER', 'onadata'),
        'PASSWORD': os.environ.get('DATABASES_DEFAULT_PASSWORD', ''),
        'HOST': os.environ.get('DATABASES_DEFAULT_HOST', '127.0.0.1'),
        'PORT': int(os.environ.get('DATABASES_DEFAULT_PORT', 5432)),
        'CONN_MAX_AGE': int(os.environ.get(
            'DATABASES_DEFAULT_CONN_MAX_AGE', 0)),
        'ATOMIC_REQUESTS': str2bool(os.environ.get(
            'DATABASES_DEFAULT_ATOMIC_REQUESTS', False))
    }
}

DATABASE_ROUTERS = os.environ.get('DATABASE_ROUTERS', '').split()

SLAVE_DATABASES = os.environ.get('SLAVE_DATABASES', '').split()

# Caching
CACHES = {
    'default': {
        'BACKEND': os.environ.get(
            'CACHES_DEFAULT_BACKEND',
            'django.core.cache.backends.memcached.PyLibMCCache'),
        'LOCATION': os.environ.get(
            'CACHES_DEFAULT_LOCATION', '127.0.0.1:11211').split(),
        'TIMEOUT': int(os.environ.get('CACHES_DEFAULT_TIMEOUT', 300)),
        'VERSION': int(os.environ.get('CACHES_DEFAULT_VERSION', 1)),
    }
}

CACHE_MIDDLEWARE_SECONDS = int(os.environ.get(
    'CACHE_MIDDLEWARE_SECONDS', 3600))
CACHE_MIDDLEWARE_KEY_PREFIX = os.environ.get('CACHE_MIDDLEWARE_KEY_PREFIX', '')

# Middleware

MIDDLEWARE = (
    'onadata.libs.profiling.sql.SqlTimingMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
    'onadata.libs.utils.middleware.LocaleMiddlewareWithTweaks',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'onadata.libs.utils.middleware.HTTPResponseNotAllowedMiddleware',
)

LOCALE_PATHS = (os.path.join(PROJECT_ROOT, 'onadata.apps.main', 'locale'), )

ROOT_URLCONF = 'onadata.apps.main.urls'
USE_TZ = str2bool(os.environ.get('USE_TZ', True))

# needed by guardian
ANONYMOUS_DEFAULT_USERNAME = os.environ.get(
    'ANONYMOUS_DEFAULT_USERNAME', 'AnonymousUser')

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.gis',
    'registration',
    'django_nose',
    'django_digest',
    'corsheaders',
    'oauth2_provider',
    'rest_framework',
    'rest_framework.authtoken',
    'taggit',
    'onadata.apps.logger',
    'onadata.apps.viewer',
    'onadata.apps.main',
    'onadata.apps.restservice',
    'onadata.apps.api',
    'guardian',
    'onadata.apps.sms_support',
    'onadata.libs',
    'reversion',
    'actstream',
    'onadata.apps.messaging.apps.MessagingConfig',
    'django_celery_results',
)

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
        'groups': 'Access to your groups'}
}

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
    'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'onadata.libs.authentication.DigestAuthentication',
        'onadata.libs.authentication.TempTokenAuthentication',
        'onadata.libs.authentication.EnketoTokenAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework_jsonp.renderers.JSONPRenderer',
        'rest_framework_csv.renderers.CSVRenderer',
    ),
}

SWAGGER_SETTINGS = {
    "exclude_namespaces": [],    # List URL namespaces to ignore
    "api_version": '1.0',  # Specify your API's version (optional)
    "enabled_methods": [         # Methods to enable in UI
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ],
}

CORS_ORIGIN_ALLOW_ALL = str2bool(os.environ.get(
    'CORS_ORIGIN_ALLOW_ALL', False))
CORS_ALLOW_CREDENTIALS = str2bool(os.environ.get(
    'CORS_ALLOW_CREDENTIALS', True))
CORS_ORIGIN_WHITELIST = os.environ.get(
    'CORS_ORIGIN_WHITELIST', 'dev.ona.io').split()
CORS_URLS_ALLOW_ALL_REGEX = (
    r'^/api/v1/osm/.*$',
)

USE_THOUSAND_SEPARATOR = True

COMPRESS = str2bool(os.environ.get('COMPRESS', True))

# extra data stored with users
AUTH_PROFILE_MODULE = 'onadata.apps.main.UserProfile'

# case insensitive usernames
AUTHENTICATION_BACKENDS = (
    'onadata.apps.main.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

# Settings for Django Registration
ACCOUNT_ACTIVATION_DAYS = int(os.environ.get('ACCOUNT_ACTIVATION_DAYS', 1))


def skip_suspicious_operations(record):
    """Prevent django from sending 500 error
    email notifications for SuspiciousOperation
    events, since they are not true server errors,
    especially when related to the ALLOWED_HOSTS
    configuration

    background and more information:
    http://www.tiwoc.de/blog/2013/03/django-prevent-email-notification-on-susp\
    iciousoperation/
    """
    if record.exc_info:
        exc_value = record.exc_info[1]
        if isinstance(exc_value, SuspiciousOperation):
            return False
    return True


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s' +
                      ' %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'profiler': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
        'sql': {
            'format': '%(levelname)s %(process)d %(thread)d' +
                      ' %(time)s seconds %(message)s %(sql)s'
        },
        'sql_totals': {
            'format': '%(levelname)s %(process)d %(thread)d %(time)s seconds' +
                      ' %(message)s %(num_queries)s sql queries'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        # Define filter for suspicious urls
        'skip_suspicious_operations': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': skip_suspicious_operations,
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false', 'skip_suspicious_operations'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': sys.stdout
        },
        'audit': {
            'level': 'DEBUG',
            'class': 'onadata.libs.utils.log.AuditLogHandler',
            'formatter': 'verbose',
            'model': 'onadata.apps.main.models.audit.AuditLog'
        },
        # 'sql_handler': {
        #     'level': 'DEBUG',
        #     'class': 'logging.StreamHandler',
        #     'formatter': 'sql',
        #     'stream': sys.stdout
        # },
        # 'sql_totals_handler': {
        #     'level': 'DEBUG',
        #     'class': 'logging.StreamHandler',
        #     'formatter': 'sql_totals',
        #     'stream': sys.stdout
        # }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'console_logger': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'audit_logger': {
            'handlers': ['audit'],
            'level': 'DEBUG',
            'propagate': True
        },
        # 'sql_logger': {
        #     'handlers': ['sql_handler'],
        #     'level': 'DEBUG',
        #     'propagate': True
        # },
        # 'sql_totals_logger': {
        #     'handlers': ['sql_totals_handler'],
        #     'level': 'DEBUG',
        #     'propagate': True
        # }
    }
}

# PROFILE_API_ACTION_FUNCTION is used to toggle profiling a viewset's action
PROFILE_API_ACTION_FUNCTION = False
PROFILE_LOG_BASE = '/tmp/'


def configure_logging(logger, **kwargs):
    admin_email_handler = AdminEmailHandler()
    admin_email_handler.setLevel(logging.ERROR)
    logger.addHandler(admin_email_handler)


after_setup_logger.connect(configure_logging)

GOOGLE_STEP2_URI = os.environ.get('GOOGLE_STEP2_URI', 'http://ona.io/gwelcome')
GOOGLE_OAUTH2_CLIENT_ID = os.environ.get(
    'GOOGLE_OAUTH2_CLIENT_ID', 'REPLACE ME')
GOOGLE_OAUTH2_CLIENT_SECRET = os.environ.get(
    'GOOGLE_OAUTH2_CLIENT_SECRET', 'REPLACE ME')

THUMB_CONF = {
    'large': {'size': 1280, 'suffix': '-large'},
    'medium': {'size': 640, 'suffix': '-medium'},
    'small': {'size': 240, 'suffix': '-small'},
}
# order of thumbnails from largest to smallest
THUMB_ORDER = os.environ.get('THUMB_ORDER', 'large medium small').split()
IMG_FILE_TYPE = os.environ.get('IMG_FILE_TYPE', 'jpg')

# celery
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'django-db')
CELERY_TASK_ALWAYS_EAGER = str2bool(os.environ.get(
    'CELERY_TASK_ALWAYS_EAGER', False))
CELERY_TASK_IGNORE_RESULT = str2bool(os.environ.get(
    'CELERY_TASK_IGNORE_RESULT', False))
CELERY_TASK_TRACK_STARTED = str2bool(os.environ.get(
    'CELERY_TASK_TRACK_STARTED', False))
CELERY_IMPORTS = ('onadata.libs.utils.csv_import',)


CSV_FILESIZE_IMPORT_ASYNC_THRESHOLD = int(os.environ.get(
    'CSV_FILESIZE_IMPORT_ASYNC_THRESHOLD', 100000))  # Bytes
GOOGLE_SHEET_UPLOAD_BATCH = int(os.environ.get(
    'GOOGLE_SHEET_UPLOAD_BATCH', 1000))

# duration to keep zip exports before deletion (in seconds)
ZIP_EXPORT_COUNTDOWN = int(os.environ.get('ZIP_EXPORT_COUNTDOWN', 3600))

# number of records on export or CSV import before a progress update
EXPORT_TASK_PROGRESS_UPDATE_BATCH = int(os.environ.get(
    'EXPORT_TASK_PROGRESS_UPDATE_BATCH', 1000))
EXPORT_TASK_LIFESPAN = int(os.environ.get('EXPORT_TASK_LIFESPAN', 6))  # hours

# default content length for submission requests
DEFAULT_CONTENT_LENGTH = int(os.environ.get(
    'DEFAULT_CONTENT_LENGTH', 10000000))

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['--with-fixture-bundling', '--nologcapture', '--nocapture']

# fake endpoints for testing
TEST_HTTP_HOST = 'testserver.com'
TEST_USERNAME = 'bob'

# specify the root folder which may contain a templates folder and a static
# folder used to override templates for site specific details
TEMPLATE_OVERRIDE_ROOT_DIR = None

# Use 1 or 0 for multiple selects instead of True or False for csv, xls exports
BINARY_SELECT_MULTIPLES = False

# Use 'n/a' for empty values by default on csv exports
NA_REP = 'n/a'

if isinstance(TEMPLATE_OVERRIDE_ROOT_DIR, basestring):
    # site templates overrides
    TEMPLATES[0]['DIRS'] = [
        os.path.join(PROJECT_ROOT, TEMPLATE_OVERRIDE_ROOT_DIR, 'templates'),
    ] + TEMPLATES[0]['DIRS']
    # site static files path
    STATICFILES_DIRS += (
        os.path.join(PROJECT_ROOT, TEMPLATE_OVERRIDE_ROOT_DIR, 'static'),
    )

# Set wsgi url scheme to HTTPS
os.environ['wsgi.url_scheme'] = 'https'

SUPPORTED_MEDIA_UPLOAD_TYPES = [
    'audio/mp3',
    'audio/mpeg',
    'audio/wav',
    'audio/x-m4a',
    'image/jpeg',
    'image/png',
    'image/svg+xml',
    'text/csv',
    'text/json',
    'video/3gpp',
    'video/mp4',
    'application/json',
    'application/pdf',
    'application/msword',
    'application/vnd.ms-excel',
    'application/vnd.ms-powerpoint',
    'application/vnd.oasis.opendocument.text',
    'application/vnd.oasis.opendocument.spreadsheet',
    'application/vnd.oasis.opendocument.presentation',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.openxmlformats-officedocument.presentationml.\
     presentation',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/zip',
]

CSV_ROW_IMPORT_ASYNC_THRESHOLD = int(os.environ.get(
    'CSV_ROW_IMPORT_ASYNC_THRESHOLD', 100))
SEND_EMAIL_ACTIVATION_API = str2bool(os.environ.get(
    'SEND_EMAIL_ACTIVATION_API', False))
METADATA_SEPARATOR = os.environ.get('METADATA_SEPARATOR', '|')

PARSED_INSTANCE_DEFAULT_LIMIT = int(os.environ.get(
    'PARSED_INSTANCE_DEFAULT_LIMIT', 1000000))
PARSED_INSTANCE_DEFAULT_BATCHSIZE = int(os.environ.get(
    'PARSED_INSTANCE_DEFAULT_BATCHSIZE', 1000))

PROFILE_SERIALIZER = \
    "onadata.libs.serializers.user_profile_serializer.UserProfileSerializer"
ORG_PROFILE_SERIALIZER = \
    "onadata.libs.serializers.organization_serializer.OrganizationSerializer"
BASE_VIEWSET = "onadata.libs.baseviewset.DefaultBaseViewset"

path = os.path.join(PROJECT_ROOT, "..", "extras", "reserved_accounts.txt")

EXPORT_WITH_IMAGE_DEFAULT = str2bool(os.environ.get(
    'EXPORT_WITH_IMAGE_DEFAULT', True))
try:
    with open(path, 'r') as f:
        RESERVED_USERNAMES = [line.rstrip() for line in f]
except EnvironmentError:
    RESERVED_USERNAMES = []

STATIC_DOC = os.environ.get('STATIC_DOC', '/static/docs/index.html')

try:
    HOSTNAME = socket.gethostname()
except Exception:
    HOSTNAME = 'localhost'

CACHE_MIXIN_SECONDS = int(os.environ.get('CACHE_MIXIN_SECONDS', 60))

TAGGIT_CASE_INSENSITIVE = str2bool(os.environ.get(
    'TAGGIT_CASE_INSENSITIVE', True))

DEFAULT_CELERY_MAX_RETIRES = int(os.environ.get(
    'DEFAULT_CELERY_MAX_RETIRES', 3))
DEFAULT_CELERY_INTERVAL_START = float(os.environ.get(
    'DEFAULT_CELERY_INTERVAL_START', 2))
DEFAULT_CELERY_INTERVAL_MAX = float(os.environ.get(
    'DEFAULT_CELERY_INTERVAL_MAX', 0.5))
DEFAULT_CELERY_INTERVAL_STEP = float(os.environ.get(
    'DEFAULT_CELERY_INTERVAL_STEP', 0.5))

CUSTOM_MAIN_URLS = set(os.environ.get('CUSTOM_MAIN_URLS', '').split())

# legacy setting for old sites who still use a local_settings.py file and have
# not updated to presets/
try:
    from local_settings import *  # noqa
except ImportError:
    pass

# email verification
ENABLE_EMAIL_VERIFICATION = str2bool(os.environ.get(
    'ENABLE_EMAIL_VERIFICATION', False))
VERIFIED_KEY_TEXT = os.environ.get('VERIFIED_KEY_TEXT', 'ALREADY_ACTIVATED')
