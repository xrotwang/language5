# Django settings for website project.
import os
SITE_ROOT = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]

DEBUG = TEMPLATE_DEBUG = False

ADMINS = (
    ('Simon J. Greenhill', 'simon@simon.net.nz'),
)

INTERNAL_IPS = ('127.0.0.1',)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(SITE_ROOT, 'database.db'),
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'TEST_NAME': None,               # use SQLite in-memory for testing
    }
}

# Site details
SITE_ID = 1
SITE_NAME = SITE_DOMAIN = 'TransNewGuinea.org'
SITE_DESCRIPTION = "Trans-New Guinea Language Database"

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'


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
    os.path.join(os.path.split(SITE_ROOT)[0], 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '=_1)@n652y5qic+)1sj)7!#p##kn0#!k2@yr&amp;e)!019$0tynt2'

# Replace Test Runner with the auto-discover one (django-discover-runner)
TEST_RUNNER = 'discover_runner.DiscoverRunner'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = [
    'djangosecure.middleware.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]    

ROOT_URLCONF = 'website.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'website.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
    "website.apps.core.context_processors.InjectSettings",
    "website.apps.olac.context_processors.InjectOLACSettings",
]


INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.humanize',

    # Admin site
    'django.contrib.admin',
    'django.contrib.admindocs',
    
    # third-party
    'south',                             # south: database migrations
    'reversion',                         # reversion: object version control.
    'robots',                            # django-robots: robots.txt handling
    'djangosecure',                      # django-secure: Security helper
    'django_tables2',                    # django-tables2: tables helper
    'watson',                            # search
    'mptt',                              # django-mptt for classification app

    # website
    'website.apps.core',                 # core functionality
    'website.apps.lexicon',              # Lexicon
    'website.apps.olac',                 # OLAC utils
    'website.apps.classification',       # classification

]

# Django-Security settings
SECURE_FRAME_DENY = True         # prevent framing of pages.
SECURE_BROWSER_XSS_FILTER = True # enable XSS protection
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True

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

# Caching:
CACHES = {
    'default': {
        # 'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache',
    }
}

# Setup OLAC
from website.apps.olac.settings import OLAC_SETTINGS
OLAC_SETTINGS['institution'] = 'Australian National University'
OLAC_SETTINGS['institutionURL'] = 'http://anu.edu.au'
OLAC_SETTINGS['shortLocation'] = 'Canberra, Australia'
OLAC_SETTINGS['description'] = SITE_DESCRIPTION

# cache the ``robots.txt`` for 24 hours (86400 seconds).
ROBOTS_CACHE_TIMEOUT = 60*60*24

