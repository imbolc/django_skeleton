import os
from pathlib import Path

from django.core.management.base import BaseCommand
from django.conf import settings


COMMAND = '''
    ./var/env/bin/certbot {}
        --config-dir=./var/certbot/cfg
        --work-dir=./var/certbot/work
        --logs-dir=./var/log/certbot
        --renew-hook "sudo /etc/init.d/nginx reload"
'''
COMMAND = ' '.join(COMMAND.split())
ROOT = Path(__file__).resolve().parents[3]


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('command')

    def handle(self, *args, **options):
        command = options['command']
        assert command in ['obtain', 'renew']
        globals()[command]()


def obtain():
    dir = './var/static/root'
    os.makedirs(dir, exist_ok=True)
    hosts = ' '.join(f'-d {h}' for h in settings.CERTBOT_HOSTS)
    command = COMMAND.format(f'certonly --webroot -w {dir} {hosts}')
    print(command)
    os.system(command)
    print('Do not forget to add RENEW command to your CRONTAB:')
    print(f'15 4 * * *  cd {ROOT}; timeout 10m ./manage.py certbot renew')


def renew():
    command = COMMAND.format(f'renew')
    print(command)
    os.system(command)
