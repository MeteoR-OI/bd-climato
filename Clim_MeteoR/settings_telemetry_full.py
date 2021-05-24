"""
Django settings for Clim_MeteoR project.

Generated by 'django-admin startproject' using Django 2.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
SITE_ROOT = os.path.dirname(PROJECT_ROOT)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n=m9oh3l5np7o!63#ad5tgjy_r7*tqlm6l!%lzjw#^=pue0ba)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
        'beta.meteor-oi.re',
        '127.0.0.1',
        '10.5.0.90',
        'data.meteor-oi.re',
        'localhost']

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "app", "static"),
]
# Application definition

INSTALLED_APPS = [
    'app',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_json_widget',
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

ROOT_URLCONF = 'Clim_MeteoR.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # Cette ligne ajoute le dossier templates/ à la racine du projet
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Clim_MeteoR.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# tester si le password a blanc est pareil que pas de mot de passe...
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'climatest',
        'USER': os.getenv('PGUSER', 'postgres'),
        'PASSWORD': os.getenv('PGPASS', 'Funiculi'),
        'HOST': 'climatodb',                        # defined in dc-telemetry.yaml
        'PORT': '5435',                             # defined in dc-telemetry.yaml
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Indian/Reunion'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_ROOT = "/srv/beta_data/meteor_oi/bd_climato/bd-climato/static"
STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = "/srv/beta_data/meteor_oi/bd_climato/bd-climato/media"
DATA_FS_PATH = os.path.join(MEDIA_ROOT, 'data')

# App settings
AUTOLOAD_DIR = "/home/django/auto"              # in symc with dc-telemetry.yaml
LOCAL_REMOTE_DIR = "/home/django/manual"        # server loading file thru view
LOCAL_DIR = './data/json_not_in_git'            # client loaded file with loadson command

TELEMETRY = True                                # activate telemetry
JAEGER_COLLECTOR = "jaeger:14250"
JAEGER_INSECURE = True

PROD = True
LOG_FILE_DIR = "/home/django/log"    # log storage

# see comments in mytools.py(LogMe class definition)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'logInfoFile': {
            'handlers': ['logInfoFile_hdl'],
            'level': 'INFO'
        },
        'logDebugFile': {
            'handlers': ['logDebugFile_hdl'],
            'level': 'DEBUG'
        },
        'logInfoConsole': {
            'handlers': ['console'],
            'level': 'INFO'
        },
        'logDebugConsole': {
            'handlers': ['console'],
            'level': 'DEBUG'
        }
    },
    'handlers': {
        'logInfoFile_hdl': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_FILE_DIR + '/django.log',
            'formatter': 'file_fmt'
        },
        'logDebugFile_hdl': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOG_FILE_DIR + '/django.log',
            'formatter': 'file_fmt'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console_fmt'
        }
    },
    'formatters': {
        'console_fmt': {
            'format': '{asctime} {levelname} {module} {lineno} {message}',
            'style': '{'
        },
        'file_fmt': {
            'format': '',
            'style': '{'
        }
    }
}
