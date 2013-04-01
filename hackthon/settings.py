import os
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG
PYSCSS_DEBUG_INFO = False

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

def rel(*x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

sys.path.insert(0, rel('apps'))

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': rel('dev.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

TIME_ZONE = 'Europe/Moscow'

LANGUAGE_CODE = 'ru-ru'

SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = ''
MEDIA_URL = ''

STATIC_ROOT = rel('static')
STATIC_URL = '/static/'

SECRET_KEY = '#mnn@3!uyvuim%bk2#i2@78pq_2%-erqhx6ib--ch@*pts8%9f'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.request",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

EMAIL_BACKEND = "mailer.backend.DbBackend"

#AUTHENTICATION_BACKENDS = (
    #'guardian.backends.ObjectPermissionBackend',
#    'django.contrib.auth.backends.ModelBackend',
#)

ROOT_URLCONF = 'hackthon.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'hackthon.wsgi.application'

TEMPLATE_DIRS = (
    rel('templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django_assets',
    'django_extensions',
    'activelink',
    'annoying',
    'gravatar',
    'mailer',
    'pymorphy',
    'widget_tweaks',
    'ajax_validation',
    'local',
    'profiles',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

LOGIN_REDIRECT_URL = '/accounts/edit/'
AUTHENTICATION_BACKENDS = (
    'profiles.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend'
)
ALLOWED_HOSTS = ('www.hackpoint.ru', 'hackpoint.ru', 'demo.hackpoint.ru')
DEFAULT_FROM_EMAIL = 'info@hackpoint.ru'
AJAX_VALIDATION_FORMS = [
    'profiles.forms.UserProfileForm',
    'profiles.forms.RegistrationFormUniqueEmail',
    'profiles.forms.SponsorshipForm',
    #'auth.contrib.auth.forms.AuthenticationForm',
]

PYMORPHY_DICTS = {
    'ru': { 'dir': rel('pymorphy/dicts') },
}

try:
    from settings_local import *
except:
    pass
