import os
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from django.conf import settings


def check_requirements():
    required_settings = ['SUPERVISOR_NAME', 'SUPERVISOR_USER', 'DEPLOY_PORT']
    unset = [k for k in required_settings if not getattr(settings, k, None)]
    if unset:
        raise CommandError(
            'you have to set next settings: {}'.format(unset))


class Command(BaseCommand):
    help = 'Configure and restart supervisor'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true')

    def handle(self, *args, **options):
        check_requirements()

        root = Path(__file__).resolve().parents[3]
        text = render_to_string('deploy/supervisor.conf', {
            'root': root,
            'name': settings.SUPERVISOR_NAME,
            'user': settings.SUPERVISOR_USER,
            'port': settings.DEPLOY_PORT,
            'settings': settings,
        })
        print(text)

        if options['dry_run']:
            print("Dry-run, real config wasn't touched")
            return

        filename = '/etc/supervisor/conf.d/{}.conf'.format(
            settings.SUPERVISOR_NAME)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f'Supervisor config created: {filename}')

        os.system('/etc/init.d/supervisor restart')
