"""
Django settings for akbash project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import datetime
from configparser import ConfigParser

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'django_extensions',
    'api.apps.ApiConfig',
    'bpm.apps.BpmConfig',
    'akjob.apps.AkjobConfig',
    'auditlog.apps.AuditlogConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'akbash.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'akbash.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

# CORS Access Controls. Currently set to allow all hosts
CORS_ORIGIN_ALLOW_ALL = True

# Private and local configurations read from a config file

private_config_file = os.environ.get(
    'AKBASH_CONFIG_FILE',
    os.path.join(BASE_DIR, '..', 'akbash_private_settings', 'akbash.ini'))
config = ConfigParser(interpolation=None)
config.read(private_config_file)

# Get all allowed hosts from private config files
# In config file, hosts are entered in as comma seperated
hosts_list = []
permission_classes = ()

if 'security' in config:
    if 'ALLOWED_HOSTS' in config['security']:
        hosts = config['security']['ALLOWED_HOSTS']
        hosts_list = [host.strip() for host in hosts.split(',')]
    if 'ENABLE_JWT' in config['security']:
        is_jwt_enabled = config.getboolean('security', 'ENABLE_JWT')
        if is_jwt_enabled:
            permission_classes = ('rest_framework.permissions.IsAuthenticated',)

ALLOWED_HOSTS = hosts_list

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['secrets']['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.getboolean('debug', 'DEBUG')

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

# check database config for unrecognized options.
for k in config['default database']:
    if k.startswith('option'):
        continue
    elif k.startswith('test'):
        continue
    elif k.upper() in (
            'ATOMIC_REQUESTS',
            'AUTOCOMMIT',
            'ENGINE',
            'HOST',
            'NAME',
            'CONN_MAX_AGE',
            'PASSWORD',
            'PORT',
            'TIME_ZONE',
            'USER'):
        continue
    else:
        raise KeyError("Unrecognized default database option: {}".format(k))

# setup DATABASES settings dictionary
DATABASES = {
    'default': {}
}
for k in config['default database']:
    if k.startswith('option'):
        DATABASES['default']['OPTIONS'] = {}
        break
for k in config['default database']:
    if k.startswith('test'):
        DATABASES['default']['TEST'] = {}
        break

# iterate through default databases config and add to DATABASES dictionary.
# configparser "section" and "option" are always lowercase
for po, v in config['default database'].items():
    o = po.split('-')
    # django-pyodbc-azure options use lowercase
    if o[0] == 'options':
        DATABASES['default']['OPTIONS'][o[1]] = v
    elif o[0] == 'test':
        DATABASES['default']['TEST'][o[1].upper()] = v
    else:
        DATABASES['default'][o[0].upper()] = v


# Talented API key
TALENTED_API_KEY = config['secrets']['TALENTED_API_KEY']

# EMAIL_FROM_ADDRESS is required in bpm.models. /
# Set it to blank in case the private settings file does not define it.
# Also set EMAIL_ACTIVE to False, unless specifically enabled in private settings.
EMAIL_FROM_ADDRESS = ''
EMAIL_ACTIVE = False

# Email settings (use private settings file)
if 'email' in config:
    email = config['email']
    EMAIL_HOST = email['EMAIL_HOST']
    EMAIL_PORT = email['EMAIL_PORT']
    EMAIL_FROM_ADDRESS = email['EMAIL_FROM_ADDRESS']
    EMAIL_ACTIVE = config.getboolean('email', 'EMAIL_ACTIVE')
    if 'EMAIL_HOST_USER' in email:
        EMAIL_HOST_USER = config['email']['EMAIL_HOST_USER']
    if 'EMAIL_HOST_PASSWORD' in email:
        EMAIL_HOST_PASSWORD = config['email']['EMAIL_HOST_PASSWORD']
    if 'EMAIL_USE_TLS' in email:
        EMAIL_USE_TLS = config.getboolean('email', 'EMAIL_USE_TLS')

# REST Framework authentication settings. Defaulting to JWT Auth.
# See: http://getblimp.github.io/django-rest-framework-jwt/
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': permission_classes,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=1800),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_ALLOW_REFRESH': True,
}
