import subprocess
import paramiko
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = 'Deploy code to server'

    def add_arguments(self, parser):
        parser.add_argument('remote')
        parser.add_argument('--no-build', action='store_true')
        parser.add_argument('--no-static', action='store_true')

    def handle(self, *args, **options):
        remote = get_remote(options)
        subprocess.run(f'git push', shell=True)
        ssh = SSHClient(remote)
        ssh.run('git pull')
        if not options['no_build']:
            ssh.run('npm run build')
        if not options['no_static']:
            ssh.run('./manage.py collectstatic -l --noinput --link')
        ssh.run('./manage.py migrate --no-input')
        ssh.run(f'sudo supervisorctl restart {settings.SUPERVISOR_NAME}:*')


def get_remote(options):
    name = options['remote']
    try:
        url = subprocess.check_output(
            ['git', 'remote', 'get-url', '--push', name],
            stderr=subprocess.STDOUT,
            encoding='utf-8')
    except subprocess.CalledProcessError as e:
        raise CommandError(e.output)
    return url.strip()


def parse_git_url(git_url):
    host, path = git_url.split(':')
    user = None
    if '@' in host:
        user, host = host.split('@')
    return user, host, path


class SSHClient(paramiko.SSHClient):
    def __init__(self, git_url):
        super().__init__()
        user, host, self.path = parse_git_url(git_url)
        self.load_system_host_keys()
        self.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.connect(host, username=user)

    def run_silently(self, command):
        command = f'cd {self.path}; {command}'
        print('[remote]', command)
        stdin, stdout, stderr = self.exec_command(command, get_pty=True)
        out = []
        while True:
            char = stdout.read(1).decode('utf-8', 'ignore')
            if not char:
                break
            out.append(char)
            print(char, end="")
        out = ''.join(out)
        status = stdout.channel.recv_exit_status()
        return out, status

    def run(self, command):
        out, status = self.run_silently(command)
        if status:
            raise CommandError(f'Command finished with error status: {status}')
        return out
