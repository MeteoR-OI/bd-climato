"""
Django settings for Clim_MeteoR project.

Generated by 'django-admin startproject' using Django 3.2.9.

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
        'climato.meteor-oi.re',
        '127.0.0.1',
        'localhost',
]

ALLOWED_CIDR_NETS = ['10.2.0.0/16']

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "app", "static"),
]
# Application definition

INSTALLED_APPS = [
    'app',
    # 'django_prometheus',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_json_widget',
]

MIDDLEWARE = [
    'allow_cidr.middleware.AllowCIDRMiddleware',
    # 'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django_prometheus.middleware.PrometheusAfterMiddleware',
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

# Database

PG_ADDON_HOST = os.getenv('POSTGRESQL_ADDON_HOST', 'localhost')
PG_ADDON_USER = os.getenv('POSTGRESQL_ADDON_USER', 'postgres')
PG_ADDON_PASSWORD = os.getenv('POSTGRESQL_ADDON_PASSWORD', 'Funiculi')
PG_ADDON_PORT = int(os.getenv('POSTGRESQL_ADDON_PORT','5432'))
PG_DATABASE = os.getenv('POSTGRESQL_ADDON_DB', 'climato')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': PG_DATABASE,
        'USER': PG_ADDON_USER,
        'PASSWORD': PG_ADDON_PASSWORD,
        'HOST': PG_ADDON_HOST,
        'PORT': PG_ADDON_PORT,
        'CONN_MAX_AGE': None,
    }
}

# mysql weewx dump db server
MS_SQL_HOST = os.getenv('MYSQL_DINA_HOST', 'localhost')
MS_SQL_USER = os.getenv('MYSQL_DINA_USER', 'nico')
MS_SQL_PASS = os.getenv('MYSQL_DINA_PASSWORD', 'Funiculi')
MS_SQL_PORT = int(os.getenv('MYSQL_DINA_PORT', '3306'))
MS_SQL_DB = os.getenv('MYSQL_DINA_DB', '??')

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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False          # need to use no timezone !!!

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = "/srv/beta_data/meteor_oi/bd_climato/bd-climato/media"
DATA_FS_PATH = os.path.join(MEDIA_ROOT, 'data')

# App settings
JSON_AUTOLOAD = "./fs_bucket/climato/json_auto_load"
JSON_WAITING = "./fs_bucket/climato/waiting_json"
CSV_AUTOLOAD = "./fs_bucket/climato/csv_auto_load"
OVPF_FILES = "./fs_bucket/climato/ovpf"
ARCHIVE_DIR = "./fs_bucket/climato/json_archive"
FAILED_DIR = "./fs_bucket/climato/erreur"
NO_DELETE_JSON = True                # do not delete json file after processing

TELEMETRY_PROVIDER = False          # None, Console, Jaeger, Thrift
TELEMETRY_HOST = "localhost"
JAEGER_PORT = 14250
THRIFT_PORT = 14250

PROD = False
LOG_FILE_DIR = "./fs_bucket/climato/log"    # log storage

# see comments in mytools.py(LogMe class definition)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'log_dev': {
            'handlers': ['console_dev'],
            'level': 'DEBUG'
        },
        'log_prod': {
            'handlers': ['console_prod'],
            'level': 'DEBUG'
        }
    },
    'handlers': {
        'console_prod': {
            'class': 'logging.StreamHandler',
            'formatter': 'console_fmt',
            'level': 'ERROR'
        },
        'console_dev': {
            'class': 'logging.StreamHandler',
            'formatter': 'console_fmt',
            'level': 'DEBUG'
        }
    },
    'formatters': {
        'console_fmt': {
            'format': '{levelname} {message}',
            'style': '{'
        }
    }
}
