import environ
from pathlib import Path
import os
from django.urls import reverse_lazy

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = environ.Path(__file__) - 3
APPS_DIR = ROOT_DIR.path("futgoal")

DEV = env.bool('FUTGOAL_DJANGO_DEV')
DEVJS = env.bool('FUTGOAL_DJANGO_DEVJS')
FUTGOAL_DEBUG_TOOLBAR = env.bool('FUTGOAL_DEBUG_TOOLBAR', False)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9mgu=0t7adojsh2zgkfn2kw(a!@ob(t^3f6ebch3_q7(2=yn)v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("FUTGOAL_DJANGO_DEBUG")

# Language (activar esto añade subcarpetas de idiomas en las URLs)
USE_L10N = False
USE_I18N = False
LANGUAGE_CODE = 'es-ES'

# Timezone (activar esto para que se pueda usar la fecha y hora en el sistema)
USE_TZ = False
TIME_ZONE = "Europe/Madrid"

def gettext(s):
    return s


# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

THIRD_PARTY_APPS = [
    "crispy_forms",
    "crispy_bootstrap4",
    'django_extensions',
    # django-allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

LOCAL_APPS = [
    'configuration',
    'users'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
AUTH_USER_MODEL = 'users.User'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

# django-allauth
UTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# django-allauth settings
SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_EMAIL_FIELD = 'email'
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

# Social account settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    }
}

SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_ADAPTER = 'futgoal.users.adapters.CustomSocialAccountAdapter'

# Authentication settings
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# OAuth settings
SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'
ACCOUNT_ADAPTER = 'allauth.account.adapter.DefaultAccountAdapter'

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

# DATABASES
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'futgoal'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

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

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATIC_ROOT = str(ROOT_DIR("staticfiles"))
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    str(ROOT_DIR.path("futgoal").path('static')),
]

# Media
MEDIA_ROOT = "/futgoal-media"
MEDIA_URL = "/media/"

CRISPY_TEMPLATE_PACK = 'bootstrap4'

TEMPLATES_DIR = str(APPS_DIR.path("_templates"))
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR, ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'futgoal.utils.context_processors.get_menu_urls',
            ],
            'libraries': {

            },
            'builtins': [
                'django.templatetags.static'
            ]
        },
    },
]

# Email
EMAIL_BACKEND = env("FUTGOAL_DJANGO_EMAIL_BACKEND")
SERVER_EMAIL = "disadamsdsdnts@gmail.com"

# Admin
ADMIN_URL = "admin/"
ADMINS = [
    ("""Adan Martin""", "disadamsdsdnts@gmail.com"),
]
MANAGERS = ADMINS

LOGIN_REDIRECT_URL = "/"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# URL config
SITE_URL = env.str("FUTGOAL_SITE_URL")

FILE_UPLOAD_PERMISSIONS = 0o640  # De audax
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = reverse_lazy('auth:login')


# Email
EMAIL_BACKEND = env.str("FUTGOAL_DJANGO_EMAIL_BACKEND")
EMAIL_FROM = env.str("FUTGOAL_EMAIL_FROM")
EMAIL_HOST = env.str("FUTGOAL_EMAIL_HOST")
EMAIL_PORT = env.int("FUTGOAL_EMAIL_PORT")
EMAIL_USE_TLS = env.bool("FUTGOAL_EMAIL_USE_TLS")
EMAIL_HOST_USER = env.str("FUTGOAL_EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env.str("FUTGOAL_EMAIL_HOST_PASSWORD")
EMAIL_BCC = env.str("FUTGOAL_EMAIL_BCC")

CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
    'http://localhost:3000',
    'localhost:8000',
    'localhost:3000',
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://localhost:3000',
    'localhost:8000',
    'localhost:3000',
]

ALLOWED_HOSTS = [
    'http://localhost:8000',
    'http://localhost:3000',
    'localhost:8000',
    'localhost:3000',
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SITE_ID = 1


import locale
# Intentar establecer el locale en español
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # En Linux o macOS
except locale.Error:
    locale.setlocale(locale.LC_TIME, 'es_ES')  # Fallback en caso de error
