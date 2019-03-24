# dev-specific settings
from os.path import join
from .common import *

PROJECT_ENV = 'dev'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(DEPLOY_ROOT, 'dev_db.sqlite'),
    },
}

MEDIA_ROOT = join(DEPLOY_ROOT, 'dev-media')

# required by debug_toolbar
INTERNAL_IPS = ('127.0.0.1',)

# https://github.com/robhudson/django-debug-toolbar
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'HIDE_DJANGO_SQL': False,
}

MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS = INSTALLED_APPS + (
    'debug_toolbar',
    'django_extensions',
)
