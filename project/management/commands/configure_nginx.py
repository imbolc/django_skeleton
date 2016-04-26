import os

from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from django.conf import settings


def check_requirements():
    required_settings = ['BASE_DIR', 'HOST', 'PORT', 'NGINX_NAME']
    unset = [k for k in required_settings if not getattr(settings, k, None)]
    if unset:
        raise CommandError(
            'you have to set next settings: {}'.format(unset))


class Command(BaseCommand):
    help = 'Configure and restart nginx'

    def handle(self, *args, **options):
        check_requirements()

        root = os.path.dirname(settings.BASE_DIR)
        text = render_to_string('deploy/nginx.txt', {
            'settings': settings, 'root': root})

        if settings.DEBUG:
            self.stdout.write(self.style.SUCCESS('You can check this config:'))
            self.stdout.write(text)
            self.stdout.write(self.style.WARNING(
                'Disable settings.DEBUG to real configuring.'))
            return

        filename = '/etc/nginx/sites-enabled/{}'.format(settings.NGINX_NAME)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
        self.stdout.write('Nginx config created: {}'.format(filename))

        os.system('nginx -t && /etc/init.d/nginx restart')
