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
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

logging.basicConfig(level=logging.INFO)

sentry_sdk.init(
    dsn="https://518037d272e5426895df091967e1b949@sentry.io/1821508",
    environment=os.getenv("SENTRY_ENVIRONMENT", "dev"),
    release=os.getenv("RELEASE", None),
    integrations=[DjangoIntegration()],
    send_default_pii=True
)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "")
OTP_SECRET = os.getenv("OTP_SECRET", "")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [os.getenv("HOST", "cardifftec.uk")]


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
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.getenv("DB_HOST", "localhost"),
        "NAME": os.getenv("DB_NAME", "cls"),
        "USER": os.getenv("DB_USER", "cls"),
        "PASSWORD": os.getenv("DB_PASS"),
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
EXTERNAL_URL_BASE = os.getenv("EXTERNAL_URL", f"https://{ALLOWED_HOSTS[0]}")

STATIC_URL = f"{EXTERNAL_URL_BASE}/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = f"{EXTERNAL_URL_BASE}/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

PHONENUMBER_DEFAULT_REGION = 'GB'

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 25))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", False)
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", False)

CUSTOMER_SUPPORT_URL = os.getenv("CUSTOMER_SUPPORT_URL", "https://bot.cardifftec.uk/")
VSMS_URL = os.getenv("VSMS_URL", "http://vsms/")

TWILIO_ACCOUNT = os.getenv("TWILIO_ACCOUNT_ID")
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
TWILIO_MSID = os.getenv("TWILIO_MSID")

UPDATES_EMAIL = os.getenv("UPDATES_EMAIL", "")

KEYCLOAK_SERVER_URL = os.getenv("KEYCLOAK_SERVER_URL")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM")
OIDC_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
OIDC_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET")
OIDC_SCOPES = os.getenv("KEYCLOAK_SCOPES")

FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
FACEBOOK_APP_ID = os.getenv("FACEBOOK_APP_ID")
FACEBOOK_OPTIN_SECRET = os.getenv("FACEBOOK_OPTIN_SECRET")

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'width': '100%',
        'skin': 'office2013',
    },
}

FIREBASE_URL_API_KEY = os.getenv("FIREBASE_URL_KEY")

CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost")
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "pyamqp://")
CELERY_TASK_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]

SLACK_URL = os.getenv("SLACK_WEBHOOK")
SLACK_INTERACTIVITY_TOKEN = os.getenv("SLACK_INTERACTIVITY_TOKEN")
SLACK_ACCESS_TOKEN = os.getenv("SLACK_ACCESS_TOKEN")

PRINTER_DRIVER = 'tickets.print_label.BrotherDriver'
PRINTER_DRIVER_OPS = {
    "printer": f"tcp://{os.getenv('LABEL_PRINTER', '')}:9100",
    "model": "QL-720NW",
    "label": "62"
}
