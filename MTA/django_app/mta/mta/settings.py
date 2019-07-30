"""
Django settings for mta project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from configparser import RawConfigParser


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = RawConfigParser()
config.read(os.path.join(BASE_DIR, 'settings.ini'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get('secrets', 'SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'mta2014.appspot.com']


# Application definition

INSTALLED_APPS = [
    'mta2014.apps.Mta2014Config',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django_generate_secret_key',
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

ROOT_URLCONF = 'mta.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'mta.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# [START db_setup]
if os.getenv('GAE_INSTANCE', None):
    # Running on production App Engine, so connect to Google Cloud SQL using
    # the unix socket at /cloudsql/<your-cloudsql-connection
    db_config = RawConfigParser()
    db_config.read(os.path.join(BASE_DIR, 'db-settings.ini.app'))

    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'HOST': db_config.get('database', 'DATABASE_HOST'),
            'PORT': db_config.get('database', 'DATABASE_PORT'),
            'NAME': db_config.get('database', 'DATABASE_NAME'),
            'USER': db_config.get('database', 'DATABASE_USER'),
            'PASSWORD': db_config.get('database', 'DATABASE_PASSWORD'),
        }
    }
else:
    # Running locally so connect to either a local Postgres instance or connect
    # to Cloud SQL via the proxy.  To start the proxy via command line:
    # $ cloud_sql_proxy -instances=[INSTANCE_CONNECTION_NAME]=tcp:3306
    # See https://cloud.google.com/sql/docs/mysql-connect-proxy
    db_config = RawConfigParser()
    db_config.read(os.path.join(BASE_DIR, 'db-settings.ini'))

    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'HOST': db_config.get('database', 'DATABASE_HOST'),
            'PORT': db_config.get('database', 'DATABASE_PORT'),
            'NAME': db_config.get('database', 'DATABASE_NAME'),
            'USER': db_config.get('database', 'DATABASE_USER'),
            'PASSWORD': db_config.get('database', 'DATABASE_PASSWORD'),
        }
    }
# [END db_setup]

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = 'https://storage.googleapis.com/mta2014/static/'

STATIC_ROOT = 'static'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS =[
    os.path.join(BASE_DIR, 'static'),
]

DAJAXICE_MEDIA_PREFIX = 'dajaxice'

ACCESS_KEY = config.get('secrets', 'ACCESS_KEY')

