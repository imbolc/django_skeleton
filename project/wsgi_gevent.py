from gevent import monkey
monkey.patch_all()

import os
from psycogreen.gevent import patch_psycopg

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
patch_psycopg()

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
