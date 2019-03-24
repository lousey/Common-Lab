# common Django settings for commonlab project.
from os.path import abspath, dirname, join
import sys

DEPLOY_ROOT = dirname(dirname(dirname(abspath(__file__))))
PROJECT_ROOT = join(DEPLOY_ROOT, 'project')
APPS_ROOT = join(DEPLOY_ROOT, 'apps')
DB_ROOT = join(dirname(DEPLOY_ROOT), 'dbs')

sys.path.insert(0, DEPLOY_ROOT)
sys.path.insert(0, APPS_ROOT)

ADMINS = (
    ('Alice', 'awtzou@gmail.com'),
)

MANAGERS = ADMINS

# DEBUG, DATABASES overriden in dev settings file

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(DB_ROOT, 'db_v1.sqlite'),
    },
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = join(dirname(DEPLOY_ROOT), 'media') # overriden by dev

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# http://docs.djangoproject.com/en/dev/ref/settings/#file-upload-permissions
FILE_UPLOAD_PERMISSIONS = 0644

# Absolute path to the directory that holds static files.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = join(DEPLOY_ROOT, 'static')

# URL that handles the static files served from STATIC_ROOT.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/grappelli/'

# grappelli settings
# http://code.google.com/p/django-grappelli/wiki/settings
GRAPPELLI_ADMIN_URL = '/admin/'
GRAPPELLI_ADMIN_TITLE = 'CommonLab Admin'

# A list of locations of additional static files
STATICFILES_DIRS = (
    join(PROJECT_ROOT, 'static'),
    join(APPS_ROOT, 'commonlab', 'static')
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# http://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (
    join(PROJECT_ROOT, 'fixtures'),
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '(74j1alyw@%3_ta+l3982ii6q11r8t5a&9_l9td3j8==t$%mon'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

# http://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'commonlab.context_processors.base'
)

EMAIL_DOMAIN = "commonlab.com"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'commonlabquestion'
EMAIL_HOST_PASSWORD = 'common1010'
DEFAULT_FROM_EMAIL = 'Commonlab.com <{0}>'.format(EMAIL_HOST_USER)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'project.urls'

TEMPLATE_DIRS = (
    join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'grappelli', # must come before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.admindocs',

    'commonlab'
)


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request':{
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
