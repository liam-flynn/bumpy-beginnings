"""
Django settings for bumpybeginnings project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path
import environ
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1g0n=^itp0uzp%_)012fu8nf$*+_i*r2ofvz=w^yarw+*khrw&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

LOGIN_REDIRECT_URL = '/get-details/'
LOGOUT_REDIRECT_URL = '/'

SOCIALACCOUNT_LOGIN_ON_GET = True

SITE_ID = 1

# Application definition
INSTALLED_APPS = [
    'users.apps.UsersConfig',
    'forum.apps.ForumConfig',
    'api.apps.ApiConfig',
    'articles.apps.ArticlesConfig',
    'tracker.apps.TrackerConfig',
    'calculator.apps.CalculatorConfig',
    'notifications.apps.NotificationsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'rest_framework',
    'sslserver',
    'tinymce',
    'django_bleach',
    'drf_yasg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
    'users.middleware.RequireDetailsMiddleware',
]

ROOT_URLCONF = 'bumpybeginnings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'bumpybeginnings', 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'notifications.context_processors.notifications_processor',
            ],
        },
    },
]


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '604285495106-nkkk0mqpoji9dv0hneuqrkjg5c4ek9n2.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
    },
    'facebook': {
        'APP': {
            'client_id': '1021988409693731', 
            'secret': 'f38ccefd8ccde53e80d4b6abe328ba09', 
            'key': ''
        },
        'METHOD': 'oauth2',
        'SCOPE': ['public_profile'],  
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': ['id','email', 'name', 'first_name', 'last_name'],
        'EXCHANGE_TOKEN': True,
        'VERIFIED_EMAIL': False,
    }
}

WSGI_APPLICATION = 'bumpybeginnings.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bumpydb',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': 5432
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

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'


STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


TINYMCE_DEFAULT_CONFIG = {
    'height': 300,
    'width': '100%',
    'menubar': False,  
    'plugins': 'link lists',  
    'toolbar': 'undo redo | bold italic underline | bullist numlist | link',
    'statusbar': False,
    'content_style': "body { font-family: Arial, sans-serif; font-size: 14px; }",
}

BLEACH_ALLOWED_TAGS = [
    'a', 'ul', 'ol', 'li', 'strong', 'em', 'u', 'p', 'br', 'span'
]

BLEACH_ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'target'],
    'p': ['style'],
    'span': ['style'],
}

BLEACH_ALLOWED_STYLES = [
    'font-weight', 'text-decoration', 'list-style-type'
]

BLEACH_STRIP_TAGS = True
BLEACH_STRIP_COMMENTS = True
