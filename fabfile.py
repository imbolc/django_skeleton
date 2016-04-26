from __future__ import print_function
import os
from os.path import normcase, dirname

from fabric import api
from project.settings import (ENV_DIR, DEPLOY_HOST, DEPLOY_PATH,
                              SUPERVISOR_NAME, LOGGING_FILENAME)


api.env.hosts = [DEPLOY_HOST]
PIP_PATH = normcase(ENV_DIR + '/bin/pip')
PIPREQ_PATH = normcase('project/settings/pipreq.txt')


def prepare():
    for path in [ENV_DIR, dirname(LOGGING_FILENAME)]:
        try:
            os.makedirs(path)
        except OSError:
            pass


def buildenv():
    prepare()
    with api.settings(warn_only=True):
        api.local('pyvenv ' + ENV_DIR, capture=False)
    api.local(normcase(ENV_DIR + '/bin/easy_install pip'), capture=False)

    for name in open(PIPREQ_PATH):
        name = name.strip()
        if not name or name.startswith('#'):
            continue
        api.local('{} install --upgrade --force {}'.format(PIP_PATH, name))


def pull():
    api.local('git pull ssh://{}/{}'.format(DEPLOY_HOST, DEPLOY_PATH))


def deploy_fix():
    api.local("git ci -am'little fix'")
    api.local('fab deploy')


def deploy():
    push()
    collectstatic()
    restart()


def collectstatic():
    with api.cd(DEPLOY_PATH):
        api.run('./manage.py collectstatic --noinput --clear')


def restart():
    with api.cd(DEPLOY_PATH):
        api.run('sudo supervisorctl restart {}:*'.format(SUPERVISOR_NAME))


def push():
    api.local('git push')
    with api.cd(DEPLOY_PATH):
        api.run('git pull')


def log():
    with api.cd(DEPLOY_PATH):
        api.run('tail -n50 -f {}'.format(LOGGING_FILENAME))


def rm_log():
    with api.cd(DEPLOY_PATH):
        api.run('rm {}'.format(LOGGING_FILENAME))
    restart()


def uplib(name):
    for line in open(PIPREQ_PATH):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        print(name, line, name in line)
        if name in line:
            api.local('{} install --upgrade --force {}'.format(PIP_PATH, line))


def freeze():
    api.local('{} freeze'.format(PIP_PATH))
