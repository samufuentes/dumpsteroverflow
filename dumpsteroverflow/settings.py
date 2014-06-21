"""
Django settings for dumpsteroverflow project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from urllib import urlparse
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
HOME_DIR = os.path.join(BASE_DIR, 'dumpsteroverflow')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*^h%uz13-oj)(007zwer^fy3%b7_q5jyy1ntd@@!$du9d4dr6_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'dumpsteroverflow.do_core.authentication.PaypalBackend',
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dumpsteroverflow.do_core',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'dumpsteroverflow.urls'

WSGI_APPLICATION = 'dumpsteroverflow.wsgi.application'

TEMPLATE_DIRS = [os.path.join(HOME_DIR, 'templates')]


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
try:
    elephant_uri = urlparse(os.environ['ELEPHANTSQL_URL'])
    db_config = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': elephant_uri.path[1:],
        'HOST': elephant_uri.hostname,
        'PORT': elephant_uri.port,
        'USER': elephant_uri.username,
        'PASSWORD': elephant_uri.password
    }
except KeyError:
    db_config = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }

DATABASES = {
    'default': db_config
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
