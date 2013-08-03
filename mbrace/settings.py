# vim: set foldmethod=marker foldlevel=0:
# Django settings for mbrace project.
import os
# retch
PROJECT_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__))+'/..')

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    ('Ryan Rix', 'ry@n.rix.si'),
)

MANAGERS = ADMINS

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

import djcelery
djcelery.setup_loader()

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

MEDIA_ROOT = ''
MEDIA_URL = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'djaml.loaders.DjamlFilesystemLoader',
    'djaml.loaders.DjamlAppDirectoriesLoader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mbrace.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'mbrace.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, "templates"),
)

INSTALLED_APPS = (
    'south',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'registration',
    'invitation',
    'django_extensions',
    'pipeline',
    'djcelery',
    'gmapi',
    'core',
    'celeryqueue',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

ACCOUNT_ACTIVATION_DAYS = 7  # One-week activation window; you may, of course,
                             # use a different value.


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
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

LOGIN_URL = '/'

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.INFO: '',
    messages.ERROR: 'alert',
    messages.SUCCESS: 'success'
}

CELERY_TIMEZONE = 'UTC'

# {{{1 Staticfiles and pipeline handling
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
STATIC_ROOT = os.path.join(PROJECT_DIR, 'public')
STATIC_URL = '/public/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

PIPELINE_ROOT=os.path.join(STATIC_ROOT, 'pipeline')
PIPELINE_CSS = {
    'foundation': {
        'source_filenames': {
            'foundation/scss/normalize.scss',
            'foundation/scss/foundation.scss',
        },
        'output_filename': 'min/foundation.css'
    },
    'app': {
        'source_filenames': {
            'scss/app.scss'
        },
        'output_filename': 'min/app.css'
    }
}

PIPELINE_JS = {
    'libraries': {
        'source_filenames': {
            'foundation/js/vendor/jquery.js',
            'foundation/js/vendor/custom.modernizr.js',
        },
        'output_filename': 'min/libraries.js'
    },
    'foundation': {
        'source_filenames': {
            'foundation/js/foundation/foundation.js',
            'foundation/js/foundation/foundation.*.js',
        },
        'output_filename': 'min/foundation.js'
    }
}

PIPELINE_ENABLED = False
PIPELINE_CSS_COMPRESSOR = None
PIPELINE_JS_COMPRESSOR = None
PIPELINE_COMPILERS = (
    'pipeline_compass.compass.CompassCompiler',
)
#}}}

INVITATION_INVITE_ONLY = True

# Set this to django.core.mail.backends.smtp.SmtpBackend when you deploy
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

from local_settings import *
