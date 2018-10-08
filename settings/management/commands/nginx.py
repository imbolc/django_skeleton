import os
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from django.conf import settings


def check_requirements():
    required_settings = ['HOST', 'DEPLOY_PORT', 'NGINX_NAME']
    unset = [k for k in required_settings if not getattr(settings, k, None)]
    if unset:
        raise CommandError(
            'you have to set next settings: {}'.format(unset))


class Command(BaseCommand):
    help = 'Configure and restart nginx'

    def add_arguments(self, parser):
        parser.add_argument('--no-ssl', action='store_true')
        parser.add_argument('--dry-run', action='store_true')

    def handle(self, *args, **options):
        check_requirements()

        root = Path(__file__).resolve().parents[3]
        text = render_to_string('deploy/nginx.txt', {
            'ssl': not options['no_ssl'],
            'host': settings.HOST,
            'root': root,
            'name': settings.NGINX_NAME,
            'port': settings.DEPLOY_PORT,
        })
        print(text)

        if options['dry_run']:
            print("Dry-run, real config wasn't touched")
            return

        filename = '/etc/nginx/sites-enabled/{}'.format(settings.NGINX_NAME)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f'Nginx config created: {filename}')

        os.system('nginx -t && /etc/init.d/nginx restart')
