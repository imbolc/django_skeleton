Skeleton for django site
------------------------
- fabric
- nginx
- gunicorn
- supervisor
- logging
- django-debug-toolbar
- django-pipeline (assets compressor)


Install
-------
    fab buildenv
    ./manage.py migrate
    npm i
    sudo ./manage.py configure_nginx
    sudo ./manage.py configure_supervisor


Gevent
------
    gunicorn project.wsgi_gevent --worker-class gevent --worker-connections 10


Migrations
----------
./manage.py makemigrations
./manage.py migrate
