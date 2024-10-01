"""
Django settings for referee_delegation_system project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from decouple import config
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
from .secret_key import SECRET_KEY

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

    'django_dump_load_utf8',

    'accounts',
    'referees',
    'competitions',
    'delegations',
    'imports',
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

ROOT_URLCONF = 'referee_delegation_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'referee_delegation_system.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_db.sqlite3',
        'TEST': {
            'NAME': BASE_DIR / 'test_db.sqlite3',  # I explicitly specify the path to the test database.
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = False

# login redirect
LOGIN_REDIRECT_URL = 'home'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Setting for sending e-mails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_SSL = False
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_SUBJECT_PREFIX = '[Referee Delegation System - Password Reset] '

# Settings for Slovak volleyball federation
SEASON_NAMES = [
    ('2024/2025', '2024/2025'),
    ('2023/2024', '2023/2024'),
    ('2022/2023', '2022/2023'),
]

COMPETITION_NAMES = [
    ('Extraliga muži', 'Extraliga muži'),
    ('Extraliga ženy', 'Extraliga ženy'),
    ('1. liga muži', '1. liga muži'),
    ('1. liga ženy', '1. liga ženy'),
    ('1. liga juniori', '1. liga juniori'),
    ('1. liga juniorky', '1. liga juniorky'),
    ('Kadeti západ', 'Kadeti západ'),
    ('Kadetky západ', 'Kadetky západ'),
]

COMPETITION_LEVELS = [
    ('extra_league', 'extra_league'),
    ('first_league', 'first_league'),
    ('regional', 'regional'),
]

COMPETITION_CATEGORIES = [
    ('men', 'men'),
    ('women', 'women'),
    ('junior boys', 'junior boys'),
    ('junior girls', 'junior girls'),
    ('cadet boys', 'cadet boys'),
    ('cadet girls', 'cadet girls'),
]

REFEREE_ROLES = [
    ('1.R', '1.R'),
    ('2.R', '2.R'),
    ('1.L', '1.L'),
    ('2.L', '2.L'),
]

REFEREE_LICENCE_TYPES = [
    ('AM', 'AM'),
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
]