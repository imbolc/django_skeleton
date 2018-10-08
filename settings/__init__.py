from pathlib import Path
from .secret import SECRET_KEY  # noqa

DEBUG = False
ROOT = Path(__file__).resolve().parents[1]

# fill this
HOST = ''
DEPLOY_HOST = HOST
DEPLOY_PORT = ''
DEPLOY_PATH = ''
NGINX_NAME = ''
SUPERVISOR_NAME = DEPLOY_PATH
SUPERVISOR_USER = ''
CERTBOT_HOSTS = [HOST]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
    }
}

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', HOST]
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'settings',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['settings/templates', ''],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            #  'loaders': [
            #      ('django.template.loaders.cached.Loader', [
            #          'django.template.loaders.filesystem.Loader',
            #          'django.template.loaders.app_directories.Loader',
            #      ]),
            #  ],
        },
    },
]

ROOT_URLCONF = 'settings.urls'
WSGI_APPLICATION = 'settings.wsgi.application'

contrib_validator = 'django.contrib.auth.password_validation.{}'
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': contrib_validator.format('UserAttributeSimilarityValidator')},
    {'NAME': contrib_validator.format('MinimumLengthValidator')},
    {'NAME': contrib_validator.format('CommonPasswordValidator')},
    {'NAME': contrib_validator.format('NumericPasswordValidator')},
]


STATIC_URL = '/static/'
STATIC_ROOT = './var/static'
STATICFILES_DIRS = [
    ROOT / 'static',
]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname).1s %(name)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '%(levelname).1s %(name)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'info_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': ROOT / 'var/log/info',
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 3,
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': ROOT / 'var/log/error',
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 3,
        },
    },
    'loggers': {
        'django': {
            'level': 'WARNING',
            'handlers': ['console', 'info_file', 'error_file'],
            'propagate': False,
        },
        'paramiko': {
            'level': 'WARNING',
            'handlers': ['console', 'info_file', 'error_file'],
            'propagate': False,
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'info_file', 'error_file'],
    },
}

try:
    from .local import *  # noqa
except ImportError:
    pass
