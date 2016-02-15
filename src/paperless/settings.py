"""
Django settings for paperless project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e11fl1oa-*ytql8p)(06fbj4ukrlo+n7k&q5+$1md7i+mge=ee'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'suit',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "django_extensions",

    "documents",
    "logger",

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

ROOT_URLCONF = 'paperless.urls'

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

TEMPLATE_CONTEXT_PROCESSORS = TCP + ['django.core.context_processors.request']

WSGI_APPLICATION = 'paperless.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "..", "data", "db.sqlite3"),
    }
}
if os.environ.get("PAPERLESS_DBUSER") and os.environ.get("PAPERLESS_DBPASS"):
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("PAPERLESS_DBNAME", "paperless"),
        "USER": os.environ.get("PAPERLESS_DBUSER"),
        "PASSWORD": os.environ.get("PAPERLESS_DBPASS")
    }


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "..", "static")
MEDIA_ROOT = os.path.join(BASE_DIR, "..", "media")

STATIC_URL = '/static/'
MEDIA_URL = "/media/"


# Paperless-specific stuffs
# Change these paths if yours are different
# ----------------------------------------------------------------------------

# The default language that tesseract will attempt to use when parsing
# documents.  It should be a 3-letter language code consistent with ISO 639.
OCR_LANGUAGE = "eng"

# The amount of threads to use for OCR
OCR_THREADS = os.environ.get("PAPERLESS_OCR_THREADS")

# If this is true, any failed attempts to OCR a PDF will result in the PDF being
# indexed anyway, with whatever we could get.  If it's False, the file will
# simply be left in the CONSUMPTION_DIR.
FORGIVING_OCR = True

# GNUPG needs a home directory for some reason
GNUPG_HOME = os.environ.get("HOME", "/dev/null")

# Convert is part of the Imagemagick package
CONVERT_BINARY = "/usr/bin/convert"

# This will be created if it doesn't exist
SCRATCH_DIR = "/tmp/paperless"

# This is where Paperless will look for PDFs to index
CONSUMPTION_DIR = os.environ.get("PAPERLESS_CONSUME")

# If you want to use IMAP mail consumption, populate this with useful values.
# If you leave HOST set to None, we assume you're not going to use this feature.
MAIL_CONSUMPTION = {
    "HOST": os.environ.get("PAPERLESS_CONSUME_MAIL_HOST"),
    "PORT": os.environ.get("PAPERLESS_CONSUME_MAIL_PORT"),
    "USERNAME": os.environ.get("PAPERLESS_CONSUME_MAIL_USER"),
    "PASSWORD": os.environ.get("PAPERLESS_CONSUME_MAIL_PASS"),
    "USE_SSL": True,  # If True, use SSL/TLS to connect
    "INBOX": "INBOX"  # The name of the inbox on the server
}

# This is used to encrypt the original documents and decrypt them later when you
# want to download them.  Set it and change the permissions on this file to
# 0600, or set it to `None` and you'll be prompted for the passphrase at
# runtime.  The default looks for an environment variable.
# DON'T FORGET TO SET THIS as leaving it blank may cause some strange things
# with GPG, including an interesting case where it may "encrypt" zero-byte
# files.
PASSPHRASE = os.environ.get("PAPERLESS_PASSPHRASE")

# If you intend to use the "API" to push files into the consumer, you'll need to
# provide a shared secret here.  Leaving this as the default will disable the
# API.
UPLOAD_SHARED_SECRET = os.environ.get("PAPERLESS_SECRET", "")
