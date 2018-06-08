"""
Django settings for monitor_receiver project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from cloghandler import ConcurrentRotatingFileHandler
from mongoengine import connect

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0ya!k7^)s264vu)^gh5q4@aiw01v)ren&xl&k_c9&d@$dlv5e6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'temperature',
    'controll_agent'
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

ROOT_URLCONF = 'monitor_receiver.urls'
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

WSGI_APPLICATION = 'monitor_receiver.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
       'ENGINE': None,
       # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'abc',
    #     'USER': 'abc',
    #     'PASSWORD': '123456',
    #     'HOST': '127.0.0.1',
    #     'PORT': '3306',
    #     'OPTIONS': {
    #         'init_command': 'SET NAMES utf8, sql_mode="STRICT_TRANS_TABLES"',
    #     },
    #     'TEST': {
    #         'CHARSET': 'utf8',
    #         'COLLATION': 'utf8_general_ci',
    #     }
    # },
}
connect(db='test', host='127.0.0.1',port=27017,username='mymongo',password='mymongo')

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

# Logging
# https://docs.djangoproject.com/en/1.10/topics/logging/
VA = '%(asctime)s,%(msecs)03d'
VB = '[%(module)s:%(name)s:%(funcName)s:%(lineno)d]'
VC = '[P%(process)d:T%(thread)d]'
VD = '%(levelname)-5s - %(message)s'
SA = '%(asctime)s,%(msecs)03d'
SB = '[%(name)s:%(funcName)s:%(lineno)d]'
SC = '%(levelname)-5s - %(message)s'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{} {} {} {}'.format(VA, VB, VC, VD),
            'datefmt' : '%Y-%m-%d %H:%M:%S'
        },
        'standard': {
            'format': '{} {} {}'.format(SA, SB, SC),
            'datefmt' : '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'log/monitor_receiver.log'),
            'formatter': 'standard'
        },
        'rotatingFile': {
            'level': 'INFO',
            #'class': 'logging.handlers.RotatingFileHandler',
            'class': 'logging.handlers.ConcurrentRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'log/monitor_receiver.log'),
            'maxBytes': 1024 * 1024 * 20,
            'backupCount': 50,
            'formatter': 'standard'
        },
        'timedRotatingFile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'log/monitor_receiver.log'),
            'when':'midnight',
            'interval': 1,
            'backupCount': 90,
            'formatter':'standard'
        },
    },
    'loggers': {
        # root, '' and 'cmdb' would be duplicated
        #'': {
        #    'handlers': ['rotatingFile'],
        #    'level': 'INFO'
        #},
        'django': {
            'handlers':['rotatingFile'],
            'propagate': True,
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO')
        },
        'temperature': {
            'handlers': ['rotatingFile'],
            'level': 'INFO'
        },
        'controll_agent': {
            'handlers': ['rotatingFile'],
            'level': 'INFO'
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
