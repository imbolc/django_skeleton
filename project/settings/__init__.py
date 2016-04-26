from os.path import dirname, abspath, join

DEBUG = False
BASE_DIR = dirname(dirname(abspath(__file__)))

# fill this settings
SECRET_KEY = ''
HOST = ''
PORT = ''
DEPLOY_HOST = HOST
DEPLOY_PATH = ''
NGINX_NAME = DEPLOY_PATH
SUPERVISOR_NAME = DEPLOY_PATH
SUPERVISOR_USER = ''

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
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

    'debug_toolbar',
    'pipeline',

    'project',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['project/templates', ''],
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

ENV_DIR = './var/env'
ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = 'project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django_skeleton',
    }
}

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
    join(BASE_DIR, 'static'),
]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
    'pipeline.finders.CachedFileFinder',
)
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

PIPELINE = {
    'PIPELINE_ENABLED': True,
    'YUGLIFY_BINARY': join(BASE_DIR, '../node_modules/yuglify/bin/yuglify'),

    'STYLESHEETS': {
        'common': {
            'source_filenames': (
              'vendors/bootstrap/bootstrap.css',
            ),
            'output_filename': 'gen/common.css',
        },
    },
    'JAVASCRIPT': {
        'common': {
            'source_filenames': (
              'vendors/bootstrap/bootstrap.js',
            ),
            'output_filename': 'gen/common.js',
        }
    }
}

LOGGING_FILENAME = './var/log/site'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)-8s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '%(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': LOGGING_FILENAME,
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 1,
        }
    },
    'loggers': {
        'django': {
            'level': 'WARNING',
            'handlers': ['console', 'file'],
            'propagate': False,
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file'],
    },
}


try:
    from .local import *  # noqa
except ImportError:
    pass
