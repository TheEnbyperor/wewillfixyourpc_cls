"""
Django settings for wewillfixyourpc_cls project.

Generated by 'django-admin startproject' using Django 2.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import json
import logging

logging.basicConfig(level=logging.DEBUG)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '()%cgo!+bsth-2k=!6fp62d2$)o)-fr0r(9_1j57l-mi+#zt$e'
OTP_SECRET = 'C6NHIELPLV7R3OCG'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', 'wwfypc-cls.eu.ngrok.io']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django_keycloak_auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'phonenumber_field',
    'cls',
    'customers',
    'checkin',
    'tickets',
    'sale',
    'scrap',
    'crispy_forms',
    'ckeditor',
    'ckeditor_uploader',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    "django_keycloak_auth.middleware.OIDCMiddleware",
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wewillfixyourpc_cls.urls'

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
                'cls.context_processors.facebook_processor',
                'cls.context_processors.keycloak_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'wewillfixyourpc_cls.wsgi.application'

AUTHENTICATION_BACKENDS = ["django_keycloak_auth.auth.KeycloakAuthorization"]

LOGIN_URL = "oidc_login"
LOGOUT_REDIRECT_URL = "oidc_login"

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

EXTERNAL_URL_BASE = "https://wwfypc-cls.eu.ngrok.io"
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

PHONENUMBER_DEFAULT_REGION = 'GB'

with open(os.path.join(BASE_DIR, "secrets/keycloak.json")) as f:
    keycloak_conf = json.load(f)
with open(os.path.join(BASE_DIR, "secrets/google.json")) as f:
    google_conf = json.load(f)
with open(os.path.join(BASE_DIR, "secrets/twilio.json")) as f:
    twilio_conf = json.load(f)
with open(os.path.join(BASE_DIR, "secrets/slack.json")) as f:
    slack_conf = json.load(f)
with open(os.path.join(BASE_DIR, "secrets/facebook.json")) as f:
    facebook_conf = json.load(f)

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
UPDATES_EMAIL = "test@example.com"

CUSTOMER_SUPPORT_URL = "https://wewillfixyourpc-bot.eu.ngrok.io/"
VSMS_URL = "https://localhost:3000/"

KEYCLOAK_SERVER_URL = keycloak_conf["server_url"]
KEYCLOAK_REALM = keycloak_conf["realm"]
OIDC_CLIENT_ID = keycloak_conf["client_id"]
OIDC_CLIENT_SECRET = keycloak_conf["client_secret"]
OIDC_SCOPES = keycloak_conf["scopes"]

FIREBASE_URL_API_KEY = google_conf["short_links"]

FACEBOOK_PAGE_ID = facebook_conf["page_id"]
FACEBOOK_APP_ID = facebook_conf["app_id"]
FACEBOOK_OPTIN_SECRET = facebook_conf["optin_secret"]

TWILIO_ACCOUNT = twilio_conf["account"]
TWILIO_TOKEN = twilio_conf["token"]
TWILIO_MSID = twilio_conf["msid"]

SLACK_URL = slack_conf["webhook"]
SLACK_INTERACTIVITY_TOKEN = slack_conf["interactivity_token"]
SLACK_ACCESS_TOKEN = slack_conf["access_token"]

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'width': '100%',
        'skin': 'office2013',
    },
}

PRINTER_DRIVER = 'tickets.print_label.DummyDriver'
PRINTER_DRIVER_OPS = {}

# PRINTER_DRIVER = 'tickets.print_label.BrotherDriver'
# PRINTER_DRIVER_OPS = {
#     "printer": f"tcp://10.5.0.1:9100",
#     "model": "QL-720NW",
#     "label": "62"
# }
