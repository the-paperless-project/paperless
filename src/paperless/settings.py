"""
Django settings for paperless project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import uuid

from dotenv import load_dotenv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("PAPERLESS_SECRET_KEY") or str(uuid.uuid4())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

LOGIN_URL = '/admin/login'

ALLOWED_HOSTS = ["*"]

_allowed_hosts = os.getenv("PAPERLESS_ALLOWED_HOSTS")
if _allowed_hosts:
    ALLOWED_HOSTS = _allowed_hosts.split(",")

# Tap paperless.conf if it's available
if os.path.exists("/etc/paperless.conf"):
    load_dotenv("/etc/paperless.conf")


# Application definition

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "django_extensions",

    "documents.apps.DocumentsConfig",

    "rest_framework",
    "crispy_forms",

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

WSGI_APPLICATION = 'paperless.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(
            os.getenv(
                "PAPERLESS_DBDIR",
                os.path.join(BASE_DIR, "..", "data")
            ),
            "db.sqlite3"
        )
    }
}

if os.getenv("PAPERLESS_DBUSER") and os.getenv("PAPERLESS_DBPASS"):
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("PAPERLESS_DBNAME", "paperless"),
        "USER": os.getenv("PAPERLESS_DBUSER"),
        "PASSWORD": os.getenv("PAPERLESS_DBPASS")
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

TIME_ZONE = os.getenv("PAPERLESS_TIME_ZONE", "UTC")

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "..", "static")
MEDIA_ROOT = os.getenv(
    "PAPERLESS_MEDIADIR", os.path.join(BASE_DIR, "..", "media"))

STATIC_URL = '/static/'
MEDIA_URL = "/media/"


# Paperless-specific stuff
# You shouldn't have to edit any of these values.  Rather, you can set these
# values in /etc/paperless.conf instead.
# ----------------------------------------------------------------------------

# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "consumer": {
            "class": "documents.loggers.PaperlessLogger",
        }
    },
    "loggers": {
        "documents": {
            "handlers": ["consumer"],
            "level": os.getenv("PAPERLESS_CONSUMER_LOG_LEVEL", "INFO"),
        },
    },
}


# The default language that tesseract will attempt to use when parsing
# documents.  It should be a 3-letter language code consistent with ISO 639.
OCR_LANGUAGE = os.getenv("PAPERLESS_OCR_LANGUAGE", "eng")

# The amount of threads to use for OCR
OCR_THREADS = os.getenv("PAPERLESS_OCR_THREADS")

# If this is true, any failed attempts to OCR a PDF will result in the PDF
# being indexed anyway, with whatever we could get.  If it's False, the file
# will simply be left in the CONSUMPTION_DIR.
FORGIVING_OCR = bool(os.getenv("PAPERLESS_FORGIVING_OCR", "YES").lower() in ("yes", "y", "1", "t", "true"))

# GNUPG needs a home directory for some reason
GNUPG_HOME = os.getenv("HOME", "/tmp")

# Convert is part of the ImageMagick package
CONVERT_BINARY = os.getenv("PAPERLESS_CONVERT_BINARY", "convert")
CONVERT_TMPDIR = os.getenv("PAPERLESS_CONVERT_TMPDIR")
CONVERT_MEMORY_LIMIT = os.getenv("PAPERLESS_CONVERT_MEMORY_LIMIT")
CONVERT_DENSITY = os.getenv("PAPERLESS_CONVERT_DENSITY")

# Unpaper
UNPAPER_BINARY = os.getenv("PAPERLESS_UNPAPER_BINARY", "unpaper")

# This will be created if it doesn't exist
SCRATCH_DIR = os.getenv("PAPERLESS_SCRATCH_DIR", "/tmp/paperless")

# This is where Paperless will look for PDFs to index
CONSUMPTION_DIR = os.getenv("PAPERLESS_CONSUMPTION_DIR")

# The number of seconds that Paperless will wait between checking
# CONSUMPTION_DIR.  If you tend to write documents to this directory very
# slowly, you may want to use a higher value than the default.
CONSUMER_LOOP_TIME = int(os.getenv("PAPERLESS_CONSUMER_LOOP_TIME", 10))

# If you want to use IMAP mail consumption, populate this with useful values.
# If you leave HOST set to None, we assume you're not going to use this
# feature.
MAIL_CONSUMPTION = {
    "HOST": os.getenv("PAPERLESS_CONSUME_MAIL_HOST"),
    "PORT": os.getenv("PAPERLESS_CONSUME_MAIL_PORT"),
    "USERNAME": os.getenv("PAPERLESS_CONSUME_MAIL_USER"),
    "PASSWORD": os.getenv("PAPERLESS_CONSUME_MAIL_PASS"),
    "USE_SSL": os.getenv("PAPERLESS_CONSUME_MAIL_USE_SSL", "y").lower() == "y",  # If True, use SSL/TLS to connect
    "INBOX": "INBOX"  # The name of the inbox on the server
}

# This is used to encrypt the original documents and decrypt them later when
# you want to download them.  Set it and change the permissions on this file to
# 0600, or set it to `None` and you'll be prompted for the passphrase at
# runtime.  The default looks for an environment variable.
# DON'T FORGET TO SET THIS as leaving it blank may cause some strange things
# with GPG, including an interesting case where it may "encrypt" zero-byte
# files.
PASSPHRASE = os.getenv("PAPERLESS_PASSPHRASE")

# If you intend to use the "API" to push files into the consumer, you'll need
# to provide a shared secret here.  Leaving this as the default will disable
# the API.
SHARED_SECRET = os.getenv("PAPERLESS_SHARED_SECRET", "")

# Trigger a script after every successful document consumption?
PRE_CONSUME_SCRIPT = os.getenv("PAPERLESS_PRE_CONSUME_SCRIPT")
POST_CONSUME_SCRIPT = os.getenv("PAPERLESS_POST_CONSUME_SCRIPT")

# The number of items on each page in the web UI.  This value must be a
# positive integer, but if you don't define one in paperless.conf, a default of
# 100 will be used.
PAPERLESS_LIST_PER_PAGE = int(os.getenv("PAPERLESS_LIST_PER_PAGE", 100))
