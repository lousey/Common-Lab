# Django settings broken into dev, staging, and live
from os import environ

# if we don't have a properly defined environment, refuse to run
PROJECT_ENV_NAME = 'CL_ENV'

env = environ.get(PROJECT_ENV_NAME)
if env == 'live':
    from live import *
elif env == 'stage':
    from stage import *
elif env == 'dev':
    from dev import *
else:
    import sys
    sys.stderr.write(
"""Error: Production, staging or development?
Plz set the environment variable '%s' and try again.
Your choices are 'live', 'stage', or 'dev'.\n""" %
        PROJECT_ENV_NAME)
    sys.exit(1)

