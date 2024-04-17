"""
Django settings for izvoli project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = dict(
    SECRET_KEY=os.getenv(
        "DJANGO_SECRET_KEY", "r^&^$8c*g$6db1s!s7uk9c!v%*ps)_0)h$!f3m7$%(o4b+5qwk"
    ),
    DEBUG=os.getenv("DJANGO_DEBUG", False),
    DATABASE_HOST=os.getenv("DJANGO_DATABASE_HOST", "db"),
    DATABASE_PORT=os.getenv("DJANGO_DATABASE_PORT", "5432"),
    DATABASE_NAME=os.getenv("DJANGO_DATABASE_NAME", "izvoli"),
    DATABASE_USER=os.getenv("DJANGO_DATABASE_USERNAME", "postgres"),
    DATABASE_PASSWORD=os.getenv("DJANGO_DATABASE_PASSWORD", "postgres"),
    STATIC_ROOT=os.getenv("DJANGO_STATIC_ROOT", os.path.join(BASE_DIR, "../static")),
    STATIC_URL=os.getenv("DJANGO_STATIC_URL_BASE", "/static/"),
    MEDIA_ROOT=os.getenv("DJANGO_MEDIA_ROOT", os.path.join(BASE_DIR, "media")),
    MEDIA_URL=os.getenv("DJANGO_MEDIA_URL_BASE", "/media/"),
)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env["DEBUG"]

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'parties'
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

ROOT_URLCONF = 'izvoli.urls'

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

WSGI_APPLICATION = 'izvoli.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "HOST": env["DATABASE_HOST"],
        "PORT": env["DATABASE_PORT"],
        "NAME": env["DATABASE_NAME"],
        "USER": env["DATABASE_USER"],
        "PASSWORD": env["DATABASE_PASSWORD"],
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "sl"

TIME_ZONE = "Europe/Ljubljana"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"),
]

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

STATIC_ROOT = env["STATIC_ROOT"]
STATIC_URL = env["STATIC_URL"]

MEDIA_ROOT = env["MEDIA_ROOT"]
MEDIA_URL = env["MEDIA_URL"]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
