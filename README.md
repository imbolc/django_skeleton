Skeleton for django site
------------------------
- fabric
- nginx
- gunicorn
- supervisor
- logging
- django-debug-toolbar
- django-pipeline (assets compressor)


Development setup
-----------------

    mkdir -p var/log
    python -m venv var/env; var/env/bin/pip install -r settings/requirements.txt
    ./manage.py runserver

Add server repo remotes:

    git remote add dev user@django-skeleton.imbolc.name:django_skeleton

Deployment
----------

    git clone git@bitbucket.org:imbolc/django_skeleton.git
    cd django_skeleton; mkdir -p var/log
    python -m venv var/env; var/env/bin/pip install -r settings/requirements.txt
    sudo ./manage.py nginx --no-ssl
    ./manage.py certbot obtain
    sudo ./manage.py nginx
    sudo ./manage.py supervisor


Gevent
------
    gunicorn project.wsgi_gevent --worker-class gevent --worker-connections 10


Migrations
----------
./manage.py makemigrations
./manage.py migrate
