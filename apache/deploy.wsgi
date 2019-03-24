import os, sys

# following this as a general set-up:
# http://code.google.com/p/modwsgi/wiki/VirtualEnvironments
#
# We use the global python interpreter (with mod_wsgi, one python
# interpreter must be shared between all virtualenv's)
# The global /usr/bin/python is used by default.
# We install only very stable, usually compliled python extensions
# to the global python site-packages (since these are shared by all
# virtualenvs.)  If there isn't a good reason to install it globally - don't.

# get into the correct virtualenv
from os.path import abspath, dirname, join
project_base = dirname (dirname (abspath (__file__)))
activate_this = join(project_base, 'venv', 'bin', 'activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

from django.core.handlers.wsgi import WSGIHandler

sys.path.append(dirname(dirname(__file__)))

def application(environ, start_response):
    """
    This wsgi handler will only allow the application to run if we have
    correctly defined an environment for our project.
    """
    if not environ['CL_ENV']:
        start_response(
            '500 INTERNAL SERVER ERROR',
            [('Content-Type', 'text/plain')]
        ) 
    else:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
        os.environ['CL_ENV'] = environ['CL_ENV']
        return WSGIHandler()(environ, start_response)
